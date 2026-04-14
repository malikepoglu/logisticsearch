# Crawler Exports

## Overview

**Crawler Exports** is the repository-managed export surface for LogisticSearch crawler output that is intentionally promoted into Git when repository-level reviewability, transport history, or auditability is desired. It is not the primary operational path for bulk Pi51 database/export transfer into Ubuntu Desktop. This area is not a generic dump folder. It exists to preserve export artifacts that are important for transport, auditability, reproducibility, and downstream processing.

## Genel Bakış

**Crawler Exports**, repository seviyesinde gözden geçirilebilirlik, taşıma geçmişi veya denetlenebilirlik istendiğinde Git içine bilinçli olarak alınan LogisticSearch crawler çıktılarının repository tarafından yönetilen export yüzeyidir. Pi51 veritabanı/export payload’ını Ubuntu Desktop’a toplu biçimde taşımanın birincil operasyon yolu bu yüzey değildir. Bu alan genel amaçlı bir döküm klasörü değildir. Taşıma, denetlenebilirlik, tekrar üretilebilirlik ve sonraki işlem katmanları açısından önemli olan export artefact’larını korumak için vardır.
## Purpose

This directory exists to define a clean and durable contract for crawler-side export delivery. Exported batches are expected to be packaged in a predictable structure, accompanied by integrity and metadata files, and stored in a way that makes later inspection and desktop-side import straightforward. The main goal is to keep the repository-visible export transport path disciplined, inspectable, and operationally stable without confusing it with the separate removable-media path used for the current primary physical Pi51-to-Ubuntu Desktop crawler data movement.

## Amaç

Bu dizin, crawler tarafındaki export teslimatı için temiz ve kalıcı bir sözleşme tanımlamak amacıyla vardır. Export edilen batch’lerin öngörülebilir bir yapıda paketlenmesi, bütünlük ve metadata dosyalarıyla birlikte gelmesi ve daha sonra incelenmesini ve desktop tarafındaki import işlemini kolaylaştıracak biçimde saklanması beklenir. Temel amaç, repository’de görünür export taşıma yolunu; mevcut birincil fiziksel Pi51->Ubuntu Desktop crawler veri hareketi için kullanılan ayrı çıkarılabilir-medya yolu ile karıştırmadan disiplinli, denetlenebilir ve operasyonel olarak stabil tutmaktır.
## Current Flow

The current operational truth is more specific. Repository-visible export batches may still be intentionally promoted into GitHub through this surface when auditability or transport history is required. However, the primary physical crawler database/export transfer path into Ubuntu Desktop is now expected to move from Pi51 `/srv/data` via removable SSD media under controlled operator handling. GitHub remains the canonical synchronization bridge for code, documentation, SQL, Python surfaces, and selectively promoted export artifacts. This means the export surface acts as an auditable handoff boundary between crawler-origin output and the main processing environment, but not as the only active physical transport path.

## Mevcut Akış

Güncel operasyon doğrusu daha özeldir. Denetlenebilirlik veya taşıma geçmişi gerektiğinde repository’de görünür export batch’leri bu yüzey üzerinden hâlâ bilinçli olarak GitHub’a alınabilir. Ancak crawler veritabanı/export payload’ının Ubuntu Desktop’a fiziksel birincil taşıma yolu artık Pi51 `/srv/data` üzerinden çıkarılabilir SSD medyası ile, kontrollü operatör işlemi altında gerçekleşmelidir. GitHub; kod, dokümantasyon, SQL, Python yüzeyleri ve seçilerek Git’e alınan export artefact’ları için kanonik senkronizasyon köprüsü olarak kalır. Bu nedenle export yüzeyi, crawler kökenli çıktı ile ana işleme ortamı arasındaki denetlenebilir teslim sınırı olarak görev yapar; ancak tek aktif fiziksel taşıma yolu değildir.
## Documentation hub

Use these surfaces as the current hub / reading map around the export area:

- `README.md` — root repository entry surface
- `docs/README.md` — documentation hub and safest beginner reading map
- `hosts/makpi51crawler/crawler_exports/pi51/README.md` — Pi51 export-source surface
- `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/README.md` — current GitHub transport/export channel surface

This file should be read as the crawler-exports hub, not as a standalone isolated note.

## Dokümantasyon merkezi

Export alanı etrafındaki mevcut merkez / okuma haritası olarak şu yüzeyleri kullan:

- `README.md` — repository kök giriş yüzeyi
- `docs/README.md` — dokümantasyon merkezi ve başlangıç için en güvenli okuma haritası
- `hosts/makpi51crawler/crawler_exports/pi51/README.md` — Pi51 export-kaynak yüzeyi
- `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/README.md` — mevcut GitHub taşıma/export kanal yüzeyi

Bu dosya, tek başına izole bir not olarak değil, crawler_exports alanının hub yüzeyi olarak okunmalıdır.

## Beginner-first reading path

If you are starting from zero, do **not** guess the export surface from filenames alone.

Use this order:

1. `README.md` — understand the repository-level direction first
2. `docs/README.md` — understand the documentation hub and reading model
3. `hosts/makpi51crawler/crawler_exports/README.md` — understand what the export surface is and is not
4. `hosts/makpi51crawler/crawler_exports/pi51/README.md` — understand the producer/source side
5. `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/README.md` — understand the current channel contract

## Başlangıç seviyesi okuma yolu

Sıfırdan başlıyorsan export yüzeyini yalnızca dosya adlarına bakarak tahmin etme.

Şu sırayı kullan:

1. `README.md` — önce repository seviyesindeki yönü anla
2. `docs/README.md` — dokümantasyon merkezini ve okuma modelini anla
3. `hosts/makpi51crawler/crawler_exports/README.md` — export yüzeyinin ne olduğunu ve ne olmadığını anla
4. `hosts/makpi51crawler/crawler_exports/pi51/README.md` — üretici/kaynak tarafını anla
5. `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/README.md` — mevcut kanal sözleşmesini anla

## Current tracked subsurfaces

At the current repository point, the main tracked export subsurfaces are:

- `hosts/makpi51crawler/crawler_exports/pi51/`
- `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/`

These are not generic decorative paths. They are part of the current export navigation and transport model.

## Güncel izlenen alt yüzeyler

Mevcut repository noktasında ana izlenen export alt yüzeyleri şunlardır:

- `hosts/makpi51crawler/crawler_exports/pi51/`
- `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/`

Bunlar genel amaçlı süs dizinleri değildir. Mevcut export gezinme ve taşıma modelinin parçasıdırlar.

## Design Principles

The export surface is designed around traceability, predictable layout, integrity checking, and minimal ambiguity. A valid export should be understandable without hidden machine context, should carry enough metadata to be inspected later, and should fit a stable directory contract. This makes the repository more useful as both a transport surface and a long-term operational record.

## Tasarım İlkeleri

Export yüzeyi; izlenebilirlik, öngörülebilir dizin yapısı, bütünlük kontrolü ve minimum belirsizlik ilkeleri etrafında tasarlanmıştır. Geçerli bir export, gizli makine bağlamına ihtiyaç duymadan anlaşılabilir olmalı, daha sonra incelenebilmesi için yeterli metadata taşımalı ve stabil bir dizin sözleşmesine uymalıdır. Bu yaklaşım, repository’yi hem bir taşıma yüzeyi hem de uzun vadeli bir operasyon kaydı olarak daha faydalı hale getirir.
## Structure

This area may contain source-scoped and channel-scoped subtrees, along with dated batch directories and supporting manifest material. A typical valid batch is expected to include machine-readable metadata, integrity material such as checksums, and delivery-state artifacts such as push receipts. The exact contract may evolve carefully over time, but the surface is intended to remain structured and explicit.

## Yapı

Bu alan; kaynak kapsamlı ve kanal kapsamlı alt ağaçlar, tarih bazlı batch dizinleri ve bunları destekleyen manifest materyallerini içerebilir. Tipik bir geçerli batch’in makine tarafından okunabilir metadata, checksum gibi bütünlük materyalleri ve push receipt gibi teslim durumu artefact’ları içermesi beklenir. Kesin sözleşme zaman içinde dikkatli biçimde evrilebilir; ancak yüzeyin yapısal ve açık kalması amaçlanmaktadır.
## What Belongs Here

Only export artifacts that are intentionally promoted into the canonical repository flow should live here. Examples include valid structured batches, manifests, catalog files, latest-batch pointers, and other durable transport-layer records. Files that are necessary for later verification, import, or audit are suitable candidates for this surface.

## Burada Ne Yer Alır

Burada yalnızca kanonik repository akışına bilinçli olarak alınan export artefact’ları yer almalıdır. Buna geçerli yapısal batch’ler, manifest’ler, catalog dosyaları, latest-batch pointer’ları ve diğer kalıcı taşıma katmanı kayıtları örnek verilebilir. Daha sonra doğrulama, import veya audit için gerekli olan dosyalar bu yüzey için uygun adaylardır.
## What Does Not Belong Here

Machine-local scratch output, temporary working files, disposable experiments, hidden host-specific clutter, and unrelated runtime artifacts should not accumulate here. This surface should stay focused on canonical export delivery, not become a mixed storage area for every crawler-side byproduct.

## Burada Ne Yer Almaz

Makineye özel geçici çıktılar, temporary çalışma dosyaları, tek kullanımlık deneyler, host’a özgü gizli dağınık içerikler ve ilgisiz runtime artefact’ları burada birikmemelidir. Bu yüzeyin odağı kanonik export teslimatı olmalıdır; crawler tarafında üretilen her yan çıktının karıştığı genel bir depolama alanına dönüşmemelidir.
## Operational Role

From an operational perspective, this directory is part of the project’s controlled data-transfer fabric. It helps separate “data collected on the crawler” from “data accepted into the main engineering and database workflow.” That separation is valuable because it keeps the transfer boundary explicit and makes later review, troubleshooting, and import validation much easier.

## Operasyonel Rol

Operasyonel açıdan bu dizin, projenin kontrollü veri aktarım dokusunun bir parçasıdır. “Crawler üzerinde toplanan veri” ile “ana mühendislik ve veritabanı iş akışına kabul edilen veri” arasındaki sınırı ayırmaya yardımcı olur. Bu ayrım değerlidir; çünkü transfer sınırını açık tutar ve daha sonraki inceleme, sorun giderme ve import doğrulamasını çok daha kolay hale getirir.
## Current Status

This export surface is already active and in use. Structured crawler export batches have been pushed into the repository, normalized into a cleaner surface, and paired with catalog-style navigation files. The current refinement direction is to keep this area clean, explicit, and aligned with the broader repository standardization effort.

## Mevcut Durum

Bu export yüzeyi halihazırda aktif olarak kullanılmaktadır. Yapısal crawler export batch’leri repository’ye gönderilmiş, daha temiz bir yüzeye normalize edilmiş ve catalog benzeri yönlendirme dosyalarıyla eşleştirilmiştir. Mevcut iyileştirme yönü, bu alanı temiz, açık ve daha geniş repository standardizasyon çalışmasıyla uyumlu tutmaktır.
## Notes

This directory should be read as a controlled project surface, not merely as stored output. Its value comes from consistency, integrity, and operational clarity.

## Notlar

Bu dizin, yalnızca depolanmış çıktı olarak değil, kontrollü bir proje yüzeyi olarak okunmalıdır. Değeri; tutarlılık, bütünlük ve operasyonel açıklıktan gelir.
## Current root-surface truth
## Güncel kök-yüzey doğrusu

At the current repository point, this export surface now lives at `hosts/makpi51crawler/crawler_exports/`.

It is intentionally located under the active crawler-host surface.

The `hosts/` family documents host-specific operational truth, and this subtree is now the tracked export and handoff surface for `makpi51crawler` inside the repository.

For host-side boundary reading, also see:

- `hosts/README.md`
- `hosts/makpi51crawler/README.md`

Mevcut repository noktasında bu export yüzeyi artık `hosts/makpi51crawler/crawler_exports/` yolunda yaşamaktadır.

Bu yüzey aktif crawler-host yüzeyi altında bilinçli olarak konumlandırılmıştır.

`hosts/` ailesi host-özel operasyon doğrusunu belgeler; bu alt ağaç ise artık repository içinde `makpi51crawler` için tracked export ve teslim yüzeyidir.

Host-tarafı sınır okuması için ayrıca şunlara bak:

- `hosts/README.md`
- `hosts/makpi51crawler/README.md`
