# Crawler Core Systemd Service Invocation Patch Seal — 2026-05-05

## 1. Purpose

This document records the R106 and R106B systemd user service invocation correction for the LogisticSearch crawler-core runtime.

TR: Bu doküman, LogisticSearch crawler-core runtime için R106 ve R106B systemd user service invocation düzeltmesini kayda alır.

## 2. Canonical basis

Canonical repository commit before this documentation patch:

```text
f6258f133c5cbb447b3667eb3444ddb9b0e6fd2b
docs(crawler): seal entrypoint invocation contract
```

Entrypoint contract document:

```text
docs/TOPIC_CRAWLER_CORE_ENTRYPOINT_INVOCATION_CONTRACT_2026_05_05.md
```

## 3. R105 finding

R105 read-only audit found that the pi51c user service still used the wrong top-level invocation corridor.

Wrong previous pattern:

```text
PYTHONPATH=/logisticsearch/makpi51crawler/python_live_runtime
-m logisticsearch1_main_entry
```

TR: R105 read-only audit, service unit dosyasının hâlâ yanlış top-level invocation corridor kullandığını buldu.

## 4. R106 patch

R106 patched only the systemd user service invocation corridor.

Correct package-context pattern:

```text
PYTHONPATH=/logisticsearch/makpi51crawler
-m python_live_runtime.logisticsearch1_main_entry
```

Patched service file:

```text
/home/makpi51/.config/systemd/user/logisticsearch-webcrawler.service
```

Backup file created during R106:

```text
/home/makpi51/.config/systemd/user/logisticsearch-webcrawler.service.r106_backup_2026-05-05_21-44-32
```

Backup SHA256:

```text
327b0b741729cdb83435101b842c46f0fdee434f02d835c0d5b8254c814f01b9
```

Post-patch service fragment SHA256:

```text
1f80296a2d3f5548f238e64823b96db93b0eb2fdf86a919b509d4c508b7d13bb
```

## 5. R106B final seal

R106B read-only final seal passed.

Verified state:

```text
SERVICE_ACTIVE=inactive
SERVICE_ENABLED=disabled
SERVICE_LOAD=loaded
CRAWLER_PROCESS_COUNT=0
HAS_PACKAGE_CONTEXT=YES
HAS_WRONG_PYTHONPATH=NO
HAS_WRONG_MODULE=NO
HAS_LIVE_PYTHONPATH=YES
HAS_SECURE_ENV=YES
HAS_RAW_DSN=NO
HELP_SMOKE_CHECK=PASS
HELP_DID_NOT_START_CRAWLER=PASS
NO_DB_MUTATION=TRUE
NO_SYSTEMD_START_STOP_RESTART_ENABLE_DISABLE=TRUE
NO_CRAWLER_START=TRUE
```

## 6. Secure env boundary

The service continues to source the secure untracked env file:

```text
/home/makpi51/.config/logisticsearch/secrets/webcrawler.env
```

Rules:

- The path may be documented.
- Secret values must never be printed.
- DSN, password, and token values must never be committed.
- Runtime code must not move DSN values into tracked files.

## 7. Forbidden actions during R106 and R106B

The following actions were not performed:

- service start
- service stop
- service restart
- service enable
- service disable
- crawler start
- DB mutation
- raw fetch
- network crawl

## 8. Next safe step

After this documentation is committed and synced, the next safe crawler-core step is controls safety review and main-loop state-machine read-only trace.

TR: Bu dokümantasyon commit, push ve sync sonrası sıradaki güvenli adım controls safety review ve main-loop state-machine read-only trace olmalıdır.
