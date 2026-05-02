#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EN: LogisticSearch multilingual source_seed planner.
TR: LogisticSearch çok dilli source_seed planlayıcı modülü.

EN:
This module is intentionally a PLANNER, not a WORKER.
It reads canonical startpoint catalogs and taxonomy JSON inventory, then writes
reviewable source_seed evidence files. It does not claim URLs, fetch pages,
write frontier rows, create database objects, touch Pi51c, or start services.

TR:
Bu modül bilinçli olarak WORKER değil PLANNER modülüdür.
Canonical startpoint kataloglarını ve taxonomy JSON envanterini okur, ardından
incelenebilir source_seed kanıt dosyaları üretir. URL claim etmez, sayfa çekmez,
frontier satırı yazmaz, DB nesnesi oluşturmaz, Pi51c'ye dokunmaz ve servis
başlatmaz.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


# EN: Canonical language order used across LogisticSearch taxonomy work.
# TR: LogisticSearch taxonomy hattında kullanılan canonical dil sırası.
CANONICAL_LANGUAGE_ORDER: tuple[str, ...] = (
    "ar",
    "bg",
    "cs",
    "de",
    "el",
    "en",
    "es",
    "fr",
    "hu",
    "it",
    "ja",
    "ko",
    "nl",
    "pt",
    "ro",
    "ru",
    "tr",
    "zh",
    "hi",
    "bn",
    "ur",
    "uk",
    "id",
    "vi",
    "he",
)


@dataclass(frozen=True)
class SourceSeedCandidate:
    """EN/TR: Reviewable source_seed candidate row, never a durable runtime write."""

    source_seed_id: str
    language: str
    source_family_code: str
    source_family_name: str
    source_host: str
    source_category: str
    surface_code: str
    surface_type: str
    seed_index: int
    seed_type: str
    canonical_url: str
    url_host: str
    priority: int
    planner_status: str
    mutation_allowed_now: str


def _repo_default() -> Path:
    """EN/TR: Infer repo root from this hierarchical webcrawler/lib module path."""
    return Path(__file__).resolve().parents[5]


def _sha256_file(path: Path) -> str:
    """EN/TR: Return SHA256 for audit evidence."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    """EN/TR: Read UTF-8 JSON with explicit error context."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - operator-facing guard
        raise ValueError(f"failed to read JSON: {path}: {exc}") from exc


def _write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    """EN/TR: Write deterministic TSV evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """EN/TR: Write deterministic JSONL planner evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _safe_code(value: str) -> str:
    """EN/TR: Normalize human/source codes for stable source_seed IDs."""
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return normalized or "unknown"


def _first_text(mapping: dict[str, Any], keys: tuple[str, ...], default: str = "") -> str:
    """EN/TR: Return first non-empty string value from a JSON object."""
    for key in keys:
        value = mapping.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return default


def _first_int(mapping: dict[str, Any], keys: tuple[str, ...], default: int = 100) -> int:
    """EN/TR: Return first integer-like value from a JSON object."""
    for key in keys:
        value = mapping.get(key)
        if value is None or str(value).strip() == "":
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return default


def load_taxonomy_inventory(language_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """EN/TR: Validate the canonical 25-language taxonomy JSON inventory."""
    hard_errors: list[str] = []
    rows: list[dict[str, Any]] = []

    files = sorted(language_dir.glob("logisticsearch_taxonomy_*_*.json"))
    if len(files) != 25:
        hard_errors.append(f"expected 25 taxonomy language files, found {len(files)}")

    for path in files:
        try:
            data = _read_json(path)
        except ValueError as exc:
            hard_errors.append(str(exc))
            continue

        if not isinstance(data, list):
            hard_errors.append(f"taxonomy file is not a JSON list: {path}")
            continue

        language_values = sorted(
            {
                str(item.get("language", "")).strip()
                for item in data
                if isinstance(item, dict)
            }
        )
        last_term_id = str(data[-1].get("term_id", "")) if data else ""
        result = "PASS" if len(data) == 337 and len(language_values) == 1 else "FAIL"

        if result != "PASS":
            hard_errors.append(
                f"taxonomy inventory mismatch: {path.name}: "
                f"record_count={len(data)} language_values={language_values}"
            )

        rows.append(
            {
                "file": path.name,
                "record_count": len(data),
                "language_values": ",".join(language_values),
                "last_term_id": last_term_id,
                "result": result,
            }
        )

    return rows, hard_errors


def discover_startpoint_catalogs(catalog_root: Path) -> list[Path]:
    """EN/TR: Discover existing language startpoint catalogs without requiring all 25 yet."""
    if not catalog_root.exists():
        return []
    return sorted(catalog_root.glob("*/*.json"))


def build_source_seed_candidates(catalog_paths: list[Path]) -> tuple[
    list[SourceSeedCandidate],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[str],
]:
    """EN/TR: Flatten startpoint catalogs into reviewable source_seed candidate rows."""
    candidates: list[SourceSeedCandidate] = []
    family_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    hard_errors: list[str] = []

    for catalog_path in catalog_paths:
        language = catalog_path.parent.name
        try:
            catalog = _read_json(catalog_path)
        except ValueError as exc:
            hard_errors.append(str(exc))
            continue

        if not isinstance(catalog, dict):
            hard_errors.append(f"catalog root is not an object: {catalog_path}")
            continue

        source_families = catalog.get("source_families", [])
        if not isinstance(source_families, list):
            hard_errors.append(f"source_families is not a list: {catalog_path}")
            continue

        for family_index, family in enumerate(source_families, start=1):
            if not isinstance(family, dict):
                hard_errors.append(f"family is not an object: {catalog_path}:{family_index}")
                continue

            family_code = _first_text(family, ("source_family_code", "family_code"), f"family_{family_index}")
            family_name = _first_text(family, ("source_family_name", "family_name"), family_code)
            source_host = _first_text(family, ("source_host", "host"), "")
            source_category = _first_text(family, ("source_category", "category"), "")

            surfaces = family.get("seed_surfaces", [])
            if not isinstance(surfaces, list):
                hard_errors.append(f"seed_surfaces is not a list: {catalog_path}:{family_code}")
                continue

            family_seed_count = 0

            for surface_index, surface in enumerate(surfaces, start=1):
                if not isinstance(surface, dict):
                    hard_errors.append(
                        f"seed surface is not an object: {catalog_path}:{family_code}:{surface_index}"
                    )
                    continue

                surface_code = _first_text(surface, ("surface_code", "code"), f"surface_{surface_index}")
                surface_type = _first_text(surface, ("surface_type", "type"), "unknown_surface")
                seed_urls = surface.get("seed_urls", [])

                if not isinstance(seed_urls, list):
                    hard_errors.append(
                        f"seed_urls is not a list: {catalog_path}:{family_code}:{surface_code}"
                    )
                    continue

                surface_rows.append(
                    {
                        "language": language,
                        "catalog_file": str(catalog_path),
                        "source_family_code": family_code,
                        "surface_code": surface_code,
                        "surface_type": surface_type,
                        "seed_url_count": len(seed_urls),
                    }
                )

                for seed_index, seed in enumerate(seed_urls, start=1):
                    if not isinstance(seed, dict):
                        hard_errors.append(
                            f"seed row is not an object: {catalog_path}:{family_code}:{surface_code}:{seed_index}"
                        )
                        continue

                    canonical_url = _first_text(
                        seed,
                        ("canonical_url", "url", "seed_url", "source_url"),
                    )

                    if not canonical_url:
                        hard_errors.append(
                            f"missing canonical URL: {catalog_path}:{family_code}:{surface_code}:{seed_index}"
                        )
                        continue

                    parsed = urlparse(canonical_url)
                    url_host = parsed.netloc.lower()
                    seed_type = _first_text(seed, ("seed_type", "type"), "source_seed_url")
                    priority = _first_int(seed, ("priority", "seed_priority"), 100)

                    source_seed_id = (
                        "source_seed_"
                        f"{_safe_code(language)}_"
                        f"{_safe_code(family_code)}_"
                        f"{_safe_code(surface_code)}_"
                        f"{seed_index:03d}"
                    )

                    candidates.append(
                        SourceSeedCandidate(
                            source_seed_id=source_seed_id,
                            language=language,
                            source_family_code=family_code,
                            source_family_name=family_name,
                            source_host=source_host,
                            source_category=source_category,
                            surface_code=surface_code,
                            surface_type=surface_type,
                            seed_index=seed_index,
                            seed_type=seed_type,
                            canonical_url=canonical_url,
                            url_host=url_host,
                            priority=priority,
                            planner_status="PLAN_ONLY_NOT_EXECUTABLE",
                            mutation_allowed_now="NO",
                        )
                    )
                    family_seed_count += 1

            family_rows.append(
                {
                    "language": language,
                    "catalog_file": str(catalog_path),
                    "source_family_code": family_code,
                    "source_family_name": family_name,
                    "source_host": source_host,
                    "source_category": source_category,
                    "seed_surface_count": len(surfaces),
                    "seed_url_count": family_seed_count,
                }
            )

    return candidates, family_rows, surface_rows, hard_errors


def build_language_coverage(
    candidates: list[SourceSeedCandidate],
    catalog_paths: list[Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """EN/TR: Build 25-language coverage and warning evidence."""
    catalog_count_by_language: dict[str, int] = defaultdict(int)
    candidate_count_by_language: dict[str, int] = defaultdict(int)

    for path in catalog_paths:
        catalog_count_by_language[path.parent.name] += 1

    for candidate in candidates:
        candidate_count_by_language[candidate.language] += 1

    rows: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    for language in CANONICAL_LANGUAGE_ORDER:
        catalog_count = catalog_count_by_language.get(language, 0)
        candidate_count = candidate_count_by_language.get(language, 0)

        if catalog_count > 0 and candidate_count > 0:
            status = "PASS_CATALOG_PRESENT"
        elif catalog_count > 0 and candidate_count == 0:
            status = "WARNING_CATALOG_PRESENT_NO_SEEDS"
            warnings.append(
                {
                    "severity": "P2",
                    "category": "catalog_present_no_seeds",
                    "language": language,
                    "message": "Startpoint catalog exists but produced no source_seed candidates.",
                }
            )
        else:
            status = "PLANNED_MISSING_LANGUAGE_STARTPOINT_CATALOG"
            warnings.append(
                {
                    "severity": "P2",
                    "category": "missing_language_startpoint_catalog",
                    "language": language,
                    "message": "Language-specific startpoint catalog is not created yet.",
                }
            )

        rows.append(
            {
                "language": language,
                "catalog_file_count": catalog_count,
                "source_seed_candidate_count": candidate_count,
                "coverage_status": status,
                "mutation_allowed_now": "NO",
            }
        )

    return rows, warnings


def run_planner(repo_root: Path, catalog_root: Path, taxonomy_language_dir: Path, output_dir: Path) -> int:
    """EN/TR: Main validate-only planner run."""
    output_dir.mkdir(parents=True, exist_ok=True)

    taxonomy_rows, taxonomy_errors = load_taxonomy_inventory(taxonomy_language_dir)
    catalog_paths = discover_startpoint_catalogs(catalog_root)

    hard_errors: list[dict[str, Any]] = [
        {"severity": "P0", "category": "taxonomy_inventory", "message": message}
        for message in taxonomy_errors
    ]

    if not catalog_paths:
        hard_errors.append(
            {
                "severity": "P0",
                "category": "missing_startpoint_catalogs",
                "message": f"No startpoint catalogs found under {catalog_root}",
            }
        )

    candidates, family_rows, surface_rows, candidate_errors = build_source_seed_candidates(catalog_paths)

    for message in candidate_errors:
        hard_errors.append({"severity": "P0", "category": "catalog_parse", "message": message})

    coverage_rows, warning_rows = build_language_coverage(candidates, catalog_paths)

    candidate_rows = [asdict(candidate) for candidate in candidates]

    plan_rows: list[dict[str, Any]] = []
    for row in candidate_rows:
        plan = dict(row)
        plan["plan_type"] = "source_seed_plan"
        plan["worker_allowed_now"] = "NO"
        plan["frontier_write_allowed_now"] = "NO"
        plan["db_write_allowed_now"] = "NO"
        plan_rows.append(plan)

    source_family_coverage: dict[tuple[str, str], dict[str, Any]] = {}
    for row in family_rows:
        key = (str(row["language"]), str(row["source_family_code"]))
        source_family_coverage[key] = dict(row)

    _write_tsv(
        output_dir / "canonical_taxonomy_language_inventory.tsv",
        taxonomy_rows,
        ["file", "record_count", "language_values", "last_term_id", "result"],
    )
    _write_tsv(
        output_dir / "source_seed_language_coverage.tsv",
        coverage_rows,
        ["language", "catalog_file_count", "source_seed_candidate_count", "coverage_status", "mutation_allowed_now"],
    )
    _write_tsv(
        output_dir / "source_seed_source_family_coverage.tsv",
        list(source_family_coverage.values()),
        ["language", "catalog_file", "source_family_code", "source_family_name", "source_host", "source_category", "seed_surface_count", "seed_url_count"],
    )
    _write_tsv(
        output_dir / "source_seed_surface_coverage.tsv",
        surface_rows,
        ["language", "catalog_file", "source_family_code", "surface_code", "surface_type", "seed_url_count"],
    )
    _write_tsv(
        output_dir / "source_seed_candidate_matrix.tsv",
        candidate_rows,
        [
            "source_seed_id",
            "language",
            "source_family_code",
            "source_family_name",
            "source_host",
            "source_category",
            "surface_code",
            "surface_type",
            "seed_index",
            "seed_type",
            "canonical_url",
            "url_host",
            "priority",
            "planner_status",
            "mutation_allowed_now",
        ],
    )
    _write_jsonl(output_dir / "source_seed_plan.jsonl", plan_rows)
    _write_tsv(
        output_dir / "warnings.tsv",
        warning_rows,
        ["severity", "category", "language", "message"],
    )
    _write_tsv(
        output_dir / "hard_errors.tsv",
        hard_errors,
        ["severity", "category", "message"],
    )

    final_verdict = "PASS_VALIDATE_ONLY" if not hard_errors else "FAIL_VALIDATE_ONLY"

    summary = {
        "task": "SOURCE_SEED_PLANNER",
        "final_verdict": final_verdict,
        "repo_root": str(repo_root),
        "catalog_root": str(catalog_root),
        "taxonomy_language_dir": str(taxonomy_language_dir),
        "canonical_language_count": len(CANONICAL_LANGUAGE_ORDER),
        "taxonomy_language_file_count": len(taxonomy_rows),
        "taxonomy_total_record_count": sum(int(row["record_count"]) for row in taxonomy_rows),
        "startpoint_catalog_file_count": len(catalog_paths),
        "source_family_count": len(source_family_coverage),
        "seed_surface_count": len(surface_rows),
        "source_seed_candidate_count": len(candidate_rows),
        "missing_language_catalog_count": sum(
            1
            for row in coverage_rows
            if row["coverage_status"] == "PLANNED_MISSING_LANGUAGE_STARTPOINT_CATALOG"
        ),
        "warning_count": len(warning_rows),
        "hard_error_count": len(hard_errors),
        "validate_only": True,
        "planner_written": True,
        "worker_written": False,
        "claim_done": False,
        "fetch_done": False,
        "frontier_write_done": False,
        "db_write_done": False,
        "pi51c_touched": False,
        "runtime_systemd_touched": False,
    }

    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    summary_lines = [
        "SOURCE_SEED_PLANNER_VALIDATE_ONLY",
        f"final_verdict={summary['final_verdict']}",
        f"taxonomy_language_file_count={summary['taxonomy_language_file_count']}",
        f"taxonomy_total_record_count={summary['taxonomy_total_record_count']}",
        f"startpoint_catalog_file_count={summary['startpoint_catalog_file_count']}",
        f"source_family_count={summary['source_family_count']}",
        f"seed_surface_count={summary['seed_surface_count']}",
        f"source_seed_candidate_count={summary['source_seed_candidate_count']}",
        f"missing_language_catalog_count={summary['missing_language_catalog_count']}",
        f"warning_count={summary['warning_count']}",
        f"hard_error_count={summary['hard_error_count']}",
        "validate_only=True",
        "worker_written=False",
        "claim_done=False",
        "fetch_done=False",
        "frontier_write_done=False",
        "db_write_done=False",
        "pi51c_touched=False",
        "runtime_systemd_touched=False",
    ]
    (output_dir / "FINAL_SOURCE_SEED_PLANNER_VALIDATE_ONLY_SUMMARY.txt").write_text(
        "\n".join(summary_lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(summary_lines))

    return 0 if not hard_errors else 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    """EN/TR: CLI parser. The planner defaults to validate-only mode."""
    default_repo = _repo_default()

    parser = argparse.ArgumentParser(
        description="Validate-only multilingual source_seed planner for LogisticSearch.",
    )
    parser.add_argument("--repo-root", default=str(default_repo))
    parser.add_argument(
        "--catalog-root",
        default="hosts/makpi51crawler/python/webcrawler/catalog/startpoints",
    )
    parser.add_argument(
        "--taxonomy-language-dir",
        default="hosts/makpi51crawler/taxonomy/languages",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        default=True,
        help="Planner is validate-only by default and never executes crawler work.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """EN/TR: Entry point for validate-only planner execution."""
    args = parse_args(sys.argv[1:] if argv is None else argv)

    repo_root = Path(args.repo_root).resolve()
    catalog_root = (repo_root / args.catalog_root).resolve()
    taxonomy_language_dir = (repo_root / args.taxonomy_language_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    return run_planner(
        repo_root=repo_root,
        catalog_root=catalog_root,
        taxonomy_language_dir=taxonomy_language_dir,
        output_dir=output_dir,
    )


if __name__ == "__main__":
    raise SystemExit(main())
