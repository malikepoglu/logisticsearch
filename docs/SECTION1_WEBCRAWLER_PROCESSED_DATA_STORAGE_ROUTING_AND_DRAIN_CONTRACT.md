# SECTION1_WEBCRAWLER_PROCESSED_DATA_STORAGE_ROUTING_AND_DRAIN_CONTRACT

Documentation hub:

* `docs/README.md` — documentation hub
* `README.md` — repository root surface

Dokümantasyon merkezi:

* `docs/README.md` — dokümantasyon merkezi
* `README.md` — repository kök yüzeyi

## Purpose

This document defines the canonical behavior contract for processed-data storage routing, buffer-drain behavior, and storage-class crawler pause behavior in the LogisticSearch webcrawler line.

This contract exists to bridge the gap between:

- the processed-data storage tier policy
- the executed storage-tier mount reality
- the future Python/service-layer implementation

This document is a behavior contract.
It is not a runbook and it is not an implementation file.

## Amaç

Bu belge, LogisticSearch webcrawler hattında işlenmiş-veri depolama yönlendirmesi, buffer-drain davranışı ve storage-sınıfı crawler pause davranışı için kanonik davranış sözleşmesini tanımlar.

Bu sözleşme şu üç şey arasındaki boşluğu kapatmak için vardır:

- işlenmiş-veri depolama katmanı politikası
- uygulanmış storage-tier mount gerçeği
- gelecekteki Python/service-layer implementation'ı

Bu belge bir davranış sözleşmesidir.
Bir runbook değildir ve bir implementation dosyası değildir.

## Related canonical surfaces

This contract must be read together with:

- `docs/SECTION1_WEBCRAWLER_PROCESSED_DATA_STORAGE_TIER_POLICY.md`
- `docs/SECTION1_WEBCRAWLER_RUNBOOK_PROCESSED_DATA_STORAGE_TIER_FORMAT_AND_MOUNT.md`
- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_CONTROLS.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`

## İlgili kanonik yüzeyler

Bu sözleşme şu yüzeylerle birlikte okunmalıdır:

- `docs/SECTION1_WEBCRAWLER_PROCESSED_DATA_STORAGE_TIER_POLICY.md`
- `docs/SECTION1_WEBCRAWLER_RUNBOOK_PROCESSED_DATA_STORAGE_TIER_FORMAT_AND_MOUNT.md`
- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_CONTROLS.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`

## Scope

This contract applies only to processed and pre-ranked useful output placement behavior.

It does not apply to:

- raw crawl storage placement
- PostgreSQL data placement
- shutdown-class drain semantics
- reboot or poweroff semantics
- lease ownership rules
- host politeness backoff rules

## Kapsam

Bu sözleşme yalnızca işlenmiş ve pre-ranked faydalı çıktının yerleşim davranışına uygulanır.

Şunlara uygulanmaz:

- ham crawl depolama yerleşimi
- PostgreSQL veri yerleşimi
- shutdown-sınıfı drain semantiği
- reboot veya poweroff semantiği
- lease ownership kuralları
- host politeness backoff kuralları

## Canonical live storage truth assumed by this contract

The contract assumes the current live mounted storage truth is:

- `/srv/data`
  primary removable processed-data target

- `/srv/buffer`
  temporary removable fallback target

The contract also assumes that `/srv` on internal NVMe remains the host-local operational surface and is not itself the processed-data routing target defined here.

## Bu sözleşmenin varsaydığı kanonik canlı depolama doğrusu

Bu sözleşme mevcut canlı mount edilmiş depolama doğrusunun şu olduğunu varsayar:

- `/srv/data`
  birincil çıkarılabilir işlenmiş-veri hedefi

- `/srv/buffer`
  geçici çıkarılabilir fallback hedefi

Bu sözleşme ayrıca iç NVMe üzerindeki `/srv` yüzeyinin host-local operasyon yüzeyi olarak kaldığını ve burada tanımlanan işlenmiş-veri yönlendirme hedefinin kendisi olmadığını varsayar.

## Required observable inputs

Any later Python or service-layer implementation must make storage-routing decisions from observable state, not from wishful assumptions.

At minimum the behavior decision layer must be able to observe:

- whether `/srv/data` exists
- whether `/srv/data` is mounted
- whether `/srv/data` is writable
- whether `/srv/buffer` exists
- whether `/srv/buffer` is mounted
- whether `/srv/buffer` is writable
- whether buffered backlog currently exists
- whether a storage drain is already in progress
- whether storage-class pause is currently active

## Gerekli gözlenebilir girdiler

Daha sonraki herhangi bir Python veya service-layer implementation'ı depolama yönlendirme kararlarını temennilere göre değil, gözlenebilir duruma göre vermelidir.

Davranış karar katmanı asgari olarak şunları gözleyebilmelidir:

- `/srv/data` mevcut mu
- `/srv/data` mount edilmiş mi
- `/srv/data` yazılabilir mi
- `/srv/buffer` mevcut mu
- `/srv/buffer` mount edilmiş mi
- `/srv/buffer` yazılabilir mi
- buffer backlog şu anda var mı
- bir storage drain zaten sürüyor mu
- storage-sınıfı pause şu anda aktif mi

## Canonical storage routing states

The processed-data routing layer has four canonical behavior states:

1. `route_to_data`
2. `route_to_buffer`
3. `drain_buffer_to_data`
4. `pause_for_storage_reconciliation`

These are behavior states, not necessarily final code enum names.

## Kanonik depolama yönlendirme durumları

İşlenmiş-veri yönlendirme katmanının dört kanonik davranış durumu vardır:

1. `route_to_data`
2. `route_to_buffer`
3. `drain_buffer_to_data`
4. `pause_for_storage_reconciliation`

Bunlar davranış durumlarıdır; zorunlu olarak nihai kod enum isimleri olmak zorunda değildir.

## Primary routing rule

The system must select `route_to_data` only when `/srv/data` is actually usable for normal processed-data writes.

For this contract, “usable” means at least:

- present
- mounted
- writable
- not currently blocked by an active storage-drain cycle

When these conditions are true, new processed-data output should go to `/srv/data`.

## Birincil yönlendirme kuralı

Sistem, `route_to_data` durumunu yalnızca `/srv/data` normal işlenmiş-veri yazımları için gerçekten kullanılabilir olduğunda seçmelidir.

Bu sözleşmede “kullanılabilir” en azından şunları ifade eder:

- mevcut
- mount edilmiş
- yazılabilir
- aktif bir storage-drain döngüsü tarafından o anda engellenmiyor

Bu koşullar doğru olduğunda, yeni işlenmiş-veri çıktısı `/srv/data` yoluna gitmelidir.

## Fallback routing rule

The system must select `route_to_buffer` whenever `/srv/data` is not currently usable but `/srv/buffer` remains usable.

This fallback rule exists for continuity.
It must not silently redefine `/srv/buffer` as the preferred steady-state destination.

## Fallback yönlendirme kuralı

Sistem, `/srv/data` o anda kullanılabilir değilken `/srv/buffer` hâlâ kullanılabilir durumdaysa `route_to_buffer` durumunu seçmelidir.

Bu fallback kuralı süreklilik içindir.
`/srv/buffer` yolunu sessizce tercih edilen steady-state hedef olarak yeniden tanımlamamalıdır.

## Buffer backlog priority rule

If processed-data backlog already exists in `/srv/buffer` and `/srv/data` becomes usable again, the system must not immediately resume ordinary new writes to `/srv/data`.

Instead, backlog reconciliation has priority.

The system must transition toward controlled drain behavior before normal steady-state placement is resumed.

## Buffer backlog öncelik kuralı

Eğer `/srv/buffer` içinde zaten işlenmiş-veri backlog'u varsa ve `/srv/data` yeniden kullanılabilir hale gelirse, sistem normal yeni yazımlara hemen `/srv/data` üzerinde geri dönmemelidir.

Bunun yerine backlog uzlaştırması önceliklidir.

Sistem, normal steady-state yerleşime dönmeden önce kontrollü drain davranışına geçmelidir.

## Storage drain rule

The canonical storage-drain behavior is:

- source: `/srv/buffer`
- destination: `/srv/data`

This drain is not a shutdown-class drain.
It is a storage reconciliation drain.

Its purpose is to move buffered processed-data backlog back into the primary processed-data tier.

## Storage drain kuralı

Kanonik storage-drain davranışı şudur:

- kaynak: `/srv/buffer`
- hedef: `/srv/data`

Bu drain, shutdown-sınıfı bir drain değildir.
Bu bir storage reconciliation drain davranışıdır.

Amacı, buffer içinde birikmiş işlenmiş-veri backlog'unu birincil işlenmiş-veri katmanına geri taşımaktır.

## Storage pause rule during storage drain

During `drain_buffer_to_data`, the crawler must enter `pause_for_storage_reconciliation`.

This pause is required to prevent ambiguous mixed placement during reconciliation.

The required behavioral effect is:

- do not emit new normal processed-data writes to either steady-state route while storage reconciliation is active
- allow the controlled storage backlog movement to complete first
- return to ordinary routing only after the storage-drain phase finishes cleanly

## Storage drain sırasındaki storage pause kuralı

`drain_buffer_to_data` sırasında crawler `pause_for_storage_reconciliation` durumuna girmelidir.

Bu pause, uzlaştırma sırasında belirsiz karışık yerleşimi önlemek için gereklidir.

Gerekli davranış etkisi şudur:

- storage reconciliation aktifken yeni normal işlenmiş-veri yazımlarını iki steady-state rota üzerinden de üretme
- kontrollü storage backlog taşımasının önce tamamlanmasına izin ver
- ancak storage-drain evresi temiz biçimde bittikten sonra normal yönlendirmeye dön

## Separation from shutdown drain semantics

This contract must remain separate from shutdown-class drain semantics.

The canonical shutdown/drain document governs graceful stop behavior.
This storage routing contract governs processed-data placement reconciliation.

They may interact in the future, but they are not the same behavior class.

## Shutdown drain semantiğinden ayrım

Bu sözleşme shutdown-sınıfı drain semantiğinden ayrı kalmalıdır.

Kanonik shutdown/drain dokümanı graceful stop davranışını yönetir.
Bu storage routing sözleşmesi ise işlenmiş-veri yerleşim uzlaştırmasını yönetir.

Gelecekte etkileşebilirler, ancak aynı davranış sınıfı değildirler.

## Separation from raw-data placement

Raw crawl data must remain outside this routing contract unless a later sealed document explicitly broadens the scope.

This contract is only for processed and pre-ranked useful output.

## Ham-veri yerleşiminden ayrım

Ham crawl verisi, daha sonra mühürlenecek başka bir belge kapsamı açıkça genişletmedikçe bu yönlendirme sözleşmesinin dışında kalmalıdır.

Bu sözleşme yalnızca işlenmiş ve pre-ranked faydalı çıktı içindir.

## Implementation constraints for later Python code

Any later Python implementation must follow these constraints:

- read live observable state first
- decide the storage routing state explicitly
- keep storage pause separate from shutdown drain intent
- keep raw-data placement out of this behavior path
- avoid silently downgrading steady-state destination from `/srv/data` to `/srv/buffer`
- treat storage drain as a bounded reconciliation phase, not as the new normal

## Daha sonraki Python kodu için implementation kısıtları

Daha sonraki herhangi bir Python implementation'ı şu kısıtlara uymalıdır:

- önce canlı gözlenebilir durumu oku
- depolama yönlendirme durumunu açık biçimde belirle
- storage pause davranışını shutdown drain niyetinden ayrı tut
- ham-veri yerleşimini bu davranış yolunun dışında tut
- steady-state hedefi sessizce `/srv/data` yolundan `/srv/buffer` yoluna düşürme
- storage drain davranışını yeni normal durum olarak değil, sınırlı bir uzlaştırma evresi olarak ele al

## Deliberately unresolved details

This contract does not yet freeze:

- fullness thresholds
- exact backlog detection mechanism
- exact file naming layout inside `/srv/data` or `/srv/buffer`
- exact pause/resume signal transport
- exact service names
- exact Python module names
- exact retry timing around storage availability probing

These belong to later implementation and validation work.

## Bilinçli olarak çözülmemiş ayrıntılar

Bu sözleşme henüz şunları sabitlemez:

- doluluk eşikleri
- kesin backlog tespit mekanizması
- `/srv/data` veya `/srv/buffer` içindeki kesin dosya yerleşim düzeni
- kesin pause/resume sinyal taşıma yöntemi
- kesin servis isimleri
- kesin Python modül isimleri
- depolama kullanılabilirliği sorgulaması etrafındaki kesin retry zamanlaması

Bunlar daha sonraki implementation ve doğrulama işine aittir.

## Required next implementation order

The next disciplined implementation order should be:

1. define the storage status probe surface
2. define the routing decision surface
3. define backlog detection truth
4. define storage-drain controller behavior
5. define storage pause gate behavior for worker/service flow
6. implement the Python-side contract carefully
7. validate with detachable-disk reality
8. only then write the next runbook for the higher-layer storage behavior

## Gerekli sonraki implementation sırası

Sonraki disiplinli implementation sırası şöyle olmalıdır:

1. storage status probe yüzeyini tanımla
2. routing decision yüzeyini tanımla
3. backlog detection doğrusunu tanımla
4. storage-drain controller davranışını tanımla
5. worker/service akışı için storage pause gate davranışını tanımla
6. Python-side sözleşmeyi dikkatlice uygula
7. çıkarılabilir disk gerçeği ile doğrula
8. ancak bundan sonra üst katman storage davranışı için sonraki runbook'u yaz
