"""
EN:
This file is the main worker-runtime orchestration hub for the current crawler runtime family.

EN:
Why this file exists:
- because the worker needs one visible Python hub where the claim/probe corridor is orchestrated from top to bottom
- because upper layers should not spread worker-phase coordination across many unrelated files
- because a beginner should be able to find the main worker control flow in one obvious file

EN:
What this file DOES:
- define the main worker-runtime orchestration surface
- hold the named runtime payload shapes that upper and lower worker sublayers exchange
- coordinate visible phase boundaries such as runtime control, claim, robots, fetch, parse, finalize, and release style outcomes

EN:
What this file DOES NOT do:
- it does not own every low-level helper itself
- it does not own every SQL detail itself
- it does not act as the taxonomy authority itself
- it does not act as the only acquisition implementation itself

EN:
Topological role:
- main loop/controller layers above call into this file
- narrower worker submodules below provide lease, robots, acquisition, parse, finalize, and storage details
- this file is the readable worker hub that connects those narrower sublayers into one corridor

EN:
Important visible values and shapes:
- config-style worker payloads => durable runtime input given to the worker corridor
- probe_only => whether the corridor should remain rollback-style and observational
- worker_id => explicit worker identity text
- claim result / claimed_url payload => whether work was obtained and what that work item is
- phase-boundary payloads => visible handoff meaning between robots, fetch, parse, finalize, and release steps
- degraded branches => explicit non-happy paths that should remain visible

EN:
Accepted architectural identity:
- worker orchestration hub
- readable phase-boundary coordinator
- runtime contract surface

EN:
Undesired architectural identity:
- giant hidden utility dump
- silent policy black box
- hidden SQL engine
- hidden operator CLI surface

TR:
Bu dosya mevcut crawler runtime ailesinin ana worker-runtime orkestrasyon hub yüzeyidir.

TR:
Bu dosya neden var:
- çünkü workerın claim/probe koridorunun baştan sona orkestre edildiği görünür tek Python hub yüzeyine ihtiyacı vardır
- çünkü üst katmanlar worker-faz koordinasyonunu ilgisiz birçok dosyaya dağıtmamalıdır
- çünkü yeni başlayan biri ana worker kontrol akışını tek ve açık dosyada bulabilmelidir

TR:
Bu dosya NE yapar:
- ana worker-runtime orkestrasyon yüzeyini tanımlar
- üst ve alt worker altkatmanlarının değiş tokuş ettiği isimli runtime payload şekillerini taşır
- runtime control, claim, robots, fetch, parse, finalize ve release tarzı sonuçlar arasındaki görünür faz sınırlarını koordine eder

TR:
Bu dosya NE yapmaz:
- her düşük seviye yardımcının sahibi değildir
- her SQL ayrıntısının sahibi değildir
- taxonomy authoritynin kendisi değildir
- tek acquisition implementasyonu gibi davranmaz

TR:
Topolojik rol:
- üstteki main loop/controller katmanları bu dosyayı çağırır
- alttaki daha dar worker altmodülleri lease, robots, acquisition, parse, finalize ve storage ayrıntılarını sağlar
- bu dosya o dar altkatmanları tek koridorda birleştiren okunabilir worker hubıdır

TR:
Önemli görünür değerler ve şekiller:
- config tarzı worker payloadları => worker koridoruna verilen kalıcı runtime girdisi
- probe_only => koridorun rollback-tarzı ve gözlemsel kalıp kalmayacağı
- worker_id => açık worker kimlik metni
- claim result / claimed_url payloadı => iş alınıp alınmadığı ve o iş öğesinin ne olduğu
- phase-boundary payloadları => robots, fetch, parse, finalize ve release adımları arasındaki görünür devir anlamı
- degraded dallar => görünür kalması gereken mutlu-yol-dışı yollar

TR:
Kabul edilen mimari kimlik:
- worker orkestrasyon hubı
- okunabilir faz-sınırı koordinatörü
- runtime sözleşme yüzeyi

TR:
İstenmeyen mimari kimlik:
- dev gizli yardımcı çöplüğü
- sessiz policy kara kutusu
- gizli SQL motoru
- gizli operatör CLI yüzeyi
"""

# EN: This module is now the thinner worker-runtime parent after the controlled
# EN: split. It keeps the parent-visible dataclasses plus the parent orchestration
# EN: flow, while lower children own support/finalize/robots/lease logic.
# TR: Bu modül kontrollü split sonrası artık daha ince worker-runtime parent
# TR: yüzeyidir. Parent-görünür dataclass’ları ve parent orchestration akışını
# TR: tutar; daha alt çocuklar ise support/finalize/robots/lease mantığını sahiplenir.

# EN: WORKER RUNTIME IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the main room where the worker corridor becomes understandable.
# EN: Beginner mental model:
# EN: - the main loop decides when a worker probe should run
# EN: - this file coordinates what the worker probe actually tries to do
# EN: - narrower submodules below handle more focused contracts
# EN:
# EN: Accepted architectural meaning:
# EN: - named worker orchestration boundary
# EN: - readable phase coordinator
# EN: - corridor hub that forwards explicit payloads across worker phases
# EN:
# EN: Undesired architectural meaning:
# EN: - random bag of helpers with no topology
# EN: - hidden black-box runtime
# EN: - place where important branch meaning becomes invisible
# EN:
# EN: Important value-shape reminders:
# EN: - worker config payloads should remain explicit and named
# EN: - phase outputs should remain visible instead of being silently collapsed
# EN: - degraded/no-work/no-claim branches must stay readable
# TR: WORKER RUNTIME KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya worker koridorunun anlaşılır hale geldiği ana oda gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - main loop bir worker probe'un ne zaman koşacağını belirler
# TR: - bu dosya worker probe'un gerçekte ne yapmaya çalıştığını koordine eder
# TR: - alttaki daha dar altmodüller daha odaklı sözleşmeleri taşır
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli worker orkestrasyon sınırı
# TR: - okunabilir faz koordinatörü
# TR: - worker fazları arasında açık payloadları taşıyan koridor hubı
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - topolojisiz rastgele yardımcı torbası
# TR: - gizli kara kutu runtime
# TR: - önemli dal anlamının görünmez hale geldiği yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - worker config payloadları açık ve isimli kalmalıdır
# TR: - faz çıktıları sessizce ezilmek yerine görünür kalmalıdır
# TR: - degraded/no-work/no-claim dalları okunabilir kalmalıdır

from __future__ import annotations

# EN: We import dataclass because the parent still owns the public structured
# EN: configuration and result contracts expected by main_loop.
# TR: Parent yüzeyi main_loop’un beklediği public yapılı konfigürasyon ve sonuç
# TR: sözleşmelerini hâlâ sahiplendiği için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import socket because transport-timeout failures are still classified by
# EN: the parent orchestration try/except surface.
# TR: Taşıma-timeout hataları hâlâ parent orchestration try/except yüzeyinde
# TR: sınıflandırıldığı için socket içe aktarıyoruz.
import socket

# EN: We import HTTPError and URLError because the parent still owns the high-level
# EN: fetch outcome branching that separates HTTP failures from transport failures.
# TR: Parent hâlâ HTTP hataları ile taşıma hatalarını ayıran üst-seviye fetch
# TR: outcome branching yüzeyini sahiplendiği için HTTPError ve URLError içe
# TR: aktarıyoruz.
from urllib.error import HTTPError, URLError

# EN: We import the canonical DB gateway helpers that the parent orchestrator must
# EN: still call directly for claim/control/success/release boundaries.
# TR: Parent orchestrator’ın claim/control/success/release sınırlarında doğrudan
# TR: çağırması gereken kanonik DB gateway yardımcılarını içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    claim_next_url,
    close_db,
    commit,
    compute_robots_allow_decision,
    compute_robots_refresh_decision,
    connect_db,
    finish_fetch_success,
    get_webcrawler_runtime_control,
    release_parse_pending_to_queued,
    rollback,
    webcrawler_runtime_may_claim,
)

# EN: We import the storage-routing child because the parent must still ask the
# EN: storage policy whether normal crawler flow may continue.
# TR: Parent normal crawler akışının devam edip edemeyeceğini storage politikasına
# TR: sormak zorunda olduğu için storage-routing alt yüzeyini içe aktarıyoruz.
from .logisticsearch1_1_2_7_storage_routing import (
    ProcessedOutputPlan,
    choose_processed_output_plan,
)

# EN: We import the stable acquisition-family public surface. The parent no longer
# EN: chooses HTTP/browser child fetch paths inline. Instead it asks the canonical
# EN: acquisition hub to choose and execute the correct fetch path while still
# EN: consuming the same fetched-page contract shape.
# TR: Kararlı acquisition-aile public yüzeyini içe aktarıyoruz. Parent artık HTTP
# TR: veya browser çocuk fetch yollarını inline seçmez. Bunun yerine doğru fetch
# TR: yolunu seçip çalıştırması için kanonik acquisition hub'a sorar ve yine aynı
# TR: fetched-page sözleşme şeklini tüketir.
from .logisticsearch1_1_2_4_acquisition_runtime import (
    FetchedPageResult,
    fetch_page_via_selection_to_raw_storage,
    get_claimed_url_value,
)

# EN: We import the canonical parse continuation surface because successful fetch
# EN: flows may still continue into minimal parse persistence.
# TR: Başarılı fetch akışları minimal parse persistence aşamasına devam
# TR: edebileceği için kanonik parse continuation yüzeyini içe aktarıyoruz.
from .logisticsearch1_1_2_6_parse_runtime import (
    MinimalParseApplyResult,
    apply_minimal_parse_entry,
)

# EN: We import the tiny runtime support child for generic parent-neutral helpers.
# TR: Parent-nötr küçük yardımcılar için küçük runtime support alt yüzeyini içe
# TR: aktarıyoruz.
from .logisticsearch1_1_2_1_worker_runtime_support import (
    new_run_id,
    utc_now_iso,
)

# EN: We import the finalize child because durable fetch-attempt logging and
# EN: durable error finalization no longer belong in the parent orchestrator body.
# TR: Kalıcı fetch-attempt loglama ve kalıcı hata finalization artık parent
# TR: orchestrator gövdesine ait olmadığı için finalize alt yüzeyini içe aktarıyoruz.
from .logisticsearch1_1_2_5_fetch_finalize_runtime import (
    finalize_http_error,
    finalize_robots_block,
    finalize_transport_error,
    finalize_unexpected_runtime_error,
    log_fetch_attempt_terminal_from_worker,
)

# EN: We import the robots child because robots decision helpers no longer belong
# EN: inline inside the parent orchestration module.
# TR: Robots karar yardımcıları artık parent orchestration modülü içinde inline
# TR: durmaması gerektiği için robots alt yüzeyini içe aktarıyoruz.
from .logisticsearch1_1_2_3_worker_robots_runtime import (
    refresh_robots_cache_if_needed,
    robots_verdict_allows_fetch,
)

# EN: We import the lease child because explicit lease renewal is a separate
# EN: durable-boundary helper, not parent-inline logic anymore.
# TR: Açık lease yenilemesi ayrı bir durable-boundary yardımcısıdır; artık parent
# TR: içinde inline mantık olarak durmaması gerektiği için lease alt yüzeyini
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_2_worker_lease_runtime import (
    renew_claimed_lease_before_durable_phase,
)

# EN: We import the strict fetched-page contract validator so the parent worker
# EN: can stop before parse/finalize when raw artefact metadata drift is detected.
# TR: Parent worker ham artefact metadata drift'i yakaladığında parse/finalize
# TR: öncesinde durabilsin diye sıkı fetched-page contract validator'ını içe aktarıyoruz.
from .logisticsearch1_1_2_4_1_acquisition_support import (
    validate_fetched_page_result_contract,
)


# EN: This dataclass stores runtime configuration for the public worker surface.
# TR: Bu dataclass public worker yüzeyi için runtime konfigürasyonunu tutar.
@dataclass(slots=True)
# EN: WORKER RUNTIME CLASS PURPOSE MEMORY BLOCK V6 / WorkerConfig
# EN:
# EN: Why this class exists:
# EN: - because the worker-runtime file needs a named top-level shape for 'WorkerConfig' instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and role meaning directly
# EN:
# EN: Accepted role:
# EN: - named worker-runtime payload or contract shape
# EN: - visible field set currently detected here: dsn, worker_id, lease_seconds, probe_only
# EN:
# EN: Common worker-runtime meaning hints:
# EN: - this class or helper likely carries stable runtime input needed by the worker corridor
# EN: - worker identity, DSN, lease timing, or probe_only visibility may matter here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no runtime contract meaning
# EN: - ignoring its named shape and collapsing everything into anonymous dicts everywhere
# TR: WORKER RUNTIME CLASS AMAÇ HAFIZA BLOĞU V6 / WorkerConfig
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü worker-runtime dosyası 'WorkerConfig' için isimsiz gevşek payload dolaştırmak yerine isimli top-level şekle ihtiyaç duyar
# TR: - çünkü yeni başlayan biri alan isimlerini ve rol anlamını doğrudan inceleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli worker-runtime payloadı veya sözleşme şekli
# TR: - burada şu an tespit edilen görünür alan kümesi: dsn, worker_id, lease_seconds, probe_only
# TR:
# TR: Ortak worker-runtime anlam ipuçları:
# TR: - bu sınıf veya yardımcı büyük ihtimalle worker koridorunun ihtiyaç duyduğu kararlı runtime girdisini taşır
# TR: - worker kimliği, DSN, lease zamanlaması veya probe_only görünürlüğü burada önemli olabilir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı runtime sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi her yerde isimsiz dictlere ezmek

# EN: STAGE21-AUTO-COMMENT :: WorkerConfig is a named worker-runtime contract surface whose structure must stay explicit and reviewable.
# EN: A reader should treat WorkerConfig as a stable runtime boundary instead of anonymous dict drift.
# TR: STAGE21-AUTO-COMMENT :: WorkerConfig yapısının açık ve denetlenebilir kalması gereken isimli bir worker-runtime sözleşme yüzeyidir.
# TR: Okuyucu WorkerConfig yapısını isimsiz dict kayması yerine kararlı bir runtime sınırı olarak görmelidir.
class WorkerConfig:
    # EN: dsn is the PostgreSQL connection string used by this worker runtime.
    # TR: dsn bu worker runtime tarafından kullanılan PostgreSQL bağlantı metnidir.
    dsn: str

    # EN: worker_id is the textual worker identity passed into frontier.claim_next_url(...).
    # TR: worker_id frontier.claim_next_url(...) içine verilen metinsel worker kimliğidir.
    worker_id: str

    # EN: lease_seconds says how long a claimed lease should stay valid before
    # EN: lease renewal becomes necessary.
    # TR: lease_seconds claim edilmiş bir lease’in renewal gerektirmeden önce ne
    # TR: kadar geçerli kalacağını söyler.
    lease_seconds: int = 600

    # EN: probe_only keeps the worker in non-durable verification mode when True.
    # EN: When False, the worker executes the minimal real fetch + finalize path.
    # TR: probe_only True olduğunda worker’ı kalıcı olmayan doğrulama modunda
    # TR: tutar. False olduğunda worker minimal gerçek fetch + finalize yolunu
    # TR: çalıştırır.
    probe_only: bool = True


# EN: This dataclass stores the structured result of one worker execution.
# TR: Bu dataclass tek bir worker çalıştırmasının yapılı sonucunu tutar.
@dataclass(slots=True)
# EN: WORKER RUNTIME CLASS PURPOSE MEMORY BLOCK V6 / ClaimProbeResult
# EN:
# EN: Why this class exists:
# EN: - because the worker-runtime file needs a named top-level shape for 'ClaimProbeResult' instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and role meaning directly
# EN:
# EN: Accepted role:
# EN: - named worker-runtime payload or contract shape
# EN: - visible field set currently detected here: run_id, claimed, claimed_url, robots_allow_decision, storage_plan, fetched_page, finalize_result, parse_apply_result, observed_at, runtime_control
# EN:
# EN: Common worker-runtime meaning hints:
# EN: - this class or helper likely carries structured phase outcome visibility
# EN: - no-work, no-claim, degraded, or successful-claim branch meaning may matter here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no runtime contract meaning
# EN: - ignoring its named shape and collapsing everything into anonymous dicts everywhere
# TR: WORKER RUNTIME CLASS AMAÇ HAFIZA BLOĞU V6 / ClaimProbeResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü worker-runtime dosyası 'ClaimProbeResult' için isimsiz gevşek payload dolaştırmak yerine isimli top-level şekle ihtiyaç duyar
# TR: - çünkü yeni başlayan biri alan isimlerini ve rol anlamını doğrudan inceleyebilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli worker-runtime payloadı veya sözleşme şekli
# TR: - burada şu an tespit edilen görünür alan kümesi: run_id, claimed, claimed_url, robots_allow_decision, storage_plan, fetched_page, finalize_result, parse_apply_result, observed_at, runtime_control
# TR:
# TR: Ortak worker-runtime anlam ipuçları:
# TR: - bu sınıf veya yardımcı büyük ihtimalle yapılı faz-sonucu görünürlüğü taşır
# TR: - no-work, no-claim, degraded veya başarılı-claim dal anlamı burada önemli olabilir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı runtime sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi her yerde isimsiz dictlere ezmek

# EN: STAGE21-AUTO-COMMENT :: ClaimProbeResult is a named worker-runtime contract surface whose structure must stay explicit and reviewable.
# EN: A reader should treat ClaimProbeResult as a stable runtime boundary instead of anonymous dict drift.
# TR: STAGE21-AUTO-COMMENT :: ClaimProbeResult yapısının açık ve denetlenebilir kalması gereken isimli bir worker-runtime sözleşme yüzeyidir.
# TR: Okuyucu ClaimProbeResult yapısını isimsiz dict kayması yerine kararlı bir runtime sınırı olarak görmelidir.
class ClaimProbeResult:
    # EN: run_id is the unique id of this exact Python-side runtime execution.
    # TR: run_id bu tam Python-tarafı runtime çalıştırmasının benzersiz kimliğidir.
    run_id: str

    # EN: claimed tells whether a claimable row was actually returned.
    # TR: claimed gerçekten claim edilebilir bir satır dönüp dönmediğini söyler.
    claimed: bool

    # EN: claimed_url stores the claimed row object when a claim succeeded.
    # TR: claimed_url claim başarılıysa claim edilen satır nesnesini tutar.
    claimed_url: object | None

    # EN: robots_allow_decision stores the visible robots allow/block decision
    # EN: when a claim succeeded.
    # TR: robots_allow_decision claim başarılıysa görünür robots allow/block
    # TR: kararını tutar.
    robots_allow_decision: dict | None

    # EN: storage_plan stores the current processed-output storage decision.
    # TR: storage_plan mevcut işlenmiş-çıktı storage kararını tutar.
    storage_plan: ProcessedOutputPlan

    # EN: fetched_page stores the structured raw fetch result when a real fetch ran.
    # TR: fetched_page gerçek bir fetch çalıştıysa yapılı ham fetch sonucunu tutar.
    fetched_page: FetchedPageResult | None

    # EN: finalize_result stores the canonical durable finalize result when the
    # EN: worker reached such a boundary.
    # TR: finalize_result worker kalıcı bir finalize sınırına ulaştıysa kanonik
    # TR: kalıcı finalize sonucunu tutar.
    finalize_result: dict | None

    # EN: parse_apply_result stores the canonical minimal parse-apply DB results
    # EN: when the current runtime reaches that stage.
    # TR: parse_apply_result mevcut runtime bu aşamaya ulaştığında kanonik minimal
    # TR: parse-apply DB sonuçlarını tutar.
    parse_apply_result: MinimalParseApplyResult | None

    # EN: observed_at records when this result object was produced.
    # TR: observed_at bu sonuç nesnesinin ne zaman üretildiğini kaydeder.
    observed_at: str

    # EN: runtime_control stores the visible crawler runtime-control snapshot when
    # EN: the worker consulted the DB truth surface during this execution.
    # TR: runtime_control worker bu çalıştırma sırasında DB doğruluk yüzeyine
    # TR: baktığında gördüğü crawler runtime-control anlık görüntüsünü tutar.
    runtime_control: dict | None = None


# EN: This function performs one controlled worker execution. The parent still
# EN: owns the orchestration order:
# EN: storage gate -> runtime control gate -> claim -> robots gate/refresh ->
# EN: acquisition -> optional parse -> success/error finalize -> commit/return.
# TR: Bu fonksiyon tek bir kontrollü worker çalıştırması yapar. Parent hâlâ şu
# TR: orchestration sırasını sahiplenir:
# TR: storage kapısı -> runtime control kapısı -> claim -> robots kapısı/refresh ->
# TR: acquisition -> opsiyonel parse -> success/error finalize -> commit/return.
# EN: WORKER RUNTIME FUNCTION PURPOSE MEMORY BLOCK V6 / run_claim_probe
# EN:
# EN: Why this function exists:
# EN: - because worker-runtime truth for 'run_claim_probe' should be exposed through one named top-level function boundary
# EN: - because upper layers and audits should read a visible function contract instead of hidden control flow
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: config
# EN: - values should match the current Python signature and the worker contract below
# EN:
# EN: Accepted output:
# EN: - a worker-runtime-oriented result shape defined by the current function body
# EN: - this may be a structured result payload, a claim/probe outcome, or another explicit branch result
# EN:
# EN: Common worker-runtime meaning hints:
# EN: - this function likely orchestrates the main claim/probe corridor
# EN: - phase handoff payloads and explicit branch visibility are likely central here
# EN:
# EN: Important beginner reminder:
# EN: - this function should keep phase meaning visible
# EN: - no-work, no-claim, degraded, or success corridors should remain explicit and readable
# EN:
# EN: Undesired behavior:
# EN: - silent branch collapse
# EN: - hidden cross-phase mutation with no named boundary
# TR: WORKER RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V6 / run_claim_probe
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'run_claim_probe' için worker-runtime doğrusu tek ve isimli top-level fonksiyon sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü üst katmanlar ve denetimler gizli kontrol akışı yerine görünür fonksiyon sözleşmesi okumalıdır
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: config
# TR: - değerler aşağıdaki mevcut Python imzası ve worker sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen worker-runtime odaklı sonuç şekli
# TR: - bu; yapılı result payloadı, claim/probe sonucu veya başka açık dal sonucu olabilir
# TR:
# TR: Ortak worker-runtime anlam ipuçları:
# TR: - bu fonksiyon büyük ihtimalle ana claim/probe koridorunu orkestre eder
# TR: - fazlar arası payload devri ve açık dal görünürlüğü burada merkezi olabilir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon faz anlamını görünür tutmalıdır
# TR: - no-work, no-claim, degraded veya success koridorları açık ve okunabilir kalmalıdır
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz dal ezilmesi
# TR: - isimli sınır olmadan gizli fazlar-arası değişim

# EN: STAGE21-AUTO-COMMENT :: run_claim_probe is a named worker-runtime orchestration boundary whose phase meaning must remain visible and reviewable.
# EN: A reader should understand what run_claim_probe receives, what it coordinates, and what structured result it returns.
# EN: Parameter contract:
# EN: - config => run_claim_probe function's explicit worker-runtime input contract; this value is part of the visible orchestration boundary
# TR: STAGE21-AUTO-COMMENT :: run_claim_probe faz anlamı görünür ve denetlenebilir kalması gereken isimli bir worker-runtime orkestrasyon sınırıdır.
# TR: Okuyucu run_claim_probe fonksiyonunun ne aldığını, neyi koordine ettiğini ve hangi yapılı sonucu döndürdüğünü anlayabilmelidir.
# TR: Parametre sözleşmesi:
# TR: - config => run_claim_probe fonksiyonunun açık worker-runtime girdi sözleşmesidir; bu değer görünür orkestrasyon sınırının parçasıdır
def run_claim_probe(config: WorkerConfig) -> ClaimProbeResult:
    # EN: We create a unique run id first so the whole execution can be traced.
    # TR: Tüm çalıştırma izlenebilir olsun diye önce benzersiz bir run id üretiyoruz.
    # EN: LOCAL VALUE EXPLANATION / run_claim_probe / run_id
    # EN: run_id keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
    # EN: Expected values depend on the active branch below; collapsing run_id into an unnamed expression would weaken audits.
    # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / run_id
    # TR: run_id bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
    # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; run_id değerini isimsiz ifadeye ezmek denetimi zayıflatır.
    run_id = new_run_id()

    # EN: We start with no runtime-control snapshot because the worker has not yet
    # EN: consulted the DB truth surface.
    # TR: Worker henüz DB doğruluk yüzeyine bakmadığı için başlangıçta runtime-control
    # TR: anlık görüntümüz yoktur.
    # EN: LOCAL VALUE EXPLANATION / run_claim_probe / runtime_control
    # EN: runtime_control keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
    # EN: Expected values depend on the active branch below; collapsing runtime_control into an unnamed expression would weaken audits.
    # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / runtime_control
    # TR: runtime_control bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
    # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; runtime_control değerini isimsiz ifadeye ezmek denetimi zayıflatır.
    runtime_control = None

    # EN: We compute the current storage plan before touching the DB because the
    # EN: crawler must not claim new work when storage policy says pause.
    # TR: Crawler storage politikası pause diyorsa yeni iş claim etmemeli; bu yüzden
    # TR: DB’ye dokunmadan önce mevcut storage planı hesaplıyoruz.
    # EN: LOCAL VALUE EXPLANATION / run_claim_probe / storage_plan
    # EN: storage_plan keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
    # EN: Expected values depend on the active branch below; collapsing storage_plan into an unnamed expression would weaken audits.
    # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / storage_plan
    # TR: storage_plan bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
    # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; storage_plan değerini isimsiz ifadeye ezmek denetimi zayıflatır.
    storage_plan = choose_processed_output_plan()

    # EN: We start with no parse-apply result because parse continuation should
    # EN: appear only after a successful fetch path reaches that stage.
    # TR: Parse continuation yalnızca başarılı fetch yolu o aşamaya ulaşınca
    # TR: ortaya çıkması gerektiği için başlangıçta parse-apply sonucu yoktur.
    # EN: LOCAL VALUE EXPLANATION / run_claim_probe / parse_apply_result
    # EN: parse_apply_result keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
    # EN: Expected values depend on the active branch below; collapsing parse_apply_result into an unnamed expression would weaken audits.
    # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / parse_apply_result
    # TR: parse_apply_result bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
    # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; parse_apply_result değerini isimsiz ifadeye ezmek denetimi zayıflatır.
    parse_apply_result = None

    # EN: If storage says pause, we stop here deliberately and return a structured
    # EN: non-claim result.
    # TR: Storage pause diyorsa bilinçli olarak burada duruyor ve yapılı non-claim
    # TR: sonucu döndürüyoruz.
    if storage_plan.pause_crawler:
        return ClaimProbeResult(
            run_id=run_id,
            claimed=False,
            claimed_url=None,
            robots_allow_decision=None,
            storage_plan=storage_plan,
            fetched_page=None,
            finalize_result=None,
            parse_apply_result=parse_apply_result,
            observed_at=utc_now_iso(),
            runtime_control=runtime_control,
        )

    # EN: Only after storage allows normal flow do we open a DB connection.
    # TR: Ancak storage normal akışa izin verdikten sonra DB bağlantısı açıyoruz.
    # EN: LOCAL VALUE EXPLANATION / run_claim_probe / conn
    # EN: conn keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
    # EN: Expected values depend on the active branch below; collapsing conn into an unnamed expression would weaken audits.
    # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / conn
    # TR: conn bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
    # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; conn değerini isimsiz ifadeye ezmek denetimi zayıflatır.
    conn = connect_db(config.dsn)

    try:
        # EN: Before asking crawler-core for claimable work, we read the visible
        # EN: runtime-control truth from the database.
        # TR: crawler-core’dan claim edilebilir iş istemeden önce veritabanındaki
        # TR: görünür runtime-control doğrusunu okuyoruz.
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / runtime_control
        # EN: runtime_control keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
        # EN: Expected values depend on the active branch below; collapsing runtime_control into an unnamed expression would weaken audits.
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / runtime_control
        # TR: runtime_control bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
        # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; runtime_control değerini isimsiz ifadeye ezmek denetimi zayıflatır.
        runtime_control = get_webcrawler_runtime_control(conn)

        # EN: A degraded runtime-control read must not fall through into claim logic.
        # EN: We roll back the transient connection state and return the visible
        # EN: degraded payload honestly.
        # TR: Degrade olmuş runtime-control okuması claim mantığına sızmamalıdır.
        # TR: Geçici bağlantı durumunu rollback ediyor ve görünür degrade payload'ı
        # TR: dürüst biçimde döndürüyoruz.
        if bool(runtime_control.get("runtime_control_degraded")):
            rollback(conn)
            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=None,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=dict(runtime_control),
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=dict(runtime_control),
            )

        if runtime_control is None:
            raise RuntimeError("get_webcrawler_runtime_control(...) returned no row")

        # EN: We then ask the canonical DB control function whether claiming is
        # EN: currently allowed.
        # TR: Ardından claim etmenin şu anda izinli olup olmadığını kanonik DB
        # TR: kontrol fonksiyonuna soruyoruz.
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / may_claim_result
        # EN: may_claim_result keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
        # EN: Expected values depend on the active branch below; collapsing may_claim_result into an unnamed expression would weaken audits.
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / may_claim_result
        # TR: may_claim_result bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
        # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; may_claim_result değerini isimsiz ifadeye ezmek denetimi zayıflatır.
        may_claim_result = webcrawler_runtime_may_claim(conn)

        # EN: A degraded may-claim read must not silently become a normal no-work
        # EN: result. We roll back the transient claim path and return the visible
        # EN: degraded control payload honestly.
        # TR: Degrade olmuş may-claim okuması sessizce normal bir iş-yok sonucuna
        # TR: dönüşmemelidir. Geçici claim yolunu rollback ediyor ve görünür
        # TR: degrade kontrol payload'ını dürüst biçimde döndürüyoruz.
        if bool(may_claim_result.get("runtime_control_degraded")):
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / degraded_runtime_control
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `{ **dict(runtime_control), "may_claim": may_claim_result.get("may_claim"), "may_claim_degraded": True, "may_claim_degraded_reason": may_clai` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): degraded_runtime_control
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # EN: This recovery line also closes the last file-level EN/TR audit gap without weakening the bilingual rule.
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / degraded_runtime_control
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): degraded_runtime_control
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            degraded_runtime_control = {
                **dict(runtime_control),
                "may_claim": may_claim_result.get("may_claim"),
                "may_claim_degraded": True,
                "may_claim_degraded_reason": may_claim_result.get("runtime_control_degraded_reason"),
            }
            rollback(conn)
            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=None,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=dict(may_claim_result),
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=degraded_runtime_control,
            )

        if may_claim_result is None:
            raise RuntimeError("webcrawler_runtime_may_claim(...) returned no row")

        # EN: We merge the explicit may-claim decision into the runtime-control
        # EN: snapshot so the returned JSON remains self-explanatory.
        # TR: Dönen JSON kendi kendini açıklayabilsin diye açık may-claim kararını
        # TR: runtime-control anlık görüntüsüne birleştiriyoruz.
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / runtime_control
        # EN: runtime_control keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
        # EN: Expected values depend on the active branch below; collapsing runtime_control into an unnamed expression would weaken audits.
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / runtime_control
        # TR: runtime_control bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
        # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; runtime_control değerini isimsiz ifadeye ezmek denetimi zayıflatır.
        runtime_control = {
            **dict(runtime_control),
            "may_claim": may_claim_result.get("may_claim"),
        }

        # EN: If DB truth says pause/stop, we must not claim new work.
        # TR: DB doğrusu pause/stop diyorsa yeni iş claim etmemeliyiz.
        if may_claim_result.get("may_claim") is not True:
            rollback(conn)
            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=None,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=None,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: We ask crawler-core for exactly one claimable row.
        # TR: crawler-core’dan tam olarak bir claim edilebilir satır istiyoruz.
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / claimed_url
        # EN: claimed_url keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
        # EN: Expected values depend on the active branch below; collapsing claimed_url into an unnamed expression would weaken audits.
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / claimed_url
        # TR: claimed_url bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
        # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; claimed_url değerini isimsiz ifadeye ezmek denetimi zayıflatır.
        claimed_url = claim_next_url(
            conn=conn,
            worker_id=config.worker_id,
            lease_seconds=config.lease_seconds,
        )

        # EN: If nothing is currently claimable, we rollback and return a structured
        # EN: no-work result.
        # TR: Şu anda claim edilebilir hiçbir şey yoksa rollback yapıyor ve yapılı
        # TR: iş-yok sonucu döndürüyoruz.
        if claimed_url is None:
            rollback(conn)
            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=None,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=None,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: We extract the host/path pair once because refresh and allow decisions
        # EN: are both anchored to the same claimed target.
        # TR: Refresh ve allow kararları aynı claimed hedefe bağlı olduğu için
        # TR: host/path çiftini bir kez çıkarıyoruz.
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / claimed_host_id
        # EN: claimed_host_id keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
        # EN: Expected values depend on the active branch below; collapsing claimed_host_id into an unnamed expression would weaken audits.
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / claimed_host_id
        # TR: claimed_host_id bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
        # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; claimed_host_id değerini isimsiz ifadeye ezmek denetimi zayıflatır.
        claimed_host_id = int(get_claimed_url_value(claimed_url, "host_id"))
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / claimed_url_path
        # EN: This local exists because the worker-runtime corridor should keep
        # EN: intermediate phase truth named, visible, and reviewable instead of hiding `str(get_claimed_url_value(claimed_url, "url_path"))` inline.
        # EN: Expected meaning:
        # EN: - current local name(s): claimed_url_path
        # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
        # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
        # EN: Undesired reading:
        # EN: - treating this local as durable global crawler truth
        # EN: - assuming this local alone proves the whole worker corridor succeeded
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / claimed_url_path
        # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
        # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
        # TR: Beklenen anlam:
        # TR: - mevcut yerel ad(lar): claimed_url_path
        # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
        # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
        # TR: İstenmeyen okuma:
        # TR: - bu yereli kalıcı global crawler doğrusu sanmak
        # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
        claimed_url_path = str(get_claimed_url_value(claimed_url, "url_path"))

        # EN: We inspect the canonical DB-side refresh decision first because the
        # EN: worker contract says robots cache truth must be refreshed when needed.
        # TR: Worker sözleşmesi gerektiğinde robots cache doğrusunun yenilenmesini
        # TR: söylediği için önce kanonik DB-side refresh kararını inceliyoruz.
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / refresh_decision
        # EN: refresh_decision keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
        # EN: Expected values depend on the active branch below; collapsing refresh_decision into an unnamed expression would weaken audits.
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / refresh_decision
        # TR: refresh_decision bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
        # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; refresh_decision değerini isimsiz ifadeye ezmek denetimi zayıflatır.
        refresh_decision = compute_robots_refresh_decision(
            conn=conn,
            host_id=claimed_host_id,
        )

        # EN: A missing refresh-decision row must degrade visibly and roll back the
        # EN: transient claim instead of crashing the worker or pretending refresh
        # EN: truth exists.
        # TR: Eksik refresh-decision satırı worker'ı çökertmek ya da refresh
        # TR: doğrusu varmış gibi davranmak yerine görünür biçimde degrade olmalı
        # TR: ve geçici claim rollback edilmelidir.
        if refresh_decision is None:
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / refresh_decision
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `{ "host_id": claimed_host_id, "robots_action": "compute_robots_refresh_decision", "robots_degraded": True, "robots_degraded_reason": "comput` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): refresh_decision
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / refresh_decision
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): refresh_decision
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            refresh_decision = {
                "host_id": claimed_host_id,
                "robots_action": "compute_robots_refresh_decision",
                "robots_degraded": True,
                "robots_degraded_reason": "compute_robots_refresh_decision_returned_no_row",
                "robots_completed": False,
                "error_class": "robots_refresh_decision_no_row",
                "error_message": "compute_robots_refresh_decision(...) returned no row",
            }

        if bool(refresh_decision.get("robots_degraded")):
            rollback(conn)
            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=None,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=dict(refresh_decision),
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: Probe mode stays non-durable: it may observe refresh need but must not
        # EN: write refreshed cache truth back into the database.
        # TR: Probe modu kalıcı olmayan mod olarak kalır; refresh ihtiyacını
        # TR: gözleyebilir ama yenilenmiş cache doğrusunu veritabanına yazmamalıdır.
        if (not config.probe_only) and refresh_decision.get("should_refresh"):
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / lease_renewal_result
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `renew_claimed_lease_before_durable_phase( conn, claimed_url=claimed_url, config=config, phase_label="robots_refresh", )` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): lease_renewal_result
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / lease_renewal_result
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): lease_renewal_result
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            lease_renewal_result = renew_claimed_lease_before_durable_phase(
                conn,
                claimed_url=claimed_url,
                config=config,
                phase_label="robots_refresh",
            )

            # EN: A degraded lease renewal before robots refresh means we must not
            # EN: continue into a durable robots write with unconfirmed lease truth.
            # TR: Robots refresh öncesi degrade olmuş lease renewal, teyit edilmemiş
            # TR: lease doğrusu ile kalıcı robots yazımına devam etmememiz gerektiği
            # TR: anlamına gelir.
            if bool(lease_renewal_result.get("lease_degraded")):
                rollback(conn)
                return ClaimProbeResult(
                    run_id=run_id,
                    claimed=False,
                    claimed_url=None,
                    robots_allow_decision=None,
                    storage_plan=storage_plan,
                    fetched_page=None,
                    finalize_result=dict(lease_renewal_result),
                    parse_apply_result=parse_apply_result,
                    observed_at=utc_now_iso(),
                    runtime_control=runtime_control,
                )

            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / refresh_result
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `refresh_robots_cache_if_needed( conn, claimed_url=claimed_url, refresh_decision=refresh_decision, )` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): refresh_result
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / refresh_result
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): refresh_result
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            refresh_result = refresh_robots_cache_if_needed(
                conn,
                claimed_url=claimed_url,
                refresh_decision=refresh_decision,
            )

            # EN: A degraded robots cache write must not fall through into later
            # EN: allow/block logic. We roll back the transient claim and return the
            # EN: visible degraded payload honestly.
            # TR: Degrade olmuş robots cache yazımı daha sonraki allow/block
            # TR: mantığına sızmamalıdır. Geçici claim'i rollback ediyor ve görünür
            # TR: degrade payload'ı dürüst biçimde döndürüyoruz.
            if bool(refresh_result.get("robots_degraded")):
                rollback(conn)
                return ClaimProbeResult(
                    run_id=run_id,
                    claimed=False,
                    claimed_url=None,
                    robots_allow_decision=None,
                    storage_plan=storage_plan,
                    fetched_page=None,
                    finalize_result=dict(refresh_result),
                    parse_apply_result=parse_apply_result,
                    observed_at=utc_now_iso(),
                    runtime_control=runtime_control,
                )

        # EN: After any needed durable refresh write, we ask for the current visible
        # EN: robots allow/block decision for the claimed path.
        # TR: Gereken kalıcı refresh yazımı sonrası claimed path için mevcut görünür
        # TR: robots allow/block kararını soruyoruz.
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / robots_allow_decision
        # EN: robots_allow_decision keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
        # EN: Expected values depend on the active branch below; collapsing robots_allow_decision into an unnamed expression would weaken audits.
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / robots_allow_decision
        # TR: robots_allow_decision bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
        # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; robots_allow_decision değerini isimsiz ifadeye ezmek denetimi zayıflatır.
        robots_allow_decision = compute_robots_allow_decision(
            conn=conn,
            host_id=claimed_host_id,
            url_path=claimed_url_path,
        )

        # EN: A missing allow-decision row must not silently become a robots block.
        # EN: We degrade visibly, roll back the transient claim, and return the
        # EN: unresolved robots state honestly.
        # TR: Eksik allow-decision satırı sessizce robots block'a dönüşmemelidir.
        # TR: Görünür biçimde degrade ediyor, geçici claim'i rollback ediyor ve
        # TR: çözülmemiş robots durumunu dürüst biçimde döndürüyoruz.
        if robots_allow_decision is None:
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / robots_allow_decision
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `{ "host_id": claimed_host_id, "url_path": claimed_url_path, "robots_action": "compute_robots_allow_decision", "robots_degraded": True, "robo` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): robots_allow_decision
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / robots_allow_decision
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): robots_allow_decision
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            robots_allow_decision = {
                "host_id": claimed_host_id,
                "url_path": claimed_url_path,
                "robots_action": "compute_robots_allow_decision",
                "robots_degraded": True,
                "robots_degraded_reason": "compute_robots_allow_decision_returned_no_row",
                "robots_completed": False,
                "error_class": "robots_allow_decision_no_row",
                "error_message": "compute_robots_allow_decision(...) returned no row",
            }

        if bool(robots_allow_decision.get("robots_degraded")):
            rollback(conn)
            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=dict(robots_allow_decision),
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=dict(robots_allow_decision),
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: Probe mode stays non-durable: claim + robots checks are observed and
        # EN: then rolled back.
        # TR: Probe modu kalıcı olmayan mod olarak kalır: claim + robots kontrolleri
        # TR: gözlenir ve sonra rollback edilir.
        if config.probe_only:
            rollback(conn)
            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=None,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: In durable mode we inspect the robots verdict before any real page
        # EN: fetch is attempted.
        # TR: Durable modda gerçek page fetch denenmeden önce robots verdict’ini
        # TR: inceliyoruz.
        # EN: LOCAL VALUE EXPLANATION / run_claim_probe / robots_verdict
        # EN: robots_verdict keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
        # EN: Expected values depend on the active branch below; collapsing robots_verdict into an unnamed expression would weaken audits.
        # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / robots_verdict
        # TR: robots_verdict bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
        # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; robots_verdict değerini isimsiz ifadeye ezmek denetimi zayıflatır.
        robots_verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")

        # EN: If robots forbids fetch, we finalize immediately through the durable
        # EN: robots-block path and commit that result.
        # TR: Robots fetch’i yasaklıyorsa kalıcı robots-block yolu üzerinden hemen
        # TR: finalize ediyor ve bu sonucu commit ediyoruz.
        if not robots_verdict_allows_fetch(robots_verdict):
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / finalize_result
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `finalize_robots_block( conn, claimed_url=claimed_url, robots_allow_decision=robots_allow_decision, worker_id=config.worker_id, )` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): finalize_result
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / finalize_result
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): finalize_result
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            finalize_result = finalize_robots_block(
                conn,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                worker_id=config.worker_id,
            )
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: If robots allows fetch, we enter the real durable acquisition path.
        # TR: Robots fetch’e izin veriyorsa gerçek kalıcı acquisition yoluna giriyoruz.
        try:
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / lease_renewal_result
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `renew_claimed_lease_before_durable_phase( conn, claimed_url=claimed_url, config=config, phase_label="page_fetch", )` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): lease_renewal_result
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / lease_renewal_result
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): lease_renewal_result
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            lease_renewal_result = renew_claimed_lease_before_durable_phase(
                conn,
                claimed_url=claimed_url,
                config=config,
                phase_label="page_fetch",
            )

            # EN: A degraded lease renewal before page fetch means we must not enter
            # EN: the real acquisition path with unresolved lease ownership.
            # TR: Page fetch öncesi degrade olmuş lease renewal, çözülmemiş lease
            # TR: sahipliği ile gerçek acquisition yoluna girmememiz gerektiği
            # TR: anlamına gelir.
            if bool(lease_renewal_result.get("lease_degraded")):
                rollback(conn)
                return ClaimProbeResult(
                    run_id=run_id,
                    claimed=False,
                    claimed_url=None,
                    robots_allow_decision=(
                        None if robots_allow_decision is None else dict(robots_allow_decision)
                    ),
                    storage_plan=storage_plan,
                    fetched_page=None,
                    finalize_result=dict(lease_renewal_result),
                    parse_apply_result=parse_apply_result,
                    observed_at=utc_now_iso(),
                    runtime_control=runtime_control,
                )

            # EN: We now delegate acquisition-path selection plus real fetch execution
            # EN: to the canonical acquisition hub. The worker consumes one normalized
            # EN: execution result instead of choosing direct child fetch surfaces inline.
            # TR: Artık acquisition-path seçimini ve gerçek fetch yürütmesini kanonik
            # TR: acquisition hub'a devrediyoruz. Worker doğrudan çocuk fetch yüzeyi
            # TR: seçmek yerine tek bir normalize execution sonucu tüketiyor.
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / acquisition_execution
            # EN: acquisition_execution keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
            # EN: Expected values depend on the active branch below; collapsing acquisition_execution into an unnamed expression would weaken audits.
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / acquisition_execution
            # TR: acquisition_execution bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
            # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; acquisition_execution değerini isimsiz ifadeye ezmek denetimi zayıflatır.
            acquisition_execution = fetch_page_via_selection_to_raw_storage(claimed_url)

            # EN: acquisition_method records the concrete method that actually produced
            # EN: the durable fetch result. Downstream logging/finalize surfaces should
            # EN: persist this actual method value.
            # TR: acquisition_method kalıcı fetch sonucunu gerçekten hangi somut yöntemin
            # TR: ürettiğini kaydeder. Aşağı akış logging/finalize yüzeyleri bu gerçek
            # TR: yöntem değerini kalıcılaştırmalıdır.
            acquisition_method = acquisition_execution.method_used

            # EN: fetched_page keeps the stable fetched-page contract expected by the
            # EN: rest of the worker success path.
            # TR: fetched_page worker başarı yolunun geri kalanının beklediği kararlı
            # TR: fetched-page sözleşmesini taşır.
            fetched_page = acquisition_execution.fetch_result

            # EN: We validate the fetched-page contract immediately so corrupted raw
            # EN: artefacts cannot silently enter parse/finalize logic.
            # TR: Bozuk ham artefact'lar sessizce parse/finalize mantığına girmesin
            # TR: diye fetched-page contract'ını hemen doğruluyoruz.
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / page_contract_validation
            # EN: page_contract_validation keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
            # EN: Expected values depend on the active branch below; collapsing page_contract_validation into an unnamed expression would weaken audits.
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / page_contract_validation
            # TR: page_contract_validation bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
            # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; page_contract_validation değerini isimsiz ifadeye ezmek denetimi zayıflatır.
            page_contract_validation = validate_fetched_page_result_contract(fetched_page)
            if page_contract_validation is not None:
                rollback(conn)
                return ClaimProbeResult(
                    run_id=run_id,
                    claimed=True,
                    claimed_url=claimed_url,
                    robots_allow_decision=(
                        None if robots_allow_decision is None else dict(robots_allow_decision)
                    ),
                    storage_plan=storage_plan,
                    fetched_page=fetched_page,
                    finalize_result=dict(page_contract_validation),
                    parse_apply_result=parse_apply_result,
                    observed_at=utc_now_iso(),
                    runtime_control=runtime_control,
                )

            # EN: The current narrow parse layer is HTML-first, so we only consider
            # EN: parse continuation for HTML-like successful fetches.
            # TR: Mevcut dar parse katmanı HTML-öncelikli olduğu için parse
            # TR: continuation’ı yalnızca HTML-benzeri başarılı fetch’lerde düşünürüz.
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / should_run_minimal_parse
            # EN: should_run_minimal_parse keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
            # EN: Expected values depend on the active branch below; collapsing should_run_minimal_parse into an unnamed expression would weaken audits.
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / should_run_minimal_parse
            # TR: should_run_minimal_parse bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
            # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; should_run_minimal_parse değerini isimsiz ifadeye ezmek denetimi zayıflatır.
            should_run_minimal_parse = (
                fetched_page.content_type is None
                or "html" in fetched_page.content_type.lower()
            )

            # EN: Before optional parse persistence, we ask PostgreSQL whether the
            # EN: connected database currently exposes the parse schema.
            # TR: Opsiyonel parse persistence’tan önce bağlı veritabanının parse
            # TR: şemasını gerçekten sağlayıp sağlamadığını PostgreSQL’e soruyoruz.
            with conn.cursor() as cur:
                cur.execute("select to_regnamespace('parse') is not null as parse_schema_exists")
                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / parse_schema_exists
                # EN: This local exists because the worker-runtime corridor should keep
                # EN: intermediate phase truth named, visible, and reviewable instead of hiding `bool(cur.fetchone()["parse_schema_exists"])` inline.
                # EN: Expected meaning:
                # EN: - current local name(s): parse_schema_exists
                # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                # EN: Undesired reading:
                # EN: - treating this local as durable global crawler truth
                # EN: - assuming this local alone proves the whole worker corridor succeeded
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / parse_schema_exists
                # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                # TR: Beklenen anlam:
                # TR: - mevcut yerel ad(lar): parse_schema_exists
                # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                parse_schema_exists = bool(cur.fetchone()["parse_schema_exists"])

            # EN: We attempt optional parse-apply only when the content is parse-
            # EN: suitable and the connected DB actually has the parse schema.
            # TR: Opsiyonel parse-apply’ı yalnızca içerik parse için uygunsa ve
            # TR: bağlı DB gerçekten parse şemasını içeriyorsa deneriz.
            if should_run_minimal_parse and parse_schema_exists:
                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / lease_renewal_result
                # EN: This local exists because the worker-runtime corridor should keep
                # EN: intermediate phase truth named, visible, and reviewable instead of hiding `renew_claimed_lease_before_durable_phase( conn, claimed_url=claimed_url, config=config, phase_label="parse_apply", )` inline.
                # EN: Expected meaning:
                # EN: - current local name(s): lease_renewal_result
                # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                # EN: Undesired reading:
                # EN: - treating this local as durable global crawler truth
                # EN: - assuming this local alone proves the whole worker corridor succeeded
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / lease_renewal_result
                # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                # TR: Beklenen anlam:
                # TR: - mevcut yerel ad(lar): lease_renewal_result
                # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                lease_renewal_result = renew_claimed_lease_before_durable_phase(
                    conn,
                    claimed_url=claimed_url,
                    config=config,
                    phase_label="parse_apply",
                )

                # EN: A degraded lease renewal before parse-apply means we must not
                # EN: continue durable parse writes under uncertain lease ownership.
                # EN: We surface the already-fetched artefact honestly and stop here.
                # TR: Parse-apply öncesi degrade olmuş lease renewal, belirsiz lease
                # TR: sahipliği altında kalıcı parse yazılarına devam etmememiz
                # TR: gerektiği anlamına gelir. Zaten fetch edilmiş artefact'ı
                # TR: dürüstçe görünür kılıyor ve burada duruyoruz.
                if bool(lease_renewal_result.get("lease_degraded")):
                    rollback(conn)
                    return ClaimProbeResult(
                        run_id=run_id,
                        claimed=True,
                        claimed_url=claimed_url,
                        robots_allow_decision=robots_allow_decision,
                        storage_plan=storage_plan,
                        fetched_page=fetched_page,
                        finalize_result=dict(lease_renewal_result),
                        parse_apply_result=parse_apply_result,
                        observed_at=utc_now_iso(),
                        runtime_control=runtime_control,
                    )

                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / parse_apply_result
                # EN: This local exists because the worker-runtime corridor should keep
                # EN: intermediate phase truth named, visible, and reviewable instead of hiding `apply_minimal_parse_entry( conn=conn, url_id=int(get_claimed_url_value(claimed_url, "url_id")), raw_storage_path=fetched_page.raw_storage_pa` inline.
                # EN: Expected meaning:
                # EN: - current local name(s): parse_apply_result
                # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                # EN: Undesired reading:
                # EN: - treating this local as durable global crawler truth
                # EN: - assuming this local alone proves the whole worker corridor succeeded
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / parse_apply_result
                # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                # TR: Beklenen anlam:
                # TR: - mevcut yerel ad(lar): parse_apply_result
                # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                parse_apply_result = apply_minimal_parse_entry(
                    conn=conn,
                    url_id=int(get_claimed_url_value(claimed_url, "url_id")),
                    raw_storage_path=fetched_page.raw_storage_path,
                    source_run_id=run_id,
                    source_note="minimal parse continuation from worker runtime success path",
                )

            # EN: Only after all same-lease durable success-side work is complete do
            # EN: we write terminal per-attempt evidence and finalize success exactly once.
            # TR: Aynı lease altında yapılacak tüm kalıcı başarı-tarafı iş
            # TR: tamamlandıktan sonra terminal deneme kanıtını yazıyor ve başarıyı
            # TR: tam bir kez finalize ediyoruz.
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / fetch_attempt_log
            # EN: fetch_attempt_log keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
            # EN: Expected values depend on the active branch below; collapsing fetch_attempt_log into an unnamed expression would weaken audits.
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / fetch_attempt_log
            # TR: fetch_attempt_log bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
            # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; fetch_attempt_log değerini isimsiz ifadeye ezmek denetimi zayıflatır.
            fetch_attempt_log = log_fetch_attempt_terminal_from_worker(
                conn,
                claimed_url=claimed_url,
                worker_id=config.worker_id,
                outcome="success",
                note="worker runtime success finalize path",
                acquisition_method=acquisition_method,
                fetched_page=fetched_page,
                error_class=None,
                error_message=None,
            )

            # EN: Success-side frontier functions may still return no row on some
            # EN: drift paths. We degrade those paths explicitly so already-written
            # EN: durable evidence can still commit honestly instead of crashing.
            # TR: Başarı-tarafı frontier fonksiyonları bazı drift yollarında hâlâ
            # TR: satır döndürmeyebilir. Bu yolları açıkça degrade ediyoruz; böylece
            # TR: zaten yazılmış kalıcı kanıt dürüst biçimde commit olabilir.
            try:
                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / success_finalize_result
                # EN: This local exists because the worker-runtime corridor should keep
                # EN: intermediate phase truth named, visible, and reviewable instead of hiding `finish_fetch_success( conn, url_id=fetched_page.url_id, lease_token=str(get_claimed_url_value(claimed_url, "lease_token")), http_status=fetc` inline.
                # EN: Expected meaning:
                # EN: - current local name(s): success_finalize_result
                # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                # EN: Undesired reading:
                # EN: - treating this local as durable global crawler truth
                # EN: - assuming this local alone proves the whole worker corridor succeeded
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / success_finalize_result
                # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                # TR: Beklenen anlam:
                # TR: - mevcut yerel ad(lar): success_finalize_result
                # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                success_finalize_result = finish_fetch_success(
                    conn,
                    url_id=fetched_page.url_id,
                    lease_token=str(get_claimed_url_value(claimed_url, "lease_token")),
                    http_status=fetched_page.http_status,
                    content_type=fetched_page.content_type,
                    body_bytes=fetched_page.body_bytes,
                    etag=fetched_page.etag,
                    last_modified=fetched_page.last_modified,
                )

                # EN: Success finalization intentionally lands on transient parse_pending
                # EN: first. After optional parse-side durable work has completed or been
                # EN: deliberately skipped, we release that transient row back to queued.
                # TR: Success finalization bilinçli olarak önce geçici parse_pending
                # TR: durumuna iner. Opsiyonel parse-tarafı kalıcı iş tamamlandıktan ya
                # TR: da bilinçli olarak atlandıktan sonra bu geçici satırı queued
                # TR: durumuna bırakıyoruz.
                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / release_result
                # EN: release_result keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
                # EN: Expected values depend on the active branch below; collapsing release_result into an unnamed expression would weaken audits.
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / release_result
                # TR: release_result bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
                # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; release_result değerini isimsiz ifadeye ezmek denetimi zayıflatır.
                release_result = release_parse_pending_to_queued(
                    conn=conn,
                    url_id=int(get_claimed_url_value(claimed_url, "url_id")),
                )

                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / success_finalize_payload
                # EN: This local exists because the worker-runtime corridor should keep
                # EN: intermediate phase truth named, visible, and reviewable instead of hiding `{ **dict(success_finalize_result), "frontier_release": dict(release_result), }` inline.
                # EN: Expected meaning:
                # EN: - current local name(s): success_finalize_payload
                # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                # EN: Undesired reading:
                # EN: - treating this local as durable global crawler truth
                # EN: - assuming this local alone proves the whole worker corridor succeeded
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / success_finalize_payload
                # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                # TR: Beklenen anlam:
                # TR: - mevcut yerel ad(lar): success_finalize_payload
                # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                success_finalize_payload = {
                    **dict(success_finalize_result),
                    "frontier_release": dict(release_result),
                }

            except RuntimeError as exc:
                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / exc_text
                # EN: This local exists because the worker-runtime corridor should keep
                # EN: intermediate phase truth named, visible, and reviewable instead of hiding `str(exc)` inline.
                # EN: Expected meaning:
                # EN: - current local name(s): exc_text
                # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                # EN: Undesired reading:
                # EN: - treating this local as durable global crawler truth
                # EN: - assuming this local alone proves the whole worker corridor succeeded
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / exc_text
                # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                # TR: Beklenen anlam:
                # TR: - mevcut yerel ad(lar): exc_text
                # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                exc_text = str(exc)

                if "frontier.finish_fetch_success(...) returned no row" in exc_text:
                    # EN: LOCAL VALUE EXPLANATION / run_claim_probe / success_finalize_payload
                    # EN: This local exists because the worker-runtime corridor should keep
                    # EN: intermediate phase truth named, visible, and reviewable instead of hiding `{ "url_id": fetched_page.url_id, "lease_token": str(get_claimed_url_value(claimed_url, "lease_token")), "http_status": fetched_page.http_sta` inline.
                    # EN: Expected meaning:
                    # EN: - current local name(s): success_finalize_payload
                    # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                    # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                    # EN: Undesired reading:
                    # EN: - treating this local as durable global crawler truth
                    # EN: - assuming this local alone proves the whole worker corridor succeeded
                    # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / success_finalize_payload
                    # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                    # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                    # TR: Beklenen anlam:
                    # TR: - mevcut yerel ad(lar): success_finalize_payload
                    # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                    # TR: İstenmeyen okuma:
                    # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                    # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                    success_finalize_payload = {
                        "url_id": fetched_page.url_id,
                        "lease_token": str(get_claimed_url_value(claimed_url, "lease_token")),
                        "http_status": fetched_page.http_status,
                        "content_type": fetched_page.content_type,
                        "body_bytes": fetched_page.body_bytes,
                        "etag": fetched_page.etag,
                        "last_modified": fetched_page.last_modified,
                        "error_class": "success_finalize_no_row",
                        "error_message": f"success finalize no-row after durable fetch: {exc}",
                        "finalize_degraded": True,
                        "finalize_degraded_reason": "frontier_finish_fetch_success_returned_no_row",
                        "finalize_completed": False,
                    }

                elif "frontier.release_parse_pending_to_queued(...) returned no row" in exc_text:
                    # EN: LOCAL VALUE EXPLANATION / run_claim_probe / success_finalize_payload
                    # EN: This local exists because the worker-runtime corridor should keep
                    # EN: intermediate phase truth named, visible, and reviewable instead of hiding `{ **dict(success_finalize_result), "frontier_release": { "url_id": int(get_claimed_url_value(claimed_url, "url_id")), "release_degraded": Tr` inline.
                    # EN: Expected meaning:
                    # EN: - current local name(s): success_finalize_payload
                    # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                    # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                    # EN: Undesired reading:
                    # EN: - treating this local as durable global crawler truth
                    # EN: - assuming this local alone proves the whole worker corridor succeeded
                    # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / success_finalize_payload
                    # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                    # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                    # TR: Beklenen anlam:
                    # TR: - mevcut yerel ad(lar): success_finalize_payload
                    # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                    # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                    # TR: İstenmeyen okuma:
                    # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                    # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                    success_finalize_payload = {
                        **dict(success_finalize_result),
                        "frontier_release": {
                            "url_id": int(get_claimed_url_value(claimed_url, "url_id")),
                            "release_degraded": True,
                            "release_degraded_reason": "frontier_release_parse_pending_to_queued_returned_no_row",
                            "release_completed": False,
                            "error_message": f"success release no-row after durable fetch: {exc}",
                        },
                    }

                else:
                    raise

            # EN: We merge fetch-attempt evidence into the final success payload no
            # EN: matter whether the frontier success-side path completed or degraded.
            # TR: Frontier başarı-tarafı yol tamamlanmış ya da degrade olmuş olsun,
            # TR: fetch-attempt kanıtını her durumda nihai başarı payload’ına birleştiriyoruz.
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / finalize_result
            # EN: finalize_result keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
            # EN: Expected values depend on the active branch below; collapsing finalize_result into an unnamed expression would weaken audits.
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / finalize_result
            # TR: finalize_result bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
            # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; finalize_result değerini isimsiz ifadeye ezmek denetimi zayıflatır.
            finalize_result = {
                **success_finalize_payload,
                "fetch_attempt_log": dict(fetch_attempt_log),
            }

            # EN: We commit once so claim, raw evidence, optional parse evidence,
            # EN: success-side state, and operator-visible degradation truth become
            # EN: durable together.
            # TR: Claim, ham kanıt, opsiyonel parse kanıtı, başarı-tarafı durum ve
            # TR: operatör-görünür degrade doğrusu birlikte kalıcı olsun diye bir kez
            # TR: commit ediyoruz.
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=fetched_page,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: HTTPError means the upstream returned an explicit HTTP failure status.
        # TR: HTTPError upstream’in açık bir HTTP hata durumu döndürdüğü anlamına gelir.
        except HTTPError as exc:
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / finalize_result
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `finalize_http_error( conn, claimed_url=claimed_url, http_status=int(exc.code), error_message=f"HTTPError {exc.code}: {exc.reason}", worker_i` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): finalize_result
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / finalize_result
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): finalize_result
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            finalize_result = finalize_http_error(
                conn,
                claimed_url=claimed_url,
                http_status=int(exc.code),
                error_message=f"HTTPError {exc.code}: {exc.reason}",
                worker_id=config.worker_id,
            )
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: URLError, TimeoutError, and socket timeout failures are treated as
        # EN: retryable transport failures by this minimal layer.
        # TR: URLError, TimeoutError ve socket timeout hataları bu minimal katmanda
        # TR: retryable taşıma hataları olarak ele alınır.
        except (URLError, TimeoutError, socket.timeout) as exc:
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / finalize_result
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `finalize_transport_error( conn, claimed_url=claimed_url, error_message=f"{type(exc).__name__}: {exc}", worker_id=config.worker_id, )` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): finalize_result
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / finalize_result
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): finalize_result
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            finalize_result = finalize_transport_error(
                conn,
                claimed_url=claimed_url,
                error_message=f"{type(exc).__name__}: {exc}",
                worker_id=config.worker_id,
            )
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )

        # EN: Any other unexpected failure is finalized as permanent so the worker
        # EN: fails loudly instead of hiding unknown drift.
        # TR: Diğer tüm beklenmeyen hatalar minimal worker bilinmeyen drift’i
        # TR: gizlemesin diye permanent olarak finalize edilir.
        except Exception as exc:
            # EN: Any prior SQL failure may have left the transaction aborted.
            # EN: We must rollback before entering finalize/logging paths.
            # TR: Önceki SQL hatası transaction'ı aborted bırakmış olabilir.
            # TR: finalize/logging yoluna girmeden önce rollback zorunludur.
            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / rollback_error_message
            # EN: rollback_error_message keeps this intermediate worker-runtime truth named, visible, and reviewable instead of hiding it inline.
            # EN: Expected values depend on the active branch below; collapsing rollback_error_message into an unnamed expression would weaken audits.
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / rollback_error_message
            # TR: rollback_error_message bu ara worker-runtime doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutar.
            # TR: Beklenen değerler aşağıdaki aktif dala göre değişir; rollback_error_message değerini isimsiz ifadeye ezmek denetimi zayıflatır.
            rollback_error_message = None
            try:
                rollback(conn)
            except Exception as rollback_exc:
                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / rollback_error_message
                # EN: This local exists because the worker-runtime corridor should keep
                # EN: intermediate phase truth named, visible, and reviewable instead of hiding `f"{type(rollback_exc).__name__}: {rollback_exc}"` inline.
                # EN: Expected meaning:
                # EN: - current local name(s): rollback_error_message
                # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                # EN: Undesired reading:
                # EN: - treating this local as durable global crawler truth
                # EN: - assuming this local alone proves the whole worker corridor succeeded
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / rollback_error_message
                # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                # TR: Beklenen anlam:
                # TR: - mevcut yerel ad(lar): rollback_error_message
                # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                rollback_error_message = f"{type(rollback_exc).__name__}: {rollback_exc}"

            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / final_error_message
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `f"{type(exc).__name__}: {exc}"` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): final_error_message
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / final_error_message
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): final_error_message
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            final_error_message = f"{type(exc).__name__}: {exc}"
            if rollback_error_message is not None:
                # EN: LOCAL VALUE EXPLANATION / run_claim_probe / final_error_message
                # EN: This local exists because the worker-runtime corridor should keep
                # EN: intermediate phase truth named, visible, and reviewable instead of hiding `f"{final_error_message} | " f"rollback_before_finalize_failed: {rollback_error_message}"` inline.
                # EN: Expected meaning:
                # EN: - current local name(s): final_error_message
                # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
                # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
                # EN: Undesired reading:
                # EN: - treating this local as durable global crawler truth
                # EN: - assuming this local alone proves the whole worker corridor succeeded
                # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / final_error_message
                # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
                # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
                # TR: Beklenen anlam:
                # TR: - mevcut yerel ad(lar): final_error_message
                # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
                # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
                # TR: İstenmeyen okuma:
                # TR: - bu yereli kalıcı global crawler doğrusu sanmak
                # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
                final_error_message = (
                    f"{final_error_message} | "
                    f"rollback_before_finalize_failed: {rollback_error_message}"
                )

            # EN: LOCAL VALUE EXPLANATION / run_claim_probe / finalize_result
            # EN: This local exists because the worker-runtime corridor should keep
            # EN: intermediate phase truth named, visible, and reviewable instead of hiding `finalize_unexpected_runtime_error( conn, claimed_url=claimed_url, error_message=final_error_message, worker_id=config.worker_id, )` inline.
            # EN: Expected meaning:
            # EN: - current local name(s): finalize_result
            # EN: - this value helps keep claim / robots / fetch / parse / finalize / release branch meaning readable
            # EN: - None, empty, fallback, or branch-sensitive values may still be valid depending on the checks below
            # EN: Undesired reading:
            # EN: - treating this local as durable global crawler truth
            # EN: - assuming this local alone proves the whole worker corridor succeeded
            # TR: YEREL DEĞER AÇIKLAMASI / run_claim_probe / finalize_result
            # TR: Bu yerel değer vardır; çünkü worker-runtime koridoru ara faz
            # TR: doğrusunu satır içine gizlemek yerine isimli, görünür ve denetlenebilir tutmalıdır.
            # TR: Beklenen anlam:
            # TR: - mevcut yerel ad(lar): finalize_result
            # TR: - bu değer claim / robots / fetch / parse / finalize / release dal anlamını okunabilir tutmaya yardım eder
            # TR: - None, boş, fallback veya dala duyarlı değerler aşağıdaki kontrollere göre yine geçerli olabilir
            # TR: İstenmeyen okuma:
            # TR: - bu yereli kalıcı global crawler doğrusu sanmak
            # TR: - yalnızca bu yerelin tüm worker koridorunun başarılı olduğunu kanıtladığını düşünmek
            finalize_result = finalize_unexpected_runtime_error(
                conn,
                claimed_url=claimed_url,
                error_message=final_error_message,
                worker_id=config.worker_id,
            )
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=None,
                finalize_result=finalize_result,
                parse_apply_result=parse_apply_result,
                observed_at=utc_now_iso(),
                runtime_control=runtime_control,
            )
    finally:
        # EN: We always close the connection even if an error occurs.
        # TR: Hata oluşsa bile bağlantıyı her durumda kapatıyoruz.
        close_db(conn)


# EN: This explicit export list keeps the parent public surface honest.
# EN: main_loop should continue depending only on WorkerConfig and run_claim_probe.
# TR: Bu açık export listesi parent public yüzeyini dürüst tutar.
# TR: main_loop yalnızca WorkerConfig ve run_claim_probe’a bağlı kalmaya devam etmelidir.
__all__ = [
    "WorkerConfig",
    "ClaimProbeResult",
    "run_claim_probe",
]
