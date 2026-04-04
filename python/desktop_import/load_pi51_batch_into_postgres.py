#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_items(batch_data: Any) -> list[dict[str, Any]]:
    if isinstance(batch_data, list):
        return batch_data
    if isinstance(batch_data, dict):
        if isinstance(batch_data.get("items"), list):
            return batch_data["items"]
        if isinstance(batch_data.get("export_items"), list):
            return batch_data["export_items"]
    raise ValueError("batch.json item structure not recognized")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: load_pi51_batch_into_postgres.py <IMPORT_DIR>")

    import_dir = Path(sys.argv[1]).resolve()
    batch_json = load_json(import_dir / "batch.json")
    manifest = load_json(import_dir / "manifest.json")
    push_receipt = load_json(import_dir / "PUSH_RECEIPT.json")
    import_receipt = load_json(import_dir / "IMPORT_RECEIPT.json")

    batch_key = manifest["batch_key"]
    export_channel = manifest["export_channel"]
    item_count_expected = int(manifest["item_count"])
    batch_payload_sha256 = manifest["payload_sha256"]
    source_repo_relpath = import_receipt["source_repo_relpath"]
    source_repo_head = import_receipt.get("source_repo_head")
    source_commit_from_push_receipt = import_receipt.get("source_commit_from_push_receipt")
    imported_at_utc = import_receipt["imported_at_utc"]

    raw_items = normalize_items(batch_json)

    manifest_items = manifest.get("items") or []
    manifest_by_export_item_id: dict[int, dict[str, Any]] = {}
    for item in manifest_items:
        if item.get("export_item_id") is not None:
            manifest_by_export_item_id[int(item["export_item_id"])] = item

    out_batch_tsv = import_dir / "_desktop_import_batch_intake.tsv"
    out_items_tsv = import_dir / "_desktop_import_page_export_raw.tsv"

    with out_batch_tsv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow([
            "batch_key",
            "export_channel",
            "source_repo_relpath",
            "source_repo_head",
            "source_commit_from_push_receipt",
            "item_count_expected",
            "item_count_loaded",
            "batch_payload_sha256",
            "imported_at_utc",
            "manifest_json",
            "push_receipt_json",
            "import_receipt_json",
        ])
        writer.writerow([
            batch_key,
            export_channel,
            source_repo_relpath,
            source_repo_head or r"\N",
            source_commit_from_push_receipt or r"\N",
            item_count_expected,
            len(raw_items),
            batch_payload_sha256,
            imported_at_utc,
            compact_json(manifest),
            compact_json(push_receipt),
            compact_json(import_receipt),
        ])

    with out_items_tsv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow([
            "batch_key",
            "item_ordinal",
            "export_item_id",
            "source_url_id",
            "source_snapshot_id",
            "canonical_url",
            "input_lang_code",
            "taxonomy_package_version",
            "top_candidate_count",
            "top_score",
            "raw_item_json",
            "raw_payload_json",
        ])

        for idx, raw_item in enumerate(raw_items, start=1):
            if not isinstance(raw_item, dict):
                raise ValueError(f"raw item at ordinal {idx} is not an object")

            payload = raw_item.get("payload")
            if not isinstance(payload, dict):
                payload = raw_item

            export_item_id = raw_item.get("export_item_id")
            if export_item_id is None:
                export_item_id = payload.get("export_item_id")

            manifest_item = None
            if export_item_id is not None:
                manifest_item = manifest_by_export_item_id.get(int(export_item_id))

            source_url_id = (
                raw_item.get("url_id")
                or payload.get("url_id")
                or (manifest_item or {}).get("url_id")
            )
            source_snapshot_id = (
                raw_item.get("snapshot_id")
                or payload.get("snapshot_id")
                or (manifest_item or {}).get("snapshot_id")
            )
            canonical_url = payload.get("canonical_url") or raw_item.get("canonical_url")
            input_lang_code = payload.get("input_lang_code") or raw_item.get("input_lang_code")
            taxonomy_package_version = (
                payload.get("taxonomy_package_version")
                or raw_item.get("taxonomy_package_version")
            )
            top_candidate_count = (
                payload.get("top_candidate_count")
                if payload.get("top_candidate_count") is not None
                else raw_item.get("top_candidate_count")
            )
            top_score = (
                payload.get("top_score")
                if payload.get("top_score") is not None
                else raw_item.get("top_score")
            )

            writer.writerow([
                batch_key,
                idx,
                export_item_id if export_item_id is not None else r"\N",
                source_url_id if source_url_id is not None else r"\N",
                source_snapshot_id if source_snapshot_id is not None else r"\N",
                canonical_url if canonical_url is not None else r"\N",
                input_lang_code if input_lang_code is not None else r"\N",
                taxonomy_package_version if taxonomy_package_version is not None else r"\N",
                top_candidate_count if top_candidate_count is not None else r"\N",
                top_score if top_score is not None else r"\N",
                compact_json(raw_item),
                compact_json(payload),
            ])

    print(f"BATCH_KEY={batch_key}")
    print(f"ITEM_COUNT_EXPECTED={item_count_expected}")
    print(f"ITEM_COUNT_LOADED={len(raw_items)}")
    print(f"BATCH_TSV={out_batch_tsv}")
    print(f"ITEMS_TSV={out_items_tsv}")


if __name__ == "__main__":
    main()
