# EN: This module is now the thinner worker-runtime parent after the controlled
# EN: split. It keeps the parent-visible dataclasses plus the parent orchestration
# EN: flow, while lower children own support/finalize/robots/lease logic.
# TR: Bu modül kontrollü split sonrası artık daha ince worker-runtime parent
# TR: yüzeyidir. Parent-görünür dataclass’ları ve parent orchestration akışını
# TR: tutar; daha alt çocuklar ise support/finalize/robots/lease mantığını sahiplenir.

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
from .logisticsearch1_1_2_1_storage_routing import (
    ProcessedOutputPlan,
    choose_processed_output_plan,
)

# EN: We import the stable acquisition-family public surface. The parent still
# EN: chooses between HTTP and browser acquisition and still consumes the same
# EN: fetched-page contract shape.
# TR: Kararlı acquisition-aile public yüzeyini içe aktarıyoruz. Parent hâlâ HTTP
# TR: ve browser acquisition arasında seçim yapar ve aynı fetched-page sözleşme
# TR: şeklini tüketir.
from .logisticsearch1_1_2_2_acquisition_runtime import (
    FetchedPageResult,
    fetch_page_to_raw_storage,
    fetch_page_with_browser_to_raw_storage,
    get_claimed_url_value,
)

# EN: We import the canonical parse continuation surface because successful fetch
# EN: flows may still continue into minimal parse persistence.
# TR: Başarılı fetch akışları minimal parse persistence aşamasına devam
# TR: edebileceği için kanonik parse continuation yüzeyini içe aktarıyoruz.
from .logisticsearch1_1_2_3_parse_runtime import (
    MinimalParseApplyResult,
    apply_minimal_parse_entry,
)

# EN: We import the tiny runtime support child for generic parent-neutral helpers.
# TR: Parent-nötr küçük yardımcılar için küçük runtime support alt yüzeyini içe
# TR: aktarıyoruz.
from .logisticsearch1_1_2_4_worker_runtime_support import (
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
from .logisticsearch1_1_2_6_worker_robots_runtime import (
    refresh_robots_cache_if_needed,
    robots_verdict_allows_fetch,
)

# EN: We import the lease child because explicit lease renewal is a separate
# EN: durable-boundary helper, not parent-inline logic anymore.
# TR: Açık lease yenilemesi ayrı bir durable-boundary yardımcısıdır; artık parent
# TR: içinde inline mantık olarak durmaması gerektiği için lease alt yüzeyini
# TR: içe aktarıyoruz.
from .logisticsearch1_1_2_7_worker_lease_runtime import (
    renew_claimed_lease_before_durable_phase,
)


# EN: This dataclass stores runtime configuration for the public worker surface.
# TR: Bu dataclass public worker yüzeyi için runtime konfigürasyonunu tutar.
@dataclass(slots=True)
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


# EN: This helper decides which acquisition method should be used for the current
# EN: claimed URL. The rule remains intentionally narrow and conservative.
# TR: Bu yardımcı mevcut claimed URL için hangi acquisition yönteminin
# TR: kullanılacağını belirler. Kural bilinçli olarak dar ve muhafazakâr kalır.
def select_acquisition_method_for_claimed_url(claimed_url: object) -> str:
    # EN: We first try attribute-style access because current claimed-url rows are
    # EN: usually exposed as attribute-bearing objects.
    # TR: Önce attribute tarzı erişimi deniyoruz; çünkü mevcut claimed-url satırları
    # TR: genellikle attribute taşıyan nesneler olarak görünür.
    method_value = getattr(claimed_url, "acquisition_method", None)

    # EN: If attribute-style access produced no value, we also support dict-like
    # EN: rows so this seam stays robust across narrow row-shape differences.
    # TR: Attribute erişimi değer üretmediyse dict-benzeri satırları da destekliyoruz;
    # TR: böylece bu seam dar satır-şekli farklarına karşı dayanıklı kalır.
    if method_value is None and isinstance(claimed_url, dict):
        method_value = claimed_url.get("acquisition_method")

    # EN: Missing value means current canonical behavior stays on the direct HTTP path.
    # TR: Değer yoksa güncel kanonik davranış direct HTTP yolunda kalır.
    if method_value is None:
        return "http"

    # EN: We normalize to a lowercase token so one explicit branch can decide the path.
    # TR: Tek bir açık branch yolu belirleyebilsin diye değeri küçük-harf token’a
    # TR: normalize ediyoruz.
    normalized_method = str(method_value).strip().lower()

    # EN: Only the explicit browser token switches the runtime into the browser path.
    # TR: Yalnızca açık browser token’ı runtime’ı browser yoluna geçirir.
    if normalized_method == "browser":
        return "browser"

    # EN: Every other value falls back to the stable direct HTTP path.
    # TR: Diğer her değer stabil direct HTTP yoluna geri düşer.
    return "http"


# EN: This function performs one controlled worker execution. The parent still
# EN: owns the orchestration order:
# EN: storage gate -> runtime control gate -> claim -> robots gate/refresh ->
# EN: acquisition -> optional parse -> success/error finalize -> commit/return.
# TR: Bu fonksiyon tek bir kontrollü worker çalıştırması yapar. Parent hâlâ şu
# TR: orchestration sırasını sahiplenir:
# TR: storage kapısı -> runtime control kapısı -> claim -> robots kapısı/refresh ->
# TR: acquisition -> opsiyonel parse -> success/error finalize -> commit/return.
def run_claim_probe(config: WorkerConfig) -> ClaimProbeResult:
    # EN: We create a unique run id first so the whole execution can be traced.
    # TR: Tüm çalıştırma izlenebilir olsun diye önce benzersiz bir run id üretiyoruz.
    run_id = new_run_id()

    # EN: We start with no runtime-control snapshot because the worker has not yet
    # EN: consulted the DB truth surface.
    # TR: Worker henüz DB doğruluk yüzeyine bakmadığı için başlangıçta runtime-control
    # TR: anlık görüntümüz yoktur.
    runtime_control = None

    # EN: We compute the current storage plan before touching the DB because the
    # EN: crawler must not claim new work when storage policy says pause.
    # TR: Crawler storage politikası pause diyorsa yeni iş claim etmemeli; bu yüzden
    # TR: DB’ye dokunmadan önce mevcut storage planı hesaplıyoruz.
    storage_plan = choose_processed_output_plan()

    # EN: We start with no parse-apply result because parse continuation should
    # EN: appear only after a successful fetch path reaches that stage.
    # TR: Parse continuation yalnızca başarılı fetch yolu o aşamaya ulaşınca
    # TR: ortaya çıkması gerektiği için başlangıçta parse-apply sonucu yoktur.
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
    conn = connect_db(config.dsn)

    try:
        # EN: Before asking crawler-core for claimable work, we read the visible
        # EN: runtime-control truth from the database.
        # TR: crawler-core’dan claim edilebilir iş istemeden önce veritabanındaki
        # TR: görünür runtime-control doğrusunu okuyoruz.
        runtime_control = get_webcrawler_runtime_control(conn)
        if runtime_control is None:
            raise RuntimeError("get_webcrawler_runtime_control(...) returned no row")

        # EN: We then ask the canonical DB control function whether claiming is
        # EN: currently allowed.
        # TR: Ardından claim etmenin şu anda izinli olup olmadığını kanonik DB
        # TR: kontrol fonksiyonuna soruyoruz.
        may_claim_result = webcrawler_runtime_may_claim(conn)
        if may_claim_result is None:
            raise RuntimeError("webcrawler_runtime_may_claim(...) returned no row")

        # EN: We merge the explicit may-claim decision into the runtime-control
        # EN: snapshot so the returned JSON remains self-explanatory.
        # TR: Dönen JSON kendi kendini açıklayabilsin diye açık may-claim kararını
        # TR: runtime-control anlık görüntüsüne birleştiriyoruz.
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
        claimed_host_id = int(get_claimed_url_value(claimed_url, "host_id"))
        claimed_url_path = str(get_claimed_url_value(claimed_url, "url_path"))

        # EN: We inspect the canonical DB-side refresh decision first because the
        # EN: worker contract says robots cache truth must be refreshed when needed.
        # TR: Worker sözleşmesi gerektiğinde robots cache doğrusunun yenilenmesini
        # TR: söylediği için önce kanonik DB-side refresh kararını inceliyoruz.
        refresh_decision = compute_robots_refresh_decision(
            conn=conn,
            host_id=claimed_host_id,
        )
        if refresh_decision is None:
            raise RuntimeError("compute_robots_refresh_decision(...) returned no row")

        # EN: Probe mode stays non-durable: it may observe refresh need but must not
        # EN: write refreshed cache truth back into the database.
        # TR: Probe modu kalıcı olmayan mod olarak kalır; refresh ihtiyacını
        # TR: gözleyebilir ama yenilenmiş cache doğrusunu veritabanına yazmamalıdır.
        if (not config.probe_only) and refresh_decision.get("should_refresh"):
            renew_claimed_lease_before_durable_phase(
                conn,
                claimed_url=claimed_url,
                config=config,
                phase_label="robots_refresh",
            )

            refresh_robots_cache_if_needed(
                conn,
                claimed_url=claimed_url,
                refresh_decision=refresh_decision,
            )

        # EN: After any needed durable refresh write, we ask for the current visible
        # EN: robots allow/block decision for the claimed path.
        # TR: Gereken kalıcı refresh yazımı sonrası claimed path için mevcut görünür
        # TR: robots allow/block kararını soruyoruz.
        robots_allow_decision = compute_robots_allow_decision(
            conn=conn,
            host_id=claimed_host_id,
            url_path=claimed_url_path,
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
        robots_verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")

        # EN: If robots forbids fetch, we finalize immediately through the durable
        # EN: robots-block path and commit that result.
        # TR: Robots fetch’i yasaklıyorsa kalıcı robots-block yolu üzerinden hemen
        # TR: finalize ediyor ve bu sonucu commit ediyoruz.
        if not robots_verdict_allows_fetch(robots_verdict):
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
            renew_claimed_lease_before_durable_phase(
                conn,
                claimed_url=claimed_url,
                config=config,
                phase_label="page_fetch",
            )

            # EN: We select one explicit acquisition method seam.
            # TR: Tek bir açık acquisition method seam seçiyoruz.
            acquisition_method = select_acquisition_method_for_claimed_url(claimed_url)

            # EN: Browser is used only when the claimed row explicitly requests it.
            # EN: Otherwise direct HTTP stays the default path.
            # TR: Browser yalnızca claimed satır bunu açıkça isterse kullanılır.
            # TR: Aksi halde varsayılan yol direct HTTP olarak kalır.
            if acquisition_method == "browser":
                fetched_page = fetch_page_with_browser_to_raw_storage(claimed_url)
            else:
                fetched_page = fetch_page_to_raw_storage(claimed_url)

            # EN: The current narrow parse layer is HTML-first, so we only consider
            # EN: parse continuation for HTML-like successful fetches.
            # TR: Mevcut dar parse katmanı HTML-öncelikli olduğu için parse
            # TR: continuation’ı yalnızca HTML-benzeri başarılı fetch’lerde düşünürüz.
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
                parse_schema_exists = bool(cur.fetchone()["parse_schema_exists"])

            # EN: We attempt optional parse-apply only when the content is parse-
            # EN: suitable and the connected DB actually has the parse schema.
            # TR: Opsiyonel parse-apply’ı yalnızca içerik parse için uygunsa ve
            # TR: bağlı DB gerçekten parse şemasını içeriyorsa deneriz.
            if should_run_minimal_parse and parse_schema_exists:
                renew_claimed_lease_before_durable_phase(
                    conn,
                    claimed_url=claimed_url,
                    config=config,
                    phase_label="parse_apply",
                )

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

            finalize_result = finish_fetch_success(
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
            release_result = release_parse_pending_to_queued(
                conn=conn,
                url_id=int(get_claimed_url_value(claimed_url, "url_id")),
            )

            # EN: We merge release evidence into the final success payload so the
            # EN: returned JSON shows both success finalize and queue release truth.
            # TR: Dönen JSON hem başarı finalization’ını hem de queue release
            # TR: doğrusunu göstersin diye release kanıtını nihai payload’a
            # TR: birleştiriyoruz.
            finalize_result = {
                **dict(finalize_result),
                "fetch_attempt_log": dict(fetch_attempt_log),
                "frontier_release": dict(release_result),
            }

            # EN: We commit once so claim, raw evidence, optional parse evidence,
            # EN: success finalize, and queue release become durable together.
            # TR: Claim, ham kanıt, opsiyonel parse kanıtı, success finalize ve
            # TR: queue release birlikte kalıcı olsun diye bir kez commit ediyoruz.
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
            finalize_result = finalize_unexpected_runtime_error(
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
    "select_acquisition_method_for_claimed_url",
    "run_claim_probe",
]
