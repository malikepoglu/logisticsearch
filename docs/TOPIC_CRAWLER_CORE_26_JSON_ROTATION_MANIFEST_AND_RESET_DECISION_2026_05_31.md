# Crawler Core 26 JSON Rotation Manifest and Reset Decision

Gate: `FULL_R4_P2C79A_26_JSON_ROTATION_MANIFEST_AND_RESET_DECISION_DOC_LOCAL_ONLY_R1`

Correction gate: `FULL_R4_P2C80C_REAL_RUNTIME_JSON_SURFACE_DECISION_DOC_PATCH_LOCAL_ONLY_R1`

Canonical head before correction: `85979468152475ee95f688c00a16f1e081526c2a`

## 1. Hard rule correction

The test surface must be the real runtime surface.

A separate testing directory, separate fixture JSON directory, separate test database, or synthetic JSON surface is not acceptable for this phase, because that would test the substitute surface rather than the crawler_core runtime surface.

The previous wording that pointed to a dedicated testing fixture directory is retired.

Correct rule:

`TEST_SURFACE_MUST_BE_THE_REAL_RUNTIME_SURFACE`

Rotation rule remains:

`26_SEPARATE_JSON_FILES_ONE_BY_ONE_27TH_READ_RETURNS_TO_FIRST`

## 2. Correct 26 JSON surface

The 26 JSON files for this phase are the existing real runtime startpoint catalog JSON files under:

`makpi51crawler/catalog/startpoints`

These files already exist in Desktop, GitHub, pi51c `/logisticsearch/repo`, and pi51c live runtime. They are not new test fixtures.

## 3. Current sealed baseline before reset

| Metric | Value |
|---|---:|
| Canonical head | `85979468152475ee95f688c00a16f1e081526c2a` |
| Current repo JSON total count | `56` |
| Real runtime startpoint JSON count | `26` |
| Wrong testing fixture JSON count | `0` |
| pi51c service state | `inactive` |
| pi51c service enabled state | `disabled` |
| crawler process count | `0` |
| browser process count | `0` |
| raw file count | `6092` |
| raw total bytes | `812424132` |
| max fetch attempt id | `1922` |
| control state | `pause` |
| control version | `85` |
| DB body path rows | `1883` |
| distinct DB body path rows | `1883` |

## 4. Reset boundary decision

Reset target remains:

`CRAWLER_ZSTD_RAW_JSON_DB_AND_COUNTERS`

The reset is not performed in this document gate.

The reset must be a separate explicit mutation gate. It must state exactly which DB counters, raw JSON/ZSTD evidence surfaces, and crawler runtime counters it resets.

The reset gate must not create a separate test database.

The reset gate must not create a separate testing JSON directory.

The reset gate must not replace the real runtime catalog JSON files with synthetic fixture files.

## 5. Real runtime 26 JSON rotation manifest

| Slot | Real runtime JSON file | Rotation rule |
|---:|---|---|
| `01` | `makpi51crawler/catalog/startpoints/ar/arabic_source_families_v2.json` | real runtime startpoint catalog JSON; read #1; read #27 returns to slot `01` |
| `02` | `makpi51crawler/catalog/startpoints/bg/bulgarian_source_families_v2.json` | real runtime startpoint catalog JSON; read #2; read #27 returns to slot `01` |
| `03` | `makpi51crawler/catalog/startpoints/bn/bengali_source_families_v2.json` | real runtime startpoint catalog JSON; read #3; read #27 returns to slot `01` |
| `04` | `makpi51crawler/catalog/startpoints/cs/czech_source_families_v2.json` | real runtime startpoint catalog JSON; read #4; read #27 returns to slot `01` |
| `05` | `makpi51crawler/catalog/startpoints/de/german_source_families_v2.json` | real runtime startpoint catalog JSON; read #5; read #27 returns to slot `01` |
| `06` | `makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json` | real runtime startpoint catalog JSON; read #6; read #27 returns to slot `01` |
| `07` | `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json` | real runtime startpoint catalog JSON; read #7; read #27 returns to slot `01` |
| `08` | `makpi51crawler/catalog/startpoints/es/spanish_source_families_v2.json` | real runtime startpoint catalog JSON; read #8; read #27 returns to slot `01` |
| `09` | `makpi51crawler/catalog/startpoints/fr/french_source_families_v2.json` | real runtime startpoint catalog JSON; read #9; read #27 returns to slot `01` |
| `10` | `makpi51crawler/catalog/startpoints/global/global_directories_source_families_v2.json` | real runtime startpoint catalog JSON; read #10; read #27 returns to slot `01` |
| `11` | `makpi51crawler/catalog/startpoints/he/hebrew_source_families_v2.json` | real runtime startpoint catalog JSON; read #11; read #27 returns to slot `01` |
| `12` | `makpi51crawler/catalog/startpoints/hi/hindi_source_families_v2.json` | real runtime startpoint catalog JSON; read #12; read #27 returns to slot `01` |
| `13` | `makpi51crawler/catalog/startpoints/hu/hungarian_source_families_v2.json` | real runtime startpoint catalog JSON; read #13; read #27 returns to slot `01` |
| `14` | `makpi51crawler/catalog/startpoints/id/indonesian_source_families_v2.json` | real runtime startpoint catalog JSON; read #14; read #27 returns to slot `01` |
| `15` | `makpi51crawler/catalog/startpoints/it/italian_source_families_v2.json` | real runtime startpoint catalog JSON; read #15; read #27 returns to slot `01` |
| `16` | `makpi51crawler/catalog/startpoints/ja/japanese_source_families_v2.json` | real runtime startpoint catalog JSON; read #16; read #27 returns to slot `01` |
| `17` | `makpi51crawler/catalog/startpoints/ko/korean_source_families_v2.json` | real runtime startpoint catalog JSON; read #17; read #27 returns to slot `01` |
| `18` | `makpi51crawler/catalog/startpoints/nl/dutch_source_families_v2.json` | real runtime startpoint catalog JSON; read #18; read #27 returns to slot `01` |
| `19` | `makpi51crawler/catalog/startpoints/pt/portuguese_source_families_v2.json` | real runtime startpoint catalog JSON; read #19; read #27 returns to slot `01` |
| `20` | `makpi51crawler/catalog/startpoints/ro/romanian_source_families_v2.json` | real runtime startpoint catalog JSON; read #20; read #27 returns to slot `01` |
| `21` | `makpi51crawler/catalog/startpoints/ru/russian_source_families_v2.json` | real runtime startpoint catalog JSON; read #21; read #27 returns to slot `01` |
| `22` | `makpi51crawler/catalog/startpoints/tr/turkish_source_families_v2.json` | real runtime startpoint catalog JSON; read #22; read #27 returns to slot `01` |
| `23` | `makpi51crawler/catalog/startpoints/uk/ukrainian_source_families_v2.json` | real runtime startpoint catalog JSON; read #23; read #27 returns to slot `01` |
| `24` | `makpi51crawler/catalog/startpoints/ur/urdu_source_families_v2.json` | real runtime startpoint catalog JSON; read #24; read #27 returns to slot `01` |
| `25` | `makpi51crawler/catalog/startpoints/vi/vietnamese_source_families_v2.json` | real runtime startpoint catalog JSON; read #25; read #27 returns to slot `01` |
| `26` | `makpi51crawler/catalog/startpoints/zh/chinese_source_families_v2.json` | real runtime startpoint catalog JSON; read #26; read #27 returns to slot `01` |

## 6. Independent read test policy

The Ubuntu Desktop independent 26 JSON test must prove:

1. read #1 uses slot `01`,
2. read #2 uses slot `02`,
3. read #26 uses slot `26`,
4. no slot is repeated within reads #1 through #26,
5. read #27 returns to slot `01`,
6. the reader uses the real runtime startpoint catalog JSON files,
7. the reader logs the exact file path and slot,
8. every read proves JSON parse success,
9. every read proves it touched the expected real runtime path,
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
11. separate testing fixture directory creation,
12. separate test database creation,
13. synthetic replacement JSON creation,
14. pretending one JSON file is twenty-six independent JSON files.

## 8. Next required gate

The next gate must audit this corrected document read-only:

`FULL_R4_P2C80D_REAL_RUNTIME_JSON_SURFACE_DECISION_DOC_AUDIT_READONLY_R1`

After that, the safe sequence is:

1. commit/push this corrected decision doc,
2. sync pi51c repo doc-only,
3. plan reset using only real runtime surfaces,
4. run explicit reset mutation gate,
5. run Ubuntu Desktop independent 26 JSON rotation test over the real startpoint catalog JSON files.
