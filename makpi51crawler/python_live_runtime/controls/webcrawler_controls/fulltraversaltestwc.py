#!/usr/bin/env python3
# DURABLE_FULL_TRAVERSAL_RUNNER_R2_BEGIN
# EN: Durable full traversal test runner for crawler_core.
# EN: Creates a per-run artifact directory and can launch the canonical crawler
# EN: loop inside tmux so SSH/browser disconnects do not destroy evidence.
# TR: crawler_core için kalıcı full traversal test runner.
# TR: Her run için artifact dizini oluşturur ve canonical crawler loop'u tmux
# TR: içinde başlatabilir; SSH/tarayıcı kopması kanıtı kaybettirmez.
# DURABLE_FULL_TRAVERSAL_RUNNER_R2_END

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Final


DEFAULT_LIVE_ROOT: Final[Path] = Path("/logisticsearch/makpi51crawler")
DEFAULT_ENV_FILE: Final[Path] = Path("/home/makpi51/.config/logisticsearch/secrets/webcrawler.env")
DEFAULT_DURABLE_RUN_ROOT: Final[Path] = Path("/srv/webcrawler/test_runs")
DEFAULT_LABEL: Final[str] = "full_26_json_r4"
# P0 note: DEFAULT_HARD_TIMEOUT_SECONDS is a test-harness safety belt,
# not a production/7x24 crawler lifecycle limit. Passing
# --hard-timeout-seconds 0 disables only this global test limit.
DEFAULT_HARD_TIMEOUT_SECONDS: Final[int] = 14400


def _non_negative_int(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if value < 0:
        raise argparse.ArgumentTypeError(
            "must be >= 0; use 0 to disable only the test-harness global timeout"
        )
    return value
DEFAULT_MONITOR_EVERY_SECONDS: Final[int] = 30
DEFAULT_TERM_GRACE_SECONDS: Final[int] = 30


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _sanitize_label(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    cleaned = cleaned.strip("._-")
    return cleaned or DEFAULT_LABEL


def _quote(value: object) -> str:
    return shlex.quote(str(value))


def _write_text(path: Path, content: str, *, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)


def _build_run_dir(durable_root: Path, label: str) -> Path:
    return durable_root / f"{_sanitize_label(label)}_{_utc_stamp()}"


def _render_runner_shell(
    *,
    run_dir: Path,
    live_root: Path,
    env_file: Path,
    hard_timeout_seconds: int,
    monitor_every_seconds: int,
    term_grace_seconds: int,
) -> str:
    python_bin = live_root / ".venv/bin/python"
    return f"""#!/usr/bin/env bash
set -Eeuo pipefail

RUN_DIR={_quote(run_dir)}
LIVE_ROOT={_quote(live_root)}
ENV_FILE={_quote(env_file)}
PYTHON_BIN={_quote(python_bin)}
HARD_TIMEOUT_SECONDS={int(hard_timeout_seconds)}
MONITOR_EVERY_SECONDS={int(monitor_every_seconds)}
TERM_GRACE_SECONDS={int(term_grace_seconds)}

CRAWLER_LOG="${{RUN_DIR}}/crawler.log"
MONITOR_LOG="${{RUN_DIR}}/monitor.log"
PREFLIGHT_TXT="${{RUN_DIR}}/preflight.txt"
DB_BEFORE_TXT="${{RUN_DIR}}/db_snapshot_before.txt"
DB_AFTER_TXT="${{RUN_DIR}}/db_snapshot_after.txt"
FINAL_JSON="${{RUN_DIR}}/final.json"
CHECKSUMS_TXT="${{RUN_DIR}}/checksums.txt"
PID_FILE="${{RUN_DIR}}/crawler.pid"
RC_FILE="${{RUN_DIR}}/crawler.rc"

mkdir -p "${{RUN_DIR}}"
cd "${{LIVE_ROOT}}"

if [ ! -x "${{PYTHON_BIN}}" ]; then
  PYTHON_BIN="python3"
fi

set -a
. "${{ENV_FILE}}"
set +a

if [ -z "${{LOGISTICSEARCH_CRAWLER_DSN:-}}" ]; then
  echo "FAIL: LOGISTICSEARCH_CRAWLER_DSN is empty after sourcing env file" >&2
  exit 12
fi

export PYTHONPATH="${{LIVE_ROOT}}"
unset LOGISTICSEARCH_CRAWLER_CORE_ENABLE_PARSE_DISCOVERY_ENQUEUE

echo "== PREFLIGHT ==" > "${{PREFLIGHT_TXT}}"
echo "TIME=$(date -Is)" >> "${{PREFLIGHT_TXT}}"
echo "LIVE_ROOT=${{LIVE_ROOT}}" >> "${{PREFLIGHT_TXT}}"
echo "PYTHON_BIN=${{PYTHON_BIN}}" >> "${{PREFLIGHT_TXT}}"
echo "DSN_LOADED=YES_REDACTED" >> "${{PREFLIGHT_TXT}}"
if [ -z "${{LOGISTICSEARCH_CRAWLER_CORE_ENABLE_PARSE_DISCOVERY_ENQUEUE:-}}" ]; then
  echo "DISCOVERY_ENQUEUE_UNSET=YES" >> "${{PREFLIGHT_TXT}}"
else
  echo "DISCOVERY_ENQUEUE_UNSET=NO" >> "${{PREFLIGHT_TXT}}"
fi

psql "${{LOGISTICSEARCH_CRAWLER_DSN}}" -X -v ON_ERROR_STOP=1 -P pager=off > "${{DB_BEFORE_TXT}}" <<'__LS_DB_BEFORE_SQL__'
BEGIN READ ONLY;
SELECT 'frontier.host' AS table_name, count(*) AS rows FROM frontier.host
UNION ALL SELECT 'frontier.url', count(*) FROM frontier.url
UNION ALL SELECT 'http_fetch.fetch_attempt', count(*) FROM http_fetch.fetch_attempt
UNION ALL SELECT 'seed.seed_url', count(*) FROM seed.seed_url
UNION ALL SELECT 'seed.source', count(*) FROM seed.source
ORDER BY table_name;

SELECT
  count(*) AS total_urls,
  count(*) FILTER (WHERE state::text='queued') AS queued_total,
  count(*) FILTER (WHERE state::text='queued' AND next_fetch_at <= now()) AS due_queued_now,
  count(*) FILTER (WHERE state::text='retry_wait') AS retry_wait_total,
  count(*) FILTER (WHERE state::text='dead') AS dead_total,
  count(*) FILTER (WHERE fetch_attempt_count > 0) AS touched_urls,
  coalesce(sum(fetch_attempt_count),0) AS attempts_sum,
  count(*) FILTER (WHERE last_http_status BETWEEN 200 AND 299) AS http_2xx,
  count(*) FILTER (WHERE last_error_class='unexpected_fetch_runtime_error') AS unexpected,
  count(*) FILTER (WHERE position('frontier_permanent_error_finalize_r1=' in coalesce(last_error_message,'')) > 0) AS old_label
FROM frontier.url;
ROLLBACK;
__LS_DB_BEFORE_SQL__

cleanup() {{
  if [ -f "${{PID_FILE}}" ]; then
    pid="$(cat "${{PID_FILE}}" 2>/dev/null || true)"
    if [ -n "${{pid}}" ] && kill -0 "${{pid}}" 2>/dev/null; then
      kill -TERM "${{pid}}" 2>/dev/null || true
      sleep "${{TERM_GRACE_SECONDS}}"
      if kill -0 "${{pid}}" 2>/dev/null; then
        kill -KILL "${{pid}}" 2>/dev/null || true
      fi
    fi
  fi
}}
trap cleanup INT TERM

START_EPOCH="$(date +%s)"
echo "RUNNER_START=$(date -Is)" > "${{MONITOR_LOG}}"

"${{PYTHON_BIN}}" -u -m python_live_runtime.crawler_core_worker.logisticsearch1_main_entry \\
  --durable-claim \\
  --loop \\
  --sleep-seconds 5 \\
  --pause-sleep-seconds 15 \\
  --output json \\
  > "${{CRAWLER_LOG}}" 2>&1 &

CRAWLER_PID="$!"
echo "${{CRAWLER_PID}}" > "${{PID_FILE}}"
echo "CRAWLER_PID=${{CRAWLER_PID}}" >> "${{MONITOR_LOG}}"

while kill -0 "${{CRAWLER_PID}}" 2>/dev/null; do
  now_epoch="$(date +%s)"
  elapsed="$(( now_epoch - START_EPOCH ))"

  metrics="$(psql "${{LOGISTICSEARCH_CRAWLER_DSN}}" -X -At -F '|' -v ON_ERROR_STOP=1 <<'__LS_MONITOR_SQL__' 2>/dev/null || true
SELECT
  count(*) AS total_urls,
  count(*) FILTER (WHERE state::text='queued') AS queued_total,
  count(*) FILTER (WHERE state::text='queued' AND next_fetch_at <= now()) AS due_queued_now,
  count(*) FILTER (WHERE state::text='retry_wait') AS retry_wait_total,
  count(*) FILTER (WHERE state::text='dead') AS dead_total,
  count(*) FILTER (WHERE fetch_attempt_count > 0) AS touched_urls,
  coalesce(sum(fetch_attempt_count),0) AS attempts_sum,
  count(*) FILTER (WHERE last_http_status BETWEEN 200 AND 299) AS http_2xx,
  count(*) FILTER (WHERE left(coalesce(last_error_class,''),5)='http_') AS http_errors,
  count(*) FILTER (WHERE last_error_class IN (
    'browser_dns_name_not_resolved',
    'browser_ssl_version_or_cipher_mismatch',
    'browser_ssl_protocol_error',
    'browser_cert_common_name_invalid',
    'browser_cert_date_invalid',
    'browser_http2_protocol_error',
    'browser_navigation_timeout',
    'runtime_transport_retryable_error',
    'browser_connection_refused',
    'browser_connection_reset',
    'browser_navigation_error'
  )) AS browser_runtime,
  count(*) FILTER (WHERE last_error_class='unexpected_fetch_runtime_error') AS unexpected,
  count(*) FILTER (WHERE position('frontier_permanent_error_finalize_r1=' in coalesce(last_error_message,'')) > 0) AS old_label,
  count(*) FILTER (WHERE position('frontier_runtime_exception_retry_wait_r1=' in coalesce(last_error_message,'')) > 0) AS new_label
FROM frontier.url;
__LS_MONITOR_SQL__
)"

  raw_files="$(find /srv/webcrawler/raw_fetch -type f 2>/dev/null | wc -l | tr -d ' ')"
  raw_bytes="$(find /srv/webcrawler/raw_fetch -type f -printf '%s\\n' 2>/dev/null | awk '{{s+=$1}} END {{print s+0}}')"

  echo "FULL_TRAVERSAL_MONITOR T+${{elapsed}}s metrics=${{metrics}} raw=${{raw_files}}/${{raw_bytes}}" >> "${{MONITOR_LOG}}"
  # P0_PROD_SEPARATION_R3_BEGIN
  # Named metrics are emitted for operators and future automation.
  # The legacy pipe-form metrics line above is intentionally preserved for backward compatibility.
  IFS='|' read -r m_total m_queued m_due m_retry_wait m_dead m_touched m_attempts_sum m_http_2xx m_http_errors m_browser_runtime m_unexpected m_old_label m_new_label <<'__LS_MONITOR_METRICS_SPLIT__'
${{metrics}}
__LS_MONITOR_METRICS_SPLIT__
  if [ "${{HARD_TIMEOUT_SECONDS}}" -gt 0 ]; then
    global_timeout_enabled=true
  else
    global_timeout_enabled=false
  fi
  printf 'FULL_TRAVERSAL_MONITOR_NAMED {{"elapsed_seconds":%s,"total":%s,"queued":%s,"due":%s,"retry_wait":%s,"dead":%s,"touched":%s,"attempts_sum":%s,"http_2xx":%s,"http_errors":%s,"browser_runtime":%s,"unexpected":%s,"old_label":%s,"new_label":%s,"raw_files":%s,"raw_bytes":%s,"hard_timeout_seconds":%s,"global_timeout_enabled":%s}}\n' \
    "${{elapsed}}" "${{m_total:-0}}" "${{m_queued:-0}}" "${{m_due:-0}}" "${{m_retry_wait:-0}}" "${{m_dead:-0}}" "${{m_touched:-0}}" "${{m_attempts_sum:-0}}" "${{m_http_2xx:-0}}" "${{m_http_errors:-0}}" "${{m_browser_runtime:-0}}" "${{m_unexpected:-0}}" "${{m_old_label:-0}}" "${{m_new_label:-0}}" "${{raw_files:-0}}" "${{raw_bytes:-0}}" "${{HARD_TIMEOUT_SECONDS}}" "${{global_timeout_enabled}}" >> "${{MONITOR_LOG}}"
  # P0_PROD_SEPARATION_R3_END

  if [ "${{HARD_TIMEOUT_SECONDS}}" -gt 0 ] && [ "${{elapsed}}" -ge "${{HARD_TIMEOUT_SECONDS}}" ]; then
    echo "HARD_TIMEOUT_REACHED=${{elapsed}}" >> "${{MONITOR_LOG}}"
    kill -TERM "${{CRAWLER_PID}}" 2>/dev/null || true
    sleep "${{TERM_GRACE_SECONDS}}"
    if kill -0 "${{CRAWLER_PID}}" 2>/dev/null; then
      kill -KILL "${{CRAWLER_PID}}" 2>/dev/null || true
    fi
    break
  fi

  sleep "${{MONITOR_EVERY_SECONDS}}"
done

wait "${{CRAWLER_PID}}" 2>/dev/null
CRAWLER_RC="$?"
echo "${{CRAWLER_RC}}" > "${{RC_FILE}}"

psql "${{LOGISTICSEARCH_CRAWLER_DSN}}" -X -v ON_ERROR_STOP=1 -P pager=off > "${{DB_AFTER_TXT}}" <<'__LS_DB_AFTER_SQL__'
BEGIN READ ONLY;
SELECT 'frontier.host' AS table_name, count(*) AS rows FROM frontier.host
UNION ALL SELECT 'frontier.url', count(*) FROM frontier.url
UNION ALL SELECT 'http_fetch.fetch_attempt', count(*) FROM http_fetch.fetch_attempt
UNION ALL SELECT 'seed.seed_url', count(*) FROM seed.seed_url
UNION ALL SELECT 'seed.source', count(*) FROM seed.source
ORDER BY table_name;

SELECT
  count(*) AS total_urls,
  count(*) FILTER (WHERE state::text='queued') AS queued_total,
  count(*) FILTER (WHERE state::text='queued' AND next_fetch_at <= now()) AS due_queued_now,
  count(*) FILTER (WHERE state::text='retry_wait') AS retry_wait_total,
  count(*) FILTER (WHERE state::text='dead') AS dead_total,
  count(*) FILTER (WHERE fetch_attempt_count > 0) AS touched_urls,
  coalesce(sum(fetch_attempt_count),0) AS attempts_sum,
  count(*) FILTER (WHERE last_http_status BETWEEN 200 AND 299) AS http_2xx,
  count(*) FILTER (WHERE last_error_class='unexpected_fetch_runtime_error') AS unexpected,
  count(*) FILTER (WHERE position('frontier_permanent_error_finalize_r1=' in coalesce(last_error_message,'')) > 0) AS old_label
FROM frontier.url;

SELECT last_error_class, count(*) AS rows
FROM frontier.url
WHERE last_error_class IS NOT NULL
GROUP BY last_error_class
ORDER BY rows DESC, last_error_class;
ROLLBACK;
__LS_DB_AFTER_SQL__

"${{PYTHON_BIN}}" -B - "${{RUN_DIR}}" "${{CRAWLER_RC}}" <<'__LS_FINAL_JSON_PY__'
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

run_dir = Path(sys.argv[1])
crawler_rc = int(sys.argv[2])

# FSTRING_LITERAL_BRACE_FIX_R3:
# This Python dict is embedded inside an outer Python f-string that renders runner.sh.
# Literal braces must therefore be doubled in the source file.
payload = {{
    "schema": "logisticsearch.full_traversal_test_run.v1",
    "run_dir": str(run_dir),
    "finished_at": datetime.now(timezone.utc).isoformat(),
    "crawler_rc": crawler_rc,
    "crawler_log": str(run_dir / "crawler.log"),
    "monitor_log": str(run_dir / "monitor.log"),
    "db_snapshot_before": str(run_dir / "db_snapshot_before.txt"),
    "db_snapshot_after": str(run_dir / "db_snapshot_after.txt"),
}}
(run_dir / "final.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
__LS_FINAL_JSON_PY__

(
  cd "${{RUN_DIR}}"
  sha256sum ./* 2>/dev/null | sort
) > "${{CHECKSUMS_TXT}}"

echo "RUNNER_DONE=$(date -Is)" >> "${{MONITOR_LOG}}"
echo "CRAWLER_RC=${{CRAWLER_RC}}" >> "${{MONITOR_LOG}}"
exit 0
"""


def _render_status_shell(run_root: Path) -> str:
    return f"""#!/usr/bin/env bash
set -Eeuo pipefail
RUN_ROOT={_quote(run_root)}
echo "== DURABLE FULL TRAVERSAL STATUS =="
echo "TIME=$(date -Is)"
echo "RUN_ROOT=${{RUN_ROOT}}"
echo
echo "== tmux sessions =="
tmux ls 2>/dev/null || true
echo
echo "== latest runs =="
find "${{RUN_ROOT}}" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\\n' 2>/dev/null | sort -nr | head -n 10
"""


def prepare_run(
    *,
    durable_root: Path,
    live_root: Path,
    env_file: Path,
    label: str,
    hard_timeout_seconds: int,
    monitor_every_seconds: int,
    term_grace_seconds: int,
) -> Path:
    run_dir = _build_run_dir(durable_root, label)
    if run_dir.exists():
        raise FileExistsError(f"run directory already exists: {run_dir}")

    run_dir.mkdir(parents=True, mode=0o775)
    os.chmod(run_dir, 0o2775)

    redacted = {
        "schema": "logisticsearch.full_traversal_run_env_redacted.v1",
        "live_root": str(live_root),
        "env_file": str(env_file),
        "dsn_value": "REDACTED_NOT_STORED",
        "discovery_enqueue_policy": "unset_by_runner",
        "hard_timeout_seconds": hard_timeout_seconds,
        "monitor_every_seconds": monitor_every_seconds,
        "term_grace_seconds": term_grace_seconds,
    }

    _write_text(run_dir / "run.env.redacted.json", json.dumps(redacted, indent=2, sort_keys=True) + "\n")
    _write_text(
        run_dir / "runner.sh",
        _render_runner_shell(
            run_dir=run_dir,
            live_root=live_root,
            env_file=env_file,
            hard_timeout_seconds=hard_timeout_seconds,
            monitor_every_seconds=monitor_every_seconds,
            term_grace_seconds=term_grace_seconds,
        ),
        executable=True,
    )
    _write_text(run_dir / "status.sh", _render_status_shell(durable_root), executable=True)

    source_file = Path(__file__).resolve()
    if source_file.exists():
        shutil.copy2(source_file, run_dir / "runner.py")

    return run_dir


def launch_tmux(run_dir: Path, *, session_name: str) -> None:
    if not shutil.which("tmux"):
        raise RuntimeError("tmux is not available")
    runner = run_dir / "runner.sh"
    if not runner.exists():
        raise FileNotFoundError(f"runner.sh missing: {runner}")
    subprocess.run(["tmux", "new-session", "-d", "-s", session_name, "bash", str(runner)], check=True)


def print_status(durable_root: Path) -> int:
    print(f"RUN_ROOT={durable_root}")
    if durable_root.exists():
        runs = sorted(
            [p for p in durable_root.iterdir() if p.is_dir()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for path in runs[:10]:
            final_json = path / "final.json"
            crawler_log = path / "crawler.log"
            monitor_log = path / "monitor.log"
            print(
                "RUN "
                f"path={path} "
                f"final_json={final_json.exists()} "
                f"crawler_log={crawler_log.exists()} "
                f"monitor_log={monitor_log.exists()}"
            )
    else:
        print("RUN_ROOT_EXISTS=NO")

    if shutil.which("tmux"):
        proc = subprocess.run(["tmux", "ls"], text=True, capture_output=True, check=False)
        print("TMUX_LS_BEGIN")
        print(proc.stdout.strip())
        print("TMUX_LS_END")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare or launch a durable crawler_core full traversal test run.",
    )
    parser.add_argument("--mode", choices=("prepare", "launch-tmux", "status"), default="prepare")
    parser.add_argument("--label", default=DEFAULT_LABEL)
    parser.add_argument("--durable-root", default=str(DEFAULT_DURABLE_RUN_ROOT))
    parser.add_argument("--live-root", default=str(DEFAULT_LIVE_ROOT))
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument(
        "--hard-timeout-seconds",
        type=_non_negative_int,
        default=DEFAULT_HARD_TIMEOUT_SECONDS,
        help=(
            "Test-harness global timeout in seconds. "
            "Use 0 to disable the global harness timeout. "
            "7/24 production crawler lifecycle must be controlled by runtime_control, "
            "request-level timeouts, watchdogs, and service supervision, not by this test limit."
        ),
    )
    parser.add_argument("--monitor-every-seconds", type=int, default=DEFAULT_MONITOR_EVERY_SECONDS)
    parser.add_argument("--term-grace-seconds", type=int, default=DEFAULT_TERM_GRACE_SECONDS)
    parser.add_argument("--tmux-session", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    durable_root = Path(args.durable_root)
    live_root = Path(args.live_root)
    env_file = Path(args.env_file)

    if args.mode == "status":
        return print_status(durable_root)

    run_dir = prepare_run(
        durable_root=durable_root,
        live_root=live_root,
        env_file=env_file,
        label=args.label,
        hard_timeout_seconds=args.hard_timeout_seconds,
        monitor_every_seconds=args.monitor_every_seconds,
        term_grace_seconds=args.term_grace_seconds,
    )

    session_name = args.tmux_session or _sanitize_label(run_dir.name)

    result = {
        "schema": "logisticsearch.full_traversal_runner.prepare_result.v1",
        "mode": args.mode,
        "run_dir": str(run_dir),
        "runner_sh": str(run_dir / "runner.sh"),
        "status_sh": str(run_dir / "status.sh"),
        "tmux_session": session_name,
        "launched": False,
    }

    if args.mode == "launch-tmux":
        launch_tmux(run_dir, session_name=session_name)
        result["launched"] = True

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
