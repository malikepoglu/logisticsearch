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
