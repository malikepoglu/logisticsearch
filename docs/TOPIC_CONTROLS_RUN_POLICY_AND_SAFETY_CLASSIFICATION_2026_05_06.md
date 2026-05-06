# Controls Run Policy and Safety Classification — 2026-05-06

## 1. Purpose

This document is the canonical run-policy and safety-classification contract for the LogisticSearch `python_live_runtime/controls` surface.

This document exists because controls are not equal in risk. Some files are passive package markers. Some are safe read-only probes. Some can mutate crawler control state, hardware behavior, Wi-Fi/netplan state, or repo/live runtime surfaces. Operator commands must therefore be classified before use.

TR: Bu doküman LogisticSearch `python_live_runtime/controls` yüzeyi için canonical çalıştırma politikası ve güvenlik sınıflandırma sözleşmesidir.

TR: Bu dokümanın var olma nedeni, tüm control dosyalarının aynı riskte olmamasıdır. Bazı dosyalar pasif paket işaretleyicisidir. Bazıları güvenli read-only durum sorgusudur. Bazıları crawler control state, donanım fan davranışı, Wi-Fi/netplan durumu veya repo/live runtime yüzeylerini değiştirebilir. Bu yüzden operatör komutları çalıştırılmadan önce sınıflandırılmalıdır.

## 2. Evidence Baseline

R112-7 produced the current read-only classification map.

Evidence baseline:

- Machine path: Ubuntu Desktop -> pi51c read-only SSH
- pi51c host: `makpi51crawler`
- Canonical commit: `4c4827eb0364d4443358522475612f9396a70eed`
- Repo controls root: `/logisticsearch/repo/makpi51crawler/python_live_runtime/controls`
- Live controls root: `/logisticsearch/makpi51crawler/python_live_runtime/controls`
- Repo control file count: 23
- Live control file count: 23
- Python control file count: 23
- Repo/live control manifest exact match: PASS
- AST parse count: 23
- AST parse failures: 0
- AST side-effect call count: 26
- Service active state during audit: inactive
- Service enabled state during audit: disabled
- Real Python crawler process count during audit: 0
- DB mutation during audit: no
- systemd mutation during audit: no
- crawler start during audit: no
- control script execution during audit: no

## 3. Non-Negotiable Operating Rule

Inventory, audit, classification, documentation, and planning steps must not execute control scripts.

Allowed during inventory:

- Read files.
- List files.
- Hash files.
- Count lines.
- Parse Python AST.
- Search text.
- Compare repo/live manifests.
- Check service state without start/stop/restart/enable/disable.
- Count crawler processes without killing or starting anything.

Forbidden during inventory:

- Running `pausewc.py`, `playwc.py`, `poweroffwc.py`, `rebootwc.py`, or `resetwc.py`.
- Running `fan0.py`, `fan1.py`, `fan2.py`, or the fan controller as an operator action.
- Running `wifioff.py` or `wifion.py`.
- Running `sync.py`, `sync_repo.py`, `sync_runtime.py`, or `sync_makpi51crawler.py`.
- Starting, stopping, restarting, enabling, disabling, or daemon-reloading systemd units.
- Starting the crawler.
- Touching PostgreSQL.
- Mutating repo, live runtime, hardware, network, or runtime-control state.

## 4. Safety Classes

### 4.1. A0_PASSIVE_PACKAGE_MARKER

Meaning:

- Passive Python package/navigation marker.
- No operator run target.
- Safe for read-only inventory.
- Should not be treated as an operational command.

Gate:

- Read-only inventory allowed.
- No run gate exists because these files are not intended operator commands.

Files:

- `__init__.py`
- `makpi51_controls/__init__.py`
- `makpi51_controls/fan_control/__init__.py`
- `makpi51_controls/wifi_control/__init__.py`
- `sync_data/__init__.py`
- `webcrawler_controls/__init__.py`

Count:

- 6 files

### 4.2. B1_READ_ONLY_HOST_STATUS_PROBE

Meaning:

- Read-only host status probe.
- Intended only for audit/status observation.
- Must not be generalized into a mutation permission.

Gate:

- Audit/status gate only.
- No DB gate.
- No systemd mutation gate.
- No crawler start gate.

Files:

- `makpi51_controls/fan_control/fan.py`

Known side-effect-shaped AST call:

- `15:subprocess.run`

Important interpretation:

- The AST contains `subprocess.run`, but R112-7 classified this file as a read-only status probe because the intended behavior is host fan/service/manual-mode status reading.

Count:

- 1 file

### 4.3. C2_CRAWLER_DURABLE_CONTROL_STATE_MUTATION_CAPABLE

Meaning:

- Changes durable crawler control intent/state.
- Does not perform OS-level reboot/poweroff.
- Must not be run during inventory.
- Requires explicit crawler-control gate.

Gate:

- Explicit crawler-control gate required.
- Service/crawler state must be checked before use.
- Operator must understand whether the requested state is `pause`, `run`, or stop-preparation.
- DB/systemd/crawler-start boundaries must be explicitly stated before execution.

Files:

- `webcrawler_controls/_runtime_control_common.py`
- `webcrawler_controls/pausewc.py`
- `webcrawler_controls/playwc.py`
- `webcrawler_controls/poweroffwc.py`
- `webcrawler_controls/rebootwc.py`
- `webcrawler_controls/resetwc.py`

Important semantics:

- `pausewc.py` requests durable pause state.
- `playwc.py` requests durable run state.
- `poweroffwc.py` performs only safe internal stop-preparation, not real host poweroff.
- `rebootwc.py` performs only safe internal stop-preparation, not real host reboot.
- `resetwc.py` performs only safe internal stop-preparation, not a full reset body.
- `_runtime_control_common.py` is shared mutation machinery for durable crawler runtime-control state.

Count:

- 6 files

### 4.4. D3_HOST_FAN_HARDWARE_MUTATION_CAPABLE

Meaning:

- Can change or drive Pi51 fan/manual hardware behavior.
- Must not be run during documentation, inventory, crawler-core trace, DB audit, or sync audit.
- Requires explicit host-hardware maintenance gate.

Gate:

- Explicit host-hardware gate required.
- Operator must confirm target host.
- Operator must confirm expected fan mode/result.
- Safety must consider thermal risk.

Files:

- `makpi51_controls/fan_control/fan0.py`
- `makpi51_controls/fan_control/fan1.py`
- `makpi51_controls/fan_control/fan2.py`
- `makpi51_controls/fan_control/pi51c_gpio_fan_controller.py`

Known side-effect AST calls:

- `fan0.py`: `44:MODE_PATH.write_text`, `51:MODE_PATH.write_text`
- `fan1.py`: `44:MODE_PATH.write_text`, `51:MODE_PATH.write_text`
- `fan2.py`: `44:MODE_PATH.write_text`, `51:MODE_PATH.write_text`

Count:

- 4 files

### 4.5. E4_HOST_NETWORK_MUTATION_CAPABLE

Meaning:

- Can change Wi-Fi/netplan behavior.
- Can affect remote access.
- Must never be run casually over SSH unless the network-maintenance gate is explicit and a recovery path exists.

Gate:

- Explicit network-maintenance gate required.
- Operator must confirm physical/alternate access risk.
- Operator must confirm exact target host.
- Operator must confirm rollback path.

Files:

- `makpi51_controls/wifi_control/wifioff.py`
- `makpi51_controls/wifi_control/wifion.py`

Known side-effect AST calls:

- `wifioff.py`: `21:subprocess.run`, `27:subprocess.run`, `37:shutil.move`
- `wifion.py`: `21:subprocess.run`, `27:subprocess.run`, `42:shutil.move`

Count:

- 2 files

### 4.6. F5_REPO_OR_LIVE_SYNC_MUTATION_CAPABLE

Meaning:

- Can mutate repo and/or live runtime surfaces.
- Can run git reset/clean/fetch-style operations and runtime sync/delete/mkdir/unlink operations.
- Must not be run during read-only inventory.

Gate:

- Explicit sync gate required.
- Service/crawler process guard required.
- Repo/live target paths must be printed.
- Retired-surface absence must be preserved.
- DB/systemd/crawler-start boundaries must be explicitly stated.
- Post-sync repo/live manifest equality must be verified.

Files:

- `sync_data/sync.py`
- `sync_data/sync_makpi51crawler.py`
- `sync_data/sync_repo.py`
- `sync_data/sync_runtime.py`

Known side-effect AST calls:

- `sync.py`: `60:os.execv`
- `sync_repo.py`: `48:subprocess.run`, `68:subprocess.run`
- `sync_runtime.py`: `65:subprocess.run`, `80:subprocess.run`, `100:subprocess.run`, `149:target.mkdir`, `159:target.parent.mkdir`, `383:live_root.mkdir`, `135:shutil.rmtree`, `172:shutil.rmtree`, `174:target.unlink`, `138:path.unlink`

Count:

- 4 files

## 5. Current Class Count Seal

Current class counts:

| Class | Count |
|---|---:|
| A0_PASSIVE_PACKAGE_MARKER | 6 |
| B1_READ_ONLY_HOST_STATUS_PROBE | 1 |
| C2_CRAWLER_DURABLE_CONTROL_STATE_MUTATION_CAPABLE | 6 |
| D3_HOST_FAN_HARDWARE_MUTATION_CAPABLE | 4 |
| E4_HOST_NETWORK_MUTATION_CAPABLE | 2 |
| F5_REPO_OR_LIVE_SYNC_MUTATION_CAPABLE | 4 |

Total:

- 23 Python files

## 6. File Classification Seal

| File | Class | Gate |
|---|---|---|
| `__init__.py` | A0_PASSIVE_PACKAGE_MARKER | read-only inventory allowed |
| `makpi51_controls/__init__.py` | A0_PASSIVE_PACKAGE_MARKER | read-only inventory allowed |
| `makpi51_controls/fan_control/__init__.py` | A0_PASSIVE_PACKAGE_MARKER | read-only inventory allowed |
| `makpi51_controls/fan_control/fan.py` | B1_READ_ONLY_HOST_STATUS_PROBE | audit/status gate only |
| `makpi51_controls/fan_control/fan0.py` | D3_HOST_FAN_HARDWARE_MUTATION_CAPABLE | explicit host-hardware gate required |
| `makpi51_controls/fan_control/fan1.py` | D3_HOST_FAN_HARDWARE_MUTATION_CAPABLE | explicit host-hardware gate required |
| `makpi51_controls/fan_control/fan2.py` | D3_HOST_FAN_HARDWARE_MUTATION_CAPABLE | explicit host-hardware gate required |
| `makpi51_controls/fan_control/pi51c_gpio_fan_controller.py` | D3_HOST_FAN_HARDWARE_MUTATION_CAPABLE | explicit host-hardware gate required |
| `makpi51_controls/wifi_control/__init__.py` | A0_PASSIVE_PACKAGE_MARKER | read-only inventory allowed |
| `makpi51_controls/wifi_control/wifioff.py` | E4_HOST_NETWORK_MUTATION_CAPABLE | explicit network-maintenance gate required |
| `makpi51_controls/wifi_control/wifion.py` | E4_HOST_NETWORK_MUTATION_CAPABLE | explicit network-maintenance gate required |
| `sync_data/__init__.py` | A0_PASSIVE_PACKAGE_MARKER | read-only inventory allowed |
| `sync_data/sync.py` | F5_REPO_OR_LIVE_SYNC_MUTATION_CAPABLE | explicit sync gate required |
| `sync_data/sync_makpi51crawler.py` | F5_REPO_OR_LIVE_SYNC_MUTATION_CAPABLE | explicit sync gate required |
| `sync_data/sync_repo.py` | F5_REPO_OR_LIVE_SYNC_MUTATION_CAPABLE | explicit sync gate required |
| `sync_data/sync_runtime.py` | F5_REPO_OR_LIVE_SYNC_MUTATION_CAPABLE | explicit sync gate required |
| `webcrawler_controls/__init__.py` | A0_PASSIVE_PACKAGE_MARKER | read-only inventory allowed |
| `webcrawler_controls/_runtime_control_common.py` | C2_CRAWLER_DURABLE_CONTROL_STATE_MUTATION_CAPABLE | explicit crawler-control gate required |
| `webcrawler_controls/pausewc.py` | C2_CRAWLER_DURABLE_CONTROL_STATE_MUTATION_CAPABLE | explicit crawler-control gate required |
| `webcrawler_controls/playwc.py` | C2_CRAWLER_DURABLE_CONTROL_STATE_MUTATION_CAPABLE | explicit crawler-control gate required |
| `webcrawler_controls/poweroffwc.py` | C2_CRAWLER_DURABLE_CONTROL_STATE_MUTATION_CAPABLE | explicit crawler-control gate required |
| `webcrawler_controls/rebootwc.py` | C2_CRAWLER_DURABLE_CONTROL_STATE_MUTATION_CAPABLE | explicit crawler-control gate required |
| `webcrawler_controls/resetwc.py` | C2_CRAWLER_DURABLE_CONTROL_STATE_MUTATION_CAPABLE | explicit crawler-control gate required |

## 7. Practical Operator Decision Table

| Intended task | Allowed control class | Required gate |
|---|---|---|
| Read package layout | A0 | read-only inventory |
| Read fan status | B1 | audit/status |
| Pause/resume crawler intent | C2 | explicit crawler-control |
| Prepare crawler stop before future reboot/poweroff/reset | C2 | explicit crawler-control |
| Change fan/manual hardware behavior | D3 | explicit host-hardware |
| Change Wi-Fi/netplan behavior | E4 | explicit network-maintenance |
| Sync GitHub repo or live runtime | F5 | explicit sync |
| Inventory/classification/documentation | A0 plus file reading only | no control script execution |

## 8. Hard Rule for Crawler-Core Return

During crawler-core read-only trace, main-loop review, DB audit, frontier/lease review, robots/fetch preflight, and documentation cleanup:

- Do not run C2 controls.
- Do not run D3 controls.
- Do not run E4 controls.
- Do not run F5 controls unless the step is explicitly a sync step.
- Do not start crawler.
- Do not mutate DB.
- Do not mutate systemd.
- Do not touch host networking.
- Do not touch fan hardware.
- Do not reinterpret `poweroffwc.py`, `rebootwc.py`, or `resetwc.py` as real host lifecycle executors.

## 9. Documentation Quality Implication

This document is a narrow controls run-policy seal. It does not replace the broader future documentation-quality pass.

<!-- R112_CONTROLS_NO_CONTROL_SCRIPT_EXECUTION_POLICY_BEGIN -->

## R112 no-control-script-execution policy needle

`NO_CONTROL_SCRIPT_EXECUTION` is the hard inventory/audit rule for this control surface.

Meaning:

- Controls inventory may read files, compare hashes, parse AST, and classify risk.
- Controls inventory must not execute `pausewc`, `playwc`, `poweroffwc`, `rebootwc`, `resetwc`, fan controls, Wi-Fi controls, sync controls, or any other control entry point.
- Any future run of a C2/D3/E4/F5 control surface requires its own explicit task gate, stated mutation boundary, and post-run validation.
- During crawler-core trace work, documentation review, and repo/live equivalence checks, the accepted execution state is: control script execution is absent.

<!-- R112_CONTROLS_NO_CONTROL_SCRIPT_EXECUTION_POLICY_END -->

Future docs-global work should audit every `docs/*.md` file for:

- duplicate titles,
- stale path references,
- retired legacy live-root path references,
- canonical/live path mismatches,
- missing hub links,
- TODO vs sealed-doc contradictions,
- missing safety guard language,
- old systemd invocation language,
- outdated sync behavior,
- crawler-start ambiguity,
- DB mutation ambiguity,
- and weak bilingual explanation density.

That future docs-global work must start as read-only inventory before any patch.
