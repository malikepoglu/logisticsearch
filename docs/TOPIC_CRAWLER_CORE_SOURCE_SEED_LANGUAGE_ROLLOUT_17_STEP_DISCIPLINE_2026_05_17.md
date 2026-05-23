# Source-seed language rollout 17-step discipline / Source-seed dil rollout 17 adım disiplini

Gate / Kapı: `R367A_SOURCE_SEED_17_STEP_LANGUAGE_ROLLOUT_DISCIPLINE_DOC_COMMIT_PUSH_GATE`
Date / Tarih: `2026-05-17`
Scope / Kapsam: `crawler_core source-seed language rollout discipline`
Status / Durum: `CANONICAL_STANDARD`

## Purpose / Amaç

This document permanently defines the source-seed language rollout workflow for LogisticSearch crawler_core startpoint catalogs.

Bu doküman LogisticSearch crawler_core startpoint katalogları için dil bazlı source-seed rollout sürecini kalıcı standart olarak tanımlar.

## Non-negotiable user review request / Pazarlık dışı kullanıcı kontrol isteği

Every language must include the following user-review request exactly before decision-doc or catalog creation:

(xxx dili icin directory sitelerini önceleyen, standartlarimiza, formatimiza uygun, cok kaliteli olarak belirledigin tiklanabilir, numaralandirilmis web-linkli, kalite durumunu da gösteren sources ve seeds listeni yayinla, kontrol edeyim.)

This sentence is mandatory. It means:

- The candidate list must prioritize directory sites.
- The candidate list must follow our standards and format.
- The candidate list must be high-quality.
- Links must be clickable web links.
- Sources and seeds must be numbered.
- Quality status must be visible.
- User review is required before writing decision/catalog artifacts.

## Global hard rules / Genel sert kurallar

1. One language at a time.
2. No next language before the current language is fully sealed.
3. No pi51c sync before GitHub/local post-push seal passes.
4. No pi51c live copy before pi51c repo sync is verified.
5. No DB insert, no frontier activation, no crawler start, no systemd mutation, no URL fetch, and no live probe unless a gate explicitly allows it.
6. Candidate source-seed catalog is not live crawler activation.
7. Runtime activation policy must stay `pi51c_live_probe_required_before_db_or_frontier_insert`.
8. Safety state must stay `candidate_only_not_live`.
9. All crawler_core source-seed data must remain PostgreSQL + JSON/JSONB aligned.
10. Dirty scope must be explicit at every mutation gate.
11. Commit scope must be exact and audited.
12. GitHub raw exact-head checks are required before pi51c sync.
13. pi51c service must remain disabled/inactive unless a dedicated service gate says otherwise.
14. Crawler process count must remain `0` during source-seed rollout.
15. Secrets, DSN, token, and passwords must never be printed.
16. If a gate false-fails, stop and classify instead of forcing the next step.
17. If an audit script counts Markdown links, it must distinguish line count from occurrence count.

## Standard 17-step language rollout / Standart 17 adımlı dil rollout akışı

### Step 1/17 — Baseline audit / Başlangıç denetimi

Goal: confirm clean Ubuntu/GitHub/pi51c baseline before starting a new language.

Checks:

- Local HEAD equals `origin/main`.
- GitHub remote main equals local HEAD.
- Worktree is clean, except explicitly expected pre-existing untracked files.
- Staged area is empty.
- Canonical rule document SHA matches.
- Current previous language final seal remains intact.
- Target language decision doc does not exist unless this is a repair flow.
- Target language catalog JSON does not exist unless this is a repair flow.
- README does not already index the target language.
- No mutation.

Output:

- `LANGUAGE_STEP=1/17_COMPLETE`
- Next gate: candidate list / user review.

### Step 2/17 — Candidate list for user review / Kullanıcı kontrolü için aday liste

Goal: publish the candidate source/seed list in chat before writing files.

Mandatory request text:

(xxx dili icin directory sitelerini önceleyen, standartlarimiza, formatimiza uygun, cok kaliteli olarak belirledigin tiklanabilir, numaralandirilmis web-linkli, kalite durumunu da gösteren sources ve seeds listeni yayinla, kontrol edeyim.)

Candidate list requirements:

- Numbered list.
- Clickable web links.
- Quality status for every source.
- Directory sites prioritized.
- Official company/service pages included only as controlled candidates.
- Discovery-only surfaces clearly marked.
- No repo write.
- No catalog JSON.
- No README change.
- No pi51c operation.

Output:

- User approval or revision request.

### Step 3/17 — Decision doc local-only / Karar dokümanı local-only

Goal: create only the language decision document.

Allowed mutation:

- One untracked decision doc under `docs/`.

Forbidden:

- No catalog JSON.
- No README update.
- No Git add/commit/push.
- No pi51c.
- No DB/crawler/systemd/URL fetch/live probe.

Required content:

- Gate name.
- Language step.
- Target catalog path.
- Target decision doc path.
- Safety contract.
- Candidate metrics.
- Source family decisions.
- Seed surface candidates.
- Runtime policy.
- Safety state.

Output:

- Dirty scope exactly one untracked decision doc.

### Step 4/17 — Decision doc audit / Karar dokümanı denetimi

Goal: read-only audit of decision doc.

Checks:

- Decision doc SHA, line count, byte count.
- Required needles.
- Source family count.
- Unique source code count.
- Seed URL count.
- Unique URL count.
- Duplicate URL classification.
- Non-HTTPS count.
- Empty URL count.
- Runtime policy.
- Safety state.
- README unchanged.
- Catalog JSON absent.

Important Markdown audit rule:

- If the same source code appears once in source-family table and once in seed-surface table, total text occurrence may be twice the unique source count.
- Do not fail merely because Markdown/table content repeats a source code in separate valid sections.
- For unique source-code checks, deduplicate by section or use section-specific parsing.

Output:

- `LANGUAGE_STEP=4/17_COMPLETE`

### Step 5/17 — Decision doc commit/push / Karar dokümanı commit-push

Goal: commit and push only the decision doc.

Commit scope:

- Exactly one decision doc.

Forbidden:

- No catalog JSON.
- No README.
- No pi51c.
- No DB/crawler/systemd/URL fetch/live probe.

Output:

- New GitHub HEAD.

### Step 6/17 — Decision doc post-push seal / Karar dokümanı push sonrası mühür

Goal: read-only GitHub raw exact-head seal.

Checks:

- Local HEAD equals origin/main and remote main.
- Commit scope exact.
- GitHub raw decision doc status 200.
- SHA matches.
- Worktree clean.
- Staged empty.

Output:

- Decision doc sealed.

### Step 7/17 — Catalog JSON local-only / Catalog JSON local-only

Goal: create only the language catalog JSON.

Allowed mutation:

- One untracked catalog JSON under `makpi51crawler/catalog/startpoints/<lang>/`.

Forbidden:

- No README.
- No Git add/commit/push.
- No pi51c.
- No DB/crawler/systemd/URL fetch/live probe.

Required JSON semantics:

- `schema = source_families_v2`
- `language_code = <lang>`
- `candidate_manifest = true`
- `is_live = false`
- all families disabled
- all surfaces disabled
- all seed URLs disabled
- all require live check
- runtime policy `pi51c_live_probe_required_before_db_or_frontier_insert`
- safety state candidate-only/not-live.

### Step 8/17 — Catalog JSON strict audit / Catalog JSON sert denetim

Goal: read-only strict JSON audit.

Checks:

- JSON parse.
- Schema.
- Language code.
- Candidate manifest true.
- Is live false.
- Source family count.
- Seed surface count.
- Seed URL count.
- Unique URL count.
- Non-HTTPS count.
- Empty URL count.
- Disabled flags.
- Needs-live-check flags.
- Runtime policy.
- Safety state.
- No README change.

### Step 9/17 — Catalog JSON commit/push / Catalog JSON commit-push

Goal: commit and push only the catalog JSON, unless the approved flow intentionally commits doc+catalog together.

Default commit scope:

- Exactly one catalog JSON.

Forbidden:

- No README.
- No pi51c.
- No DB/crawler/systemd/URL fetch/live probe.

### Step 10/17 — Catalog post-push seal / Catalog push sonrası mühür

Goal: GitHub raw exact-head catalog seal.

Checks:

- Local/GitHub alignment.
- Commit scope.
- Raw catalog status 200.
- Raw catalog SHA.
- JSON mini-invariants.

### Step 11/17 — README/docs canonical index audit / README-docs canonical index denetimi

Goal: inspect README/docs canonical source-seed index before patching.

Checks:

- Current sealed catalog table.
- Decision record list.
- Next-language rollout block.
- Target language missing or stale status.
- Ad-hoc block absence.
- Stale schema doc absence.
- GitHub raw exact-head status.

No mutation.

### Step 12/17 — README canonical index local-only patch / README canonical index local-only patch

Goal: patch only README.

Allowed mutation:

- `docs/README.md`

Required README updates:

- Current sealed startpoint catalogs table row.
- Source-seed policy and decision record entry.
- Next-language rollout decision block.
- Rolled language list.
- Safety line: no DB/frontier/live activation.
- No stale schema doc reference.

Forbidden:

- No decision doc rewrite.
- No catalog rewrite.
- No Git add/commit/push.
- No pi51c.

### Step 13/17 — README canonical index audit / README canonical index denetim

Goal: read-only audit of README patch.

Checks:

- README SHA/line/byte.
- Target language table row count.
- Decision doc link occurrence count.
- Catalog link occurrence count.
- Rolled list.
- Runtime policy.
- Safety line.
- No ad-hoc block.
- No stale previous language block.
- Non-README files unchanged.

Important Markdown link rule:

- A Markdown link may contain the same filename twice: link text and link target.
- Use occurrence-aware counting when needed.
- Use section-aware counting for table/record checks.

### Step 14/17 — README canonical index commit/push / README canonical index commit-push

Goal: commit and push only README.

Commit scope:

- Exactly `docs/README.md`.

Forbidden:

- No decision doc rewrite.
- No catalog rewrite.
- No pi51c.

### Step 15/17 — README/docs/GitHub post-push seal / README-docs GitHub push sonrası mühür

Goal: exact-head GitHub raw seal.

Checks:

- Local/GitHub alignment.
- Commit scope exact.
- README raw status 200.
- Decision doc raw status 200.
- Catalog raw status 200.
- Stale schema doc raw status 404.
- README canonical sections pass.

### Step 16/17 — pi51c sync decision / pi51c senkron karar kapısı

Goal: decide if pi51c repo/live sync is needed.

Read-only checks:

- pi51c repo HEAD.
- pi51c repo origin/main.
- pi51c repo tree.
- pi51c repo tracked count.
- pi51c repo status clean.
- pi51c live catalog exists.
- pi51c live catalog SHA/mode/bytes.
- Service disabled/inactive.
- Crawler process count 0.

Possible results:

- `PASS_REPO_SYNC_REQUIRED`
- `PASS_LIVE_COPY_REQUIRED`
- `PASS_ALREADY_FULLY_SYNCED`
- `FAIL_BLOCKED`

### Step 17/17 — pi51c sync/copy/final 3-system seal / pi51c senkron ve final 3 sistem mühür

Goal: complete pi51c sync and final seal.

Sub-steps may be used:

- `17.1` repo sync decision.
- `17.2` repo sync gate.
- `17.3` live catalog copy gate, only if needed.
- `17.4` final 3-system post-sync seal.

Final checks:

- Ubuntu Desktop HEAD equals GitHub origin/main.
- GitHub remote main equals local HEAD.
- pi51c `/logisticsearch/repo` HEAD equals canonical HEAD.
- pi51c repo origin/main equals canonical HEAD.
- pi51c repo clean.
- pi51c live catalog SHA/mode/bytes match.
- Service disabled/inactive.
- Crawler process count 0.
- No DB/crawler/systemd mutation occurred in final seal.

Output:

- `<LANGUAGE>_SOURCE_SEED_3SYSTEM_SEAL=PASS`
- `<LANGUAGE>_DONE=TRUE`
- `LANGUAGE_STEP=17/17_COMPLETE`

## Repair/STOP_AND_CLASSIFY gates / Onarım ve sınıflandırma kapıları

Repair gates do not change the 17-step count.

Use a repair gate when:

- A script false-fails.
- Markdown line count is confused with occurrence count.
- Regex spans the wrong section.
- README has ad-hoc blocks or stale next-language blocks.
- Dirty scope is valid but audit logic is wrong.
- GitHub raw surface contradicts local assumptions.

Repair gates must:

- State whether mutation is allowed.
- Preserve existing valid artifacts.
- Avoid broad `git add`.
- Avoid accidental catalog/README/doc rewrites.
- End with a deterministic next gate.

## Current example / Güncel örnek

Bulgarian (`bg`) is currently in decision-doc audit phase after local-only decision doc creation.

Known audit lesson:

- Source codes may appear once in source-family table and once in seed-surface table.
- Unique source code count can be correct even when raw occurrence count is double.
- Audits must parse sections separately.


<!-- SOURCE_SEED_METADATA_MODEL_17_PLUS_DISCIPLINE_EXTENSION_BEGIN -->

## 17+ source-seed rollout discipline extension: metadata / locale / country gates

The language rollout process is now extended from a strict 17-step workflow to a 17+ workflow when language, locale, country coverage, or live reachability risk is present.

The following gates are mandatory before treating any rolled catalog as final-sealed:

### Metadata model gates

1. Candidate list user review
   - User-visible candidate source/seed list must be reviewed before JSON mutation.
2. Decision doc gate
   - Decision doc must explain source families, country coverage, language/locale assumptions, and exclusion rationale.
3. Catalog JSON gate
   - Candidate JSON must remain `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`.
4. Structural audit gate
   - JSON parse, schema, counts, URL uniqueness, HTTPS, empty URL, quality fields, and runtime activation policy must pass.
5. Language / locale / country metadata audit gate
   - Every `seed_urls[]` entry must include:
     - `target_language_code`
     - `content_language_code`
     - `url_locale_code`
     - `source_country_codes`
     - `covered_country_codes`
     - `language_fit`
     - `coverage_fit`
     - `locale_review_status`
6. Public live reachability audit gate
   - Must be separate from schema repair.
   - Must not activate DB/frontier/crawler by itself.
   - Broken or blocked URLs must be classified, not silently accepted.
7. Locale / native / fallback classification audit gate
   - Native URLs, multilingual URLs, English fallback URLs, foreign-language country-relevant URLs, and unknown URLs must be separated.
8. Commit/push gate
   - Dirty scope and staged scope must be exact.
   - Commit must be narrow and reversible.
9. Post-push exact-head raw GitHub seal
   - Raw GitHub files at exact pushed HEAD must match local SHA evidence.
10. pi51c sync decision gate
   - Deferred until all 25 language catalogs are completed and sealed on Ubuntu Desktop + GitHub.
   - No pi51c `/logisticsearch/repo` sync and no `/logisticsearch/makpi51crawler` live copy before that global gate.

### Required audit result names

For each language, use explicit gates like:

- `<LANG>_METADATA_MODEL_GAP_AUDIT_READONLY`
- `<LANG>_METADATA_MODEL_LOCAL_ONLY`
- `<LANG>_METADATA_MODEL_AUDIT_READONLY`
- `<LANG>_METADATA_MODEL_COMMIT_PUSH_GATE`
- `<LANG>_METADATA_MODEL_POST_PUSH_SEAL_READONLY`
- `<LANG>_LIVE_AND_LOCALE_REPAIR_PLAN_READONLY`
- `<LANG>_FINAL_JSON_TRUTH_SEAL_READONLY`

### Non-negotiable safety line

Metadata repair does not imply runtime activation.

No DB insert, no frontier activation, no crawler start/stop, no systemd mutation, no pi51c sync, and no live copy are allowed in metadata model gates.

<!-- SOURCE_SEED_METADATA_MODEL_17_PLUS_DISCIPLINE_EXTENSION_END -->

<!-- SOURCE_SEED_DOCS_STANDARDS_CHECKPOINT_BEGIN -->

## Mandatory docs / rules / standards checkpoint

After each language reaches final JSON truth seal, run a documentation checkpoint before moving to the next rolled-catalog audit.

Required order:

1. Final JSON truth seal for the language.
2. Documentation/rules/standards/format gap audit.
3. Local-only documentation update if README, canonical rules, or discipline docs are missing current standards.
4. Read-only documentation audit.
5. Commit/push documentation update.
6. Post-push exact-head documentation seal.
7. Only then continue to broad rolled-catalog metadata audits or the next language.

This checkpoint must verify that:

- README summarizes the current JSON format and source-seed safety state.
- Canonical rules define required seed-level metadata fields.
- Canonical rules define reachability review encoding such as `broken_or_blocked`.
- 17+ discipline includes docs/rules/standards checkpoint before cross-language rollout work.
- All source-seed catalogs remain candidate-only unless a separate explicit activation gate exists.
- 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

This checkpoint never permits DB insert, frontier activation, crawler start, systemd mutation, pi51c sync, or live copy.

<!-- SOURCE_SEED_DOCS_STANDARDS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_EN_DOCS_CHECKPOINT_BEGIN -->

## After English final JSON truth seal

After English final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_EN`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_EN`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-English docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_EN_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_TR_DOCS_CHECKPOINT_BEGIN -->

## After Turkish final JSON truth seal

After Turkish final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_TR`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_TR`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Turkish docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_TR_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_DE_DOCS_CHECKPOINT_BEGIN -->

## After German final JSON truth seal

After German final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_DE`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_DE`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-German docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_DE_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_AR_DOCS_CHECKPOINT_BEGIN -->

## After Arabic final JSON truth seal

After Arabic final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_AR`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_AR`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Arabic docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_AR_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_ZH_DOCS_CHECKPOINT_BEGIN -->

## After Chinese final JSON truth seal

After Chinese final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_ZH`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_ZH`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Chinese docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_ZH_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_FR_DOCS_CHECKPOINT_BEGIN -->

## After French final JSON truth seal

After French final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_FR`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_FR`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-French docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_FR_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_ES_DOCS_CHECKPOINT_BEGIN -->

## After Spanish final JSON truth seal

After Spanish final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_ES`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_ES`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Spanish docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_ES_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_IT_DOCS_CHECKPOINT_BEGIN -->

## After Italian final JSON truth seal

After Italian final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_IT`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_IT`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Italian docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_IT_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_PT_DOCS_CHECKPOINT_BEGIN -->

## After Portuguese final JSON truth seal

After Portuguese final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_PT`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_PT`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Portuguese docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_PT_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_NL_DOCS_CHECKPOINT_BEGIN -->

## After Dutch final JSON truth seal

After Dutch final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_NL`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_NL`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Dutch docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_NL_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_RU_DOCS_CHECKPOINT_BEGIN -->

## After Russian final JSON truth seal

After Russian final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_RU`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_RU`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Russian docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_RU_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_AFTER_UK_DOCS_CHECKPOINT_BEGIN -->

## After Ukrainian final JSON truth seal

After Ukrainian final JSON truth seal, the mandatory documentation checkpoint is:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_UK`

If that audit reports documentation gaps, run:

`SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_UK`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before running the all-rolled metadata gap audit.

No all-rolled metadata audit or next-language mutation should begin until the after-Ukrainian docs/rules/standards/format checkpoint is sealed.

This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

<!-- SOURCE_SEED_AFTER_UK_DOCS_CHECKPOINT_END -->

<!-- SOURCE_SEED_CS_DISCIPLINE_STANDARD_PATCH_2026_05_19 -->

## Czech (`cs`) rollout discipline record — 2026-05-19

Czech (`cs`) follows the 17-step language rollout discipline.

- CS-01 — baseline and remaining-language discovery read-only
- CS-02 — decision document and candidate catalog local-only
- CS-03 — local-only audit read-only
- CS-04 — diff and dirty-scope audit read-only
- CS-05 — commit/push gate
- CS-06 — post-push seal read-only
- CS-07 — docs standards format gap audit read-only
- CS-08 — docs standards format patch local-only
- CS-09 — docs standards format audit read-only
- CS-10 — docs standards commit/push gate
- CS-11 — docs standards post-push seal read-only
- CS-12 — rolled metadata gap audit read-only after Czech
- CS-13 — pi51c sync preflight read-only
- CS-14 — pi51c repo sync gate
- CS-15 — pi51c live sync gate
- CS-16 — 4-layer equality seal read-only
- CS-17 — next language decision read-only

Czech (`cs`) approved candidate size:

- 45 source families
- 90 seed surfaces
- 90 seed URLs

The Czech (`cs`) catalog remains candidate-only: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`, `safety_state=candidate_only_not_live`.

## After Greek final JSON truth seal

After Greek final JSON truth seal, the mandatory documentation checkpoint is: `SOURCE_SEED_DOCS_STANDARDS_FORMAT_GAP_AUDIT_READONLY_AFTER_EL`

If that audit reports documentation gaps, run: `SOURCE_SEED_DOCS_STANDARDS_FORMAT_LOCAL_ONLY_AFTER_EL`

Then run a read-only audit, commit/push gate, and exact-head post-push seal before continuing to the next rolled-language repair.

No next-language mutation should begin until the after-Greek docs/rules/standards/format checkpoint is sealed. This preserves the rule: 25 dil tamamlanmadan pi51c repo/live sync yapılmaz.

## Greek (`el`) rollout discipline record — 2026-05-19

Greek (`el`) follows the 17-step language rollout discipline.

- EL-01 — baseline and remaining-language discovery read-only
- EL-02 — source/seed candidate review list
- EL-03 — decision document and candidate catalog local-only
- EL-04 — local-only audit read-only
- EL-05 — diff and dirty-scope audit read-only
- EL-06 — commit/push gate
- EL-07 — post-push seal read-only
- EL-08 — docs standards format patch local-only
- EL-09 — docs standards format audit read-only
- EL-10 — docs standards commit/push gate
- EL-11 — docs standards post-push seal read-only
- EL-12 — rolled metadata gap audit read-only after Greek
- EL-13 — pi51c sync preflight read-only
- EL-14 — pi51c repo sync gate
- EL-15 — pi51c live sync gate
- EL-16 — 4-layer equality seal read-only
- EL-17 — next language decision read-only

Greek (`el`) approved candidate size:

- 45 source families
- 90 seed surfaces
- 90 seed URLs

The Greek (`el`) catalog remains candidate-only: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`, `safety_state=candidate_only_not_live`.

Greek (`el`) source-seed artifacts:

- `docs/TOPIC_CRAWLER_CORE_GREEK_SOURCE_SEED_URLS_DECISION_2026_05_19.md`
- `makpi51crawler/catalog/startpoints/el/greek_source_families_v2.json`

## After Hungarian final JSON truth seal

Hungarian (`hu`) rollout discipline record:

- Final JSON truth head: `3c8700358f0b71e16ed55fde65b15e35ca20d19c`
- Commit subject: `feat(source-seed): add Hungarian startpoint catalog`
- Decision document: `docs/TOPIC_CRAWLER_CORE_HUNGARIAN_SOURCE_SEED_URLS_DECISION_2026_05_19.md`
- Catalog: `makpi51crawler/catalog/startpoints/hu/hungarian_source_families_v2.json`
- Decision document SHA256: `5df6d40afaa10d61ace2d3979c3b99b1e9652db7eb262bb95ffa3fee0b2e839c`
- Catalog SHA256: `2c2bc39e02679950410299288b08966222de494533990749deeb761125f3a2a1`
- Source families: 45 source families
- Seed surfaces: 90 seed surfaces
- Seed URLs: 90 seed URLs
- Unique seed URLs: 90 unique seed URLs
- Duplicate seed URLs: 0
- Empty seed URLs: 0
- Non-HTTPS seed URLs: 0
- Safety state: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`, `safety_state=candidate_only_not_live`
- Rolled languages on GitHub after Hungarian: `en,tr,de,ar,zh,fr,es,it,pt,nl,ru,uk,bg,cs,el,hu`
- Remaining languages after Hungarian: `ro,ja,ko,id,vi,hi,bn,ur,he`
- pi51c sync status: not done for Hungarian in this gate.
- Next language decision gate should select Romanian (`ro`) unless a later read-only gate changes the rollout order.

## After Romanian final JSON truth seal

Romanian (`ro`) rollout discipline record:

- Final JSON truth sealed head: `c86a2e72c235c6752df45b1d3a7993394f898c31`
- Decision doc: `docs/TOPIC_CRAWLER_CORE_ROMANIAN_SOURCE_SEED_URLS_DECISION_2026_05_20.md`
- Catalog path: `makpi51crawler/catalog/startpoints/ro/romanian_source_families_v2.json`
- Catalog SHA256: `aec39f2cde047a65d970aff68c60317ce9b549a373a507fce6b20bdae5e33ca4`
- Taxonomy SHA256: `3e38cbe8d12579fcb68d84d049f65c7771194293b100c0d6d37345775e4f32bb`
- Counts: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique URLs.
- Candidate-only safety: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`, `safety_state=candidate_only_not_live`.
- Rolled languages after Romanian: `en,tr,de,ar,zh,fr,es,it,pt,nl,ru,uk,bg,cs,el,hu,ro`.
- Remaining languages after Romanian: `ja,ko,id,vi,hi,bn,ur,he`.
- Next language after Romanian: Japanese (`ja`).
- pi51c sync after Romanian: not done yet at this docs-standard local-only gate; final completion sync must make Ubuntu Desktop repo = GitHub main = pi51c `/logisticsearch/repo` = pi51c `/logisticsearch/makpi51crawler` runtime subtree.

### After Japanese final JSON truth seal

- Gate passed: `JA-08R2_JAPANESE_FINAL_JSON_TRUTH_SEAL_READONLY_CORRECTED_HEAD`
- Head: `b056ffaa185889815af09a89b98647dccbcb500a`
- Parent: `7911ca2028d73c10daec6a2e3fb06efa2b7cff6e`
- Tree: `f52fdccb546aaa4666e876a966a51c82ddfb90bb`
- Japanese decision doc SHA256: `e19590eabef76ab4f0b7ef253139bda8838303b0df8c116d270b44989d97d77d`
- Japanese catalog SHA256: `ef766100e03d43c3d33d042753154ba0b18c702d718b91b21dd2a96888243cf9`
- Japanese taxonomy SHA256: `d96868184073187c3283342a799f7c1b159c3e9b6703d6e76baa83bc2b324911`
- Japanese catalog truth: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique URLs
- Japanese quality counts: A_PLUS=4, A=6, A_MINUS=8, B_PLUS=21, B=6
- Japanese decision counts: ACCEPT=7, ACCEPT_REVIEW=38
- Rolled languages on GitHub after Japanese: 18
- Remaining rollout order after Japanese: `ko,id,vi,hi,bn,ur,he`
- Next language: Korean (`ko`)
- pi51c sync after Japanese: not done at this checkpoint
- Final completion sync policy remains: Ubuntu Desktop repo = GitHub main = pi51c `/logisticsearch/repo` = pi51c `/logisticsearch/makpi51crawler` runtime subtree.

### After Korean final JSON truth seal

- Gate: `KO-08_KOREAN_FINAL_JSON_TRUTH_SEAL_READONLY`
- Result: PASS.
- Head: `61b879102c2acb189866f7aec06c3a1e7f3bd5e2`
- Korean decision doc SHA256: `5d915489ae9e3b98edd3c7bb49ec4ad9dc9345640330ab35b3acbbb24ded8dfa`
- Korean catalog SHA256: `fb4d9aa0a2e87b5b0fa7364bfc5408093f165abdfe6a5a49ce974341f353bca7`
- Korean taxonomy SHA256: `ec3175fcef4ec450a8c812c20ae7e5b8fa503bbfa14eea0055a5d8ec18aeaca3`
- Korean catalog truth: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique seed URLs.
- Candidate-only safety remains active: `candidate_manifest=true`, `is_live=false`, `enabled=false`, `needs_live_check=true`, `safety_state=candidate_only_not_live`.
- Duplicate family/surface/seed/url count: 0; empty URL count: 0; non-HTTPS URL count: 0; metadata missing/bad count: 0.
- Rolled languages on GitHub after Korean: 19.
- Remaining rollout order after Korean: `id,vi,hi,bn,ur,he`.
- Next language after Korean: Indonesian (`id`).
- Korean pi51c sync status after KO-08: not done.
- Final completion policy remains: Ubuntu Desktop = GitHub = pi51c `/logisticsearch/repo` = pi51c `/logisticsearch/makpi51crawler` tracked subtree.

### After Indonesian final JSON truth seal

- Indonesian (`id`) final JSON truth sealed at head `0e248abcce0a019c8ee23363787bc3e41a618c6e`.
- Indonesian decision doc SHA256: `6e87a0d6d3cb135108042c7ca14e792e261dc2e22c1fe79ad92880c2ee39af45`.
- Indonesian catalog SHA256: `adc44a4be281c5c8021295a024b083acae4852c6c235aee5ce50ccfaa610d80b`.
- Indonesian taxonomy SHA256: `658ab2385399b1109d244b62fd5599161763028d813cb44a70a76b4466ee0d88`.
- Indonesian counts: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique seed URLs.
- Indonesian quality distribution: `A=21`, `A_MINUS=4`, `A_PLUS=6`, `B=3`, `B_MINUS=2`, `B_PLUS=9`.
- Indonesian decision distribution: `ACCEPT=10`, `ACCEPT_REVIEW=33`, `HOLD_REVIEW=2`.
- Remaining rollout order after Indonesian: `vi,hi,bn,ur,he`.
- Next language after Indonesian four-layer equality: Vietnamese (`vi`).
- Indonesian pi51c sync status after ID-08: not done.
- Final completion policy remains: Ubuntu Desktop = GitHub = pi51c `/logisticsearch/repo` = pi51c `/logisticsearch/makpi51crawler` tracked subtree.

### After Vietnamese final JSON truth seal

- Gate sealed: `VI-08_VIETNAMESE_FINAL_JSON_TRUTH_SEAL_READONLY`
- Final JSON truth head: `999d8ea78d7113945f30c289b8fd79ceab8ee4a3`
- Vietnamese catalog: `makpi51crawler/catalog/startpoints/vi/vietnamese_source_families_v2.json`
- Vietnamese catalog SHA256: `2df88ebf0947f173f0ea8931d2b0a5fdfdf6d36e75843cad38abc38b16140280`
- Vietnamese taxonomy SHA256: `04de0caa3bcce317def635c3838e6091d92c278d384d036e7bc7fa5f51db2819`
- Vietnamese decision doc SHA256: `1657e27715188eb8760413a7e072aee0275b6d820b7356ecd96a93e02387e65a`
- Final counts: 45 source families / 90 seed surfaces / 90 seed URLs / 90 unique URLs.
- Quality distribution: `{'A': 11, 'A_MINUS': 9, 'A_PLUS': 6, 'B': 7, 'B_PLUS': 12}`
- Decision distribution: `{'ACCEPT': 15, 'ACCEPT_REVIEW': 29, 'HOLD_REVIEW': 1}`
- Rolled languages after Vietnamese: 21.
- Remaining languages after Vietnamese: `hi,bn,ur,he`.
- Next language: Hindi (`hi`).
- pi51c sync after Vietnamese is not done until the dedicated repo/live sync gate.
- Final completion sync policy remains: Ubuntu Desktop = GitHub = pi51c `/logisticsearch/repo` = pi51c `/logisticsearch/makpi51crawler` tracked subtree.

## After Hindi (`hi`) docs checkpoint — HI-08 sealed

- Hindi final JSON truth gate: `HI-08_HINDI_FINAL_JSON_TRUTH_SEAL_READONLY`.
- Canonical GitHub HEAD after Hindi catalog commit: `7a70e6d8e668e4c5ff0b3222610f6d64ec5a405b`.
- Hindi decision doc SHA256: `2f2fe3093a73c8826d8f7e594cf2d6c516748c84a493671f5b614c6e32d0fe64`.
- Hindi catalog SHA256: `73b7e54da70743e84e71c94bc0155b4fa8303ad1199142f55a63a27c00c652ff`.
- Hindi taxonomy SHA256: `0f4de3dc0f11a61b14df9cffad16fe89345f8c50b444cbc4262f60e73f96227f`.
- Hindi source-seed counts: 45 source families / 90 seed surfaces / 90 seed URLs / 90 unique URLs.
- Safety state remains candidate-only/not-live: no DB insert, no frontier activation, no crawler start, no public URL probe.
- Rolled languages on GitHub after Hindi: 22.
- Remaining languages after Hindi: `bn,ur,he`.
- Next language: Bengali (`bn`).
- pi51c repo/live sync after Hindi is intentionally not done until docs standard patch is committed, pushed, and sealed.
- Final completion policy remains: Ubuntu Desktop equals GitHub equals pi51c `/logisticsearch/repo` equals pi51c `/logisticsearch/makpi51crawler`.

### After Bengali (`bn`) docs checkpoint

- Base source-seed commit: `386003f96ae1eca4bf000d1105507dc1943cf840` (`feat(source-seed): add Bengali startpoint catalog`).
- Bengali final JSON truth sealed: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique URLs.
- Bengali doc SHA: `f6b6126b0e72d99b692d9f5c44ccc6adeccf2448614ac2ae7a1439e5a213260f`.
- Bengali catalog SHA: `0f50d0193656e612564fcb9d501998cea72470fad49a2dd53ddfc73635d1ed94`.
- Bengali taxonomy SHA: `4167f8d5daff48d646939bbbddea1e6735b3f38bfd7c12e8d525ea9e5a15bdd5`.
- Docs standard patch required after BN-08: true; this local-only patch records it.
- Remaining languages after Bengali: `ur,he`.
- Next language: Urdu (`ur`).
- pi51c sync after Bengali: false until docs standard post-push seal and explicit sync gate.
- Safety: candidate-only/not-live; no DB/frontier/crawler/systemd/public URL probe.
- Final completion sync policy remains Ubuntu Desktop = GitHub = pi51c repo = pi51c makpi51crawler.
### After Urdu (`ur`) docs checkpoint
- Base source-seed commit: `d1c39607a075cdbf8f00778e39995b4f2f0cf400` (`feat(source-seed): add Urdu startpoint catalog`).
- Urdu final JSON truth sealed: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique URLs.
- Urdu doc SHA: `760ff04b696b23cc490733cf643ef25b19147f2041bc20d8f55fdd3da2b93fa0`.
- Urdu catalog SHA: `5d8b689677adca054d9221e82cedc015cfbd8de773eb4df7a1cea079b550e7f2`.
- Urdu taxonomy SHA: `b96cec8f9d426d01ba7f74f6f951b4030a5e31795cdf72e14cd368291cf12650`.
- Docs standard patch required after UR-08: true; this local-only patch records it.
- Remaining languages after Urdu: `he`.
- Next language: Hebrew (`he`).
- pi51c sync after Urdu: false until docs standard post-push seal and explicit sync gate.
- Safety: candidate-only/not-live; no DB/frontier/crawler/systemd/public URL probe.
- Final completion sync policy remains Ubuntu Desktop = GitHub = pi51c repo = pi51c makpi51crawler.

## After Hebrew (`he`) docs checkpoint

- Source-seed language rollout state: Hebrew (`he`) final JSON truth is sealed and all 25 language catalogs are now present.
- Canonical HEAD before docs patch: `949de3d8474e007d305371faeeb48f43c4610363`.
- Hebrew decision doc SHA256: `cdb63b18723e94ef67d48f87959d6e96d49151686ea52e73b10ee858c372cada`.
- Hebrew catalog SHA256: `f27339a493ad6b62adb29c3cc068a9403d8666c3c72e3042f3e361131d46074f`.
- Hebrew taxonomy SHA256: `15cfd433e3708c280e284163a06c204e8cf2ab8d041b5f05887a63ed4145b50b`.
- Hebrew counts: 45 source families, 90 seed surfaces, 90 seed URLs, 90 unique HTTPS seed URLs.
- Hebrew quality distribution: `{"A": 10, "A_MINUS": 12, "A_PLUS": 3, "B": 8, "B_PLUS": 12}`.
- Hebrew decision distribution: `{"ACCEPT": 13, "ACCEPT_REVIEW": 24, "HOLD_REVIEW": 8}`.
- Global rollout completion: 25 rolled catalogs / 25 taxonomy languages; remaining languages `NONE`.
- Docs patch scope after Hebrew: README, canonical rules doc, and 17-step discipline doc only.
- Runtime safety: pi51c sync after Hebrew remains false; no DB/frontier/crawler/systemd mutation; no public URL probe.
- Next safe gate: `HE-09_SOURCE_SEED_DOCS_STANDARDS_FORMAT_AUDIT_READONLY_AFTER_HE`.
- Planned next artifact after Hebrew final sync/seals: prepare `global directories` JSON in the same canonical source-seed standard and format.
<!-- GLOBAL_DIR_R2A34_DOCS_INDEX_PATCH_LOCAL_ONLY:DISCIPLINE -->

## GLOBAL_DIR_R2A global directories rollout discipline

The global directories catalog used a controlled R2A gate sequence and must remain governed separately from the 25 language rollout sequence.

Sealed gate summary:

| Gate | Purpose | Result |
| --- | --- | --- |
| R2A20 | Confirm expected 1072 gap after 960+9+3 staged rows | PASS |
| R2A21 | Append correct `EXTRA_RAW_960_PLUS` group 7 and group 8 rows | PASS |
| R2A22 | Rebuild dedup/canonical reports after 1072 rows | PASS |
| R2A23 | Confirm +100 contributed metadata only, no new unique hosts | PASS |
| R2A24 | Build 1072 merge policy pack | PASS |
| R2A25 | Seal 1072 tmp state | PASS |
| R2A26 | JSON builder dry-run, no file write | PASS |
| R2A27 | Create local global JSON | PASS |
| R2A28/R2A28B | Classify corrected audit false-fail for no-www canonical and HTTP duplicate collapse | PASS |
| R2A29 | Corrected local JSON audit | PASS |
| R2A30 | Diff scope audit | PASS |
| R2A31 | Commit and push one-file global JSON | PASS |
| R2A32 | Post-push seal | PASS |

Discipline constraints:

- Do not activate global directories directly into DB/frontier.
- Do not start crawler from this catalog before pi51c live probe gates.
- Do not convert `language_code=global` into a taxonomy language.
- Treat this as the `25 language catalogs + 1 global directories catalog` source-seed layer.
- Maintain raw reference preservation: `1072 raw refs -> 696 canonical source families`.
- Every future added global source batch must rebuild dedup/canonical/merge policy before any JSON rewrite.

Next required documentation gates after R2A32:

- `GLOBAL_DIR_R2A34_DOCS_INDEX_PATCH_LOCAL_ONLY`
- `GLOBAL_DIR_R2A35_DOCS_INDEX_AUDIT_READONLY`
- `GLOBAL_DIR_R2A36_DOCS_INDEX_COMMIT_PUSH_GATE`
- `GLOBAL_DIR_R2A37_DOCS_INDEX_POST_PUSH_SEAL_READONLY`
<!-- GLOBAL_DIR_R2A34B2_DOCS_NEEDLE_FIX_LOCAL_ONLY_ROBUST:DISCIPLINE -->

## Global directories exact index needles / Küresel dizin kesin indeks işaretleri

This corrective note intentionally preserves the exact searchable literals required by the documentation gate.

- Catalog file: `global_directories_source_families_v2.json`
- Catalog title: Global directories
- Catalog identity: `language_code=global`
- Canonical raw-to-family model: `1072 raw refs -> 696 canonical source families`
- Duplicate root-domain groups: `204`
- Merge-excess raw records: `376`
- Safety state: `candidate_only_not_live`
- Runtime activation policy: `pi51c_live_probe_required_before_db_or_frontier_insert`
- Gate family: `GLOBAL_DIR_R2A`

Operational rule: this global catalog is the `+1 global directories` layer beside the 25 language catalogs; it is not a live crawler insertion list.
