# GitHub Batch v1 Channel

**GitHub Batch v1** is the current canonical repository transport channel for Pi51 crawler export batches. It defines the layout and repository-facing contract for structured batch delivery that moves from the Pi51 crawler node into GitHub and then into Ubuntu Desktop for controlled intake and PostgreSQL loading.

**GitHub Batch v1**, Pi51 crawler export batch’leri için mevcut kanonik repository taşıma kanalıdır. Pi51 crawler düğümünden GitHub’a ve oradan Ubuntu Desktop üzerindeki kontrollü intake ile PostgreSQL yükleme sürecine taşınan yapısal batch teslimatı için yerleşimi ve repository’ye bakan sözleşmeyi tanımlar.

## Purpose

This channel exists to provide a disciplined, predictable, and auditable batch transport surface. Its goal is to make export delivery stable enough that downstream intake logic can rely on a consistent directory structure and a known set of supporting metadata and integrity files.

Bu kanal, disiplinli, öngörülebilir ve denetlenebilir bir batch taşıma yüzeyi sağlamak için vardır. Amacı; export teslimatını, aşağı akış intake mantığının tutarlı bir dizin yapısına ve bilinen bir metadata/bütünlük dosyası setine güvenebileceği kadar stabil hale getirmektir.

## Current Role in the Flow

In the current working model, Pi51 assembles a crawler export batch, pushes it into this channel, Ubuntu Desktop pulls the current state from GitHub, and the desktop-side import layer loads accepted records into PostgreSQL. This makes the channel a critical transport and handoff boundary in the live data path.

Mevcut çalışma modelinde Pi51 bir crawler export batch’i oluşturur, bu kanala gönderir, Ubuntu Desktop güncel durumu GitHub’dan çeker ve desktop tarafındaki import katmanı kabul edilen kayıtları PostgreSQL içine yükler. Bu da kanalı, canlı veri yolunda kritik bir taşıma ve teslim sınırı haline getirir.

## Expected Layout

This channel is expected to contain:
- dated batch directories under a stable path hierarchy
- one directory per immutable historical batch
- channel-level navigation files such as `LATEST_BATCH.json`
- channel-level catalog material such as `BATCH_CATALOG.json`

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

Kanal-seviyesi okunabilirlik veya yönlendirme materyalleri, payload anlamı değiştirilmediği sürece Ubuntu Desktop üzerinde yeniden üretilebilir. Pratikte bu özellikle şu dosyalar için geçerlidir:
- `LATEST_BATCH.json`
- `BATCH_CATALOG.json`

Bu dosyalar gezinmeyi ve keşfi kolaylaştırır; ancak tarihsel kaydı çarpıtmamalıdır.

## Operational Value

The main value of this channel is that it turns crawler export delivery into a visible and reviewable contract. Instead of an opaque file transfer, the project gets a stable transport surface with history, structure, integrity cues, and a clear import boundary.

Bu kanalın temel değeri, crawler export teslimatını görünür ve gözden geçirilebilir bir sözleşmeye dönüştürmesidir. Opak bir dosya aktarımı yerine proje; geçmişi, yapısı, bütünlük işaretleri ve net bir import sınırı olan stabil bir taşıma yüzeyi kazanır.

## Notes

This channel should remain explicit, narrow in scope, and conservative in mutation. Historical truth matters here.

Bu kanal açık, kapsamı dar ve değişiklik açısından muhafazakâr kalmalıdır. Burada tarihsel doğruluk önemlidir.
