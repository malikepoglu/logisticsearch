# SECTION1_WEBCRAWLER_PROCESSED_DATA_STORAGE_TIER_POLICY

## Purpose

This document defines the canonical processed-data storage tier policy for the LogisticSearch webcrawler line.

It exists to separate three different storage concerns clearly:

- the host-local crawler operating surface
- the primary removable processed-data surface
- the temporary fallback processed-data surface

This document is a policy and contract surface. It is not a runbook and it is not an implementation script.

## Amaç

Bu belge, LogisticSearch webcrawler hattı için kanonik işlenmiş-veri depolama katmanı politikasını tanımlar.

Belge, üç farklı depolama konusunu açık biçimde ayırmak için vardır:

- host-local crawler çalışma yüzeyi
- birincil çıkarılabilir işlenmiş-veri yüzeyi
- geçici fallback işlenmiş-veri yüzeyi

Bu belge bir politika ve sözleşme yüzeyidir. Bir runbook değildir ve bir implementation betiği değildir.

## Scope

This policy applies only to processed / normalized / pre-ranked crawler output handling on Pi51.

It does not replace the already-established host-native crawler roots under `/srv/crawler/logisticsearch`.

It also does not redefine database storage under `/srv` for PostgreSQL/PostGIS or other local host services.

## Kapsam

Bu politika yalnızca Pi51 üzerindeki işlenmiş / normalize edilmiş / pre-ranked crawler çıktısı yönetimine uygulanır.

Halihazırda kurulmuş olan `/srv/crawler/logisticsearch` altındaki host-native crawler köklerini değiştirmez.

Ayrıca PostgreSQL/PostGIS veya diğer yerel host servisleri için `/srv` altındaki veritabanı depolamasını yeniden tanımlamaz.

## Canonical storage roles

The canonical storage roles are:

- `/srv/crawler/logisticsearch`
  The host-local crawler runtime and working surface.
  Raw crawl state, crawler runtime state, local pipeline state, temporary host-native operational artefacts, and other non-removable working surfaces remain here unless a later sealed document explicitly changes that rule.

- `/srv/data`
  The primary storage target for processed and pre-ranked useful output that is intended to persist on the primary removable data disk.

- `/srv/buffer`
  The temporary fallback storage target for processed and pre-ranked useful output when `/srv/data` is not currently usable.

## Kanonik depolama rolleri

Kanonik depolama rolleri şunlardır:

- `/srv/crawler/logisticsearch`
  Host-local crawler runtime ve çalışma yüzeyidir.
  Ham crawl durumu, crawler runtime durumu, yerel pipeline durumu, geçici host-native operasyon artıkları ve çıkarılabilir olmayan diğer çalışma yüzeyleri, daha sonra mühürlenecek başka bir belge bu kuralı açıkça değiştirmedikçe burada kalır.

- `/srv/data`
  Birincil çıkarılabilir veri diski üzerinde kalıcı tutulması amaçlanan işlenmiş ve pre-ranked faydalı çıktı için birincil depolama hedefidir.

- `/srv/buffer`
  `/srv/data` o anda kullanılabilir değilse, işlenmiş ve pre-ranked faydalı çıktı için geçici fallback depolama hedefidir.

## Detailed reading of `/srv/crawler/logisticsearch`

`/srv/crawler/logisticsearch` must be read as the host-local **umbrella crawler root**, not as a single flat dump directory.

That means this path is the parent operational root under which narrower crawler-local subpaths may exist for different purposes.

Current narrow operational reading:

- when someone says “the webcrawler stores first unprocessed data under `/srv/crawler/logisticsearch`”, that statement is broadly true at the root level
- but the current first real raw HTTP response-body artefacts are not meant to be written loosely anywhere under that tree
- instead, they currently belong under the more specific child path `/srv/crawler/logisticsearch/raw_fetch`

So the correct relationship is:

- `/srv/crawler/logisticsearch`
  the broader host-local crawler runtime and working root

- `/srv/crawler/logisticsearch/raw_fetch`
  the currently visible dedicated child location for raw fetched HTTP body artefacts

This distinction matters because the parent path expresses storage **class**, while the child path expresses a more specific **artifact role**.

## `/srv/crawler/logisticsearch` yolunun ayrıntılı okuması

`/srv/crawler/logisticsearch`, tek ve düz bir dump dizini gibi değil, host-local **şemsiye crawler kökü** olarak okunmalıdır.

Yani bu yol, farklı amaçlar için daha dar crawler-local alt yolların bulunabileceği üst operasyon köküdür.

Güncel dar operasyon okuması şudur:

- biri “webcrawler ilk işlenmemiş veriyi `/srv/crawler/logisticsearch` altına kaydeder” dediğinde bu ifade kök-seviye açısından genel olarak doğrudur
- ancak ilk gerçek ham HTTP response-body artıkları bu ağacın herhangi bir yerine dağınık biçimde yazılmak için düşünülmemektedir
- bunun yerine şu anda daha özel çocuk yol olan `/srv/crawler/logisticsearch/raw_fetch` altına aittir

Dolayısıyla doğru ilişki şudur:

- `/srv/crawler/logisticsearch`
  daha geniş host-local crawler runtime ve çalışma kökü

- `/srv/crawler/logisticsearch/raw_fetch`
  ham fetch edilmiş HTTP body artıkları için şu anda görünür olan dedicated çocuk konum

Bu ayrım önemlidir; çünkü üst yol depolama **sınıfını**, alt yol ise daha özel bir **artefact rolünü** ifade eder.

## Detailed role of `/srv/crawler/logisticsearch/raw_fetch`

`/srv/crawler/logisticsearch/raw_fetch` is the current dedicated on-host location for the first durable raw-fetch body artefacts produced by real page-fetch work.

Its role is intentionally narrow.

It exists so the crawler can preserve the fetched HTTP response body in a host-local raw form before later layers do any of the following:

- parse the content
- normalize it
- classify it
- derive processed evidence from it
- emit processed or pre-ranked useful output

So `raw_fetch` is **not** the same thing as:

- processed output storage
- normalized output storage
- pre-ranked useful output storage
- removable-disk persistence tier
- `/srv/data`
- `/srv/buffer`

It is part of the raw/working crawler-local runtime surface.

## `/srv/crawler/logisticsearch/raw_fetch` yolunun ayrıntılı rolü

`/srv/crawler/logisticsearch/raw_fetch`, gerçek sayfa fetch işi tarafından üretilen ilk kalıcı ham-fetch body artıkları için mevcut dedicated host-üzeri konumdur.

Rolü bilinçli olarak dardır.

Bu yol, crawler’ın fetch edilmiş HTTP response body’sini daha sonraki katmanlar aşağıdakilerden herhangi birini yapmadan önce host-local ham biçimde koruyabilmesi için vardır:

- içeriği parse etmek
- normalize etmek
- sınıflandırmak
- ondan işlenmiş evidence türetmek
- işlenmiş veya pre-ranked faydalı çıktı üretmek

Dolayısıyla `raw_fetch` şu şeylerle **aynı şey değildir**:

- işlenmiş çıktı depolaması
- normalize edilmiş çıktı depolaması
- pre-ranked faydalı çıktı depolaması
- çıkarılabilir disk kalıcılık katmanı
- `/srv/data`
- `/srv/buffer`

Bu yol, ham/çalışma crawler-local runtime yüzeyinin bir parçasıdır.

## Boundary between raw crawler storage and processed-data tiers

The canonical storage reading must remain simple:

- raw crawler-local artefacts stay under the host-local crawler root
- the currently visible raw fetched HTTP bodies live under `/srv/crawler/logisticsearch/raw_fetch`
- processed and pre-ranked useful output belongs to `/srv/data` when usable
- processed and pre-ranked useful output falls back to `/srv/buffer` only when `/srv/data` is not currently usable

Therefore the current narrow policy reading is:

1. real fetched raw body -> host-local raw crawler surface
2. later processed / normalized / pre-ranked useful output -> removable processed-data tiers
3. never silently blur those two classes together

## Ham crawler depolaması ile işlenmiş-veri katmanları arasındaki sınır

Kanonik depolama okuması sade kalmalıdır:

- ham crawler-local artıkları host-local crawler kökü altında kalır
- şu anda görünür ham fetch edilmiş HTTP body’leri `/srv/crawler/logisticsearch/raw_fetch` altında yaşar
- işlenmiş ve pre-ranked faydalı çıktı kullanılabiliyorsa `/srv/data` yoluna aittir
- işlenmiş ve pre-ranked faydalı çıktı yalnızca `/srv/data` o anda kullanılamıyorsa `/srv/buffer` yoluna düşer

Bu nedenle güncel dar politika okuması şudur:

1. gerçek fetch edilmiş ham body -> host-local ham crawler yüzeyi
2. daha sonraki işlenmiş / normalize edilmiş / pre-ranked faydalı çıktı -> çıkarılabilir işlenmiş-veri katmanları
3. bu iki sınıfı asla sessizce birbirine karıştırma

## What this policy does and does not freeze about the raw root

This policy now makes the following current truth explicit:

- `/srv/crawler/logisticsearch` is the broad crawler-local parent root
- `/srv/crawler/logisticsearch/raw_fetch` is the currently visible dedicated raw-body child path
- `/srv/data` and `/srv/buffer` are processed-data decision targets, not raw-fetch targets

But this policy still does **not** freeze every future child directory under `/srv/crawler/logisticsearch`.

Later sealed documents may still define additional sibling subpaths under that same parent root for other crawler-local purposes, as long as they do not violate the raw-versus-processed separation rule.

## Bu politikanın ham kök hakkında neyi sabitlediği ve sabitlemediği

Bu politika artık şu güncel doğruları açık hale getirir:

- `/srv/crawler/logisticsearch` geniş crawler-local üst köktür
- `/srv/crawler/logisticsearch/raw_fetch` şu anda görünür dedicated ham-body çocuk yoludur
- `/srv/data` ve `/srv/buffer` ham-fetch hedefi değil, işlenmiş-veri karar hedefleridir

Ancak bu politika hâlâ `/srv/crawler/logisticsearch` altındaki gelecekteki her çocuk dizini sabitlemez.

Daha sonra mühürlenecek belgeler, ham-versus-işlenmiş ayrım kuralını ihlal etmedikleri sürece aynı üst kök altında başka crawler-local amaçlar için ek kardeş alt yollar yine tanımlayabilir.

## Primary decision rule

The crawler system must prefer `/srv/data` for processed and pre-ranked useful output whenever all of the following are true:

- the primary data disk is attached
- `/srv/data` is mounted
- the mount is writable
- the disk is not considered full by the later implementation threshold
- no active buffer-drain operation is blocking normal writes

## Birincil karar kuralı

Crawler sistemi, aşağıdaki koşulların tümü doğru olduğunda işlenmiş ve pre-ranked faydalı çıktı için `/srv/data` yolunu tercih etmelidir:

- birincil veri diski takılıdır
- `/srv/data` mount edilmiştir
- mount yazılabilirdir
- disk, daha sonra implementation eşiği ile dolu kabul edilmiyordur
- aktif bir buffer-drain işlemi normal yazmayı engellemiyordur

## Fallback decision rule

The crawler system must route processed and pre-ranked useful output to `/srv/buffer` whenever `/srv/data` is not currently usable.

This includes at least these states:

- the primary data disk is detached
- `/srv/data` is missing or not mounted
- the mount is read-only
- the mount is unhealthy
- the mount is considered full by the later implementation threshold

## Fallback karar kuralı

Crawler sistemi, `/srv/data` o anda kullanılamıyorsa işlenmiş ve pre-ranked faydalı çıktıyı `/srv/buffer` yoluna yönlendirmelidir.

Bu durum en azından şu halleri kapsar:

- birincil veri diski çıkarılmıştır
- `/srv/data` yoktur veya mount edilmemiştir
- mount salt-okunurdur
- mount sağlıksızdır
- mount, daha sonra implementation eşiği ile dolu kabul edilmektedir

## Buffer drain priority rule

When `/srv/data` becomes usable again, buffered processed data in `/srv/buffer` must be drained back to `/srv/data` before the system resumes ordinary processed-data writes to `/srv/data`.

This means buffered backlog has priority over new normal processed-data placement.

## Buffer drain öncelik kuralı

`/srv/data` yeniden kullanılabilir hale geldiğinde, sistem `/srv/data` içine normal işlenmiş-veri yazımına dönmeden önce `/srv/buffer` içindeki birikmiş işlenmiş veriyi tekrar `/srv/data` yönüne boşaltmalıdır.

Yani buffered backlog, yeni normal işlenmiş-veri yerleşiminden daha önceliklidir.

## Crawler pause rule during drain

During the controlled drain from `/srv/buffer` to `/srv/data`, the crawler must enter a short controlled pause window.

The reason is operational consistency:

- prevent new processed-data writes from racing with drain movement
- reduce placement ambiguity during reconciliation
- keep the storage decision model simple and auditable

The exact pause mechanism and exact timeout values belong to later implementation work and must be sealed separately.

## Drain sırasındaki crawler pause kuralı

`/srv/buffer` konumundan `/srv/data` konumuna yapılan kontrollü boşaltma sırasında crawler kısa ve kontrollü bir pause penceresine girmelidir.

Gerekçe operasyonel tutarlılıktır:

- yeni işlenmiş-veri yazımlarının drain taşıması ile yarışmasını önlemek
- uzlaştırma sırasında yerleşim belirsizliğini azaltmak
- depolama karar modelini basit ve denetlenebilir tutmak

Kesin pause mekanizması ve kesin timeout değerleri daha sonraki implementation işine aittir ve ayrı şekilde mühürlenmelidir.

## Role of the two removable disks

The removable disk roles are intentionally asymmetric:

- the 1 TB disk is the primary processed-data target behind `/srv/data`
- the 512 GB disk is the temporary fallback target behind `/srv/buffer`

The 512 GB disk does not replace the 1 TB disk as the desired steady-state destination.
Its role is temporary continuity, not primary permanence.

## İki çıkarılabilir diskin rolü

Çıkarılabilir disk rolleri bilinçli olarak asimetriktir:

- 1 TB disk, `/srv/data` arkasındaki birincil işlenmiş-veri hedefidir
- 512 GB disk, `/srv/buffer` arkasındaki geçici fallback hedefidir

512 GB disk, istenen steady-state hedef olarak 1 TB diskin yerini almaz.
Onun rolü birincil kalıcılık değil, geçici sürekliliktir.

## Raw-data separation rule

Raw crawl data must not be moved to the removable processed-data tiers by default.

The processed-data tier policy exists for processed and pre-ranked useful output.
Raw crawler state and raw crawl artefacts must remain separated unless a later sealed document explicitly defines a different rule.

## Ham-veri ayrım kuralı

Ham crawl verisi varsayılan olarak çıkarılabilir işlenmiş-veri katmanlarına taşınmamalıdır.

İşlenmiş-veri katmanı politikası, işlenmiş ve pre-ranked faydalı çıktı içindir.
Ham crawler durumu ve ham crawl artıkları, daha sonra mühürlenecek başka bir belge farklı bir kural tanımlamadıkça ayrı kalmalıdır.

## What this document does not fix yet

This document does not yet freeze:

- filesystem type
- partition table choice
- UUID values
- mount options
- disk health thresholds
- fullness thresholds
- drain trigger implementation details
- pause/resume code path details
- systemd unit names
- Python module names

Those belong to later implementation and validation steps.

## Bu belgenin henüz sabitlemediği şeyler

Bu belge henüz şunları sabitlemez:

- filesystem türü
- partition table seçimi
- UUID değerleri
- mount seçenekleri
- disk sağlık eşikleri
- doluluk eşikleri
- drain tetikleme implementation ayrıntıları
- pause/resume kod yolu ayrıntıları
- systemd unit isimleri
- Python modül isimleri

Bunlar daha sonraki implementation ve doğrulama adımlarına aittir.

## Required next implementation sequence

The next implementation sequence should remain disciplined:

1. identify the correct physical disks safely on Pi51
2. format them only after safe identity confirmation
3. mount them into the canonical paths
4. verify writable behavior and detach/reattach behavior
5. implement automatic routing logic for `/srv/data` and `/srv/buffer`
6. implement controlled drain behavior
7. implement crawler short-pause integration during drain
8. validate the working system
9. write the runbook after the implementation is real and validated

## Gerekli sonraki implementation sırası

Sonraki implementation sırası disiplinli biçimde şöyle kalmalıdır:

1. Pi51 üzerinde doğru fiziksel diskleri güvenli şekilde kimliklendir
2. ancak güvenli kimlik doğrulamasından sonra formatla
3. diskleri kanonik path'lere mount et
4. yazılabilir davranışı ve çıkar/tak davranışını doğrula
5. `/srv/data` ve `/srv/buffer` için otomatik yönlendirme mantığını uygula
6. kontrollü drain davranışını uygula
7. drain sırasında crawler kısa-pause entegrasyonunu uygula
8. çalışan sistemi doğrula
9. implementation gerçek ve doğrulanmış olduktan sonra runbook yaz

## Related runbook

The action-layer companion for this policy is:

- `docs/SECTION1_WEBCRAWLER_RUNBOOK_PROCESSED_DATA_STORAGE_TIER_FORMAT_AND_MOUNT.md`

## İlgili runbook

Bu politikanın action-layer eşi şudur:

- `docs/SECTION1_WEBCRAWLER_RUNBOOK_PROCESSED_DATA_STORAGE_TIER_FORMAT_AND_MOUNT.md`

