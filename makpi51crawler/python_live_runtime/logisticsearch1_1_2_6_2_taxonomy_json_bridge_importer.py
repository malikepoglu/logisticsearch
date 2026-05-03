#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LANGUAGE_ORDER = [
    "ar", "bg", "cs", "de", "el", "en", "es", "fr", "hu", "it",
    "ja", "ko", "nl", "pt", "ro", "ru", "tr", "zh", "hi", "bn",
    "ur", "uk", "id", "vi", "he",
]

REQUIRED_KEYS = {
    "term_id",
    "concept_id",
    "hierarchy_id",
    "unspsc_code",
    "language",
    "term",
    "description",
    "role",
    "synonyms",
    "is_searchable",
    "attributes",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_term(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).casefold()
    text = re.sub(
        r"[^\w\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af\u0590-\u05ff\u0600-\u06ff\u0900-\u097f\u0980-\u09ff\u0400-\u04ff]+",
        " ",
        text,
        flags=re.UNICODE,
    )
    return re.sub(r"\s+", " ", text).strip()


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def extract_dbname_from_dsn(dsn: str) -> str:
    dbname_match = re.search(r"(?:^|\s)dbname=([^\s]+)", dsn)
    if dbname_match:
        return dbname_match.group(1)

    uri_match = re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://[^/]*(?:/([^?]+))?", dsn)
    if uri_match and uri_match.group(1):
        return uri_match.group(1)

    local_uri_match = re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:///([^?]+)", dsn)
    if local_uri_match:
        return local_uri_match.group(1)

    return ""


def build_search_document(record: dict[str, Any]) -> str:
    synonyms = record.get("synonyms", [])
    synonym_text = " ".join(str(item) for item in synonyms if item is not None)
    return " ".join(
        part.strip()
        for part in [
            str(record.get("term", "")),
            synonym_text,
            str(record.get("description", "")),
            str(record.get("unspsc_code", "")),
            str(record.get("hierarchy_id", "")),
            str(record.get("concept_id", "")),
        ]
        if part and part.strip()
    )


def load_canonical_json(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    language_dir = Path(args.language_dir)
    hard_errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    language_inventory: list[dict[str, Any]] = []
    staging_rows: list[dict[str, Any]] = []

    files = sorted(language_dir.glob("logisticsearch_taxonomy_*_*.json"))
    discovered_languages: set[str] = set()

    if len(files) != args.expected_language_count:
        hard_errors.append({
            "severity": "P0",
            "category": "language_file_count",
            "message": f"Expected {args.expected_language_count} language files but found {len(files)}",
        })

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            hard_errors.append({
                "severity": "P0",
                "category": "invalid_json",
                "file": path.name,
                "message": str(exc),
            })
            continue

        if not isinstance(data, list):
            hard_errors.append({
                "severity": "P0",
                "category": "invalid_root_type",
                "file": path.name,
                "message": "JSON root must be a list",
            })
            continue

        file_languages = {str(record.get("language", "")) for record in data if isinstance(record, dict)}
        file_language = sorted(file_languages)[0] if len(file_languages) == 1 else ""
        discovered_languages.update(lang for lang in file_languages if lang)

        if len(file_languages) != 1:
            hard_errors.append({
                "severity": "P0",
                "category": "mixed_or_missing_language",
                "file": path.name,
                "message": f"Expected exactly one language per file, got {sorted(file_languages)}",
            })

        if args.expected_record_count_per_language > 0 and len(data) != args.expected_record_count_per_language:
            hard_errors.append({
                "severity": "P0",
                "category": "record_count_per_language",
                "file": path.name,
                "language": file_language,
                "message": f"Expected {args.expected_record_count_per_language} records but found {len(data)}",
            })

        language_inventory.append({
            "file": path.name,
            "language": file_language,
            "record_count": len(data),
            "result": "PASS" if len(data) == args.expected_record_count_per_language else "FAIL",
        })

        for position, record in enumerate(data, start=1):
            if not isinstance(record, dict):
                hard_errors.append({
                    "severity": "P0",
                    "category": "invalid_record_type",
                    "file": path.name,
                    "position": position,
                    "message": "Record must be an object",
                })
                continue

            missing = sorted(REQUIRED_KEYS - set(record.keys()))
            if missing:
                hard_errors.append({
                    "severity": "P0",
                    "category": "missing_required_keys",
                    "file": path.name,
                    "position": position,
                    "term_id": record.get("term_id", ""),
                    "message": ",".join(missing),
                })

            lang = str(record.get("language", ""))
            term_id = str(record.get("term_id", ""))
            concept_id = str(record.get("concept_id", ""))
            hierarchy_id = str(record.get("hierarchy_id", ""))
            unspsc_code = str(record.get("unspsc_code", ""))
            term = str(record.get("term", ""))
            description = str(record.get("description", ""))
            role = str(record.get("role", ""))
            synonyms = record.get("synonyms", [])
            attributes = record.get("attributes", {})

            if lang and term_id and not term_id.startswith(f"{lang}-"):
                hard_errors.append({
                    "severity": "P0",
                    "category": "term_id_language_prefix_mismatch",
                    "file": path.name,
                    "position": position,
                    "term_id": term_id,
                    "language": lang,
                    "message": "term_id must start with '<language>-'",
                })

            for field_name, field_value in [
                ("language", lang),
                ("term_id", term_id),
                ("concept_id", concept_id),
                ("hierarchy_id", hierarchy_id),
                ("unspsc_code", unspsc_code),
                ("term", term),
                ("description", description),
                ("role", role),
            ]:
                if not field_value.strip():
                    hard_errors.append({
                        "severity": "P0",
                        "category": "blank_required_value",
                        "file": path.name,
                        "position": position,
                        "term_id": term_id,
                        "field": field_name,
                        "message": "Required value is blank",
                    })

            if not isinstance(synonyms, list):
                hard_errors.append({
                    "severity": "P0",
                    "category": "synonyms_not_list",
                    "file": path.name,
                    "position": position,
                    "term_id": term_id,
                    "message": "synonyms must be a list",
                })

            if not isinstance(attributes, dict):
                hard_errors.append({
                    "severity": "P0",
                    "category": "attributes_not_object",
                    "file": path.name,
                    "position": position,
                    "term_id": term_id,
                    "message": "attributes must be an object",
                })

            normalized_term = normalize_term(term)
            search_document = build_search_document(record)

            staging_rows.append({
                "source_file": path.name,
                "source_position": position,
                "language": lang,
                "term_id": term_id,
                "concept_id": concept_id,
                "hierarchy_id": hierarchy_id,
                "unspsc_code": unspsc_code,
                "term": term,
                "normalized_term": normalized_term,
                "description": description,
                "role": role,
                "is_searchable": bool(record.get("is_searchable", False)),
                "entity_family": str(attributes.get("entity_family", "")) if isinstance(attributes, dict) else "",
                "search_document": search_document,
                "record": record,
            })

    expected_language_set = set(LANGUAGE_ORDER)
    if discovered_languages != expected_language_set:
        hard_errors.append({
            "severity": "P0",
            "category": "language_set_mismatch",
            "message": f"Expected {sorted(expected_language_set)} but found {sorted(discovered_languages)}",
        })

    if args.expected_total_record_count > 0 and len(staging_rows) != args.expected_total_record_count:
        hard_errors.append({
            "severity": "P0",
            "category": "total_record_count",
            "message": f"Expected total {args.expected_total_record_count} rows but found {len(staging_rows)}",
        })

    concept_languages: dict[str, set[str]] = defaultdict(set)
    for row in staging_rows:
        concept_languages[row["concept_id"]].add(row["language"])

    concept_coverage_rows: list[dict[str, Any]] = []
    for concept_id in sorted(concept_languages, key=lambda item: int(item.replace("CID-", "")) if item.startswith("CID-") and item.replace("CID-", "").isdigit() else item):
        langs = concept_languages[concept_id]
        missing = [lang for lang in LANGUAGE_ORDER if lang not in langs]
        result = "PASS" if not missing and len(langs) == args.expected_language_count else "FAIL"
        if result != "PASS":
            hard_errors.append({
                "severity": "P0",
                "category": "concept_language_coverage",
                "concept_id": concept_id,
                "message": f"language_count={len(langs)} missing={','.join(missing)}",
            })
        concept_coverage_rows.append({
            "concept_id": concept_id,
            "language_count": len(langs),
            "missing_languages": ",".join(missing),
            "result": result,
        })

    duplicate_counter: Counter[tuple[str, str]] = Counter(
        (row["language"], row["normalized_term"])
        for row in staging_rows
        if row["normalized_term"]
    )

    duplicate_rows: list[dict[str, Any]] = []
    for (language, normalized_term), count in sorted(duplicate_counter.items()):
        if count <= 1:
            continue
        matching = [
            row for row in staging_rows
            if row["language"] == language and row["normalized_term"] == normalized_term
        ]
        duplicate_rows.append({
            "language": language,
            "normalized_term": normalized_term,
            "group_size": count,
            "term_ids": ";".join(row["term_id"] for row in matching),
            "concept_ids": ";".join(row["concept_id"] for row in matching),
            "hierarchy_ids": ";".join(row["hierarchy_id"] for row in matching),
            "terms": " || ".join(row["term"] for row in matching),
            "classification": "WARNING_NORMALIZED_DUPLICATE_REVIEW_DEBT",
        })

    if duplicate_rows:
        warnings.append({
            "severity": "P2",
            "category": "normalized_duplicate_review_debt",
            "message": f"{len(duplicate_rows)} normalized duplicate groups found. This is warning-only unless --fail-on-normalized-duplicates is set.",
        })
        if args.fail_on_normalized_duplicates:
            hard_errors.append({
                "severity": "P0",
                "category": "normalized_duplicate_blocked_by_flag",
                "message": f"{len(duplicate_rows)} normalized duplicate groups found",
            })

    return staging_rows, language_inventory, concept_coverage_rows, duplicate_rows, hard_errors, warnings


def write_to_scratch_database(args: argparse.Namespace, staging_rows: list[dict[str, Any]]) -> None:
    if not args.execute_db_write:
        return

    if not args.dsn:
        raise RuntimeError("--dsn is required with --execute-db-write")

    if not args.scratch_only_confirm:
        raise RuntimeError("--scratch-only-confirm is required with --execute-db-write")

    dbname = extract_dbname_from_dsn(args.dsn)
    if not dbname or "scratch" not in dbname.lower():
        raise RuntimeError(f"Refusing DB write: target database name must contain 'scratch'. Parsed dbname={dbname!r}")

    try:
        import psycopg
    except Exception as exc:
        raise RuntimeError(f"psycopg import failed: {exc}") from exc

    batch_id = args.import_batch_id

    ddl_statements = [
        "CREATE SCHEMA IF NOT EXISTS taxonomy_bridge_staging",
        "CREATE SCHEMA IF NOT EXISTS taxonomy_runtime",
        """
        CREATE TABLE IF NOT EXISTS taxonomy_bridge_staging.canonical_json_term_import (
            import_batch_id text NOT NULL,
            source_file text NOT NULL,
            source_position integer NOT NULL,
            language text NOT NULL,
            term_id text NOT NULL,
            concept_id text NOT NULL,
            hierarchy_id text NOT NULL,
            unspsc_code text NOT NULL,
            term text NOT NULL,
            normalized_term text NOT NULL,
            description text NOT NULL,
            role text NOT NULL,
            is_searchable boolean NOT NULL,
            entity_family text NOT NULL,
            search_document text NOT NULL,
            record jsonb NOT NULL,
            imported_at timestamptz NOT NULL DEFAULT now(),
            PRIMARY KEY (import_batch_id, term_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS taxonomy_runtime.term_lookup (
            term_id text PRIMARY KEY,
            concept_id text NOT NULL,
            hierarchy_id text NOT NULL,
            unspsc_code text NOT NULL,
            language text NOT NULL,
            term text NOT NULL,
            normalized_term text NOT NULL,
            description text NOT NULL,
            role text NOT NULL,
            is_searchable boolean NOT NULL,
            entity_family text NOT NULL,
            search_document text NOT NULL,
            record jsonb NOT NULL,
            import_batch_id text NOT NULL,
            refreshed_at timestamptz NOT NULL DEFAULT now()
        )
        """,
        """
        CREATE OR REPLACE VIEW taxonomy_runtime.term_lookup_presence_audit AS
        SELECT
            concept_id,
            hierarchy_id,
            count(*) AS term_count,
            count(DISTINCT language) AS language_count,
            string_agg(DISTINCT language, ',' ORDER BY language) AS languages
        FROM taxonomy_runtime.term_lookup
        GROUP BY concept_id, hierarchy_id
        """
    ]

    with psycopg.connect(args.dsn) as conn:
        with conn.transaction():
            with conn.cursor() as cur:
                for statement in ddl_statements:
                    cur.execute(statement)

                cur.execute(
                    "DELETE FROM taxonomy_bridge_staging.canonical_json_term_import WHERE import_batch_id = %s",
                    (batch_id,),
                )

                for row in staging_rows:
                    cur.execute(
                        """
                        INSERT INTO taxonomy_bridge_staging.canonical_json_term_import (
                            import_batch_id,
                            source_file,
                            source_position,
                            language,
                            term_id,
                            concept_id,
                            hierarchy_id,
                            unspsc_code,
                            term,
                            normalized_term,
                            description,
                            role,
                            is_searchable,
                            entity_family,
                            search_document,
                            record
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s::jsonb
                        )
                        """,
                        (
                            batch_id,
                            row["source_file"],
                            row["source_position"],
                            row["language"],
                            row["term_id"],
                            row["concept_id"],
                            row["hierarchy_id"],
                            row["unspsc_code"],
                            row["term"],
                            row["normalized_term"],
                            row["description"],
                            row["role"],
                            row["is_searchable"],
                            row["entity_family"],
                            row["search_document"],
                            json.dumps(row["record"], ensure_ascii=False),
                        ),
                    )

                cur.execute("TRUNCATE taxonomy_runtime.term_lookup")
                cur.execute(
                    """
                    INSERT INTO taxonomy_runtime.term_lookup (
                        term_id,
                        concept_id,
                        hierarchy_id,
                        unspsc_code,
                        language,
                        term,
                        normalized_term,
                        description,
                        role,
                        is_searchable,
                        entity_family,
                        search_document,
                        record,
                        import_batch_id
                    )
                    SELECT
                        term_id,
                        concept_id,
                        hierarchy_id,
                        unspsc_code,
                        language,
                        term,
                        normalized_term,
                        description,
                        role,
                        is_searchable,
                        entity_family,
                        search_document,
                        record,
                        import_batch_id
                    FROM taxonomy_bridge_staging.canonical_json_term_import
                    WHERE import_batch_id = %s
                    ORDER BY language, source_position
                    """,
                    (batch_id,),
                )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate and optionally import canonical LogisticSearch taxonomy JSON into a scratch PostgreSQL runtime bridge."
    )
    parser.add_argument("--repo-root", default=str(Path.cwd()))
    parser.add_argument("--language-dir", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--expected-language-count", type=int, default=25)
    parser.add_argument("--expected-record-count-per-language", type=int, default=337)
    parser.add_argument("--expected-total-record-count", type=int, default=8425)
    parser.add_argument("--fail-on-normalized-duplicates", action="store_true")
    parser.add_argument("--execute-db-write", action="store_true")
    parser.add_argument("--dsn", default="")
    parser.add_argument("--scratch-only-confirm", action="store_true")
    parser.add_argument("--import-batch-id", default="")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    if not args.language_dir:
        args.language_dir = str(repo_root / "makpi51crawler/taxonomy/languages")

    if not args.output_dir:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        args.output_dir = f"/tmp/logisticsearch_taxonomy_json_import_validate_{stamp}"

    if not args.import_batch_id:
        args.import_batch_id = "taxonomy_json_runtime_bridge_import_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    staging_rows, language_inventory, concept_coverage_rows, duplicate_rows, hard_errors, warnings = load_canonical_json(args)

    write_tsv(
        output_dir / "language_inventory.tsv",
        ["file", "language", "record_count", "result"],
        language_inventory,
    )
    write_tsv(
        output_dir / "concept_coverage.tsv",
        ["concept_id", "language_count", "missing_languages", "result"],
        concept_coverage_rows,
    )
    write_tsv(
        output_dir / "normalized_duplicates.tsv",
        ["language", "normalized_term", "group_size", "term_ids", "concept_ids", "hierarchy_ids", "terms", "classification"],
        duplicate_rows,
    )
    write_tsv(
        output_dir / "hard_errors.tsv",
        ["severity", "category", "file", "position", "term_id", "language", "field", "concept_id", "message"],
        hard_errors,
    )
    write_tsv(
        output_dir / "warnings.tsv",
        ["severity", "category", "message"],
        warnings,
    )
    write_jsonl(output_dir / "staging_rows.jsonl", staging_rows)

    final_verdict = "PASS_VALIDATE_ONLY"
    db_write_done = False

    if hard_errors:
        final_verdict = "FAIL_VALIDATE_ONLY"
    elif args.execute_db_write:
        write_to_scratch_database(args, staging_rows)
        db_write_done = True
        final_verdict = "PASS_SCRATCH_DB_IMPORT"

    summary = {
        "task": "load_canonical_json_to_taxonomy_bridge_staging",
        "final_verdict": final_verdict,
        "utc_finished_at": utc_now_iso(),
        "repo_root": str(repo_root),
        "language_dir": args.language_dir,
        "output_dir": str(output_dir),
        "expected_language_count": args.expected_language_count,
        "expected_record_count_per_language": args.expected_record_count_per_language,
        "expected_total_record_count": args.expected_total_record_count,
        "language_file_count": len(language_inventory),
        "total_record_count": len(staging_rows),
        "concept_count": len(concept_coverage_rows),
        "normalized_duplicate_group_count": len(duplicate_rows),
        "hard_error_count": len(hard_errors),
        "warning_count": len(warnings),
        "execute_db_write": args.execute_db_write,
        "scratch_only_confirm": args.scratch_only_confirm,
        "db_write_done": db_write_done,
        "import_batch_id": args.import_batch_id,
    }
    write_json(output_dir / "summary.json", summary)

    print("TAXONOMY_JSON_IMPORTER_VALIDATE")
    for key in [
        "final_verdict",
        "language_file_count",
        "total_record_count",
        "concept_count",
        "normalized_duplicate_group_count",
        "hard_error_count",
        "warning_count",
        "execute_db_write",
        "scratch_only_confirm",
        "db_write_done",
        "output_dir",
    ]:
        print(f"{key}={summary[key]}")

    return 0 if not hard_errors else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
