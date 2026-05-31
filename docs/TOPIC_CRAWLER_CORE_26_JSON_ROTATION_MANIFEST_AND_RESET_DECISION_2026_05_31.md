# Crawler Core 26 JSON Rotation Manifest and Reset Decision

Gate: `FULL_R4_P2C79A_26_JSON_ROTATION_MANIFEST_AND_RESET_DECISION_DOC_LOCAL_ONLY_R1`

Canonical head before document creation: `976593d31aae05f3b6329852ca6c590883284b95`

## 1. Purpose

This document records the reset boundary and the 26 independent JSON rotation rule for the next crawler_core test phase.

The rule is strict:

`26_SEPARATE_JSON_FILES_ONE_BY_ONE_27TH_READ_RETURNS_TO_FIRST`

That means:

1. The first read must use JSON file `001`.
2. The second read must use JSON file `002`.
3. The sequence continues through JSON file `026`.
4. The same JSON file must not be reused before the 27th read.
5. The 27th read returns to JSON file `001`.

## 2. Current sealed baseline before reset

| Metric | Value |
|---|---:|
| Canonical head | `976593d31aae05f3b6329852ca6c590883284b95` |
| Current repo JSON total count | `56` |
| Existing 26 JSON test candidate count | `0` |
| pi51c service state | `inactive` |
| pi51c service enabled state | `disabled` |
| crawler process count | `0` |
| browser process count | `0` |
| raw file count | `6092` |
| raw total bytes | `812424132` |
| max fetch attempt id | `1922` |
| control state | `pause` |
| control version | `85` |
| `retry_wait` HTTP 3xx rows | `0` |
| dead high-priority HTTP 3xx rows | `0` |
| HTTP 3xx mismatch rows | `0` |
| global mismatch rows | `223` |
| historical 3xx alignment rows | `13` |
| DB body path rows | `1883` |
| distinct DB body path rows | `1883` |
| body bytes sum | `454013656` |
| retry_wait expired lease rows | `0` |
| non-retry_wait lease rows | `0` |

## 3. Reset boundary decision

Reset target:

`CRAWLER_ZSTD_RAW_JSON_DB_AND_COUNTERS`

The reset is not performed in this document gate.

The reset must be a separate explicit mutation gate. It must state exactly which surfaces it resets and which surfaces it preserves.

Required reset preconditions:

1. Desktop and GitHub must be clean and aligned.
2. pi51c `/logisticsearch/repo` must be clean and aligned.
3. pi51c live runtime must match expected runtime hashes.
4. service must be inactive and disabled.
5. crawler process count must be `0`.
6. browser process count must be `0`.
7. reset must not start crawler.
8. reset must not mutate systemd enablement.
9. reset must not blindly delete raw evidence outside the declared reset target.
10. reset must keep the committed policy docs as canonical evidence.

## 4. Planned 26 JSON fixture manifest

Planned fixture directory:

`makpi51crawler/testing/independent_json_rotation_26`

The exact planned fixture paths are:

| Slot | Planned JSON file | Rotation rule |
|---:|---|---|
| `01` | `makpi51crawler/testing/independent_json_rotation_26/rotation_001.json` | read #1, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `02` | `makpi51crawler/testing/independent_json_rotation_26/rotation_002.json` | read #2, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `03` | `makpi51crawler/testing/independent_json_rotation_26/rotation_003.json` | read #3, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `04` | `makpi51crawler/testing/independent_json_rotation_26/rotation_004.json` | read #4, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `05` | `makpi51crawler/testing/independent_json_rotation_26/rotation_005.json` | read #5, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `06` | `makpi51crawler/testing/independent_json_rotation_26/rotation_006.json` | read #6, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `07` | `makpi51crawler/testing/independent_json_rotation_26/rotation_007.json` | read #7, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `08` | `makpi51crawler/testing/independent_json_rotation_26/rotation_008.json` | read #8, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `09` | `makpi51crawler/testing/independent_json_rotation_26/rotation_009.json` | read #9, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `10` | `makpi51crawler/testing/independent_json_rotation_26/rotation_010.json` | read #10, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `11` | `makpi51crawler/testing/independent_json_rotation_26/rotation_011.json` | read #11, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `12` | `makpi51crawler/testing/independent_json_rotation_26/rotation_012.json` | read #12, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `13` | `makpi51crawler/testing/independent_json_rotation_26/rotation_013.json` | read #13, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `14` | `makpi51crawler/testing/independent_json_rotation_26/rotation_014.json` | read #14, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `15` | `makpi51crawler/testing/independent_json_rotation_26/rotation_015.json` | read #15, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `16` | `makpi51crawler/testing/independent_json_rotation_26/rotation_016.json` | read #16, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `17` | `makpi51crawler/testing/independent_json_rotation_26/rotation_017.json` | read #17, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `18` | `makpi51crawler/testing/independent_json_rotation_26/rotation_018.json` | read #18, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `19` | `makpi51crawler/testing/independent_json_rotation_26/rotation_019.json` | read #19, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `20` | `makpi51crawler/testing/independent_json_rotation_26/rotation_020.json` | read #20, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `21` | `makpi51crawler/testing/independent_json_rotation_26/rotation_021.json` | read #21, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `22` | `makpi51crawler/testing/independent_json_rotation_26/rotation_022.json` | read #22, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `23` | `makpi51crawler/testing/independent_json_rotation_26/rotation_023.json` | read #23, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `24` | `makpi51crawler/testing/independent_json_rotation_26/rotation_024.json` | read #24, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `25` | `makpi51crawler/testing/independent_json_rotation_26/rotation_025.json` | read #25, then read #27 returns to `rotation_001.json` only after all 26 have been read once |
| `26` | `makpi51crawler/testing/independent_json_rotation_26/rotation_026.json` | read #26, then read #27 returns to `rotation_001.json` only after all 26 have been read once |

## 5. Fixture creation policy

The 26 JSON files do not exist yet. They must be created in a later explicit local-only fixture creation gate.

The fixture creation gate must:

1. create exactly 26 JSON files,
2. create no extra JSON files,
3. use deterministic names `rotation_001.json` through `rotation_026.json`,
4. make every JSON file syntactically valid,
5. make every JSON file semantically distinct,
6. include rotation_slot values `1` through `26`,
7. include a stable `rotation_manifest_version`,
8. include a `source_file_id` matching the filename,
9. include data that can prove which file was read,
10. include enough payload variety to catch accidental same-file reuse.

## 6. Independent read test policy

The Ubuntu Desktop independent 26 JSON test must prove:

1. read #1 uses `rotation_001.json`,
2. read #2 uses `rotation_002.json`,
3. read #26 uses `rotation_026.json`,
4. no slot is repeated within reads #1 through #26,
5. read #27 returns to `rotation_001.json`,
6. the reader state is deterministic,
7. the reader state survives the test window exactly as specified,
8. every read logs the file path and `rotation_slot`,
9. every read proves JSON parse success,
10. any deviation fails the gate.

## 7. Forbidden actions before explicit reset gate

The following actions remain forbidden until an explicit mutation gate authorizes them:

1. DB reset,
2. raw delete,
3. raw move,
4. raw compression,
5. git reset,
6. catalog mutation,
7. systemd mutation,
8. rsync/copy to live runtime,
9. crawler start,
10. control mutation,
11. fixture creation outside the declared fixture directory,
12. reusing one JSON file as if it were 26 independent files.

## 8. Next required gate

The next gate must audit this document read-only:

`FULL_R4_P2C79B_26_JSON_ROTATION_MANIFEST_AND_RESET_DECISION_DOC_AUDIT_READONLY_R1`

After that, the safe sequence is:

1. commit/push this decision doc,
2. sync pi51c repo doc-only,
3. create 26 JSON fixtures local-only,
4. audit 26 JSON fixtures,
5. commit/push fixtures,
6. sync pi51c repo if needed,
7. run explicit reset mutation gate,
8. run Ubuntu Desktop independent 26 JSON rotation test.
