"""
EN:
This file is the storage-routing child of the worker-runtime family.

EN:
Why this file exists:
- because storage-specific runtime truth should live in one explicit child instead of being hidden inside the main worker hub
- because storage_plan, route selection, tier choice, drain behavior, processed-data placement, and downstream write intent must remain readable
- because a beginner should be able to find where worker-visible results stop being only parse or taxonomy meaning and start becoming concrete storage routing meaning

EN:
What this file DOES:
- expose storage-oriented runtime helper, class, and payload boundaries
- preserve visible storage_plan, route decision, tier/path selection, drain-aware handling, and degraded branch meaning
- keep storage routing semantics separate from broader worker orchestration, parse logic, and taxonomy logic

EN:
What this file DOES NOT do:
- it does not become the full worker orchestrator
- it does not become the full parse runtime hub
- it does not become the full taxonomy authority
- it does not become the final search-ranking or outreach-decision layer

EN:
Topological role:
- parse and taxonomy related surfaces can shape material that eventually reaches this child
- this file interprets how processed material should be routed toward storage targets, tiers, plans, or drains
- later layers may consume the visible storage-routing outputs to perform durable persistence, export, or downstream movement

EN:
Important visible values and shapes:
- storage_plan => structured statement of how data should be routed or stored
- route or routing payloads => explicit explanation of selected storage direction
- tier/path/device related values => visible indicators for storage destination meaning
- drain-aware or hold/defer related payloads => visible non-happy or controlled-delay storage branches
- degraded branch payloads => explicit non-happy storage-routing outcomes that must remain readable

EN:
Accepted architectural identity:
- storage-routing runtime child
- narrow storage contract layer
- readable parse/taxonomy-to-storage boundary

EN:
Undesired architectural identity:
- hidden second worker hub
- vague filesystem helper dump
- hidden operator CLI surface
- hidden persistence side-effect maze

TR:
Bu dosya worker-runtime ailesinin storage-routing child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü storagea özgü runtime doğrusu ana worker hubının içinde gizlenmek yerine tek ve açık child yüzeyde yaşamalıdır
- çünkü storage_plan, route seçimi, tier tercihi, drain davranışı, processed-data yerleşimi ve downstream write intent anlamı okunabilir kalmalıdır
- çünkü yeni başlayan biri worker-görünür sonuçların nerede yalnızca parse veya taxonomy anlamı olmaktan çıkıp somut storage routing anlamına dönüştüğünü bulabilmelidir

TR:
Bu dosya NE yapar:
- storage odaklı runtime helper, class ve payload sınırlarını açığa çıkarır
- storage_plan, route kararı, tier/path seçimi, drain-aware işleme ve degraded dal anlamını görünür tutar
- storage routing semantiklerini daha geniş worker orkestrasyonundan, parse mantığından ve taxonomy mantığından ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam worker orchestratorun kendisi olmaz
- tam parse runtime hubının kendisi olmaz
- tam taxonomy authoritynin kendisi olmaz
- final search-ranking veya outreach-decision katmanının kendisi olmaz

TR:
Topolojik rol:
- parse ve taxonomy ile ilgili yüzeyler sonunda bu child yüzeye ulaşabilecek malzemeyi şekillendirebilir
- bu dosya işlenmiş malzemenin storage hedeflerine, tierlara, planlara veya drain davranışına nasıl yönlendirileceğini yorumlar
- sonraki katmanlar kalıcı persistence, export veya downstream movement için görünür storage-routing çıktıları tüketebilir

TR:
Önemli görünür değerler ve şekiller:
- storage_plan => verinin nasıl yönlendirileceğini veya saklanacağını anlatan yapılı ifade
- route veya routing payloadları => seçilen storage yönünü açıkça anlatan yapı
- tier/path/device ile ilgili değerler => storage hedef anlamı için görünür göstergeler
- drain-aware veya hold/defer ile ilgili payloadlar => görünür mutlu-yol-dışı veya kontrollü-gecikme storage dalları
- degraded dal payloadları => okunabilir kalması gereken mutlu-yol-dışı storage-routing sonuçları

TR:
Kabul edilen mimari kimlik:
- storage-routing runtime child
- dar storage sözleşme katmanı
- okunabilir parse/taxonomy-to-storage sınırı

TR:
İstenmeyen mimari kimlik:
- gizli ikinci worker hubı
- belirsiz filesystem helper çöplüğü
- gizli operatör CLI yüzeyi
- gizli persistence yan-etki labirenti
"""

# EN: We enable postponed evaluation of annotations so type hints can stay
# EN: readable even when they refer to classes declared later in this file.
# TR: Type hint'ler bu dosyada daha sonra tanımlanan sınıflara referans verse
# TR: bile okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
# EN: STORAGE ROUTING IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the narrow storage corner of the worker corridor.
# EN: Beginner mental model:
# EN: - parse and taxonomy layers shape meaning
# EN: - this child explains how that meaning is routed toward storage destinations or plans
# EN: - it exists so the crawler can later answer: where should this processed material go, on which tier, under which plan, with which visible routing meaning
# EN:
# EN: Accepted architectural meaning:
# EN: - named storage-routing child
# EN: - focused storage-plan and route-decision helper surface
# EN: - readable boundary for processed runtime meaning becoming storage-directed meaning
# EN:
# EN: Undesired architectural meaning:
# EN: - random filesystem helper pile
# EN: - hidden second worker orchestrator
# EN: - place where storage routing failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - storage_plan should stay explicit
# EN: - route and tier decisions should stay structured and readable
# EN: - degraded storage-routing branches must remain visible
# TR: STORAGE ROUTING KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya worker koridorunun dar storage köşesi gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - parse ve taxonomy katmanları anlamı şekillendirir
# TR: - bu child o anlamın storage hedeflerine veya planlarına nasıl yönlendirildiğini açıklar
# TR: - crawlerın daha sonra şu sorulara cevap verebilmesi için vardır: bu işlenmiş malzeme nereye gitmeli, hangi tierda, hangi plan altında, hangi görünür routing anlamıyla
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli storage-routing child
# TR: - odaklı storage-plan ve route-decision yardımcı yüzeyi
# TR: - işlenmiş runtime anlamının storage-yönelimli anlama dönüşmesi için okunabilir sınır
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele filesystem helper yığını
# TR: - gizli ikinci worker orchestrator
# TR: - storage routing hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - storage_plan açık kalmalıdır
# TR: - route ve tier kararları yapılı ve okunabilir kalmalıdır
# TR: - degraded storage-routing dalları görünür kalmalıdır

from __future__ import annotations

# EN: We import dataclass because small structured result objects are much
# EN: clearer than loose tuples or unnamed dictionaries.
# TR: Küçük yapılı sonuç nesneleri dağınık tuple veya isimsiz sözlüklere göre
# TR: çok daha açık olduğu için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import Path because filesystem path work is clearer and safer with
# EN: pathlib objects than with raw strings.
# TR: Filesystem path işlemleri pathlib nesneleriyle ham metinlere göre daha
# TR: açık ve daha güvenli olduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import os because writability checks use operating-system permission
# EN: probing.
# TR: Yazılabilirlik kontrolleri işletim sistemi izin probe'u kullandığı için
# TR: os modülünü içe aktarıyoruz.
import os


# EN: This constant expresses the user's canonical raw/working collection root.
# TR: Bu sabit, kullanıcının kanonik ham/çalışma veri toplama kökünü ifade eder.
RAW_COLLECTION_ROOT = Path("/srv/webcrawler/raw_fetch")

# EN: This constant is the first preferred destination for processed output.
# TR: Bu sabit işlenmiş çıktı için ilk tercih edilen hedeftir.
PROCESSED_PRIMARY_ROOT = Path("/srv/data")

# EN: This constant is the temporary fallback destination for processed output
# EN: when the primary root is not currently usable.
# TR: Bu sabit, birincil kök o anda kullanılamıyorsa işlenmiş çıktı için geçici
# TR: fallback hedeftir.
PROCESSED_FALLBACK_ROOT = Path("/srv/buffer")


# EN: This dataclass stores the observed state of one storage path.
# TR: Bu dataclass tek bir storage path'inin gözlenen durumunu tutar.
@dataclass(slots=True)
# EN: STORAGE CLASS PURPOSE MEMORY BLOCK V6 / StoragePathStatus
# EN:
# EN: Why this class exists:
# EN: - because storage-layer truth for 'StoragePathStatus' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand storage-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named storage payload, route shape, plan structure, or structured result carrier
# EN: - visible field set currently detected here: path, exists, is_dir, is_mount, is_writable, reason
# EN:
# EN: Common storage meaning hints:
# EN: - this surface likely deals with storage planning, route selection, or storage-destination meaning
# EN: - explicit success vs degraded routing meaning may matter here
# EN: - these helpers often decide whether later layers receive usable storage-shaped routing payloads
# EN: - visible routed vs deferred distinction is especially important here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no storage contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: STORAGE CLASS AMAÇ HAFIZA BLOĞU V6 / StoragePathStatus
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'StoragePathStatus' için storage katmanı doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip storage tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli storage payloadı, route şekli, plan yapısı veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: path, exists, is_dir, is_mount, is_writable, reason
# TR:
# TR: Ortak storage anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle storage planlama, route seçimi veya storage hedef anlamı ile ilgilenir
# TR: - açık success vs degraded routing anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir storage şekilli routing payload alıp almayacağını belirler
# TR: - görünür routed vs deferred ayrımı burada özellikle önemlidir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı storage sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

# EN: StoragePathStatus is the structured storage-path probe result container for this storage-routing child.
# TR: StoragePathStatus bu storage-routing child yuzeyi icin yapili storage-path probe sonucu kapsayicisidir.
class StoragePathStatus:
    # EN: path is the filesystem path that was checked.
    # TR: path kontrol edilen filesystem path'idir.
    path: str

    # EN: exists tells whether the path exists at all.
    # TR: exists path'in hiç var olup olmadığını söyler.
    exists: bool

    # EN: is_dir tells whether the path is a directory.
    # TR: is_dir path'in bir dizin olup olmadığını söyler.
    is_dir: bool

    # EN: is_mount tells whether the path is currently a mountpoint.
    # TR: is_mount path'in şu anda bir mountpoint olup olmadığını söyler.
    is_mount: bool

    # EN: is_writable tells whether the current process appears able to write there.
    # TR: is_writable mevcut sürecin oraya yazabiliyor görünüp görünmediğini söyler.
    is_writable: bool

    # EN: reason stores a short explanation when the path is not usable.
    # TR: reason path kullanılamıyorsa kısa açıklama nedenini tutar.
    reason: str | None


# EN: This dataclass stores the minimal final storage decision for processed output.
# TR: Bu dataclass işlenmiş çıktı için asgari nihai storage kararını tutar.
@dataclass(slots=True)
# EN: STORAGE CLASS PURPOSE MEMORY BLOCK V6 / ProcessedOutputPlan
# EN:
# EN: Why this class exists:
# EN: - because storage-layer truth for 'ProcessedOutputPlan' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand storage-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named storage payload, route shape, plan structure, or structured result carrier
# EN: - visible field set currently detected here: raw_collection_root, processed_output_root, using_fallback, buffer_backlog_present, drain_buffer_to_data_first, pause_crawler, primary_status, fallback_status, explanation
# EN:
# EN: Common storage meaning hints:
# EN: - this surface likely shapes drain-aware, hold, defer, or plan-related routing payloads
# EN: - explicit payload structure is often important for audits and later export/persistence layers
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no storage contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: STORAGE CLASS AMAÇ HAFIZA BLOĞU V6 / ProcessedOutputPlan
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'ProcessedOutputPlan' için storage katmanı doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip storage tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli storage payloadı, route şekli, plan yapısı veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: raw_collection_root, processed_output_root, using_fallback, buffer_backlog_present, drain_buffer_to_data_first, pause_crawler, primary_status, fallback_status, explanation
# TR:
# TR: Ortak storage anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle drain-aware, hold, defer veya planla ilgili routing payloadlarını şekillendirir
# TR: - açık payload yapısı çoğu zaman denetimler ve sonraki export/persistence katmanları için önemlidir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı storage sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

# EN: ProcessedOutputPlan is the structured processed-output routing plan container returned by storage-routing decisions.
# TR: ProcessedOutputPlan storage-routing kararlarinin dondurdugu yapili processed-output routing plani kapsayicisidir.
class ProcessedOutputPlan:
    # EN: raw_collection_root is the canonical place where raw evidence
    # EN: accumulation lives.
    # TR: raw_collection_root ham kanıtın bulunduğu kanonik yerdir.
    raw_collection_root: str

    # EN: processed_output_root is the selected destination for normal processed
    # EN: output writes. It becomes None when crawler must pause first.
    # TR: processed_output_root normal işlenmiş çıktı yazımları için seçilen
    # TR: hedeftir. Crawler önce pause olmak zorundaysa None olur.
    processed_output_root: str | None

    # EN: using_fallback tells whether /srv/buffer was selected for normal writes.
    # TR: using_fallback normal yazımlar için /srv/buffer seçilip seçilmediğini söyler.
    using_fallback: bool

    # EN: buffer_backlog_present tells whether /srv/buffer currently appears to
    # EN: contain buffered processed-output backlog.
    # TR: buffer_backlog_present /srv/buffer içinde şu anda buffer işlenmiş çıktı
    # TR: backlog'u var görünüp görünmediğini söyler.
    buffer_backlog_present: bool

    # EN: drain_buffer_to_data_first tells whether buffered backlog must be fully
    # EN: moved into /srv/data before crawler resumes normal processed writes.
    # TR: drain_buffer_to_data_first buffer backlog'unun crawler normal işlenmiş
    # TR: yazımlara dönmeden önce tamamen /srv/data tarafına taşınması gerekip
    # TR: gerekmediğini söyler.
    drain_buffer_to_data_first: bool

    # EN: pause_crawler tells whether crawler must pause instead of continuing
    # EN: normal processed-output emission.
    # TR: pause_crawler crawler'ın normal işlenmiş çıktı üretimine devam etmek
    # TR: yerine pause olması gerekip gerekmediğini söyler.
    pause_crawler: bool

    # EN: primary_status is the observed live state of /srv/data.
    # TR: primary_status /srv/data yolunun gözlenen canlı durumudur.
    primary_status: StoragePathStatus

    # EN: fallback_status is the observed live state of /srv/buffer.
    # TR: fallback_status /srv/buffer yolunun gözlenen canlı durumudur.
    fallback_status: StoragePathStatus

    # EN: explanation stores a short human-readable explanation of the decision.
    # TR: explanation kararın kısa insan-okunur açıklamasını tutar.
    explanation: str


# EN: This helper probes one filesystem path conservatively without creating
# EN: files or mutating any live state.
# TR: Bu yardımcı tek bir filesystem path'ini dosya oluşturmadan ve canlı durumu
# TR: değiştirmeden muhafazakâr biçimde probe eder.
# EN: STORAGE FUNCTION PURPOSE MEMORY BLOCK V6 / probe_storage_path
# EN:
# EN: Why this function exists:
# EN: - because storage truth for 'probe_storage_path' should be exposed through one named top-level helper boundary
# EN: - because storage-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: path
# EN: - values should match the current Python signature and the storage-routing contract below
# EN:
# EN: Accepted output:
# EN: - a storage-oriented result shape defined by the current function body
# EN: - this may be a storage plan, route result, tier/path selection shape, drain-related payload, or another explicit storage-side branch result
# EN:
# EN: Common storage meaning hints:
# EN: - this surface likely deals with storage planning, route selection, or storage-destination meaning
# EN: - explicit success vs degraded routing meaning may matter here
# EN: - these helpers often decide whether later layers receive usable storage-shaped routing payloads
# EN: - visible routed vs deferred distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is storage-side helper logic, not the whole worker corridor
# EN: - storage results must stay explicit so audits can understand success, degraded, deferred, and downstream persistence meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague storage results that hide branch meaning
# TR: STORAGE FUNCTION AMAÇ HAFIZA BLOĞU V6 / probe_storage_path
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'probe_storage_path' için storage doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü storage tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: path
# TR: - değerler aşağıdaki mevcut Python imzası ve storage-routing sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen storage odaklı sonuç şekli
# TR: - bu; storage planı, route sonucu, tier/path seçim şekli, drain ile ilgili payload veya başka açık storage tarafı dal sonucu olabilir
# TR:
# TR: Ortak storage anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle storage planlama, route seçimi veya storage hedef anlamı ile ilgilenir
# TR: - açık success vs degraded routing anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir storage şekilli routing payload alıp almayacağını belirler
# TR: - görünür routed vs deferred ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon storage tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - storage sonuçları açık kalmalıdır ki denetimler success, degraded, deferred ve downstream persistence anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz storage sonuçları

# EN: probe_storage_path inspects the path parameter and returns a structured StoragePathStatus for that filesystem target.
# TR: probe_storage_path path parametresini inceler ve o filesystem hedefi icin yapili bir StoragePathStatus dondurur.
def probe_storage_path(path: Path) -> StoragePathStatus:
    # EN: We first ask whether the path exists because all later checks depend on it.
    # TR: Tüm sonraki kontroller buna bağlı olduğu için önce path'in var olup
    # TR: olmadığına bakıyoruz.
    exists = path.exists()

    # EN: We only ask whether it is a directory if it exists.
    # TR: Bunun dizin olup olmadığını yalnızca mevcutsa soruyoruz.
# EN: is_dir stores whether path currently resolves to a directory shape.
# TR: is_dir path degerinin su anda bir dizin sekline cozumlenip cozumlenmedigini tasir.
    is_dir = path.is_dir() if exists else False

    # EN: We only ask whether it is a mountpoint if it exists.
    # TR: Bunun mountpoint olup olmadığını yalnızca mevcutsa soruyoruz.
# EN: is_mount stores whether path currently appears as a mounted filesystem boundary.
# TR: is_mount path degerinin su anda mount edilmis bir filesystem siniri olarak gorunup gorunmedigini tasir.
    is_mount = path.is_mount() if exists else False

    # EN: We consider the path writable only when it exists, is a directory,
    # EN: is mounted, and current process permissions allow writing.
    # TR: Bir path'i ancak mevcutsa, dizinse, mounted ise ve mevcut süreç izinleri
    # TR: yazmaya izin veriyorsa yazılabilir kabul ediyoruz.
# EN: is_writable stores whether the current process can write to the accepted path shape.
# TR: is_writable mevcut surecin kabul edilen path sekline yazip yazamadigini tasir.
    is_writable = bool(
        exists
        and is_dir
        and is_mount
        and os.access(path, os.W_OK)
    )

    # EN: We derive one short reason for non-usable states.
    # TR: Kullanılamayan durumlar için tek bir kısa neden türetiyoruz.
    if not exists:
# EN: reason records the first non-usable branch as path_missing for operator-visible routing truth.
# TR: reason operatorun gorecegi routing dogrusu icin ilk kullanilamaz dali path_missing olarak kaydeder.
        reason = "path_missing"
    elif not is_dir:
# EN: reason records the first non-usable branch as not_a_directory for operator-visible routing truth.
# TR: reason operatorun gorecegi routing dogrusu icin ilk kullanilamaz dali not_a_directory olarak kaydeder.
        reason = "not_a_directory"
    elif not is_mount:
# EN: reason records the first non-usable branch as not_mounted for operator-visible routing truth.
# TR: reason operatorun gorecegi routing dogrusu icin ilk kullanilamaz dali not_mounted olarak kaydeder.
        reason = "not_mounted"
    elif not is_writable:
# EN: reason records the first non-usable branch as not_writable for operator-visible routing truth.
# TR: reason operatorun gorecegi routing dogrusu icin ilk kullanilamaz dali not_writable olarak kaydeder.
        reason = "not_writable"
    else:
# EN: reason records None only when no non-usable branch remains and the path is usable.
# TR: reason yalnizca kullanilamaz dal kalmadiginda ve path kullanilabilir oldugunda None degerini kaydeder.
        reason = None

    # EN: We return one explicit structured status object.
    # TR: Tek bir açık yapılı durum nesnesi döndürüyoruz.
    return StoragePathStatus(
        path=str(path),
        exists=exists,
        is_dir=is_dir,
        is_mount=is_mount,
        is_writable=is_writable,
        reason=reason,
    )


# EN: This helper decides whether a probed path is usable for normal processed
# EN: output writes.
# TR: Bu yardımcı probe edilmiş bir path'in normal işlenmiş çıktı yazımları için
# TR: kullanılabilir olup olmadığını belirler.
# EN: STORAGE FUNCTION PURPOSE MEMORY BLOCK V6 / path_is_usable
# EN:
# EN: Why this function exists:
# EN: - because storage truth for 'path_is_usable' should be exposed through one named top-level helper boundary
# EN: - because storage-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: status
# EN: - values should match the current Python signature and the storage-routing contract below
# EN:
# EN: Accepted output:
# EN: - a storage-oriented result shape defined by the current function body
# EN: - this may be a storage plan, route result, tier/path selection shape, drain-related payload, or another explicit storage-side branch result
# EN:
# EN: Common storage meaning hints:
# EN: - this surface likely deals with storage planning, route selection, or storage-destination meaning
# EN: - explicit success vs degraded routing meaning may matter here
# EN: - these helpers often decide whether later layers receive usable storage-shaped routing payloads
# EN: - visible routed vs deferred distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is storage-side helper logic, not the whole worker corridor
# EN: - storage results must stay explicit so audits can understand success, degraded, deferred, and downstream persistence meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague storage results that hide branch meaning
# TR: STORAGE FUNCTION AMAÇ HAFIZA BLOĞU V6 / path_is_usable
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'path_is_usable' için storage doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü storage tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: status
# TR: - değerler aşağıdaki mevcut Python imzası ve storage-routing sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen storage odaklı sonuç şekli
# TR: - bu; storage planı, route sonucu, tier/path seçim şekli, drain ile ilgili payload veya başka açık storage tarafı dal sonucu olabilir
# TR:
# TR: Ortak storage anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle storage planlama, route seçimi veya storage hedef anlamı ile ilgilenir
# TR: - açık success vs degraded routing anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir storage şekilli routing payload alıp almayacağını belirler
# TR: - görünür routed vs deferred ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon storage tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - storage sonuçları açık kalmalıdır ki denetimler success, degraded, deferred ve downstream persistence anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz storage sonuçları

# EN: path_is_usable checks whether the status parameter satisfies the observable conditions required for a usable storage route.
# TR: path_is_usable status parametresinin kullanilabilir bir storage rotasi icin gereken gozlenebilir kosullari saglayip saglamadigini kontrol eder.
def path_is_usable(status: StoragePathStatus) -> bool:
    # EN: All required observable conditions must be true together.
    # TR: Gerekli tüm gözlenebilir koşullar birlikte doğru olmalıdır.
    return (
        status.exists
        and status.is_dir
        and status.is_mount
        and status.is_writable
    )


# EN: This helper checks whether /srv/buffer currently appears to contain
# EN: processed-output backlog that is waiting to be moved into /srv/data.
# TR: Bu yardımcı /srv/buffer içinde şu anda /srv/data tarafına taşınmayı bekleyen
# TR: işlenmiş çıktı backlog'u var görünüp görünmediğini kontrol eder.
# EN: STORAGE FUNCTION PURPOSE MEMORY BLOCK V6 / detect_buffer_backlog
# EN:
# EN: Why this function exists:
# EN: - because storage truth for 'detect_buffer_backlog' should be exposed through one named top-level helper boundary
# EN: - because storage-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: buffer_path
# EN: - values should match the current Python signature and the storage-routing contract below
# EN:
# EN: Accepted output:
# EN: - a storage-oriented result shape defined by the current function body
# EN: - this may be a storage plan, route result, tier/path selection shape, drain-related payload, or another explicit storage-side branch result
# EN:
# EN: Common storage meaning hints:
# EN: - this surface exposes one named storage runtime contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is storage-side helper logic, not the whole worker corridor
# EN: - storage results must stay explicit so audits can understand success, degraded, deferred, and downstream persistence meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague storage results that hide branch meaning
# TR: STORAGE FUNCTION AMAÇ HAFIZA BLOĞU V6 / detect_buffer_backlog
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'detect_buffer_backlog' için storage doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü storage tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: buffer_path
# TR: - değerler aşağıdaki mevcut Python imzası ve storage-routing sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen storage odaklı sonuç şekli
# TR: - bu; storage planı, route sonucu, tier/path seçim şekli, drain ile ilgili payload veya başka açık storage tarafı dal sonucu olabilir
# TR:
# TR: Ortak storage anlam ipuçları:
# TR: - bu yüzey isimli bir storage runtime sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon storage tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - storage sonuçları açık kalmalıdır ki denetimler success, degraded, deferred ve downstream persistence anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz storage sonuçları

# EN: detect_buffer_backlog scans the buffer_path parameter for visible backlog items waiting behind the processed-output route.
# TR: detect_buffer_backlog buffer_path parametresini islenmis cikti rotasinin arkasinda bekleyen gorunur backlog ogeleri icin tarar.
def detect_buffer_backlog(buffer_path: Path = PROCESSED_FALLBACK_ROOT) -> bool:
    # EN: If the fallback root does not exist or is not a directory, no usable
    # EN: backlog scan can happen, so we conservatively report no backlog here.
    # TR: Fallback kök mevcut değilse veya dizin değilse kullanılabilir backlog
    # TR: taraması yapılamaz; burada muhafazakâr olarak backlog yok diyoruz.
    if not buffer_path.exists() or not buffer_path.is_dir():
        return False

    # EN: We iterate through directory children and ignore lost+found because
    # EN: ext4 may create it even when no crawler-produced backlog exists.
    # TR: Dizin çocuklarını geziyoruz ve lost+found öğesini yok sayıyoruz; çünkü
    # TR: ext4 crawler kaynaklı backlog olmasa bile bunu oluşturabilir.
    for child in buffer_path.iterdir():
        if child.name == "lost+found":
            continue
        return True

    # EN: If we found nothing except optional filesystem boilerplate, backlog
    # EN: is currently absent.
    # TR: Opsiyonel filesystem boilerplate dışında hiçbir şey bulmadıysak backlog
    # TR: şu anda yoktur.
    return False


# EN: This function implements the user's simple canonical rule:
# EN: raw data stays under /srv, processed output goes to /srv/data when usable,
# EN: otherwise to /srv/buffer, and if /srv/data becomes usable while buffer
# EN: backlog exists, crawler must pause until buffer is fully drained into /srv/data.
# TR: Bu fonksiyon kullanıcının sade kanonik kuralını uygular:
# TR: ham veri /srv altında kalır, işlenmiş çıktı kullanılabiliyorsa /srv/data
# TR: yoluna gider, aksi halde /srv/buffer yoluna gider ve /srv/data tekrar
# TR: kullanılabilir hale geldiğinde buffer backlog'u varsa crawler buffer tamamen
# TR: /srv/data tarafına boşaltılana kadar pause olur.
# EN: STORAGE FUNCTION PURPOSE MEMORY BLOCK V6 / choose_processed_output_plan
# EN:
# EN: Why this function exists:
# EN: - because storage truth for 'choose_processed_output_plan' should be exposed through one named top-level helper boundary
# EN: - because storage-side semantics should remain readable instead of being diluted inside broader worker orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: primary_path, fallback_path, raw_root
# EN: - values should match the current Python signature and the storage-routing contract below
# EN:
# EN: Accepted output:
# EN: - a storage-oriented result shape defined by the current function body
# EN: - this may be a storage plan, route result, tier/path selection shape, drain-related payload, or another explicit storage-side branch result
# EN:
# EN: Common storage meaning hints:
# EN: - this surface likely shapes drain-aware, hold, defer, or plan-related routing payloads
# EN: - explicit payload structure is often important for audits and later export/persistence layers
# EN:
# EN: Important beginner reminder:
# EN: - this function is storage-side helper logic, not the whole worker corridor
# EN: - storage results must stay explicit so audits can understand success, degraded, deferred, and downstream persistence meaning
# EN:
# EN: Undesired behavior:
# EN: - silent route mutation
# EN: - vague storage results that hide branch meaning
# TR: STORAGE FUNCTION AMAÇ HAFIZA BLOĞU V6 / choose_processed_output_plan
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'choose_processed_output_plan' için storage doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü storage tarafı semantiklerinin daha geniş worker orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: primary_path, fallback_path, raw_root
# TR: - değerler aşağıdaki mevcut Python imzası ve storage-routing sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen storage odaklı sonuç şekli
# TR: - bu; storage planı, route sonucu, tier/path seçim şekli, drain ile ilgili payload veya başka açık storage tarafı dal sonucu olabilir
# TR:
# TR: Ortak storage anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle drain-aware, hold, defer veya planla ilgili routing payloadlarını şekillendirir
# TR: - açık payload yapısı çoğu zaman denetimler ve sonraki export/persistence katmanları için önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon storage tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - storage sonuçları açık kalmalıdır ki denetimler success, degraded, deferred ve downstream persistence anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz route değişimi
# TR: - dal anlamını gizleyen belirsiz storage sonuçları

# EN: choose_processed_output_plan compares primary_path and fallback_path, keeps raw_root visible in the returned plan, and decides the processed-output routing branch.
# TR: choose_processed_output_plan primary_path ile fallback_path degerlerini karsilastirir, donen planda raw_root degerini gorunur tutar ve islenmis cikti routing dalini secer.
def choose_processed_output_plan(
    primary_path: Path = PROCESSED_PRIMARY_ROOT,
    fallback_path: Path = PROCESSED_FALLBACK_ROOT,
    raw_root: Path = RAW_COLLECTION_ROOT,
) -> ProcessedOutputPlan:
    # EN: We probe the primary processed-output root first because it is the
    # EN: intended normal destination.
    # TR: Birincil işlenmiş çıktı kökü normal hedef olduğu için önce onu probe ediyoruz.
# EN: primary_status stores the structured probe result for primary_path, the intended normal processed-output destination.
# TR: primary_status normal hedef olan primary_path icin yapili probe sonucunu tasir.
    primary_status = probe_storage_path(primary_path)

    # EN: We probe the fallback processed-output root second because it is used
    # EN: only when the primary route is unavailable.
    # TR: Fallback işlenmiş çıktı kökü yalnızca birincil rota kullanılamadığında
    # TR: kullanıldığı için ikinci olarak onu probe ediyoruz.
# EN: fallback_status stores the structured probe result for fallback_path, the secondary processed-output route.
# TR: fallback_status ikincil islenmis cikti rotasi olan fallback_path icin yapili probe sonucunu tasir.
    fallback_status = probe_storage_path(fallback_path)

    # EN: We detect whether buffered backlog currently exists in /srv/buffer.
    # TR: /srv/buffer içinde şu anda buffer backlog'u var mı bunu tespit ediyoruz.
# EN: buffer_backlog_present stores whether fallback_path currently contains backlog that should block an immediate primary-route return.
# TR: buffer_backlog_present fallback_path icinde birincil rotaya hemen donmeyi engellemesi gereken backlog bulunup bulunmadigini tasir.
    buffer_backlog_present = detect_buffer_backlog(fallback_path)

    # EN: If the primary processed-output path is usable and buffer backlog
    # EN: exists, crawler must pause first so backlog can be fully moved into /srv/data.
    # TR: Birincil işlenmiş çıktı path'i kullanılabiliyor ve buffer backlog'u varsa
    # TR: crawler önce pause olmalıdır; böylece backlog tamamen /srv/data tarafına taşınır.
    if path_is_usable(primary_status) and buffer_backlog_present:
        return ProcessedOutputPlan(
            raw_collection_root=str(raw_root),
            processed_output_root=None,
            using_fallback=False,
            buffer_backlog_present=True,
            drain_buffer_to_data_first=True,
            pause_crawler=True,
            primary_status=primary_status,
            fallback_status=fallback_status,
            explanation="primary processed output root is usable again; pause crawler until /srv/buffer is fully drained into /srv/data",
        )

    # EN: If the primary processed-output path is usable and no backlog blocks it,
    # EN: we use /srv/data.
    # TR: Birincil işlenmiş çıktı path'i kullanılabiliyor ve onu engelleyen backlog
    # TR: yoksa /srv/data yolunu kullanırız.
    if path_is_usable(primary_status):
        return ProcessedOutputPlan(
            raw_collection_root=str(raw_root),
            processed_output_root=str(primary_path),
            using_fallback=False,
            buffer_backlog_present=buffer_backlog_present,
            drain_buffer_to_data_first=False,
            pause_crawler=False,
            primary_status=primary_status,
            fallback_status=fallback_status,
            explanation="primary processed output root is usable; write processed output to /srv/data",
        )

    # EN: If the primary path is not usable but fallback is usable, we preserve
    # EN: continuity by writing processed output to /srv/buffer.
    # TR: Birincil path kullanılamıyor ama fallback kullanılabiliyorsa sürekliliği
    # TR: işlenmiş çıktıyı /srv/buffer yoluna yazarak koruruz.
    if path_is_usable(fallback_status):
        return ProcessedOutputPlan(
            raw_collection_root=str(raw_root),
            processed_output_root=str(fallback_path),
            using_fallback=True,
            buffer_backlog_present=buffer_backlog_present,
            drain_buffer_to_data_first=False,
            pause_crawler=False,
            primary_status=primary_status,
            fallback_status=fallback_status,
            explanation="primary processed output root is unusable; write processed output to /srv/buffer",
        )

    # EN: If neither path is usable, crawler must pause and surface a hard error.
    # TR: İki path de kullanılamıyorsa crawler pause olmalı ve sert hata vermelidir.
    return ProcessedOutputPlan(
        raw_collection_root=str(raw_root),
        processed_output_root=None,
        using_fallback=False,
        buffer_backlog_present=buffer_backlog_present,
        drain_buffer_to_data_first=False,
        pause_crawler=True,
        primary_status=primary_status,
        fallback_status=fallback_status,
        explanation="neither /srv/data nor /srv/buffer is currently usable; crawler must pause and surface an explicit error",
    )
