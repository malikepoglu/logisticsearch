# GitHub Batch v1 Channel

## Overview

**GitHub Batch v1** is the current repository-visible GitHub batch channel for Pi51 crawler export material that is intentionally promoted into Git. It defines the layout and repository-facing contract for structured batch delivery when GitHub-mediated history, reviewability, or transport traceability is desired. It is no longer the canonical primary path for moving Pi51 database/export payload into Ubuntu Desktop.

## Genel Bakış

**GitHub Batch v1**, Git içine bilinçli olarak alınan Pi51 crawler export materyali için repository’de görünür mevcut GitHub batch kanalıdır. GitHub aracılı geçmiş, gözden geçirilebilirlik veya taşıma izlenebilirliği istendiğinde yapısal batch teslimatının yerleşimini ve repository’ye bakan sözleşmesini tanımlar. Pi51 veritabanı/export payload’ını Ubuntu Desktop’a taşımak için artık kanonik birincil yol değildir.
## Purpose

This channel exists to provide a disciplined, predictable, and auditable batch transport surface. Its goal is to make export delivery stable enough that downstream intake logic can rely on a consistent directory structure and a known set of supporting metadata and integrity files.

## Amaç

Bu kanal, disiplinli, öngörülebilir ve denetlenebilir bir batch taşıma yüzeyi sağlamak için vardır. Amacı; export teslimatını, aşağı akış intake mantığının tutarlı bir dizin yapısına ve bilinen bir metadata/bütünlük dosyası setine güvenebileceği kadar stabil hale getirmektir.
## Current Role in the Flow

In the current working model, this channel remains available when a Pi51 crawler export batch is intentionally promoted into the repository-visible GitHub history path. Ubuntu Desktop may then pull that repository-visible state for review or controlled intake. However, the primary physical data path for Pi51 database/export payload transfer into Ubuntu Desktop is now expected to use removable media from Pi51 `/srv/data` rather than treating this GitHub channel as the default live transfer path.

## Akıştaki Mevcut Rol

Güncel çalışma modelinde bu kanal, bir Pi51 crawler export batch’i repository’de görünür GitHub tarihçe yoluna bilinçli olarak alındığında kullanılabilir durumda kalır. Ubuntu Desktop daha sonra bu repository’de görünür durumu gözden geçirme veya kontrollü intake için çekebilir. Ancak Pi51 veritabanı/export payload’ının Ubuntu Desktop’a fiziksel birincil veri yolu artık bu GitHub kanalını varsayılan canlı taşıma yolu kabul etmek yerine Pi51 `/srv/data` üzerinden çıkarılabilir medya kullanmalıdır.
## Documentation hub

Use these surfaces as the current hub / reading map around this channel:

- `README.md` — root repository entry surface
- `docs/README.md` — documentation hub and safest beginner reading map
- `hosts/makpi51crawler/crawler_exports/README.md` — crawler-exports hub surface
- `hosts/makpi51crawler/crawler_exports/pi51/README.md` — Pi51 export-source hub surface

This file should be read as the current channel contract surface, not as a standalone isolated note.

## Dokümantasyon merkezi

Bu kanal etrafındaki mevcut merkez / okuma haritası olarak şu yüzeyleri kullan:

- `README.md` — repository kök giriş yüzeyi
- `docs/README.md` — dokümantasyon merkezi ve başlangıç için en güvenli okuma haritası
- `hosts/makpi51crawler/crawler_exports/README.md` — crawler-exports hub yüzeyi
- `hosts/makpi51crawler/crawler_exports/pi51/README.md` — Pi51 export-kaynak hub yüzeyi

Bu dosya, tek başına izole bir not olarak değil, mevcut kanal sözleşmesi yüzeyi olarak okunmalıdır.

## Beginner-first reading path

If you are starting from zero, do **not** guess the channel from filenames alone.

Use this order:

1. `README.md` — understand the repository-level direction first
2. `docs/README.md` — understand the documentation hub and reading model
3. `hosts/makpi51crawler/crawler_exports/README.md` — understand the broader export surface first
4. `hosts/makpi51crawler/crawler_exports/pi51/README.md` — understand the Pi51 producer/source boundary
5. `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/README.md` — then read the current channel contract

## Başlangıç seviyesi okuma yolu

Sıfırdan başlıyorsan kanalı yalnızca dosya adlarına bakarak tahmin etme.

Şu sırayı kullan:

1. `README.md` — önce repository seviyesindeki yönü anla
2. `docs/README.md` — dokümantasyon merkezini ve okuma modelini anla
3. `hosts/makpi51crawler/crawler_exports/README.md` — önce daha geniş export yüzeyini anla
4. `hosts/makpi51crawler/crawler_exports/pi51/README.md` — Pi51 üretici/kaynak sınırını anla
5. `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/README.md` — sonra mevcut kanal sözleşmesini oku

## Current tracked channel path

At the current repository point, this channel path is:

- `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/`

This is the current repository-visible Pi51 GitHub transport/history channel, not the default physical bulk-transfer path.

## Güncel izlenen kanal yolu

Mevcut repository noktasında bu kanal yolu şudur:

- `hosts/makpi51crawler/crawler_exports/pi51/github_batch_v1/`

Bu, repository’de görünür olan güncel Pi51 GitHub taşıma/tarihçe kanalıdır; varsayılan fiziksel toplu taşıma yolu değildir.

## Expected Layout

This channel is expected to contain:
- dated batch directories under a stable path hierarchy
- one directory per immutable historical batch
- channel-level navigation files such as `LATEST_BATCH.json`
- channel-level catalog material such as `BATCH_CATALOG.json`

## Beklenen Yerleşim

Bu kanalın şunları içermesi beklenir:
- stabil bir yol hiyerarşisi altında tarih bazlı batch dizinleri
- her tarihsel batch için bir dizin
- `LATEST_BATCH.json` gibi kanal-seviyesi yönlendirme dosyaları
- `BATCH_CATALOG.json` gibi kanal-seviyesi catalog materyalleri
## Batch Contract

A valid historical batch directory is expected to carry a stable set of core files, typically including:
- `batch.json`
- `manifest.json`
- `SHA256SUMS.txt`
- `PUSH_RECEIPT.json`

These files together describe batch identity, payload metadata, integrity state, and delivery confirmation.

## Batch Kontratı

Geçerli bir tarihsel batch dizininin tipik olarak şu temel dosyaları taşıması beklenir:
- `batch.json`
- `manifest.json`
- `SHA256SUMS.txt`
- `PUSH_RECEIPT.json`

Bu dosyalar birlikte batch kimliğini, payload metadata’sını, bütünlük durumunu ve teslim teyidini tanımlar.
## Immutability Rules

Historical batch payload directories are treated as immutable once pushed. Their meaning depends on stable content and stable integrity material. For that reason:
- do not manually edit `batch.json`
- do not manually edit `manifest.json`
- do not manually edit `SHA256SUMS.txt`
- do not manually edit `PUSH_RECEIPT.json`
- do not rewrite historical payload content in place

If a new export state must be published, it should appear as a new batch, not as a silent mutation of an old batch.

## Değişmezlik Kuralları

Tarihsel batch payload dizinleri push edildikten sonra immutable kabul edilir. Anlamları stabil içerik ve stabil bütünlük materyaline dayanır. Bu nedenle:
- `batch.json` dosyasını elle düzenleme
- `manifest.json` dosyasını elle düzenleme
- `SHA256SUMS.txt` dosyasını elle düzenleme
- `PUSH_RECEIPT.json` dosyasını elle düzenleme
- tarihsel payload içeriğini bulunduğu yerde yeniden yazma

Yeni bir export durumu yayınlanacaksa, eski batch’i sessizce değiştirmek yerine yeni bir batch olarak görünmelidir.
## Channel-Level Regeneration

Channel-level readability or navigation material may be regenerated on Ubuntu Desktop as long as payload meaning is not changed. In practice, this mainly applies to files like:
- `LATEST_BATCH.json`
- `BATCH_CATALOG.json`

These files help navigation and discovery, but they should not falsify the historical record.

## Kanal Seviyesi Yeniden Üretim

Kanal-seviyesi okunabilirlik veya yönlendirme materyalleri, payload anlamı değiştirilmediği sürece Ubuntu Desktop üzerinde yeniden üretilebilir. Pratikte bu özellikle şu dosyalar için geçerlidir:
- `LATEST_BATCH.json`
- `BATCH_CATALOG.json`

Bu dosyalar gezinmeyi ve keşfi kolaylaştırır; ancak tarihsel kaydı çarpıtmamalıdır.
## Operational Value

The main value of this channel is that it turns crawler export delivery into a visible and reviewable contract. Instead of an opaque file transfer, the project gets a stable transport surface with history, structure, integrity cues, and a clear import boundary.

## Operasyonel Değer

Bu kanalın temel değeri, crawler export teslimatını görünür ve gözden geçirilebilir bir sözleşmeye dönüştürmesidir. Opak bir dosya aktarımı yerine proje; geçmişi, yapısı, bütünlük işaretleri ve net bir import sınırı olan stabil bir taşıma yüzeyi kazanır.
## Notes

This channel should remain explicit, narrow in scope, and conservative in mutation. Historical truth matters here.

## Notlar

Bu kanal açık, kapsamı dar ve değişiklik açısından muhafazakâr kalmalıdır. Burada tarihsel doğruluk önemlidir.
