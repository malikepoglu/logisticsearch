# TOPIC_TAXONOMY_STAGE2_TURKISH_LEASING_PATCH_SYNC_SEAL_2026_04_25

## EN

### Status

This document seals the Stage2 Turkish leasing label repair line.

Final state: **PASS**.

The complete chain is:

1. Stage2F: apply the Turkish minimal exact-target patch to the Ubuntu Desktop canonical taxonomy DB.
2. Stage2G: restore the patched Desktop DB into a new pi51c scratch DB and audit it.
3. Stage2H: promote the audited pi51c scratch DB to the live pi51c taxonomy DB.
4. Stage2H post-swap final seal: verify Desktop and pi51c live deterministic content equality and record the backup cleanup policy.

### Patch scope

Patch SQL:

`hosts/makpi51crawler/sql/taxonomy_core/008_taxonomy_turkish_leasing_phrase_repair_2026_04_25.sql`

Patch SQL SHA256:

`5a66b8d844c199503ce9f923e83927b06b57257aa989cdd8700825a0e8728a83`

Git commit:

`7f85148` — `feat(taxonomy): repair Turkish leasing labels`

The patch scope is intentionally narrow:

| Language | Node code | Old label | New label |
|---|---:|---|---|
| `tr` | `10.3.2` | `Hafif Kamyon / SUV Leasingi leasing hizmetleri` | `Hafif Kamyon / SUV Leasing Hizmetleri` |
| `tr` | `10.3.3` | `Yolcu Vanı / Minivan Leasingi leasing hizmetleri` | `Yolcu Vanı / Minivan Leasing Hizmetleri` |

Only the Turkish translation title and exact matching current keyword row were targeted.

The patch did not target non-Turkish rows.

The patch did not touch the semantic alias target line.

### Stage2F — Desktop canonical DB patch

Stage2F applied the corrected exact-target patch to the Ubuntu Desktop canonical taxonomy database:

`logisticsearch_desktop_taxonomy`

Important verified outcomes:

- Patched translation rows: `2`
- Patched keyword rows: `2`
- Old translation rows: `0`
- Old keyword rows: `0`
- Duplicate primary keyword groups: `0`
- Target-related duplicate groups: `0`
- Blank title/keyword count: `0`
- Required function floor: `PASS`
- `taxonomy_search_documents` is a view, so it was not updated directly.

Post-patch backup evidence:

`/home/mak/logisticsearch_local_archives/taxonomy_stage2f_r2_finalize_after_function_guard_fix_2026-04-25_00-36-00/logisticsearch_desktop_taxonomy_after_stage2f_r2_finalize_2026-04-25_00-36-00.dump`

Post-patch backup SHA256:

`35599b5d20759280d9b7974d8b5dae3e17ca611583f51058a0ad86037324f927`

### Stage2G — pi51c scratch restore/audit

Stage2G restored the patched Desktop DB dump into a new pi51c scratch DB:

`ls_tax_stage2f_tr_patch_scratch_20260425_003851`

The live pi51c DB was not mutated during Stage2G.

The preserved backup DB was not mutated during Stage2G.

Patched Desktop dump:

`/home/mak/logisticsearch_local_archives/taxonomy_stage2g_pi51c_scratch_restore_audit_2026-04-25_00-38-51/logisticsearch_desktop_taxonomy_stage2f_patch_2026-04-25_00-38-51.dump`

Patched Desktop dump SHA256:

`f2247b0e09181ca85b967c2291a729debcaff354abc8d867ea3caa0745373f39`

Stage2G deterministic Desktop-vs-scratch hashes matched:

| Surface | SHA256 |
|---|---|
| Primary title/keyword rows | `d1ba632787bf6b280292e3a96a433717c1e9d8cf24c199f21cbcb244b8bf2c27` |
| Search document rows | `41bbb6dfc5f7e307f2362bbb293751cce7229bd2361c3c4b00547cb5dbb3ccbe` |
| Guard metrics | `c3997a5a4a9b92606569f48a3d1fafc9e075dd3c66f7b455080cea5699f8d5be` |
| Patch target rows | `30a68ca35e96f3d14e16057591f337cbfdf1182246bd4e3aedeb1bcb244a2100` |

### Stage2H — pi51c controlled live swap

Stage2H promoted the audited scratch DB to the live pi51c taxonomy DB.

Final live DB:

`logisticsearch_taxonomy`

Promoted scratch DB:

`ls_tax_stage2f_tr_patch_scratch_20260425_003851`

The promoted scratch DB no longer exists after swap.

The previous live DB was not dropped. It was renamed to:

`logisticsearch_taxonomy_pre_stage2h_tr_patch_20260425_004329`

The preserved 007_R2B backup DB remains untouched:

`logisticsearch_taxonomy_pre_007_r2b_20260424_220836`

Pre-swap live dump on pi51c:

`/srv/crawler/logisticsearch/backups/taxonomy_stage2h_pi51c_live_swap_2026-04-25_00-43-29/logisticsearch_taxonomy_before_stage2h_live_swap_20260425_004329.dump`

Pre-swap live dump SHA256:

`f4728b356f051e900d0782df8f177ac44bc344442c9acb0274041550acee9370`

### Stage2H final deterministic live equality

After the post-swap final seal, Ubuntu Desktop canonical DB and pi51c live DB matched on all deterministic surfaces:

| Surface | SHA256 |
|---|---|
| Primary title/keyword rows | `d1ba632787bf6b280292e3a96a433717c1e9d8cf24c199f21cbcb244b8bf2c27` |
| Search document rows | `41bbb6dfc5f7e307f2362bbb293751cce7229bd2361c3c4b00547cb5dbb3ccbe` |
| Guard metrics | `c3997a5a4a9b92606569f48a3d1fafc9e075dd3c66f7b455080cea5699f8d5be` |
| Patch target rows | `30a68ca35e96f3d14e16057591f337cbfdf1182246bd4e3aedeb1bcb244a2100` |

### Final live guard metrics

Final pi51c live guard metrics passed:

- Supported languages: `25`
- Active supported languages: `25`
- Canonical language order: `ar,bg,cs,de,el,en,es,fr,hu,it,ja,ko,nl,pt,ro,ru,tr,zh,hi,bn,ur,uk,id,vi,he`
- Primary search languages: `en,tr`
- Taxonomy nodes: `335`
- Taxonomy translations: `8375`
- Taxonomy keywords: `8375`
- Primary keyword rows: `8375`
- Search documents: `8375`
- Closure rows: `995`
- Duplicate primary keyword groups: `0`
- Target-related duplicate groups: `0`
- Blank title/keyword count: `0`
- Orphan translation node count: `0`
- Orphan keyword node count: `0`
- Orphan translation language count: `0`
- Orphan keyword language count: `0`
- Marker count: `0`
- Required function floor pass: `TRUE`

### Backup cleanup policy

Current policy: **DELETE_NONE_NOW**.

No pi51c taxonomy backup database is deleted as part of this stage.

Keep both backup DBs:

1. `logisticsearch_taxonomy_pre_stage2h_tr_patch_20260425_004329`
2. `logisticsearch_taxonomy_pre_007_r2b_20260424_220836`

Rationale:

- The Stage2H backup is the immediate rollback point for the Turkish patch live swap.
- The 007_R2B backup is an older preserved baseline and must not be silently removed.
- Backup cleanup must be a separate explicit operation after later stability evidence.

### Next step

Return to the full `8375` title/keyword human-logic review.

English baseline review is sealed.

Turkish baseline review is patched, synced, live-swapped, and sealed.

Next language priority: **German baseline review**.

## TR

### Durum

Bu belge Stage2 Turkish leasing label repair hattını mühürler.

Final durum: **PASS**.

Tam zincir:

1. Stage2F: Turkish minimal exact-target patch Ubuntu Desktop canonical taxonomy DB üzerine uygulandı.
2. Stage2G: Patch'li Desktop DB pi51c üzerinde yeni scratch DB'ye restore edildi ve audit edildi.
3. Stage2H: Audit edilmiş pi51c scratch DB, canlı pi51c taxonomy DB olarak promote edildi.
4. Stage2H post-swap final seal: Desktop ve pi51c live deterministic içerik eşitliği tekrar doğrulandı ve backup cleanup policy yazıldı.

### Patch kapsamı

Patch SQL:

`hosts/makpi51crawler/sql/taxonomy_core/008_taxonomy_turkish_leasing_phrase_repair_2026_04_25.sql`

Patch SQL SHA256:

`5a66b8d844c199503ce9f923e83927b06b57257aa989cdd8700825a0e8728a83`

Git commit:

`7f85148` — `feat(taxonomy): repair Turkish leasing labels`

Patch kapsamı bilinçli olarak dardır:

| Dil | Node code | Eski ifade | Yeni ifade |
|---|---:|---|---|
| `tr` | `10.3.2` | `Hafif Kamyon / SUV Leasingi leasing hizmetleri` | `Hafif Kamyon / SUV Leasing Hizmetleri` |
| `tr` | `10.3.3` | `Yolcu Vanı / Minivan Leasingi leasing hizmetleri` | `Yolcu Vanı / Minivan Leasing Hizmetleri` |

Sadece Turkish translation title ve aynı node/lang/current_keyword ile tam eşleşen keyword satırı hedeflendi.

Türkçe dışı satırlar hedeflenmedi.

Semantic alias target hattına dokunulmadı.

### Stage2F — Desktop canonical DB patch

Stage2F, düzeltilmiş exact-target patch'i Ubuntu Desktop canonical taxonomy DB üzerine uyguladı:

`logisticsearch_desktop_taxonomy`

Doğrulanan önemli sonuçlar:

- Patched translation rows: `2`
- Patched keyword rows: `2`
- Old translation rows: `0`
- Old keyword rows: `0`
- Duplicate primary keyword groups: `0`
- Target-related duplicate groups: `0`
- Blank title/keyword count: `0`
- Required function floor: `PASS`
- `taxonomy_search_documents` bir view olduğu için doğrudan update edilmedi.

Post-patch backup evidence:

`/home/mak/logisticsearch_local_archives/taxonomy_stage2f_r2_finalize_after_function_guard_fix_2026-04-25_00-36-00/logisticsearch_desktop_taxonomy_after_stage2f_r2_finalize_2026-04-25_00-36-00.dump`

Post-patch backup SHA256:

`35599b5d20759280d9b7974d8b5dae3e17ca611583f51058a0ad86037324f927`

### Stage2G — pi51c scratch restore/audit

Stage2G, patch'li Desktop DB dump'ını yeni pi51c scratch DB içine restore etti:

`ls_tax_stage2f_tr_patch_scratch_20260425_003851`

Stage2G sırasında canlı pi51c DB değiştirilmedi.

Stage2G sırasında preserved backup DB değiştirilmedi.

Patch'li Desktop dump:

`/home/mak/logisticsearch_local_archives/taxonomy_stage2g_pi51c_scratch_restore_audit_2026-04-25_00-38-51/logisticsearch_desktop_taxonomy_stage2f_patch_2026-04-25_00-38-51.dump`

Patch'li Desktop dump SHA256:

`f2247b0e09181ca85b967c2291a729debcaff354abc8d867ea3caa0745373f39`

Stage2G deterministic Desktop-vs-scratch hash değerleri eşleşti:

| Yüzey | SHA256 |
|---|---|
| Primary title/keyword rows | `d1ba632787bf6b280292e3a96a433717c1e9d8cf24c199f21cbcb244b8bf2c27` |
| Search document rows | `41bbb6dfc5f7e307f2362bbb293751cce7229bd2361c3c4b00547cb5dbb3ccbe` |
| Guard metrics | `c3997a5a4a9b92606569f48a3d1fafc9e075dd3c66f7b455080cea5699f8d5be` |
| Patch target rows | `30a68ca35e96f3d14e16057591f337cbfdf1182246bd4e3aedeb1bcb244a2100` |

### Stage2H — pi51c controlled live swap

Stage2H, audit edilmiş scratch DB'yi canlı pi51c taxonomy DB yaptı.

Final live DB:

`logisticsearch_taxonomy`

Promote edilen scratch DB:

`ls_tax_stage2f_tr_patch_scratch_20260425_003851`

Promote edilen scratch DB swap sonrası artık yoktur.

Önceki live DB drop edilmedi. Şu backup DB adına rename edildi:

`logisticsearch_taxonomy_pre_stage2h_tr_patch_20260425_004329`

Korunmuş 007_R2B backup DB'ye dokunulmadı:

`logisticsearch_taxonomy_pre_007_r2b_20260424_220836`

pi51c pre-swap live dump:

`/srv/crawler/logisticsearch/backups/taxonomy_stage2h_pi51c_live_swap_2026-04-25_00-43-29/logisticsearch_taxonomy_before_stage2h_live_swap_20260425_004329.dump`

Pre-swap live dump SHA256:

`f4728b356f051e900d0782df8f177ac44bc344442c9acb0274041550acee9370`

### Stage2H final deterministic live equality

Post-swap final seal sonrası Ubuntu Desktop canonical DB ve pi51c live DB tüm deterministic yüzeylerde eşleşti:

| Yüzey | SHA256 |
|---|---|
| Primary title/keyword rows | `d1ba632787bf6b280292e3a96a433717c1e9d8cf24c199f21cbcb244b8bf2c27` |
| Search document rows | `41bbb6dfc5f7e307f2362bbb293751cce7229bd2361c3c4b00547cb5dbb3ccbe` |
| Guard metrics | `c3997a5a4a9b92606569f48a3d1fafc9e075dd3c66f7b455080cea5699f8d5be` |
| Patch target rows | `30a68ca35e96f3d14e16057591f337cbfdf1182246bd4e3aedeb1bcb244a2100` |

### Final live guard metrics

Final pi51c live guard metrics geçti:

- Supported languages: `25`
- Active supported languages: `25`
- Canonical language order: `ar,bg,cs,de,el,en,es,fr,hu,it,ja,ko,nl,pt,ro,ru,tr,zh,hi,bn,ur,uk,id,vi,he`
- Primary search languages: `en,tr`
- Taxonomy nodes: `335`
- Taxonomy translations: `8375`
- Taxonomy keywords: `8375`
- Primary keyword rows: `8375`
- Search documents: `8375`
- Closure rows: `995`
- Duplicate primary keyword groups: `0`
- Target-related duplicate groups: `0`
- Blank title/keyword count: `0`
- Orphan translation node count: `0`
- Orphan keyword node count: `0`
- Orphan translation language count: `0`
- Orphan keyword language count: `0`
- Marker count: `0`
- Required function floor pass: `TRUE`

### Backup cleanup policy

Mevcut politika: **DELETE_NONE_NOW**.

Bu stage kapsamında hiçbir pi51c taxonomy backup DB silinmeyecek.

Korunacak backup DB'ler:

1. `logisticsearch_taxonomy_pre_stage2h_tr_patch_20260425_004329`
2. `logisticsearch_taxonomy_pre_007_r2b_20260424_220836`

Gerekçe:

- Stage2H backup, Turkish patch live swap için en yakın rollback noktasıdır.
- 007_R2B backup daha eski korunmuş baseline'dır ve sessizce kaldırılmayacaktır.
- Backup cleanup daha sonraki stability evidence sonrası ayrı ve açık bir işlem olmalıdır.

### Sonraki adım

Tam `8375` title/keyword human-logic review hattına dönülecek.

English baseline review mühürlendi.

Turkish baseline review patch edildi, sync edildi, live swap edildi ve mühürlendi.

Sıradaki dil önceliği: **German baseline review**.
