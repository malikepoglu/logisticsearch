# Stage4 Arabic Taxonomy Patch / Review / Sync / Live-Swap Seal — 2026-04-25

## EN

Final state: **PASS**.

Stage4 sealed the Arabic taxonomy review and patch chain from Desktop canonical DB through pi51c scratch restore/audit and controlled pi51c live swap.

This document records the final Arabic patch chain:

1. Stage4A — Arabic baseline human-logic review from Desktop canonical taxonomy DB.
2. Stage4B — Arabic manual-actionable decision draft.
3. Stage4C — Arabic final human-language decision seal.
4. Stage4D R2 — Arabic minimal patch proposal, read-only, exact-target model.
5. Stage4E R1 — Arabic minimal exact-target patch applied to Desktop canonical taxonomy DB and committed to GitHub.
6. Stage4F — patched Desktop taxonomy restored to pi51c scratch DB and audited.
7. Stage4G — pi51c controlled live swap from Stage4F scratch DB.
8. Stage4G final seal — post-swap read-only final verification and backup cleanup policy.

No backup database was deleted during the final cleanup-policy step.

Current backup cleanup policy: **DELETE_NONE_NOW**.

## TR

Final durum: **PASS**.

Stage4, Arabic taxonomy review ve patch zincirini Desktop canonical DB'den pi51c scratch restore/audit hattına ve kontrollü pi51c live swap aşamasına kadar mühürledi.

Bu doküman Arabic patch zincirini kaydeder:

1. Stage4A — Desktop canonical taxonomy DB'den Arabic baseline human-logic review.
2. Stage4B — Arabic manual-actionable karar taslağı.
3. Stage4C — Arabic nihai human-language karar mührü.
4. Stage4D R2 — Arabic minimal patch proposal, read-only, exact-target model.
5. Stage4E R1 — Arabic minimal exact-target patch'in Desktop canonical taxonomy DB'ye uygulanması ve GitHub'a commit edilmesi.
6. Stage4F — patch'li Desktop taxonomy DB'nin pi51c scratch DB'ye restore/audit edilmesi.
7. Stage4G — Stage4F scratch DB'den kontrollü pi51c live swap.
8. Stage4G final seal — post-swap read-only final doğrulama ve backup cleanup policy.

Final cleanup-policy adımında hiçbir backup veritabanı silinmedi.

Mevcut backup cleanup policy: **DELETE_NONE_NOW**.

---

## Repository state / Repo durumu

- Final repo commit after Arabic patch SQL: `6aee8953e6e2b1db4fb2247cd6b49d19d5880f53`
- Commit message: `feat(taxonomy): repair Arabic leasing labels`
- Arabic patch SQL:
  - `hosts/makpi51crawler/sql/taxonomy_core/009_taxonomy_arabic_leasing_phrase_repair_2026_04_25.sql`
  - sha256: `1d2ef009c712a39fda77abe67ea905f5a6a57ea28ae0881164fb105bb85d978a`
- Turkish patch SQL remains unchanged:
  - `hosts/makpi51crawler/sql/taxonomy_core/008_taxonomy_turkish_leasing_phrase_repair_2026_04_25.sql`
  - sha256: `5a66b8d844c199503ce9f923e83927b06b57257aa989cdd8700825a0e8728a83`

---

## Stage4A Arabic baseline review / Stage4A Arabic baseline inceleme

Stage4A generated a fresh Arabic baseline package from Desktop canonical taxonomy DB.

| Metric | Value |
|---|---:|
| Arabic all rows | `335` |
| Arabic all non-low-risk priority rows | `218` |
| Arabic manual-actionable priority rows | `14` |
| Arabic P2 language-quality rows | `0` |
| Arabic machine-phrase rows | `0` |
| Arabic node-code-controlled service rows | `13` |
| Arabic wide service-side diagnostic rows | `217` |
| Arabic title/keyword difference rows | `1` |

Guard metrics passed:

- supported languages: `25`
- taxonomy nodes: `335`
- taxonomy node translations: `8375`
- taxonomy keywords: `8375`
- taxonomy search documents: `8375`
- duplicate primary keyword groups: `0`
- target-related duplicate groups: `0`
- blank title/keyword count: `0`
- required function floor: **PASS**

## Stage4B / Stage4C Arabic human-language decision

Stage4B produced a draft decision table.

Stage4C sealed the final human-language decision:

| Metric | Value |
|---|---:|
| Arabic manual-actionable decisions | `14` |
| Arabic KEEP decisions | `9` |
| Arabic patch-required rows | `5` |
| Arabic patch required | `TRUE` |

Patch target nodes:

- `ar / 10.2.5`
- `ar / 10.3.1`
- `ar / 10.3.2`
- `ar / 10.3.3`
- `ar / 10.3.4`

Patch target replacements:

| Node | Old label model | New label |
|---|---|---|
| `10.2.5` | mixed/transliterated leasing phrase | `تأجير قصير أو طويل الأجل لطائرات الركاب` |
| `10.3.1` | transliterated leasing phrase | `تأجير طويل الأجل لسيارات سيدان / كوبيه / ستيشن واجن` |
| `10.3.2` | transliterated leasing + English SUV | `تأجير طويل الأجل لشاحنات خفيفة / سيارات رياضية متعددة الاستخدامات` |
| `10.3.3` | transliterated van/minivan wording | `تأجير طويل الأجل لمركبات ركاب / حافلات صغيرة` |
| `10.3.4` | transliterated leasing phrase | `تأجير طويل الأجل لوسائط النقل` |

## Stage4D R2 Arabic minimal patch proposal

Stage4D R2 passed after correcting DB primary-key aliases:

- `taxonomy_nodes.id AS node_id`
- `taxonomy_node_translations.id AS translation_id`
- `taxonomy_keywords.id AS keyword_id`

Read-only proposal result:

| Metric | Value |
|---|---:|
| Proposal rows | `5` |
| Translation target rows | `5` |
| Exact keyword target rows | `5` |
| Current target rows found by exact current match | `5` |
| Virtual duplicate group count after patch | `0` |
| Virtual target-related duplicate group count after patch | `0` |
| Primary search language touch count | `0` |
| Blank title after patch | `0` |
| Blank keyword after patch | `0` |
| All keyword surface rows after count | `8375` |

Patch target model: **translation row + exact current keyword row only**.

## Stage4E Desktop DB patch

Stage4E R1 applied the Arabic patch only to Desktop canonical taxonomy DB.

Patch scope:

- only Arabic (`ar`)
- only nodes `10.2.5`, `10.3.1`, `10.3.2`, `10.3.3`, `10.3.4`
- translation title + exact current keyword row only

Post-patch Desktop audit:

| Metric | Value |
|---|---:|
| Patched translation rows | `5` |
| Patched keyword rows | `5` |
| Old translation rows | `0` |
| Old keyword rows | `0` |
| Duplicate primary keyword group count | `0` |
| Target-related duplicate group count | `0` |
| Blank title count | `0` |
| Blank keyword count | `0` |
| Primary search language touch count | `0` |
| Taxonomy node translations | `8375` |
| Taxonomy keywords | `8375` |
| Taxonomy search documents | `8375` |
| Required function floor | **PASS** |

Desktop backups:

- Pre-patch dump:
  - `/home/mak/logisticsearch_local_archives/taxonomy_stage4e_r1_fix_temp_table_scope_guard_2026-04-25_02-14-27/logisticsearch_desktop_taxonomy_before_stage4e_r1_arabic_exact_patch_2026-04-25_02-14-27.dump`
  - sha256: `f6b3e66985bfab71b29a00a230ca964360447a92e1cf0879e30f712d37ac1b70`
- Post-patch dump:
  - `/home/mak/logisticsearch_local_archives/taxonomy_stage4e_r1_fix_temp_table_scope_guard_2026-04-25_02-14-27/logisticsearch_desktop_taxonomy_after_stage4e_r1_arabic_exact_patch_2026-04-25_02-14-27.dump`
  - sha256: `d4cec20d49af3a60cdaa0e2159b88bfdc9dfdb42d345a71fcc6f48484fed6260`

## Stage4F pi51c scratch restore/audit

Stage4F restored the patched Desktop taxonomy DB to pi51c scratch DB only.

Scratch DB:

- `ls_tax_stage4e_ar_patch_scratch_20260425_021827`

Desktop dump transferred to pi51c:

- Local path:
  - `/home/mak/logisticsearch_local_archives/taxonomy_stage4f_pi51c_scratch_restore_audit_2026-04-25_02-18-27/logisticsearch_desktop_taxonomy_stage4e_arabic_patch_2026-04-25_02-18-27.dump`
- sha256:
  - `6a23bb5bb35b8d73e0f06b5ea43da09a3af15a4d163a6b81ac4b0759661e101c`

Stage4F deterministic Desktop vs pi51c scratch hashes matched:

| Surface | SHA256 |
|---|---|
| Primary title/keyword rows | `0e2ae3783c41e21ae760c51536e3bdbb9c724d09f3e8342840b6aa26b454e40a` |
| Search document rows | `14f6cda5c17b2828130f9720e6295365e2340fd40e6a35701aac8d223f7de889` |
| Guard metrics | `c3997a5a4a9b92606569f48a3d1fafc9e075dd3c66f7b455080cea5699f8d5be` |
| Arabic patch target rows | `b6769e42590b1228fb6631bdc43ce6ddfd451f69d27cb7e7e2e3ffe6a1d4fa26` |

pi51c live and backup DBs were not mutated during Stage4F.

## Stage4G pi51c controlled live swap

Stage4G promoted the audited scratch DB to live.

Final live DB:

- `logisticsearch_taxonomy`

Promoted from scratch DB:

- `ls_tax_stage4e_ar_patch_scratch_20260425_021827`

New Stage4G backup DB:

- `logisticsearch_taxonomy_pre_stage4g_ar_patch_20260425_021827`

Preserved backup DBs:

- `logisticsearch_taxonomy_pre_stage2h_tr_patch_20260425_004329`
- `logisticsearch_taxonomy_pre_007_r2b_20260424_220836`

Pre-swap live dump:

- `/srv/crawler/logisticsearch/backups/taxonomy_stage4g_pi51c_live_swap_2026-04-25_02-29-28/logisticsearch_taxonomy_before_stage4g_live_swap_20260425_022928.dump`
- sha256: `b9978f36b235b3872639ae996bf146afeeb64e4cd7e7c0cdd74df282fc81e8cb`
- bytes: `928829`

Stage4G final deterministic Desktop vs pi51c live hashes matched:

| Surface | Desktop SHA256 | pi51c live SHA256 |
|---|---|---|
| Primary title/keyword rows | `0e2ae3783c41e21ae760c51536e3bdbb9c724d09f3e8342840b6aa26b454e40a` | `0e2ae3783c41e21ae760c51536e3bdbb9c724d09f3e8342840b6aa26b454e40a` |
| Search document rows | `14f6cda5c17b2828130f9720e6295365e2340fd40e6a35701aac8d223f7de889` | `14f6cda5c17b2828130f9720e6295365e2340fd40e6a35701aac8d223f7de889` |
| Guard metrics | `c3997a5a4a9b92606569f48a3d1fafc9e075dd3c66f7b455080cea5699f8d5be` | `c3997a5a4a9b92606569f48a3d1fafc9e075dd3c66f7b455080cea5699f8d5be` |
| Arabic patch target rows | `b6769e42590b1228fb6631bdc43ce6ddfd451f69d27cb7e7e2e3ffe6a1d4fa26` | `b6769e42590b1228fb6631bdc43ce6ddfd451f69d27cb7e7e2e3ffe6a1d4fa26` |

Final live guard state:

- supported/active languages: `25`
- taxonomy nodes: `335`
- taxonomy node translations: `8375`
- taxonomy keywords: `8375`
- primary keyword rows: `8375`
- taxonomy search documents: `8375`
- taxonomy closure rows: `995`
- duplicate primary keyword group count: `0`
- target-related duplicate group count: `0`
- blank title/keyword count: `0`
- marker count: `0`
- required function floor: **PASS**

## Backup cleanup policy

Current policy: **DELETE_NONE_NOW**.

No backup DB was dropped.

Keep all currently preserved taxonomy backup DBs:

1. `logisticsearch_taxonomy_pre_stage4g_ar_patch_20260425_021827`
2. `logisticsearch_taxonomy_pre_stage2h_tr_patch_20260425_004329`
3. `logisticsearch_taxonomy_pre_007_r2b_20260424_220836`

Cleanup requires a separate explicit command and a separate read-only precheck.

## Final decision

Arabic Stage4 status: **PASS**.

Arabic patch required: **TRUE** — already applied and synchronized to pi51c live.

DB mutation status:

- Desktop canonical DB mutated in Stage4E only.
- pi51c scratch DB created/restored in Stage4F.
- pi51c live DB name swap performed in Stage4G.
- No backup DB dropped.
- No data deletion performed.

Next step: continue full `8375` title/keyword human-logic review from the next language baseline review.
