#!/usr/bin/env python3
"""
EN:
JSON-first taxonomy bridge importer.

This script is the repository-tracked importer surface for moving canonical
taxonomy JSON language files into the PostgreSQL JSON bridge staging/runtime
tables created by taxonomy_core 011.

Critical boundary:
- canonical JSON files are the authoring source of truth;
- PostgreSQL remains the crawler/search runtime database;
- the crawler worker loop must not read canonical JSON files directly;
- this importer is an offline/operator-controlled bridge step, not worker-loop code.

TR:
JSON-first taxonomy bridge importer.

Bu script, kanonik taxonomy JSON dil dosyalarını taxonomy_core 011 tarafından
oluşturulan PostgreSQL JSON bridge staging/runtime tablolarına taşımak için
repository içinde izlenen importer yüzeyidir.

Kritik sınır:
- kanonik JSON dosyaları authoring source-of-truth yüzeyidir;
- PostgreSQL crawler/search runtime veritabanı olarak kalır;
- crawler worker loop kanonik JSON dosyalarını doğrudan okumamalıdır;
- bu importer offline/operator-controlled bridge adımıdır, worker-loop kodu değildir.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


CANONICAL_LANGUAGE_ORDER: tuple[str, ...] = (
    "ar", "bg", "cs", "de", "el", "en", "es", "fr", "hu", "it",
    "ja", "ko", "nl", "pt", "ro", "ru", "tr", "zh", "hi", "bn",
    "ur", "uk", "id", "vi", "he",
)


REQUIRED_TERM_FIELDS: tuple[str, ...] = (
    "term_id",
    "concept_id",
    "hierarchy_id",
    "language",
    "term",
    "role",
    "synonyms",
    "is_searchable",
    "attributes",
)


@dataclass(frozen=True, slots=True)
class LanguageJsonFilePlan:
    """EN/TR: One canonical language JSON file and its import header plan."""

    source_file_name: str
    language_code: str
    file_sha256: str
    raw_json: list[dict[str, Any]]
    is_placeholder: bool
    record_count: int


@dataclass(frozen=True, slots=True)
class TermRecordPlan:
    """EN/TR: One validated term record destined for staging.taxonomy_json_term_records_raw."""

    source_file_name: str
    language_code: str
    record_ordinal: int
    term_id: str
    concept_id: str
    hierarchy_id: str
    unspsc_code: str | None
    language: str
    term: str
    description: str | None
    role: str
    synonyms: list[str]
    is_searchable: bool
    attributes: dict[str, Any]
    raw_record: dict[str, Any]


def repo_root_from_script() -> Path:
    """EN/TR: Resolve repository root from this tracked script location."""

    return Path(__file__).resolve().parents[4]


def default_language_dir(repo_root: Path) -> Path:
    """EN/TR: Return canonical taxonomy language JSON directory."""

    return repo_root / "hosts" / "makpi51crawler" / "taxonomy" / "languages"


def sha256_bytes(data: bytes) -> str:
    """EN/TR: Return deterministic SHA-256 hex digest for exact file bytes."""

    return hashlib.sha256(data).hexdigest()


def infer_language_code_from_filename(path: Path) -> str:
    """
    EN:
    Infer the language code from filenames such as:
    logisticsearch_taxonomy_english_en.json

    TR:
    Dil kodunu şu biçimdeki dosya adından çıkarır:
    logisticsearch_taxonomy_english_en.json
    """

    stem = path.stem
    candidate = stem.rsplit("_", 1)[-1]
    if candidate not in CANONICAL_LANGUAGE_ORDER:
        raise ValueError(f"Unsupported or non-canonical language code in filename: {path.name}")
    return candidate


def load_language_json_file(path: Path) -> LanguageJsonFilePlan:
    """EN/TR: Load one canonical language JSON file and validate top-level shape."""

    raw_bytes = path.read_bytes()
    digest = sha256_bytes(raw_bytes)

    try:
        parsed = json.loads(raw_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON file: {path}") from exc

    if not isinstance(parsed, list):
        raise ValueError(f"Top-level JSON must be an array: {path}")

    language_code = infer_language_code_from_filename(path)

    if not parsed:
        return LanguageJsonFilePlan(
            source_file_name=path.name,
            language_code=language_code,
            file_sha256=digest,
            raw_json=[],
            is_placeholder=True,
            record_count=0,
        )

    records: list[dict[str, Any]] = []
    for index, item in enumerate(parsed, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Record {index} in {path.name} is not a JSON object")
        records.append(item)

    return LanguageJsonFilePlan(
        source_file_name=path.name,
        language_code=language_code,
        file_sha256=digest,
        raw_json=records,
        is_placeholder=False,
        record_count=len(records),
    )


def validate_term_record(
    *,
    file_plan: LanguageJsonFilePlan,
    record_ordinal: int,
    record: dict[str, Any],
) -> TermRecordPlan:
    """EN/TR: Validate one populated JSON term record and map it to staging columns."""

    missing = [field for field in REQUIRED_TERM_FIELDS if field not in record]
    if missing:
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} missing required fields: {missing}"
        )

    def require_nonblank_text(field_name: str) -> str:
        value = record[field_name]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{file_plan.source_file_name} record {record_ordinal} field {field_name} must be non-blank text"
            )
        return value

    term_id = require_nonblank_text("term_id")
    concept_id = require_nonblank_text("concept_id")
    hierarchy_id = require_nonblank_text("hierarchy_id")
    language = require_nonblank_text("language")
    term = require_nonblank_text("term")
    role = require_nonblank_text("role")

    if language != file_plan.language_code:
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} language mismatch: "
            f"record={language} file={file_plan.language_code}"
        )

    synonyms_value = record["synonyms"]
    if not isinstance(synonyms_value, list):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} synonyms must be an array"
        )

    synonyms: list[str] = []
    for synonym_index, synonym in enumerate(synonyms_value, start=1):
        if not isinstance(synonym, str) or not synonym.strip():
            raise ValueError(
                f"{file_plan.source_file_name} record {record_ordinal} synonym {synonym_index} must be non-blank term_id text"
            )
        synonyms.append(synonym)

    is_searchable_value = record["is_searchable"]
    if not isinstance(is_searchable_value, bool):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} is_searchable must be boolean"
        )

    attributes_value = record["attributes"]
    if not isinstance(attributes_value, dict):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} attributes must be an object"
        )

    unspsc_value = record.get("unspsc_code")
    if unspsc_value is not None and not isinstance(unspsc_value, str):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} unspsc_code must be string or null"
        )

    description_value = record.get("description")
    if description_value is not None and not isinstance(description_value, str):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} description must be string or null"
        )

    return TermRecordPlan(
        source_file_name=file_plan.source_file_name,
        language_code=file_plan.language_code,
        record_ordinal=record_ordinal,
        term_id=term_id,
        concept_id=concept_id,
        hierarchy_id=hierarchy_id,
        unspsc_code=unspsc_value,
        language=language,
        term=term,
        description=description_value,
        role=role,
        synonyms=synonyms,
        is_searchable=is_searchable_value,
        attributes=attributes_value,
        raw_record=record,
    )


def build_import_plan(language_dir: Path) -> tuple[list[LanguageJsonFilePlan], list[TermRecordPlan]]:
    """EN/TR: Build a validated dry-run import plan from all 25 canonical language files."""

    paths = sorted(language_dir.glob("logisticsearch_taxonomy_*_*.json"))
    if len(paths) != 25:
        raise ValueError(f"Expected 25 language JSON files, found {len(paths)} in {language_dir}")

    file_plans: list[LanguageJsonFilePlan] = []
    term_plans: list[TermRecordPlan] = []

    seen_languages: set[str] = set()
    seen_term_ids: set[str] = set()

    for path in paths:
        file_plan = load_language_json_file(path)
        if file_plan.language_code in seen_languages:
            raise ValueError(f"Duplicate language file for language: {file_plan.language_code}")
        seen_languages.add(file_plan.language_code)
        file_plans.append(file_plan)

        for ordinal, record in enumerate(file_plan.raw_json, start=1):
            term_plan = validate_term_record(
                file_plan=file_plan,
                record_ordinal=ordinal,
                record=record,
            )
            if term_plan.term_id in seen_term_ids:
                raise ValueError(f"Duplicate term_id detected: {term_plan.term_id}")
            seen_term_ids.add(term_plan.term_id)
            term_plans.append(term_plan)

    missing_languages = sorted(set(CANONICAL_LANGUAGE_ORDER) - seen_languages)
    if missing_languages:
        raise ValueError(f"Missing canonical language files for: {missing_languages}")

    return file_plans, term_plans


def print_plan_summary(file_plans: Iterable[LanguageJsonFilePlan], term_plans: Iterable[TermRecordPlan]) -> None:
    """EN/TR: Print deterministic dry-run summary without touching any database."""

    file_plan_list = list(file_plans)
    term_plan_list = list(term_plans)

    populated = sorted(plan.language_code for plan in file_plan_list if not plan.is_placeholder)
    placeholders = sorted(plan.language_code for plan in file_plan_list if plan.is_placeholder)

    print("TAXONOMY_JSON_IMPORT_PLAN_MODE=DRY_RUN_ONLY")
    print("CRAWLER_LOOP_DIRECT_JSON_READ=DISALLOWED")
    print(f"LANGUAGE_FILE_COUNT={len(file_plan_list)}")
    print(f"POPULATED_LANGUAGE_CODES={','.join(populated)}")
    print(f"PLACEHOLDER_LANGUAGE_CODES={','.join(placeholders)}")
    print(f"TERM_RECORD_PLAN_COUNT={len(term_plan_list)}")


def parse_args() -> argparse.Namespace:
    """EN/TR: Parse CLI arguments."""

    parser = argparse.ArgumentParser(
        description="Build a dry-run import plan for canonical taxonomy JSON bridge staging."
    )
    parser.add_argument(
        "--language-dir",
        type=Path,
        default=default_language_dir(repo_root_from_script()),
        help="Canonical taxonomy language JSON directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print plan summary without database writes.",
    )
    return parser.parse_args()


def main() -> int:
    """EN/TR: CLI entry point. Current R9-B implementation is dry-run planning only."""

    args = parse_args()

    if not args.dry_run:
        raise SystemExit(
            "R9-B safety stop: only --dry-run is implemented. "
            "Database import execution belongs to a later explicitly audited step."
        )

    file_plans, term_plans = build_import_plan(args.language_dir)
    print_plan_summary(file_plans, term_plans)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
