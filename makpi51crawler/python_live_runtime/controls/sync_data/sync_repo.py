#!/usr/bin/env python3
"""Synchronize /logisticsearch/repo with GitHub origin/main.

EN:
This is the tracked Python replacement for legacy legacy live-only sync-repo wrapper.
It intentionally preserves the existing operational behavior: validate the repo,
fetch origin, hard-reset to origin/main, clean untracked files, and verify a clean
mirror. This command can discard local drift inside /logisticsearch/repo.

TR:
Bu dosya legacy legacy live-only sync-repo wrapper komutunun tracked Python
karşılığıdır. Mevcut operasyon davranışını bilinçli olarak korur: repo'yu doğrula,
origin'i fetch et, origin/main'e hard reset yap, untracked dosyaları temizle ve
temiz mirror doğrula. Bu komut /logisticsearch/repo altındaki local drift'i
silebilir.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPO = Path("/logisticsearch/repo")
DEFAULT_REMOTE_URL = "git@github.com:malikepoglu/logisticsearch.git"
DEFAULT_BRANCH = "main"


@dataclass(frozen=True, slots=True)
class RepoSyncResult:
    repo: Path
    branch: str
    head: str
    origin_head: str
    status_short: str


def _run(
    argv: list[str],
    *,
    cwd: Path | None = None,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run a command with strict error handling."""
    return subprocess.run(
        argv,
        cwd=str(cwd) if cwd is not None else None,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
        check=True,
    )


def _capture(argv: list[str], *, cwd: Path | None = None) -> str:
    return _run(argv, cwd=cwd, capture=True).stdout.strip()


def _capture_optional(argv: list[str], *, cwd: Path | None = None) -> str:
    """Capture command output; return an empty string when the command exits non-zero.

    EN: git config exits 1 when a key is unset; that is not an error for sparse-checkout probing.
    TR: git config anahtar yokken 1 döner; sparse-checkout yoklaması için bu hata değildir.
    """
    completed = subprocess.run(
        argv,
        cwd=str(cwd) if cwd is not None else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def sync_repo(
    repo: Path = DEFAULT_REPO,
    remote_url: str = DEFAULT_REMOTE_URL,
    branch: str = DEFAULT_BRANCH,
    *,
    dry_run: bool = False,
) -> RepoSyncResult:
    repo = repo.resolve()

    print("== sync_repo ==")
    print(f"repo={repo}")
    print(f"expected_remote={remote_url}")
    print(f"branch={branch}")
    print(f"dry_run={dry_run}")
    print()

    if not (repo / ".git").is_dir():
        raise SystemExit(f"FAIL: {repo} is not a git repository")

    current_remote = _capture(["git", "remote", "get-url", "origin"], cwd=repo)
    current_branch = _capture(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo)

    print(f"REMOTE_URL={current_remote}")
    print(f"CURRENT_BRANCH={current_branch}")

    if current_remote != remote_url:
        raise SystemExit("FAIL: origin remote mismatch")
    if current_branch != branch:
        raise SystemExit("FAIL: branch mismatch")

    if dry_run:
        print("DRY_RUN: would run git fetch --prune origin")
        print(f"DRY_RUN: would run git reset --hard origin/{branch}")
        print("DRY_RUN: would run git clean -fdx")
    else:
        _run(["git", "fetch", "--prune", "origin"], cwd=repo)
        print("OK: fetch completed")

        sparse_enabled = _capture_optional(["git", "config", "--bool", "core.sparseCheckout"], cwd=repo)
        if sparse_enabled == "true" or (repo / ".git/info/sparse-checkout").exists():
            _run(["git", "sparse-checkout", "disable"], cwd=repo)
            print("OK: sparse-checkout disabled")
        else:
            print("OK: sparse-checkout not active")

        _run(["git", "reset", "--hard", f"origin/{branch}"], cwd=repo)
        print(f"OK: hard reset to origin/{branch} completed")

        _run(["git", "clean", "-fdx"], cwd=repo)
        print("OK: git clean completed")

    head = _capture(["git", "rev-parse", "HEAD"], cwd=repo)
    origin_head = _capture(["git", "rev-parse", f"origin/{branch}"], cwd=repo)
    status_short = _capture(["git", "status", "-sb"], cwd=repo)

    print(f"POST_HEAD={head}")
    print(f"POST_ORIGIN={origin_head}")
    print(status_short)

    if not dry_run:
        if head != origin_head:
            raise SystemExit(f"FAIL: HEAD != origin/{branch}")
        if status_short != f"## {branch}...origin/{branch}":
            raise SystemExit("FAIL: repo working tree not clean after sync")

    print("OK: sync_repo completed")
    return RepoSyncResult(repo=repo, branch=branch, head=head, origin_head=origin_head, status_short=status_short)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synchronize /logisticsearch/repo with origin/main.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--remote-url", default=DEFAULT_REMOTE_URL)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    sync_repo(
        repo=args.repo,
        remote_url=args.remote_url,
        branch=args.branch,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
