# Desktop Import Surface Role Map

## Overview

This document defines the role of each important file family inside the `sql/desktop_import` surface.

Its purpose is to prevent confusion between:

- live observed schema evidence
- repository-side executable contract
- interpretation documents
- future evolution decisions

## Genel Bakış

Bu belge, `sql/desktop_import` yüzeyi içindeki önemli dosya ailelerinin rolünü tanımlar.

Amacı, şu katmanlar arasındaki karışıklığı önlemektir:

- canlı gözlenen şema kanıtı
- repository-side çalıştırılabilir contract
- yorum belgeleri
- gelecekteki evrim kararları

## 1) Live observed evidence surface

These files preserve the currently observed desktop_import schema reality from Ubuntu Desktop PostgreSQL:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

Role:

- evidence
- comparison baseline
- observed live-state reference

These files are not automatically the main editable working surface.

## 1) Canlı gözlenen kanıt yüzeyi

Bu dosyalar, Ubuntu Desktop PostgreSQL üzerindeki şu anda gözlenen desktop_import şema gerçekliğini korur:

- `001_live_desktop_import_schema.sql`
- `001_live_desktop_import_inventory.txt`
- `001_live_desktop_import_schema.sha256`

Rol:

- kanıt
- karşılaştırma tabanı
- gözlenen canlı durum referansı

Bu dosyalar otomatik olarak ana düzenlenebilir çalışma yüzeyi değildir.

## 2) Current executable contract surface

This file preserves the current repository-side executable intake contract:

- `001_pi51_batch_intake_contract.sql`

Role:

- executable repository contract
- current apply-oriented SQL surface
- hand-maintained structural contract

This file is the current executable surface, but it has not yet been formally sealed as the long-term primary working evolution surface.

## 2) Mevcut çalıştırılabilir contract yüzeyi

Bu dosya mevcut repository-side çalıştırılabilir intake contract'ını korur:

- `001_pi51_batch_intake_contract.sql`

Rol:

- çalıştırılabilir repository contract'ı
- mevcut apply odaklı SQL yüzeyi
- elde sürdürülen yapısal contract

Bu dosya mevcut çalıştırılabilir yüzeydir; ancak henüz uzun vadeli ana çalışma evrim yüzeyi olarak resmen mühürlenmemiştir.

## 3) Interpretation surface

These files explain how the surface should currently be read:

- `README.md`
- `CHRONOLOGY_SPLIT_PLAN.md`

Role:

- navigation
- chronology interpretation
- repository-side meaning layer

These files explain the surface, but they do not define executable database structure by themselves.

## 3) Yorum yüzeyi

Bu dosyalar yüzeyin şu anda nasıl okunması gerektiğini açıklar:

- `README.md`
- `CHRONOLOGY_SPLIT_PLAN.md`

Rol:

- gezinme
- kronoloji yorumu
- repository-side anlam katmanı

Bu dosyalar yüzeyi açıklar; fakat yürütülebilir veritabanı yapısını tek başlarına tanımlamazlar.

## 4) Confirmed equivalence and decision layer

The comparison and decision layer now exists and is documented in:

- `COVERAGE_OR_EQUIVALENCE_NOTE.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`

Recorded result:

- live snapshot truth and executable contract truth are structurally aligned at the audited layer
- the contract file is now the primary working surface

## 4) Doğrulanmış eşdeğerlik ve karar katmanı

Karşılaştırma ve karar katmanı artık vardır ve şu belgelerde işlenmiştir:

- `COVERAGE_OR_EQUIVALENCE_NOTE.md`
- `PRIMARY_WORKING_SURFACE_SEAL.md`

Kayda geçen sonuç:

- canlı snapshot doğruluğu ile çalıştırılabilir contract doğruluğu denetlenen katmanda yapısal olarak hizalıdır
- contract dosyası artık ana çalışma yüzeyidir

## Current rule

For now:

1. treat the snapshot files as observed live evidence
2. treat the contract file as executable repository truth
3. treat the contract file as the primary working surface
4. preserve the comparison and seal documents as justification for that status

## Güncel kural

Şimdilik:

1. snapshot dosyalarını gözlenen canlı kanıt olarak ele al
2. contract dosyasını çalıştırılabilir repository doğruluğu olarak ele al
3. contract dosyasını ana çalışma yüzeyi olarak ele al
4. karşılaştırma ve mühür belgelerini bu statünün gerekçesi olarak koru
