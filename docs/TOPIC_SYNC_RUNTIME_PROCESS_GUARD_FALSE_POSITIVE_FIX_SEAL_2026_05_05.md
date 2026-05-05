# Sync Runtime Process Guard False-Positive Fix Seal — 2026-05-05

## 1. Purpose

This document records the R108 sync_runtime process guard false-positive fix and final pi51c seal.

TR: Bu doküman, R108 sync_runtime process guard false-positive düzeltmesini ve final pi51c seal sonucunu kayda alır.

## 2. Canonical commits

Documentation commit before R108:

```text
b3d0ecd08961f5f8913a4c958e4e4dff2a86546b
docs(crawler): seal systemd service invocation patch
```

Process guard patch commit:

```text
717ef52dc25c0ec436514bfbce5c950f37b539e0
fix(sync-runtime): avoid crawler process false positives
```

Executable mode restore commit and current canonical head:

```text
0ec0a7ea841d0bd379eb8284d6872d38dae5fe92
fix(sync-runtime): restore executable mode
```

## 3. Problem found during R107/R108 sync

During R107/R108 pi51c sync, sync_runtime initially reported a crawler process even though the service was inactive and no real crawler process existed.

False-positive symptom:

```text
MATCHING_PROCESS_COUNT=1
FAIL: crawler process appears to be running
```

Read-only forensic checks showed that broad process matching caught a bash or ssh audit command line containing crawler words, not a real Python crawler process.

## 4. Root cause

The old sync_runtime guard scanned command arguments broadly.

Old pattern:

```text
ps -eo args=
if "logisticsearch1_main_entry" in line or "--durable-claim" in line:
```

This was too broad because shell, ssh, grep, and audit command lines can contain crawler-related words without being crawler processes.

## 5. R108 fix

R108 changed the process guard to count real crawler Python processes only.

New pattern:

```text
ps -eo comm=,args=
Path(command_name).name.startswith("python")
```

The new guard excludes sync commands and ignores shell, ssh, grep, and audit command lines that merely contain crawler words.

## 6. Local validation

R108 local validation passed:

```text
PY_COMPILE=PASS
PROCESS_COUNT=0
FALSE_POSITIVE_RESISTANCE=PASS
OLD_PS_ARGS_ONLY_GUARD=PASS_ABSENT
NEW_PS_COMMAND_CHECK=PASS
PYTHON_PROCESS_ONLY_CHECK=PASS
GIT_DIFF_CHECK=PASS
```

## 7. pi51c final seal

R108_STEP3C pi51c final read-only seal passed.

Verified state:

```text
REPO_HEAD=0ec0a7ea841d0bd379eb8284d6872d38dae5fe92
REPO_ORIGIN=0ec0a7ea841d0bd379eb8284d6872d38dae5fe92
REPO_STATUS_COUNT=0
SURFACE_MATCH=PASS python_live_runtime
SURFACE_MATCH=PASS catalog
SURFACE_MATCH=PASS taxonomy
SYNC_RUNTIME_SHA_MATCH=PASS
PROCESS_GUARD_PATCH_PRESENT=PASS
OLD_BROAD_GUARD_ABSENT=PASS
SERVICE_ACTIVE=inactive
SERVICE_ENABLED=disabled
REAL_PYTHON_CRAWLER_COUNT=0
CRAWLER_NOT_RUNNING_CHECK=PASS
```

## 8. Runtime sync scope confirmed

sync_runtime synchronizes these tracked runtime directories:

```text
python_live_runtime
catalog
taxonomy
```

Tracked root files:

```text
README.md
RUNBOOK_SYNC_REPO_AND_RUNTIME.md
.gitignore
```

Runtime-local preserved directories:

```text
.venv
config
```

Current project policy keeps config absent and uses secure user env instead.

## 9. Safety boundary

During R108:

- no DB mutation occurred
- no systemd start, stop, restart, enable, or disable occurred
- no crawler start occurred
- secret values were not printed
- secure env stayed outside tracked repo

## 10. Next safe step

After this documentation is committed, pushed, synced, and sealed, the next safe crawler-core step is controls safety review, followed by main-loop state-machine read-only trace.

TR: Bu dokümantasyon commit, push, sync ve seal sonrası sıradaki güvenli adım controls safety review ve ardından main-loop state-machine read-only trace olmalıdır.
