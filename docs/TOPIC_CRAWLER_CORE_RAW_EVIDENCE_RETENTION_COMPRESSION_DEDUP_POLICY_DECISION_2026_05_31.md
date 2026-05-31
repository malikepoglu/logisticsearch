# Crawler Core Raw Evidence Retention / Compression / Dedup Policy Decision

Gate: `FULL_R4_P2C77A_RAW_EVIDENCE_RETENTION_COMPRESSION_DEDUP_POLICY_DECISION_DOC_LOCAL_ONLY_R1`

Image item: `5_OF_5_RAW_EVIDENCE_RETENTION_COMPRESSION_DEDUP_POLICY`

Canonical head before document creation: `de960ef5a16403f7041ce8b8a2dc77549e3f2c16`

## 1. Scope

This document records the raw evidence retention, compression, and deduplication policy after the read-only plan gate:

`FULL_R4_P2C77_IMAGE_ITEM5_RAW_EVIDENCE_RETENTION_COMPRESSION_DEDUP_POLICY_PLAN_READONLY_R1`

The policy is intentionally conservative. Current raw evidence remains preserved. Optimization is allowed only after manifest-backed proof protects DB references and audit reproducibility.

## 2. Sealed raw evidence inventory

| Metric | Value |
|---|---:|
| Raw root | `/srv/webcrawler/raw_fetch` |
| Raw file count | `6092` |
| Raw total bytes | `812424132` |
| Date dir `2026/05/29` file count | `6065` |
| Date dir `2026/05/30` file count | `27` |
| `.fetch.json.zst` files | `1883` |
| Other raw files | `4209` |
| `.bin` suffix files | `3473` |
| `.html` suffix files | `368` |
| `.png` suffix files | `368` |
| `.zst` suffix files | `1883` |
| Zstandard magic-bad files | `0` |
| Suspicious temporary files | `0` |

## 3. DB body path inventory

| Metric | Value |
|---|---:|
| `http_fetch.fetch_attempt` rows | `1922` |
| Body path rows | `1883` |
| Distinct body path rows | `1883` |
| DB duplicate body path groups | `0` |
| DB missing body path count | `0` |
| DB resolved existing body paths | `1883` |
| Body bytes sum from DB | `454013656` |

Interpretation: all DB-referenced body paths are present. The DB body path surface is currently consistent and must not be damaged by raw evidence optimization.

## 4. Unreferenced and duplicate-content inventory

| Metric | Value |
|---|---:|
| Raw files not referenced by `body_storage_path` | `4209` |
| Same-size candidate groups | `615` |
| Same-size candidate files | `2700` |
| Duplicate content groups | `486` |
| Duplicate content files | `2066` |

The duplicate-content evidence is real, but it is not a deletion license. Many duplicate groups are robots bodies, rendered HTML, screenshots, and repeated bodies captured at different times. These may be valuable as audit evidence for crawler behavior, retry timing, browser behavior, robots handling, and historical reproducibility.

## 5. Current policy decision

### 5.1 Retention

Decision:

`PRESERVE_ALL_CURRENT_RAW_EVIDENCE_UNTIL_MANIFEST_BACKED_ARCHIVAL_POLICY_EXISTS`

Current raw files remain untouched. The current raw evidence tree is an audit source, not disposable cache.

### 5.2 Compression

Decision:

`NO_IN_PLACE_RECOMPRESSION`

No existing raw file may be recompressed in place. Future compression may be allowed only as an append-only archival artifact with a manifest that maps original path, original size, original SHA256, archive path, archive size, archive SHA256, and validation timestamp.

### 5.3 Deduplication

Decision:

`NO_RAW_DELETION_FOR_DEDUP_AT_THIS_STAGE`

Deduplication must be manifest-first. Physical deletion is not part of this phase. Hardlinks and symlinks are also not allowed at this stage because they can hide evidence loss, break path-level audit expectations, or confuse future reset/test comparisons.

### 5.4 DB protection

Decision:

`DB_BODY_STORAGE_PATH_REFERENCES_ARE_CANONICAL_PROTECTION_BOUNDARIES`

Every DB-referenced `body_storage_path` must remain readable until a future explicit migration changes the DB reference model. Manifest-only dedup reports may be created, but DB references must not be silently redirected.

### 5.5 Screenshots and rendered HTML

Decision:

`BROWSER_EVIDENCE_IS_HIGH_VALUE_EVIDENCE`

Screenshots and rendered HTML are not low-value trash. They prove browser acquisition behavior, dynamic rendering, and cleanup quality. They may be large, but compression/dedup policy must preserve traceability.

## 6. Forbidden actions

The following actions are forbidden in this phase:

1. raw evidence deletion
2. raw evidence move
3. in-place raw recompression
4. DB mutation
5. crawler start
6. systemd mutation
7. blind duplicate cleanup
8. hardlink or symlink replacement
9. body path rewrite
10. cache-style cleanup without manifest proof

## 7. Future allowed design

A future safe raw-evidence optimization design may introduce:

1. A content-addressed raw evidence archive root outside the current active raw root.
2. A manifest table or manifest JSONL with original path, raw SHA256, size, capture time, evidence type, and DB reference status.
3. Dry-run-only duplicate grouping by content hash.
4. Explicit keep rules:
   - keep all DB-referenced body paths
   - keep all `.fetch.json.zst`
   - keep all latest browser screenshots until parse/render policy is settled
   - keep historical 3xx and browser-debug evidence until final crawler_core reset
5. Optional archive-copy verification.
6. Only after successful verification, a separate explicit cleanup proposal.

## 8. Decision for the next gate

The next gate must audit this document read-only and prove:

1. The document exists only as a local untracked doc.
2. The repo has no other dirty file.
3. The sealed P2C77 metrics are recorded exactly once.
4. Forbidden actions are stated as forbidden.
5. No DB/raw/crawler/systemd/git mutation occurred after the plan gate.

Required next gate:

`FULL_R4_P2C77B_RAW_EVIDENCE_RETENTION_COMPRESSION_DEDUP_POLICY_DECISION_DOC_AUDIT_READONLY_R1`
