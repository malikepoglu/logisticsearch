#!/usr/bin/env python3
"""Safe orchestrator for repo sync + runtime sync.

EN:
Default behavior is intentionally safe and operator-controlled:
1. synchronize /logisticsearch/repo from GitHub
2. synchronize tracked makpi51crawler surfaces into /logisticsearch/makpi51crawler
3. run validation/reseal inside sync_runtime
4. do not start/restart service
5. do not touch PostgreSQL
6. do not run crawler

TR:
Varsayılan davranış bilinçli olarak güvenli ve operatör kontrollüdür:
1. /logisticsearch/repo yüzeyini GitHub'dan senkronla
2. tracked makpi51crawler yüzeylerini /logisticsearch/makpi51crawler içine senkronla
3. sync_runtime içinde doğrulama/reseal çalıştır
4. servisi başlatma/restart etme
5. PostgreSQL'e dokunma
6. crawler çalıştırma
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


try:
    from .sync_repo import DEFAULT_BRANCH, DEFAULT_REMOTE_URL, DEFAULT_REPO, sync_repo
    from .sync_runtime import DEFAULT_LIVE_ROOT, DEFAULT_REPO_SOURCE, DEFAULT_SERVICE, sync_runtime
except ImportError:  # pragma: no cover - direct script/importlib fallback
    # EN: When this file is loaded directly with importlib.spec_from_file_location,
    # the sibling-module directory is not guaranteed to be present on sys.path.
    # Add the current file's directory before falling back to sibling imports.
    #
    # TR: Bu dosya importlib.spec_from_file_location ile doğrudan yüklendiğinde,
    # kardeş modül klasörünün sys.path içinde olması garanti değildir. Kardeş
    # import fallback öncesinde mevcut dosyanın klasörünü açıkça ekle.
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

    from sync_repo import DEFAULT_BRANCH, DEFAULT_REMOTE_URL, DEFAULT_REPO, sync_repo
    from sync_runtime import DEFAULT_LIVE_ROOT, DEFAULT_REPO_SOURCE, DEFAULT_SERVICE, sync_runtime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run safe repo + runtime sync sequence for makpi51crawler.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--repo-source", type=Path, default=DEFAULT_REPO_SOURCE)
    parser.add_argument("--live-root", type=Path, default=DEFAULT_LIVE_ROOT)
    parser.add_argument("--remote-url", default=DEFAULT_REMOTE_URL)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--service", default=DEFAULT_SERVICE)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-repo-sync", action="store_true")
    parser.add_argument("--skip-runtime-sync", action="store_true")
    parser.add_argument("--allow-active-service", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    print("== sync_makpi51crawler ==")
    print(f"repo={args.repo}")
    print(f"repo_source={args.repo_source}")
    print(f"live_root={args.live_root}")
    print(f"branch={args.branch}")
    print(f"dry_run={args.dry_run}")
    print(f"skip_repo_sync={args.skip_repo_sync}")
    print(f"skip_runtime_sync={args.skip_runtime_sync}")
    print("service_start=false")
    print("db_touch=false")
    print("crawler_run=false")
    print()

    if not args.skip_repo_sync:
        sync_repo(
            repo=args.repo,
            remote_url=args.remote_url,
            branch=args.branch,
            dry_run=args.dry_run,
        )
    else:
        print("SKIP: repo sync")

    if not args.skip_runtime_sync:
        sync_runtime(
            repo=args.repo,
            repo_source=args.repo_source,
            live_root=args.live_root,
            service=args.service,
            dry_run=args.dry_run,
            allow_active_service=args.allow_active_service,
        )
    else:
        print("SKIP: runtime sync")

    print()
    print("OK: sync_makpi51crawler completed")
    print("SERVICE_STARTED=false")
    print("DB_TOUCHED=false")
    print("CRAWLER_RUN=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
