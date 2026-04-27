#!/usr/bin/env python3
"""
JSON-first taxonomy bridge importer.

EN:
This script is an offline operator/import helper for LogisticSearch taxonomy data.
It reads canonical taxonomy JSON language files, validates them, builds a deterministic
import plan, and can optionally write that plan into PostgreSQL JSON-first bridge
staging tables.

TR:
Bu script LogisticSearch taxonomy verisi için offline operatör/import yardımcısıdır.
Kanonik taxonomy JSON dil dosyalarını okur, doğrular, deterministik import planı
oluşturur ve açık izin verilirse bu planı PostgreSQL JSON-first bridge staging
tablolarına yazar.

EN:
Runtime safety boundary:
- the crawler worker loop must not read canonical JSON files directly;
- normal crawler/search execution must query PostgreSQL runtime seams/views;
- DB write mode requires explicit --execute-db-write.

TR:
Runtime güvenlik sınırı:
- crawler worker loop kanonik JSON dosyalarını doğrudan okumamalıdır;
- normal crawler/search çalışması PostgreSQL runtime seam/view yüzeyini sorgulamalıdır;
- DB write mode için açık --execute-db-write gerekir.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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

DEFAULT_LANGUAGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "taxonomy"
    / "languages"
)


@dataclass(slots=True)
class LanguageFilePlan:
    """EN/TR: One validated language JSON file destined for staging header import."""

    source_file_name: str
    source_path: Path
    language_code: str
    file_sha256: str
    raw_json: list[dict[str, Any]]
    is_placeholder: bool
    record_count: int


@dataclass(slots=True)
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


@dataclass(slots=True)
class ImportPlan:
    """EN/TR: Full deterministic import plan built before any optional DB write."""

    language_files: list[LanguageFilePlan]
    term_records: list[TermRecordPlan]


def sha256_file(path: Path) -> str:
    # EN: Read exact file bytes so the import trace can prove which JSON file was used.
    # TR: Import izinin hangi JSON dosyasını kullandığını kanıtlamak için dosya byte'larını okuyoruz.
    return hashlib.sha256(path.read_bytes()).hexdigest()


def infer_language_code_from_filename(path: Path) -> str:
    # EN: Expected names end with _<lang>.json, for example logisticsearch_taxonomy_english_en.json.
    # TR: Beklenen isimler _<dil>.json ile biter; örnek: logisticsearch_taxonomy_english_en.json.
    stem = path.stem
    parts = stem.split("_")
    if not parts:
        raise ValueError(f"Cannot infer language code from file name: {path.name}")

    language_code = parts[-1].strip().lower()
    if language_code not in CANONICAL_LANGUAGE_ORDER:
        raise ValueError(
            f"Language code inferred from {path.name!r} is not canonical: {language_code!r}"
        )

    return language_code


def load_language_file(path: Path) -> LanguageFilePlan:
    # EN: Parse JSON once and keep the exact top-level array for staging.raw_json.
    # TR: JSON'u bir kez parse edip staging.raw_json için top-level array'i koruyoruz.
    language_code = infer_language_code_from_filename(path)
    digest = sha256_file(path)

    with path.open("r", encoding="utf-8") as handle:
        raw_json = json.load(handle)

    if not isinstance(raw_json, list):
        raise ValueError(f"{path.name} must contain a top-level JSON array")

    for index, record in enumerate(raw_json, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"{path.name} record {index} must be a JSON object")

    return LanguageFilePlan(
        source_file_name=path.name,
        source_path=path,
        language_code=language_code,
        file_sha256=digest,
        raw_json=raw_json,
        is_placeholder=(len(raw_json) == 0),
        record_count=len(raw_json),
    )


def validate_term_record(file_plan: LanguageFilePlan, record: dict[str, Any], record_ordinal: int) -> TermRecordPlan:
    # EN: Required fields must be present before staging can receive the record.
    # TR: Kayıt staging'e girmeden önce zorunlu alanlar bulunmalıdır.
    missing = [field for field in REQUIRED_TERM_FIELDS if field not in record]
    if missing:
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} missing required fields: {missing}"
        )

    def require_nonblank_text(field_name: str) -> str:
        value = record[field_name]
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError(
                f"{file_plan.source_file_name} record {record_ordinal} field {field_name} "
                "must be non-blank text"
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

    synonyms_raw = record["synonyms"]
    if not isinstance(synonyms_raw, list):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} synonyms must be an array"
        )

    synonyms: list[str] = []
    for synonym_index, synonym in enumerate(synonyms_raw, start=1):
        if not isinstance(synonym, str) or synonym.strip() == "":
            raise ValueError(
                f"{file_plan.source_file_name} record {record_ordinal} synonym {synonym_index} "
                "must be non-blank term_id text"
            )
        synonyms.append(synonym)

    is_searchable = record["is_searchable"]
    if not isinstance(is_searchable, bool):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} is_searchable must be boolean"
        )

    attributes = record["attributes"]
    if not isinstance(attributes, dict):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} attributes must be an object"
        )

    unspsc_code_raw = record.get("unspsc_code")
    if unspsc_code_raw is not None and not isinstance(unspsc_code_raw, str):
        raise ValueError(
            f"{file_plan.source_file_name} record {record_ordinal} unspsc_code must be string or null"
        )

    description_raw = record.get("description")
    if description_raw is not None and not isinstance(description_raw, str):
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
        unspsc_code=unspsc_code_raw,
        language=language,
        term=term,
        description=description_raw,
        role=role,
        synonyms=synonyms,
        is_searchable=is_searchable,
        attributes=attributes,
        raw_record=record,
    )


def discover_language_files(language_dir: Path) -> list[Path]:
    # EN: Build a canonical-order file list so import output remains deterministic.
    # TR: Import çıktısı deterministik kalsın diye dosya listesini kanonik dil sırasına göre kuruyoruz.
    if not language_dir.is_dir():
        raise FileNotFoundError(f"Language directory does not exist: {language_dir}")

    files_by_language: dict[str, Path] = {}
    for path in sorted(language_dir.glob("logisticsearch_taxonomy_*_*.json")):
        language_code = infer_language_code_from_filename(path)
        if language_code in files_by_language:
            raise ValueError(f"Duplicate language JSON file for language: {language_code}")
        files_by_language[language_code] = path

    missing_languages = [code for code in CANONICAL_LANGUAGE_ORDER if code not in files_by_language]
    if missing_languages:
        raise ValueError(f"Missing canonical language JSON files: {missing_languages}")

    return [files_by_language[code] for code in CANONICAL_LANGUAGE_ORDER]


def build_import_plan(language_dir: Path) -> ImportPlan:
    # EN: Build the full plan before optional DB write, so validation fails before mutation.
    # TR: Opsiyonel DB yazısından önce tüm planı kuruyoruz; böylece validation mutasyondan önce hata verir.
    language_file_plans: list[LanguageFilePlan] = []
    term_record_plans: list[TermRecordPlan] = []

    seen_languages: set[str] = set()
    seen_term_ids: set[str] = set()

    for path in discover_language_files(language_dir):
        file_plan = load_language_file(path)

        if file_plan.language_code in seen_languages:
            raise ValueError(f"Duplicate language file for language: {file_plan.language_code}")
        seen_languages.add(file_plan.language_code)

        language_file_plans.append(file_plan)

        for record_ordinal, record in enumerate(file_plan.raw_json, start=1):
            term_plan = validate_term_record(file_plan, record, record_ordinal)

            if term_plan.term_id in seen_term_ids:
                raise ValueError(f"Duplicate term_id detected: {term_plan.term_id}")
            seen_term_ids.add(term_plan.term_id)

            term_record_plans.append(term_plan)

    return ImportPlan(
        language_files=language_file_plans,
        term_records=term_record_plans,
    )


def print_plan_summary(plan: ImportPlan, *, mode: str) -> None:
    # EN: Print stable machine-readable summary lines for audit scripts.
    # TR: Audit scriptleri için stabil ve makine-okunur özet satırları basıyoruz.
    populated = sorted(file_plan.language_code for file_plan in plan.language_files if not file_plan.is_placeholder)
    placeholders = sorted(file_plan.language_code for file_plan in plan.language_files if file_plan.is_placeholder)

    print(f"TAXONOMY_JSON_IMPORT_PLAN_MODE={mode}")
    print("CRAWLER_LOOP_DIRECT_JSON_READ=DISALLOWED")
    print(f"LANGUAGE_FILE_COUNT={len(plan.language_files)}")
    print(f"POPULATED_LANGUAGE_CODES={','.join(populated)}")
    print(f"PLACEHOLDER_LANGUAGE_CODES={','.join(placeholders)}")
    print(f"TERM_RECORD_PLAN_COUNT={len(plan.term_records)}")


def ensure_safe_db_target(*, target_db: str | None, db_dsn: str | None) -> str:
    # EN: DB write mode is intentionally scratch-only unless the code is changed in a later controlled step.
    # TR: DB write mode sonraki kontrollü adıma kadar bilinçli olarak sadece scratch hedeflidir.
    if target_db and db_dsn:
        raise ValueError("Use either --target-db or --db-dsn, not both")

    if target_db:
        if "scratch" not in target_db:
            raise ValueError(
                "Safety stop: --target-db must contain 'scratch'. "
                "This importer patch is not allowed to write live DBs."
            )
        return f"dbname={target_db}"

    if db_dsn:
        if "scratch" not in db_dsn:
            raise ValueError(
                "Safety stop: --db-dsn must contain 'scratch'. "
                "This importer patch is not allowed to write live DBs."
            )
        return db_dsn

    raise ValueError("DB write mode requires --target-db or --db-dsn")


def fetch_bridge_counts(cur: Any) -> dict[str, int]:
    # EN: Keep the verification query compact and deterministic.
    # TR: Doğrulama sorgusunu kompakt ve deterministik tutuyoruz.
    cur.execute(
        """
        SELECT 'json_language_file_import_rows' AS metric, count(*)::bigint AS value
        FROM staging.taxonomy_json_language_file_import
        UNION ALL
        SELECT 'json_term_records_raw_rows', count(*)::bigint
        FROM staging.taxonomy_json_term_records_raw
        UNION ALL
        SELECT 'json_runtime_language_state_rows', count(*)::bigint
        FROM logistics.taxonomy_json_runtime_language_state
        UNION ALL
        SELECT 'runtime_enabled_language_rows', count(*)::bigint
        FROM logistics.taxonomy_json_runtime_language_state
        WHERE is_runtime_enabled = true
        UNION ALL
        SELECT 'placeholder_language_rows', count(*)::bigint
        FROM logistics.taxonomy_json_runtime_language_state
        WHERE is_placeholder = true
        UNION ALL
        SELECT 'invalid_enabled_placeholder_rows',
               (count(*) FILTER (WHERE is_placeholder = true AND is_runtime_enabled = true))::bigint
        FROM logistics.taxonomy_json_runtime_language_state
        UNION ALL
        SELECT 'json_runtime_terms_rows', count(*)::bigint
        FROM logistics.taxonomy_json_runtime_terms
        UNION ALL
        SELECT 'json_runtime_search_view_rows', count(*)::bigint
        FROM logistics.taxonomy_json_runtime_search_view
        ORDER BY metric
        """
    )
    return {str(row[0]): int(row[1]) for row in cur.fetchall()}


def assert_empty_bridge_before_write(cur: Any) -> None:
    # EN: This patch intentionally refuses to stack imports on top of existing bridge rows.
    # TR: Bu patch mevcut bridge satırlarının üstüne yeni import yığmayı bilinçli olarak reddeder.
    counts = fetch_bridge_counts(cur)
    non_empty = {key: value for key, value in counts.items() if value != 0}
    if non_empty:
        raise ValueError(
            "Safety stop: JSON bridge tables/views are not empty before import. "
            f"Observed non-empty metrics: {non_empty}"
        )


def execute_db_write(plan: ImportPlan, *, target_db: str | None, db_dsn: str | None) -> dict[str, int]:
    # EN: Validate the target before importing psycopg, so forbidden live targets fail
    # EN: with the intended safety-stop message even on machines without psycopg.
    # TR: psycopg importundan önce hedefi doğruluyoruz; böylece yasak live hedefler
    # TR: psycopg olmayan makinelerde bile doğru safety-stop mesajı ile durur.
    dsn = ensure_safe_db_target(target_db=target_db, db_dsn=db_dsn)

    # EN: Import psycopg only after the scratch-only target safety gate passes.
    # TR: psycopg modülünü yalnızca scratch-only hedef güvenlik kapısı geçtikten sonra içe aktarıyoruz.
    import psycopg
    from psycopg.types.json import Jsonb

    expected_language_files = len(plan.language_files)
    expected_raw_terms = len(plan.term_records)
    expected_runtime_terms = len(plan.term_records)
    expected_search_rows = sum(1 for term in plan.term_records if term.is_searchable)
    expected_placeholder_languages = sum(1 for file_plan in plan.language_files if file_plan.is_placeholder)
    expected_runtime_enabled_languages = sum(1 for file_plan in plan.language_files if not file_plan.is_placeholder)

    with psycopg.connect(dsn) as conn:
        try:
            with conn.cursor() as cur:
                assert_empty_bridge_before_write(cur)

                import_id_by_language: dict[str, int] = {}

                for file_plan in plan.language_files:
                    metadata = {
                        "importer": "load_canonical_json_to_taxonomy_bridge_staging.py",
                        "mode": "json_first_bridge",
                        "crawler_loop_direct_json_read": "disallowed",
                    }

                    cur.execute(
                        """
                        INSERT INTO staging.taxonomy_json_language_file_import (
                            source_file_name,
                            language_code,
                            file_sha256,
                            raw_json,
                            is_placeholder,
                            record_count,
                            metadata
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING import_id
                        """,
                        (
                            file_plan.source_file_name,
                            file_plan.language_code,
                            file_plan.file_sha256,
                            Jsonb(file_plan.raw_json),
                            file_plan.is_placeholder,
                            file_plan.record_count,
                            Jsonb(metadata),
                        ),
                    )

                    row = cur.fetchone()
                    if row is None:
                        raise RuntimeError(f"No import_id returned for {file_plan.source_file_name}")

                    import_id_by_language[file_plan.language_code] = int(row[0])

                for term_plan in plan.term_records:
                    import_id = import_id_by_language[term_plan.language_code]

                    cur.execute(
                        """
                        INSERT INTO staging.taxonomy_json_term_records_raw (
                            import_id,
                            record_ordinal,
                            term_id,
                            concept_id,
                            hierarchy_id,
                            unspsc_code,
                            language,
                            term,
                            description,
                            role,
                            synonyms,
                            is_searchable,
                            attributes,
                            raw_record
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            import_id,
                            term_plan.record_ordinal,
                            term_plan.term_id,
                            term_plan.concept_id,
                            term_plan.hierarchy_id,
                            term_plan.unspsc_code,
                            term_plan.language,
                            term_plan.term,
                            term_plan.description,
                            term_plan.role,
                            Jsonb(term_plan.synonyms),
                            term_plan.is_searchable,
                            Jsonb(term_plan.attributes),
                            Jsonb(term_plan.raw_record),
                        ),
                    )

                cur.execute("SELECT logistics.taxonomy_json_runtime_terms_prepare()")
                prepare_row = cur.fetchone()
                print(f"PREPARE_SUMMARY_JSON={prepare_row[0] if prepare_row else None}")

                counts = fetch_bridge_counts(cur)

                expected_counts = {
                    "json_language_file_import_rows": expected_language_files,
                    "json_term_records_raw_rows": expected_raw_terms,
                    "json_runtime_language_state_rows": expected_language_files,
                    "runtime_enabled_language_rows": expected_runtime_enabled_languages,
                    "placeholder_language_rows": expected_placeholder_languages,
                    "invalid_enabled_placeholder_rows": 0,
                    "json_runtime_terms_rows": expected_runtime_terms,
                    "json_runtime_search_view_rows": expected_search_rows,
                }

                mismatches = {
                    key: {"expected": expected_value, "actual": counts.get(key)}
                    for key, expected_value in expected_counts.items()
                    if counts.get(key) != expected_value
                }

                if mismatches:
                    raise ValueError(f"Post-import count mismatch: {mismatches}")

            conn.commit()
            return counts

        except Exception:
            conn.rollback()
            raise


def parse_args() -> argparse.Namespace:
    # EN: CLI keeps dry-run as the default safe path.
    # TR: CLI dry-run davranışını varsayılan güvenli yol olarak korur.
    parser = argparse.ArgumentParser(
        description="Load canonical taxonomy JSON files into JSON-first taxonomy bridge staging."
    )

    parser.add_argument(
        "--language-dir",
        type=Path,
        default=DEFAULT_LANGUAGE_DIR,
        help="Directory containing canonical logisticsearch_taxonomy_*_<lang>.json files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build and validate the import plan only. This is the default unless --execute-db-write is used.",
    )
    parser.add_argument(
        "--execute-db-write",
        action="store_true",
        help="Explicitly write validated plan into a scratch PostgreSQL JSON bridge.",
    )
    parser.add_argument(
        "--target-db",
        default=None,
        help="Scratch PostgreSQL database name. Must contain 'scratch'.",
    )
    parser.add_argument(
        "--db-dsn",
        default=None,
        help="Scratch PostgreSQL DSN. Must contain 'scratch'.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.execute_db_write and args.dry_run:
        raise ValueError("Use either --dry-run or --execute-db-write, not both")

    plan = build_import_plan(args.language_dir)

    if not args.execute_db_write:
        print_plan_summary(plan, mode="DRY_RUN_ONLY")
        return 0

    print_plan_summary(plan, mode="DB_WRITE_REQUESTED")
    print("DB_WRITE_SAFETY_TARGET=scratch_only")
    counts = execute_db_write(plan, target_db=args.target_db, db_dsn=args.db_dsn)

    print("TAXONOMY_JSON_DB_WRITE_RESULT=PASS")
    for key in sorted(counts):
        print(f"{key}={counts[key]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
