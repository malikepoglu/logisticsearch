# Stage5 Bulgarian Taxonomy Patch / Review / Sync / Live-Swap Seal — 2026-04-25

## EN

Final state: **PASS**.

This document seals the Stage5 Bulgarian taxonomy review and synchronization chain.

Stage5 covered:

1. Stage5A Bulgarian baseline review from the Ubuntu Desktop canonical taxonomy DB.
2. Stage5B manual-actionable decision draft.
3. Stage5C final Bulgarian human-language decision seal.
4. Stage5D R2 minimal patch proposal, read-only.
5. Stage5E R1 exact-target patch applied to the Desktop canonical DB and committed to GitHub.
6. Stage5F R2 patched Desktop DB restored to a pi51c scratch DB and audited.
7. Stage5G R1 controlled pi51c live swap from the Stage5F scratch DB.
8. Stage5G post-swap final read-only seal and backup cleanup policy.

No Stage5 documentation step accessed or mutated any DB.

## TR

Final durum: **PASS**.

Bu doküman Stage5 Bulgarian taxonomy review ve senkronizasyon zincirini mühürler.

Stage5 kapsamı:

1. Stage5A Bulgarian baseline review, Ubuntu Desktop canonical taxonomy DB üzerinden üretildi.
2. Stage5B manual-actionable decision draft üretildi.
3. Stage5C final Bulgarian human-language decision seal üretildi.
4. Stage5D R2 minimal patch proposal read-only olarak mühürlendi.
5. Stage5E R1 exact-target patch Desktop canonical DB'ye uygulandı ve GitHub'a commit edildi.
6. Stage5F R2 patched Desktop DB pi51c scratch DB'ye restore edilip audit edildi.
7. Stage5G R1 Stage5F scratch DB'den kontrollü pi51c live swap yaptı.
8. Stage5G post-swap final read-only seal ve backup cleanup policy tamamlandı.

Bu Stage5 dokümantasyon adımı hiçbir DB'ye bağlanmaz ve hiçbir DB mutate etmez.

---

## Final Decision / Nihai Karar

Bulgarian patch required: **TRUE** — already applied and synchronized to pi51c live.

Patch scope:

- `bg / 10.2.3`
- `bg / 10.2.9`

Applied repair:

| Node | Old title / keyword | New title / keyword |
| --- | --- | --- |
| `10.2.3` | `Услуги за Наем на превозни средства` | `Услуги за наем на превозни средства` |
| `10.2.9` | `Услуги за Наем на камион с оператор` | `Услуги за наем на камион с оператор` |

Reason: Bulgarian mid-phrase capitalization/style repair. The word `Наем` was changed to lowercase `наем` after `за`, while preserving the original service meaning.

---

## Evidence Summary

| Stage | Result |
| --- | --- |
| Stage5A baseline rows | 335 Bulgarian rows |
| Stage5A non-low-risk priority rows | 218 |
| Stage5A manual-actionable rows | 14 |
| Stage5B draft keep candidates | 9 |
| Stage5B draft manual review required | 5 |
| Stage5C final keep decisions | 12 |
| Stage5C final patch rows | 2 |
| Stage5D R2 proposal rows | 2 |
| Stage5E R1 patched translation rows | 2 |
| Stage5E R1 patched keyword rows | 2 |
| Stage5F R2 Desktop vs pi51c scratch | MATCH |
| Stage5G R1 Desktop vs new pi51c live | MATCH |
| Stage5G final seal | PASS |

---

## Final Deterministic Hashes

Stage5G final deterministic Desktop vs pi51c live hashes matched:

| Surface | SHA256 |
| --- | --- |
| Primary title/keyword rows | `0d8725275aed5a3082cf46ad044f7a9f68a4b44c0bc5d823ecddf70f7d00746a` |
| Search document rows | `364fa761ece259498eed413a5a695780833b5909f9b1f053041acb8e62775a02` |
| Guard metrics | `c3997a5a4a9b92606569f48a3d1fafc9e075dd3c66f7b455080cea5699f8d5be` |
| Bulgarian patch target rows | `cf860368cf8d73f212caf217d3a0f2e8afe14eb45a1391b2e79dfcc2d303cee4` |

---

## Final Live DB State

pi51c live DB after Stage5G:

- Live DB: `logisticsearch_taxonomy`
- Promoted scratch DB: `ls_tax_stage5e_bg_patch_scratch_20260425_035225`
- Scratch exists after swap: **FALSE**
- New Stage5G backup DB: `logisticsearch_taxonomy_pre_stage5g_bg_patch_20260425_035225`
- Stage4G backup preserved: `logisticsearch_taxonomy_pre_stage4g_ar_patch_20260425_021827`
- Stage2H backup preserved: `logisticsearch_taxonomy_pre_stage2h_tr_patch_20260425_004329`
- 007_R2B backup preserved: `logisticsearch_taxonomy_pre_007_r2b_20260424_220836`

Remote pre-swap live dump:

`/srv/crawler/logisticsearch/backups/taxonomy_stage5g_pi51c_live_swap_2026-04-25_04-05-07/logisticsearch_taxonomy_before_stage5g_live_swap_20260425_040507.dump`

Remote dump sha256:

`ad2c83115c7fa47cb4c9a78f9843bc45efa7dce3f660e2232e45f3023d93495c`

Remote dump bytes:

`929129`

---

## Guard State

Final guard state:

- supported languages: 25
- active supported languages: 25
- taxonomy nodes: 335
- taxonomy node translations: 8375
- taxonomy keywords: 8375
- primary keyword rows: 8375
- taxonomy search documents: 8375
- taxonomy closure rows: 995
- duplicate primary keyword groups: 0
- target-related duplicate groups: 0
- blank title/keyword count: 0
- marker count: 0
- required function floor: PASS

---

## Backup Cleanup Policy

Current backup cleanup policy: **DELETE_NONE_NOW**.

No pi51c taxonomy backup DB was deleted in Stage5G post-swap final seal.

Kept backup DBs:

1. `logisticsearch_taxonomy_pre_stage5g_bg_patch_20260425_035225`
2. `logisticsearch_taxonomy_pre_stage4g_ar_patch_20260425_021827`
3. `logisticsearch_taxonomy_pre_stage2h_tr_patch_20260425_004329`
4. `logisticsearch_taxonomy_pre_007_r2b_20260424_220836`

A future cleanup decision must be a separate explicit command.

---

## SQL Patch

Patch SQL:


Patch SQL sha256:

`a18492abd8d0f0e9b7ee6cccb1f4b4e26fdeb4d5be11c811320a22288730970c`

---

## Next Step

Return to the full 8375 title/keyword human-logic review continuation.

Recommended next language baseline should be generated from the Desktop canonical taxonomy DB.

