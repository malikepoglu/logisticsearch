# Crawler Exports

**Crawler Exports** is the repository-managed export surface for LogisticSearch crawler output that is intentionally promoted into Git. Its purpose is to hold structured, reviewable, and traceable export batches that move from the crawler node into the canonical GitHub bridge and then onward to Ubuntu Desktop for controlled intake. This area is not a generic dump folder. It exists to preserve export artifacts that are important for transport, auditability, reproducibility, and downstream processing.

**Crawler Exports**, Git içine bilinçli olarak alınan LogisticSearch crawler çıktılarının repository tarafından yönetilen export yüzeyidir. Amacı; crawler düğümünden kanonik GitHub köprüsüne ve oradan Ubuntu Desktop üzerindeki kontrollü intake sürecine taşınan yapısal, gözden geçirilebilir ve izlenebilir export batch’lerini barındırmaktır. Bu alan genel amaçlı bir döküm klasörü değildir. Taşıma, denetlenebilirlik, tekrar üretilebilirlik ve sonraki işlem katmanları açısından önemli olan export artefact’larını korumak için vardır.

## Purpose

This directory exists to define a clean and durable contract for crawler-side export delivery. Exported batches are expected to be packaged in a predictable structure, accompanied by integrity and metadata files, and stored in a way that makes later inspection and desktop-side import straightforward. The main goal is to keep the crawler-to-desktop transfer path disciplined, inspectable, and operationally stable.

Bu dizin, crawler tarafındaki export teslimatı için temiz ve kalıcı bir sözleşme tanımlamak amacıyla vardır. Export edilen batch’lerin öngörülebilir bir yapıda paketlenmesi, bütünlük ve metadata dosyalarıyla birlikte gelmesi ve daha sonra incelenmesini ve desktop tarafındaki import işlemini kolaylaştıracak biçimde saklanması beklenir. Temel amaç, crawler’dan desktop’a uzanan transfer yolunu disiplinli, denetlenebilir ve operasyonel olarak stabil tutmaktır.

## Current Flow

The current working flow is: data is collected on the crawler node, assembled into a structured export batch, pushed into this repository through the GitHub bridge, pulled into Ubuntu Desktop, and then loaded into PostgreSQL through the desktop-side intake layer. This means the export surface acts as the auditable handoff boundary between crawler-origin output and the main processing environment.

Mevcut çalışan akış şudur: veri crawler düğümünde toplanır, yapısal bir export batch’i haline getirilir, GitHub köprüsü üzerinden bu repository’ye gönderilir, Ubuntu Desktop’a çekilir ve ardından desktop tarafındaki intake katmanı aracılığıyla PostgreSQL içine yüklenir. Bu nedenle export yüzeyi, crawler kökenli çıktı ile ana işleme ortamı arasındaki denetlenebilir teslim sınırı olarak görev yapar.

## Design Principles

The export surface is designed around traceability, predictable layout, integrity checking, and minimal ambiguity. A valid export should be understandable without hidden machine context, should carry enough metadata to be inspected later, and should fit a stable directory contract. This makes the repository more useful as both a transport surface and a long-term operational record.

Export yüzeyi; izlenebilirlik, öngörülebilir dizin yapısı, bütünlük kontrolü ve minimum belirsizlik ilkeleri etrafında tasarlanmıştır. Geçerli bir export, gizli makine bağlamına ihtiyaç duymadan anlaşılabilir olmalı, daha sonra incelenebilmesi için yeterli metadata taşımalı ve stabil bir dizin sözleşmesine uymalıdır. Bu yaklaşım, repository’yi hem bir taşıma yüzeyi hem de uzun vadeli bir operasyon kaydı olarak daha faydalı hale getirir.

## Structure

This area may contain source-scoped and channel-scoped subtrees, along with dated batch directories and supporting manifest material. A typical valid batch is expected to include machine-readable metadata, integrity material such as checksums, and delivery-state artifacts such as push receipts. The exact contract may evolve carefully over time, but the surface is intended to remain structured and explicit.

Bu alan; kaynak kapsamlı ve kanal kapsamlı alt ağaçlar, tarih bazlı batch dizinleri ve bunları destekleyen manifest materyallerini içerebilir. Tipik bir geçerli batch’in makine tarafından okunabilir metadata, checksum gibi bütünlük materyalleri ve push receipt gibi teslim durumu artefact’ları içermesi beklenir. Kesin sözleşme zaman içinde dikkatli biçimde evrilebilir; ancak yüzeyin yapısal ve açık kalması amaçlanmaktadır.

## What Belongs Here

Only export artifacts that are intentionally promoted into the canonical repository flow should live here. Examples include valid structured batches, manifests, catalog files, latest-batch pointers, and other durable transport-layer records. Files that are necessary for later verification, import, or audit are suitable candidates for this surface.

Burada yalnızca kanonik repository akışına bilinçli olarak alınan export artefact’ları yer almalıdır. Buna geçerli yapısal batch’ler, manifest’ler, catalog dosyaları, latest-batch pointer’ları ve diğer kalıcı taşıma katmanı kayıtları örnek verilebilir. Daha sonra doğrulama, import veya audit için gerekli olan dosyalar bu yüzey için uygun adaylardır.

## What Does Not Belong Here

Machine-local scratch output, temporary working files, disposable experiments, hidden host-specific clutter, and unrelated runtime artifacts should not accumulate here. This surface should stay focused on canonical export delivery, not become a mixed storage area for every crawler-side byproduct.

Makineye özel geçici çıktılar, temporary çalışma dosyaları, tek kullanımlık deneyler, host’a özgü gizli dağınık içerikler ve ilgisiz runtime artefact’ları burada birikmemelidir. Bu yüzeyin odağı kanonik export teslimatı olmalıdır; crawler tarafında üretilen her yan çıktının karıştığı genel bir depolama alanına dönüşmemelidir.

## Operational Role

From an operational perspective, this directory is part of the project’s controlled data-transfer fabric. It helps separate “data collected on the crawler” from “data accepted into the main engineering and database workflow.” That separation is valuable because it keeps the transfer boundary explicit and makes later review, troubleshooting, and import validation much easier.

Operasyonel açıdan bu dizin, projenin kontrollü veri aktarım dokusunun bir parçasıdır. “Crawler üzerinde toplanan veri” ile “ana mühendislik ve veritabanı iş akışına kabul edilen veri” arasındaki sınırı ayırmaya yardımcı olur. Bu ayrım değerlidir; çünkü transfer sınırını açık tutar ve daha sonraki inceleme, sorun giderme ve import doğrulamasını çok daha kolay hale getirir.

## Current Status

This export surface is already active and in use. Structured crawler export batches have been pushed into the repository, normalized into a cleaner surface, and paired with catalog-style navigation files. The current refinement direction is to keep this area clean, explicit, and aligned with the broader repository standardization effort.

Bu export yüzeyi halihazırda aktif olarak kullanılmaktadır. Yapısal crawler export batch’leri repository’ye gönderilmiş, daha temiz bir yüzeye normalize edilmiş ve catalog benzeri yönlendirme dosyalarıyla eşleştirilmiştir. Mevcut iyileştirme yönü, bu alanı temiz, açık ve daha geniş repository standardizasyon çalışmasıyla uyumlu tutmaktır.

## Notes

This directory should be read as a controlled project surface, not merely as stored output. Its value comes from consistency, integrity, and operational clarity.

Bu dizin, yalnızca depolanmış çıktı olarak değil, kontrollü bir proje yüzeyi olarak okunmalıdır. Değeri; tutarlılık, bütünlük ve operasyonel açıklıktan gelir.
