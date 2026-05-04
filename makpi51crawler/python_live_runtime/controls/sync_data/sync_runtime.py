#!/usr/bin/env python3
"""Synchronize tracked makpi51crawler surfaces into the new live root.

EN:
This is the new-topology Python replacement for legacy legacy live-only sync-runtime wrapper.
It syncs /logisticsearch/repo/makpi51crawler into /logisticsearch/makpi51crawler
while preserving runtime-local .venv and config. It verifies JSON parse, Python
ast.parse, English catalog projection, and repo/live tracked-surface hashes.
It does not start/restart the service and does not touch PostgreSQL.

TR:
Bu dosya legacy legacy live-only sync-runtime wrapper komutunun yeni topolojiye göre
Python karşılığıdır. /logisticsearch/repo/makpi51crawler yüzeyini
/logisticsearch/makpi51crawler canlı köküne senkronlar; runtime-local .venv ve
config korunur. JSON parse, Python ast.parse, English catalog projection ve
repo/live tracked-surface hash eşitliğini doğrular. Servisi başlatmaz/restart
etmez ve PostgreSQL'e dokunmaz.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_REPO = Path("/logisticsearch/repo")
DEFAULT_REPO_SOURCE = DEFAULT_REPO / "makpi51crawler"
DEFAULT_LIVE_ROOT = Path("/logisticsearch/makpi51crawler")
DEFAULT_SERVICE = "logisticsearch-webcrawler.service"

TRACKED_DIRS = ("python_live_runtime", "catalog", "taxonomy")
TRACKED_FILES = ("README.md", "RUNBOOK_SYNC_REPO_AND_RUNTIME.md", ".gitignore")
PRESERVED_DIRS = (".venv", "config")
FORBIDDEN_LEGACY_NAMES = ("bin", "lib", "webcrawler", "sql", "crawler_exports")


@dataclass(frozen=True, slots=True)
class SurfaceHash:
    name: str
    repo_count: int
    live_count: int
    repo_hash: str
    live_hash: str


@dataclass(frozen=True, slots=True)
class RuntimeSyncResult:
    repo_source: Path
    live_root: Path
    source_count: int
    seed_count: int
    surface_hashes: tuple[SurfaceHash, ...]


def _run(argv: list[str], *, cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
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


def _service_state(service: str) -> str:
    completed = subprocess.run(
        ["systemctl", "--user", "is-active", service],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.stdout.strip() or "unknown"


def _process_count() -> int:
    completed = subprocess.run(
        ["ps", "-eo", "args="],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    count = 0
    for line in completed.stdout.splitlines():
        if "logisticsearch1_main_entry" in line or "--durable-claim" in line:
            if "sync_runtime.py" not in line and "sync_all.py" not in line:
                count += 1
    return count


def _remove_python_caches(root: Path) -> int:
    removed = 0
    if not root.exists():
        return removed
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_dir() and path.name in {"__pycache__", ".pytest_cache", ".mypy_cache"}:
            shutil.rmtree(path)
            removed += 1
        elif path.is_file() and path.suffix in {".pyc", ".pyo"}:
            path.unlink()
            removed += 1
    return removed


def _rsync_dir(source: Path, target: Path, *, dry_run: bool = False) -> None:
    if not source.is_dir():
        raise SystemExit(f"FAIL: missing source directory: {source}")
    if dry_run:
        print(f"DRY_RUN: would rsync --delete {source}/ -> {target}/")
        return
    target.mkdir(parents=True, exist_ok=True)
    _run(["rsync", "-a", "--delete", f"{source}/", f"{target}/"])


def _copy_file(source: Path, target: Path, *, dry_run: bool = False) -> None:
    if not source.is_file():
        raise SystemExit(f"FAIL: missing source file: {source}")
    if dry_run:
        print(f"DRY_RUN: would copy {source} -> {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _remove_forbidden_legacy_surfaces(live_root: Path, *, dry_run: bool = False) -> None:
    for name in FORBIDDEN_LEGACY_NAMES:
        target = live_root / name
        if not target.exists():
            continue
        if dry_run:
            print(f"DRY_RUN: would remove forbidden legacy surface: {target}")
            continue
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()
        print(f"OK: removed forbidden legacy surface inside new live root: {target}")


def _validate_repo_alignment(repo: Path) -> None:
    if not (repo / ".git").is_dir():
        raise SystemExit(f"FAIL: {repo} is not a git repository")
    head = _capture(["git", "rev-parse", "HEAD"], cwd=repo)
    origin = _capture(["git", "rev-parse", "origin/main"], cwd=repo)
    status_count = _capture(["bash", "-lc", "git status --porcelain | wc -l | tr -d ' '"], cwd=repo)
    print(f"REPO_HEAD={head}")
    print(f"REPO_ORIGIN_HEAD={origin}")
    print(f"REPO_STATUS_COUNT={status_count}")
    if head != origin:
        raise SystemExit("FAIL: repo HEAD != origin/main")
    if status_count != "0":
        raise SystemExit("FAIL: repo worktree is not clean")


def _validate_local_runtime_surfaces(live_root: Path) -> None:
    required = [
        live_root / ".venv/bin/python",
        live_root / "config/webcrawler.env",
        live_root / "python_live_runtime/logisticsearch1_main_entry.py",
        live_root / "catalog/startpoints/en/english_source_families_v2.json",
        live_root / "taxonomy/schema/logisticsearch_taxonomy_language_schema_v1.json",
    ]
    for path in required:
        if not path.exists():
            raise SystemExit(f"FAIL: required live path missing: {path}")
        print(f"PASS_PATH: {path}")

    for name in FORBIDDEN_LEGACY_NAMES:
        forbidden = live_root / name
        if forbidden.exists():
            raise SystemExit(f"FAIL: forbidden legacy surface exists in new live root: {forbidden}")
        print(f"PASS_ABSENT: {forbidden}")


def _parse_json_files(root: Path) -> int:
    files = sorted(root.rglob("*.json"))
    for path in files:
        json.loads(path.read_text(encoding="utf-8"))
    return len(files)


def _parse_python_files(root: Path) -> int:
    files = sorted(root.rglob("*.py"))
    for path in files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return len(files)


def _project_catalog(live_root: Path) -> tuple[int, int]:
    runtime_file = live_root / "python_live_runtime/logisticsearch1_1_0_1_startpoint_catalog_runtime.py"
    catalog_file = live_root / "catalog/startpoints/en/english_source_families_v2.json"

    spec = importlib.util.spec_from_file_location(
        "logisticsearch_startpoint_catalog_runtime_sync_runtime_audit",
        runtime_file,
    )
    if spec is None or spec.loader is None:
        raise SystemExit("FAIL: could not load runtime module spec")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    project_catalog_to_seed_rows = getattr(module, "project_catalog_to_seed_rows", None)
    if project_catalog_to_seed_rows is None:
        raise SystemExit("FAIL: project_catalog_to_seed_rows missing")

    catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
    projected = project_catalog_to_seed_rows(catalog)

    def read_row_value(row: object, key: str) -> object:
        """Return one projected row field from dict or object-shaped rows.

        EN: The catalog runtime currently returns dictionaries, but this sync
        control should also tolerate object/dataclass-like rows if the runtime
        projection contract later becomes stricter again.

        TR: Catalog runtime şu anda dictionary döndürüyor; ancak bu sync kontrolü,
        ileride runtime projection sözleşmesi tekrar object/dataclass benzeri hale
        gelirse onu da güvenli şekilde tolere etmelidir.
        """

        if isinstance(row, dict):
            return row.get(key)
        return getattr(row, key, None)

    if isinstance(projected, dict):
        projected_sources = projected.get("projected_sources")
        projected_seed_urls = projected.get("projected_seed_urls")

        if not isinstance(projected_sources, list):
            raise SystemExit("FAIL: projected_sources missing or not list")
        if not isinstance(projected_seed_urls, list):
            raise SystemExit("FAIL: projected_seed_urls missing or not list")

        source_codes = {
            str(source_code)
            for row in projected_sources
            for source_code in [read_row_value(row, "source_code")]
            if source_code
        }
        seed_count = len(projected_seed_urls)
        return len(source_codes), seed_count

    if hasattr(projected, "sources") and hasattr(projected, "seed_urls"):
        source_codes = {
            str(source_code)
            for row in projected.sources
            for source_code in [read_row_value(row, "source_code")]
            if source_code
        }
        seed_count = len(projected.seed_urls)
        return len(source_codes), seed_count

    raise SystemExit(
        "FAIL: unsupported project_catalog_to_seed_rows return shape: "
        f"{type(projected).__name__}"
    )


def _relative_files(root: Path) -> list[Path]:
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


def _hash_surface(root: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    files = _relative_files(root)
    for rel in files:
        digest.update(str(rel).encode("utf-8"))
        digest.update(b"\0")
        digest.update((root / rel).read_bytes())
        digest.update(b"\0")
    return len(files), digest.hexdigest()


def _surface_hash(repo_source: Path, live_root: Path, name: str) -> SurfaceHash:
    repo_path = repo_source / name
    live_path = live_root / name
    repo_count, repo_hash = _hash_surface(repo_path)
    live_count, live_hash = _hash_surface(live_path)
    return SurfaceHash(name=name, repo_count=repo_count, live_count=live_count, repo_hash=repo_hash, live_hash=live_hash)


def sync_runtime(
    repo: Path = DEFAULT_REPO,
    repo_source: Path = DEFAULT_REPO_SOURCE,
    live_root: Path = DEFAULT_LIVE_ROOT,
    service: str = DEFAULT_SERVICE,
    *,
    dry_run: bool = False,
    allow_active_service: bool = False,
) -> RuntimeSyncResult:
    repo = repo.resolve()
    repo_source = repo_source.resolve()
    live_root = live_root.resolve()

    print("== sync_runtime ==")
    print(f"repo={repo}")
    print(f"repo_source={repo_source}")
    print(f"live_root={live_root}")
    print(f"service={service}")
    print(f"dry_run={dry_run}")
    print(f"allow_active_service={allow_active_service}")
    print()

    if not repo_source.is_dir():
        raise SystemExit(f"FAIL: repo source missing: {repo_source}")

    _validate_repo_alignment(repo)

    service_state = _service_state(service)
    process_count = _process_count()
    print(f"USER_SERVICE_ACTIVE={service_state}")
    print(f"MATCHING_PROCESS_COUNT={process_count}")

    if not allow_active_service and service_state == "active":
        raise SystemExit(f"FAIL: {service} is active; stop it before runtime sync")
    if process_count != 0:
        raise SystemExit("FAIL: crawler process appears to be running")

    if not dry_run:
        live_root.mkdir(parents=True, exist_ok=True)

    for preserved in PRESERVED_DIRS:
        path = live_root / preserved
        if not path.exists() and not dry_run:
            print(f"WARN: preserved runtime-local surface currently missing: {path}")

    print("== cache cleanup before sync ==")
    removed_before = 0 if dry_run else _remove_python_caches(live_root)
    print(f"CACHE_REMOVED_BEFORE={removed_before}")

    print("== sync tracked directories ==")
    for name in TRACKED_DIRS:
        _rsync_dir(repo_source / name, live_root / name, dry_run=dry_run)

    print("== sync tracked root files ==")
    for name in TRACKED_FILES:
        _copy_file(repo_source / name, live_root / name, dry_run=dry_run)

    print("== remove forbidden legacy surfaces inside new live root ==")
    _remove_forbidden_legacy_surfaces(live_root, dry_run=dry_run)

    print("== cache cleanup after sync ==")
    removed_after = 0 if dry_run else _remove_python_caches(live_root)
    print(f"CACHE_REMOVED_AFTER={removed_after}")

    if dry_run:
        print("DRY_RUN: validation skipped after non-mutating plan.")
        return RuntimeSyncResult(repo_source=repo_source, live_root=live_root, source_count=0, seed_count=0, surface_hashes=())

    _validate_local_runtime_surfaces(live_root)

    json_count = _parse_json_files(live_root / "catalog") + _parse_json_files(live_root / "taxonomy")
    python_count = _parse_python_files(live_root / "python_live_runtime")
    source_count, seed_count = _project_catalog(live_root)

    print(f"JSON_PARSE_FILE_COUNT={json_count}")
    print(f"PYTHON_AST_PARSE_FILE_COUNT={python_count}")
    print(f"PROJECTED_SOURCE_COUNT={source_count}")
    print(f"PROJECTED_SEED_URL_COUNT={seed_count}")

    if source_count != 27:
        raise SystemExit("FAIL: projected source count != 27")
    if seed_count != 43:
        raise SystemExit("FAIL: projected seed count != 43")

    surface_hashes = tuple(_surface_hash(repo_source, live_root, name) for name in TRACKED_DIRS)
    for item in surface_hashes:
        print(f"SURFACE={item.name}")
        print(f"REPO_COUNT={item.repo_count}")
        print(f"LIVE_COUNT={item.live_count}")
        print(f"REPO_HASH={item.repo_hash}")
        print(f"LIVE_HASH={item.live_hash}")
        if item.repo_count != item.live_count or item.repo_hash != item.live_hash:
            raise SystemExit(f"FAIL: repo/live surface mismatch: {item.name}")

    print("OK: sync_runtime completed")
    return RuntimeSyncResult(
        repo_source=repo_source,
        live_root=live_root,
        source_count=source_count,
        seed_count=seed_count,
        surface_hashes=surface_hashes,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synchronize tracked makpi51crawler surfaces into the new live root.")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--repo-source", type=Path, default=DEFAULT_REPO_SOURCE)
    parser.add_argument("--live-root", type=Path, default=DEFAULT_LIVE_ROOT)
    parser.add_argument("--service", default=DEFAULT_SERVICE)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-active-service", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    sync_runtime(
        repo=args.repo,
        repo_source=args.repo_source,
        live_root=args.live_root,
        service=args.service,
        dry_run=args.dry_run,
        allow_active_service=args.allow_active_service,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
