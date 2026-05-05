# Crawler Core EntryPoint Invocation Contract — 2026-05-05

## 1. Purpose

This document seals the safe invocation boundary for the LogisticSearch crawler-core runtime after the Task11 runtime cleanup.

TR: Bu doküman, Task11 runtime temizliği sonrasında LogisticSearch crawler-core çalışma zamanının güvenli çağırma sınırını mühürler.

## 2. Canonical machine roles

- Ubuntu Desktop remains the canonical development and decision workspace.
- GitHub remains the canonical sync bridge.
- pi51c / makpi51crawler remains the crawler-only node.
- pi51c is not the application decision center.

TR:

- Ubuntu Desktop ana geliştirme ve karar çalışma alanıdır.
- GitHub canonical sync bridge olarak kalır.
- pi51c / makpi51crawler yalnızca crawler node olarak kalır.
- pi51c application decision center değildir.

## 3. Forbidden wrong invocation corridor

The following top-level module corridor is forbidden for crawler-core runtime entrypoint execution:

    cd /logisticsearch/makpi51crawler/python_live_runtime
    python -m logisticsearch1_main_entry

Reason:

- It runs the module without the required package context.
- It can trigger relative import context failure.
- R102 classified this as the wrong corridor.

TR:

- Bu kullanım gerekli package context olmadan çalışır.
- Relative import context hatasına yol açabilir.
- R102 bu yolu yanlış corridor olarak sınıflandırdı.

## 4. Canonical package-context invocation corridor

The canonical help-smoke corridor is:

    PYTHONPATH=/logisticsearch/makpi51crawler \
    /logisticsearch/makpi51crawler/.venv/bin/python \
    -m python_live_runtime.logisticsearch1_main_entry --help

This package-context invocation passed in R102B.

TR: Bu package-context çağırma biçimi R102B içinde başarılı şekilde doğrulandı.

## 5. Main loop help-smoke boundary

The main-loop help-smoke must also stay package-context aware.

Expected principle:

- Run from the live runtime package boundary.
- Preserve PYTHONPATH=/logisticsearch/makpi51crawler.
- Do not start the crawler loop during help-smoke validation.

TR:

- Live runtime package sınırı korunmalıdır.
- PYTHONPATH=/logisticsearch/makpi51crawler korunmalıdır.
- Help-smoke doğrulamasında crawler loop başlatılmamalıdır.

## 6. Secret handling contract

Secrets are never printed, copied into tracked Python, or committed.

The secure untracked env file remains outside the repository:

    /home/makpi51/.config/logisticsearch/secrets/webcrawler.env

Contract:

- The env file path may be documented.
- Secret values must never be printed.
- DSN/password/token values must never be committed.
- Runtime code must load secrets from the secure untracked boundary, not from tracked source.

TR:

- Env dosya yolu dokümante edilebilir.
- Secret değerleri asla yazdırılmaz.
- DSN/password/token değerleri asla commit edilmez.
- Runtime code secret değerlerini tracked source içinden değil secure untracked sınırdan alır.

## 7. Forbidden actions under this contract step

This contract document does not authorize:

- crawler start
- network fetch
- DB mutation
- systemd start/stop/restart/enable/disable
- seed/frontier insert
- raw fetch write
- rsync
- git push

TR: Bu doküman tek başına crawler başlatma, network fetch, DB mutation, systemd mutation, seed/frontier insert, raw fetch write, rsync veya git push yetkisi vermez.

## 8. Next required gate

If the service file still uses the wrong top-level corridor, it must be patched only in a separate R105 gate.

R105 must be small, audited, reversible, and must not start the crawler unless a later explicit crawler-start gate authorizes it.

TR:

Eğer service dosyası hâlâ yanlış top-level corridor kullanıyorsa, bu yalnızca ayrı bir R105 gate ile düzeltilmelidir.

R105 küçük, audit-first, geri alınabilir olmalı ve daha sonraki açık crawler-start gate olmadan crawler başlatmamalıdır.

## 9. Sealed status after this document

After this document is created locally:

- mutation scope must be exactly this document
- no commit/push has been performed
- no pi51c sync has been performed
- no DB mutation has been performed
- no systemd mutation has been performed
- no crawler start has been performed

TR:

Bu doküman local olarak oluşturulduktan sonra mutation scope yalnızca bu doküman olmalıdır.

Commit/push, pi51c sync, DB mutation, systemd mutation ve crawler start yapılmamış olmalıdır.
