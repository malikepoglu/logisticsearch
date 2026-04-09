# EN: We enable postponed evaluation of annotations so type hints stay readable
# EN: even when they refer to classes declared later in the file.
# TR: Type hint'ler dosyada daha sonra tanımlanan sınıflara referans verse bile
# TR: okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import dataclass because configuration and result objects become much
# EN: easier to inspect when every field is explicit and named.
# TR: Konfigürasyon ve sonuç nesneleri her alan açık ve isimli olduğunda çok
# TR: daha kolay incelendiği için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import datetime and timezone so observed timestamps stay explicit and UTC-based.
# TR: Gözlenen zaman damgaları açık ve UTC tabanlı kalsın diye datetime ve timezone
# TR: içe aktarıyoruz.
from datetime import datetime, timezone

# EN: We import socket because socket-level timeout and transport failures should
# EN: be classified explicitly in the minimal fetch runtime path.
# TR: Socket düzeyi timeout ve taşıma hataları minimal fetch runtime yolunda açıkça
# TR: sınıflandırılmalı diye socket içe aktarıyoruz.
import socket

# EN: We import uuid4 so every worker execution can get a unique run id.
# TR: Her worker çalıştırması benzersiz bir run id alabilsin diye uuid4 içe aktarıyoruz.
from uuid import uuid4

# EN: We import HTTPError and URLError because the minimal fetch flow must separate
# EN: HTTP status failures from lower-level transport failures.
# TR: Minimal fetch akışı HTTP durum hatalarını daha alt düzey taşıma hatalarından
# TR: ayırmak zorunda olduğu için HTTPError ve URLError içe aktarıyoruz.
from urllib.error import HTTPError, URLError

# EN: These DB helpers express the current canonical crawler-core interaction points.
# EN: We now import not only claim/robots helpers but also the finalize helpers.
# TR: Bu DB yardımcıları mevcut kanonik crawler-core etkileşim noktalarını ifade eder.
# TR: Artık yalnızca claim/robots yardımcılarını değil finalize yardımcılarını da içe aktarıyoruz.
from .db import (
    claim_next_url,
    close_db,
    commit,
    compute_robots_allow_decision,
    connect_db,
    finish_fetch_permanent_error,
    finish_fetch_retryable_error,
    finish_fetch_success,
    rollback,
)

# EN: We import the minimal processed-output storage planner because the worker
# EN: must refuse new work when storage policy says normal flow should pause.
# TR: Worker normal akış pause olmalıysa yeni iş almamalı; bu yüzden minimal
# TR: işlenmiş-çıktı storage planlayıcısını içe aktarıyoruz.
from .storage_routing import ProcessedOutputPlan, choose_processed_output_plan

# EN: We import the minimal real fetch helper and its structured result object
# EN: because durable worker mode now performs a real HTTP fetch plus raw-body write.
# TR: Durable worker modu artık gerçek HTTP fetch ve ham body yazımı yaptığı için
# TR: minimal gerçek fetch yardımcısını ve yapılı sonuç nesnesini içe aktarıyoruz.
from .fetch_runtime import FetchedPageResult, fetch_page_to_raw_storage


# EN: This dataclass stores runtime configuration for the current worker surface.
# TR: Bu dataclass mevcut worker yüzeyi için runtime konfigürasyonunu tutar.
@dataclass(slots=True)
class WorkerConfig:
    # EN: dsn is the PostgreSQL connection string used by this worker runtime.
    # TR: dsn bu worker runtime tarafından kullanılan PostgreSQL bağlantı metnidir.
    dsn: str

    # EN: worker_id is the textual worker identity passed into frontier.claim_next_url(...).
    # TR: worker_id frontier.claim_next_url(...) içine verilen metinsel worker kimliğidir.
    worker_id: str

    # EN: lease_seconds says how long a claimed lease should stay valid before
    # EN: lease renewal would become necessary.
    # TR: lease_seconds claim edilmiş bir lease'in renewal gerekmeden önce ne kadar
    # TR: süre geçerli kalacağını söyler.
    lease_seconds: int = 600

    # EN: probe_only keeps the worker in non-durable verification mode when True.
    # EN: When False, the worker executes the minimal real fetch + finalize path.
    # TR: probe_only True olduğunda worker'ı kalıcı olmayan doğrulama modunda tutar.
    # TR: False olduğunda worker minimal gerçek fetch + finalize yolunu çalıştırır.
    probe_only: bool = True


# EN: This dataclass stores the result of one worker execution.
# TR: Bu dataclass tek bir worker çalıştırmasının sonucunu tutar.
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

    # EN: robots_allow_decision stores the current visible robots allow/block
    # EN: decision for the claimed row when a claim succeeded.
    # TR: robots_allow_decision claim başarılıysa claim edilen satır için mevcut
    # TR: görünür robots allow/block kararını tutar.
    robots_allow_decision: dict | None

    # EN: storage_plan stores the current minimal processed-output storage decision.
    # TR: storage_plan mevcut minimal işlenmiş-çıktı storage kararını tutar.
    storage_plan: ProcessedOutputPlan

    # EN: fetched_page stores the real fetch result when durable mode actually fetched a page.
    # TR: fetched_page durable mod gerçekten bir page fetch ettiyse gerçek fetch sonucunu tutar.
    fetched_page: FetchedPageResult | None

    # EN: finalize_result stores the canonical finalize SQL result when the worker
    # EN: reached a durable finalize decision.
    # TR: finalize_result worker kalıcı bir finalize kararına ulaştıysa kanonik
    # TR: finalize SQL sonucunu tutar.
    finalize_result: dict | None

    # EN: observed_at records when this result object was produced.
    # TR: observed_at bu sonuç nesnesinin ne zaman üretildiğini kaydeder.
    observed_at: str


# EN: This helper creates a unique runtime execution id.
# TR: Bu yardımcı benzersiz bir runtime çalıştırma kimliği üretir.
def new_run_id() -> str:
    # EN: We convert uuid4() to string because string ids are easier to print,
    # EN: inspect, and serialize in beginner-facing controlled surfaces.
    # TR: uuid4() sonucunu metne çeviriyoruz; çünkü metinsel kimlikler beginner
    # TR: odaklı kontrollü yüzeylerde yazdırmak, incelemek ve serileştirmek için daha kolaydır.
    return str(uuid4())


# EN: This helper returns an ISO-8601 UTC timestamp string.
# TR: Bu yardımcı ISO-8601 biçiminde UTC timestamp metni döndürür.
def utc_now_iso() -> str:
    # EN: We use timezone.utc so output never depends on a machine-local timezone.
    # TR: Çıktı makineye özgü yerel saat dilimine bağlı kalmasın diye timezone.utc kullanıyoruz.
    return datetime.now(timezone.utc).isoformat()


# EN: This helper reads a named field from either a dict-like claimed row or an
# EN: attribute-style claimed row object.
# TR: Bu yardımcı named bir alanı dict-benzeri claim satırından veya attribute-stili
# TR: claim satırı nesnesinden okur.
def claimed_url_value(claimed_url: object, field_name: str) -> object:
    # EN: If the claimed row is dict-like, we read the key directly.
    # TR: Claim satırı dict-benzeri ise anahtarı doğrudan okuyoruz.
    if isinstance(claimed_url, dict):
        if field_name not in claimed_url:
            raise KeyError(f"claimed_url is missing key: {field_name}")
        return claimed_url[field_name]

    # EN: Otherwise we fall back to attribute access.
    # TR: Aksi durumda attribute erişimine geri düşüyoruz.
    if not hasattr(claimed_url, field_name):
        raise AttributeError(f"claimed_url is missing attribute: {field_name}")

    # EN: We return the discovered attribute value.
    # TR: Bulunan attribute değerini döndürüyoruz.
    return getattr(claimed_url, field_name)


# EN: This helper decides whether the current robots verdict still allows the
# EN: minimal worker to perform a real page fetch.
# TR: Bu yardımcı mevcut robots verdict'inin minimal worker'ın gerçek page fetch
# TR: yapmasına hâlâ izin verip vermediğini belirler.
def robots_verdict_allows_fetch(verdict: str | None) -> bool:
    # EN: The current minimal worker treats these verdicts as fetch-allowed:
    # EN: explicit allow, allow with refresh recommendation, and ignore-mode allow.
    # TR: Güncel minimal worker şu verdict'leri fetch-allowed sayar:
    # TR: açık allow, refresh tavsiyesiyle allow ve ignore-mode allow.
    return verdict in {
        "allow",
        "allow_but_refresh_recommended",
        "allow_mode_ignore",
    }


# EN: This helper classifies HTTP status failures into minimal retryable vs permanent buckets.
# TR: Bu yardımcı HTTP durum hatalarını minimal retryable ve permanent kovalarına ayırır.
def classify_http_status_failure(http_status: int) -> tuple[str, bool]:
    # EN: These status codes are commonly retryable because they usually represent
    # EN: temporary overload, timeout, or transient upstream failure.
    # TR: Bu durum kodları genelde retryable kabul edilir; çünkü çoğu zaman geçici
    # TR: aşırı yük, timeout veya geçici upstream hatasını temsil eder.
    if http_status in {408, 425, 429, 500, 502, 503, 504}:
        return ("http_retryable_status", True)

    # EN: All remaining HTTP error statuses are treated as permanent for this minimal layer.
    # TR: Kalan tüm HTTP hata durumları bu minimal katmanda permanent kabul edilir.
    return ("http_permanent_status", False)


# EN: This helper finalizes a robots-blocked claim with a permanent outcome.
# EN: The project does not yet expose a dedicated robots-blocked finalize function,
# EN: so the minimal layer uses the permanent-error finalize path with an explicit class.
# TR: Bu yardımcı robots tarafından engellenmiş bir claim'i permanent sonuçla finalize eder.
# TR: Proje henüz dedicated bir robots-blocked finalize fonksiyonu göstermediği için
# TR: minimal katman açık bir hata sınıfıyla permanent-error finalize yolunu kullanır.
def finalize_robots_block(
    conn,
    *,
    claimed_url: object,
    robots_allow_decision: dict | None,
) -> dict:
    # EN: We extract the URL id because finalize must target the exact leased row.
    # TR: Finalize tam leased satırı hedeflemek zorunda olduğu için URL id'yi çıkarıyoruz.
    url_id = int(claimed_url_value(claimed_url, "url_id"))

    # EN: We extract the lease token because finalize must prove lease ownership.
    # TR: Finalize lease sahipliğini kanıtlamak zorunda olduğu için lease token'ı çıkarıyoruz.
    lease_token = str(claimed_url_value(claimed_url, "lease_token"))

    # EN: We read the visible verdict mainly so the stored error message remains explicit.
    # TR: Saklanan hata mesajı açık kalsın diye görünür verdict'i okuyoruz.
    verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")

    # EN: We call the permanent finalize wrapper with an explicit robots_blocked class.
    # TR: Açık bir robots_blocked sınıfıyla permanent finalize wrapper'ını çağırıyoruz.
    return finish_fetch_permanent_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=None,
        error_class="robots_blocked",
        error_message=f"robots verdict forbids fetch: {verdict}",
    )


# EN: This helper finalizes an HTTP error according to the minimal retryable/permanent rule.
# TR: Bu yardımcı bir HTTP hatasını minimal retryable/permanent kuralına göre finalize eder.
def finalize_http_error(
    conn,
    *,
    claimed_url: object,
    http_status: int,
    error_message: str,
) -> dict:
    # EN: We classify the status code first so the finalize branch stays explicit.
    # TR: Finalize dalı açık kalsın diye önce durum kodunu sınıflandırıyoruz.
    error_class, is_retryable = classify_http_status_failure(http_status)

    # EN: We extract the URL id because finalize must target the exact leased row.
    # TR: Finalize tam leased satırı hedeflemek zorunda olduğu için URL id'yi çıkarıyoruz.
    url_id = int(claimed_url_value(claimed_url, "url_id"))

    # EN: We extract the lease token because finalize must prove lease ownership.
    # TR: Finalize lease sahipliğini kanıtlamak zorunda olduğu için lease token'ı çıkarıyoruz.
    lease_token = str(claimed_url_value(claimed_url, "lease_token"))

    # EN: Retryable statuses go through the retryable finalize wrapper.
    # TR: Retryable durumlar retryable finalize wrapper üzerinden gider.
    if is_retryable:
        return finish_fetch_retryable_error(
            conn,
            url_id=url_id,
            lease_token=lease_token,
            http_status=http_status,
            error_class=error_class,
            error_message=error_message,
            retry_delay=None,
        )

    # EN: All other HTTP failure statuses go through the permanent finalize wrapper.
    # TR: Diğer tüm HTTP hata durumları permanent finalize wrapper üzerinden gider.
    return finish_fetch_permanent_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=http_status,
        error_class=error_class,
        error_message=error_message,
    )


# EN: This helper finalizes a lower-level transport failure as retryable.
# TR: Bu yardımcı daha alt düzey bir taşıma hatasını retryable olarak finalize eder.
def finalize_transport_error(
    conn,
    *,
    claimed_url: object,
    error_message: str,
) -> dict:
    # EN: We extract the URL id because finalize must target the exact leased row.
    # TR: Finalize tam leased satırı hedeflemek zorunda olduğu için URL id'yi çıkarıyoruz.
    url_id = int(claimed_url_value(claimed_url, "url_id"))

    # EN: We extract the lease token because finalize must prove lease ownership.
    # TR: Finalize lease sahipliğini kanıtlamak zorunda olduğu için lease token'ı çıkarıyoruz.
    lease_token = str(claimed_url_value(claimed_url, "lease_token"))

    # EN: We use the retryable finalize wrapper because transport failures are
    # EN: typically transient in this minimal first implementation.
    # TR: Bu minimal ilk implementasyonda taşıma hataları tipik olarak geçici kabul
    # TR: edildiği için retryable finalize wrapper'ını kullanıyoruz.
    return finish_fetch_retryable_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=None,
        error_class="transport_retryable_error",
        error_message=error_message,
        retry_delay=None,
    )


# EN: This helper finalizes an unexpected runtime failure as permanent.
# TR: Bu yardımcı beklenmeyen bir runtime hatasını permanent olarak finalize eder.
def finalize_unexpected_runtime_error(
    conn,
    *,
    claimed_url: object,
    error_message: str,
) -> dict:
    # EN: We extract the URL id because finalize must target the exact leased row.
    # TR: Finalize tam leased satırı hedeflemek zorunda olduğu için URL id'yi çıkarıyoruz.
    url_id = int(claimed_url_value(claimed_url, "url_id"))

    # EN: We extract the lease token because finalize must prove lease ownership.
    # TR: Finalize lease sahipliğini kanıtlamak zorunda olduğu için lease token'ı çıkarıyoruz.
    lease_token = str(claimed_url_value(claimed_url, "lease_token"))

    # EN: We use the permanent finalize wrapper because an unknown runtime error
    # EN: should not be silently retried by this minimal layer.
    # TR: Bilinmeyen bir runtime hatası bu minimal katman tarafından sessizce
    # TR: retry edilmemeli diye permanent finalize wrapper'ını kullanıyoruz.
    return finish_fetch_permanent_error(
        conn,
        url_id=url_id,
        lease_token=lease_token,
        http_status=None,
        error_class="unexpected_fetch_runtime_error",
        error_message=error_message,
    )


# EN: This function performs one worker execution.
# EN: In probe mode it still rolls back safely.
# EN: In durable mode it now executes the minimal real fetch + finalize flow.
# TR: Bu fonksiyon tek bir worker çalıştırması yapar.
# TR: Probe modunda hâlâ güvenli rollback yapar.
# TR: Durable modda artık minimal gerçek fetch + finalize akışını çalıştırır.
def run_claim_probe(config: WorkerConfig) -> ClaimProbeResult:
    # EN: We create a unique run id first so the full execution can be traced.
    # TR: Tüm çalıştırma izlenebilir olsun diye önce benzersiz bir run id üretiyoruz.
    run_id = new_run_id()

    # EN: We compute the current storage plan before touching the DB because the
    # EN: crawler must not claim new work when storage policy says it should pause.
    # TR: Crawler storage politikası pause diyorsa yeni iş claim etmemeli; bu yüzden
    # TR: DB'ye dokunmadan önce mevcut storage planı hesaplıyoruz.
    storage_plan = choose_processed_output_plan()

    # EN: If storage says pause, we stop here deliberately and return a structured result.
    # TR: Storage pause diyorsa bilinçli olarak burada duruyor ve yapılı bir sonuç döndürüyoruz.
    if storage_plan.pause_crawler:
        return ClaimProbeResult(
            run_id=run_id,
            claimed=False,
            claimed_url=None,
            robots_allow_decision=None,
            storage_plan=storage_plan,
            fetched_page=None,
            finalize_result=None,
            observed_at=utc_now_iso(),
        )

    # EN: Only after storage allows normal flow do we open a DB connection.
    # TR: Ancak storage normal akışa izin verdikten sonra DB bağlantısı açıyoruz.
    conn = connect_db(config.dsn)

    try:
        # EN: We ask crawler-core for exactly one claimable row.
        # TR: crawler-core'dan tam olarak bir claim edilebilir satır istiyoruz.
        claimed_url = claim_next_url(
            conn=conn,
            worker_id=config.worker_id,
            lease_seconds=config.lease_seconds,
        )

        # EN: If nothing is currently claimable, we rollback and return a structured result.
        # TR: Şu anda claim edilebilir hiçbir şey yoksa rollback yapıyor ve yapılı sonuç döndürüyoruz.
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
                observed_at=utc_now_iso(),
            )

        # EN: If a row was claimed, we ask for the current visible robots allow/block decision.
        # TR: Bir satır claim edildiyse mevcut görünür robots allow/block kararını soruyoruz.
        robots_allow_decision = compute_robots_allow_decision(
            conn=conn,
            host_id=claimed_url_value(claimed_url, "host_id"),
            url_path=str(claimed_url_value(claimed_url, "url_path")),
        )

        # EN: Probe mode stays non-durable: claim + robots check are observed and then rolled back.
        # TR: Probe modu kalıcı olmayan mod olarak kalır: claim + robots kontrolü gözlenir ve sonra rollback edilir.
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
                observed_at=utc_now_iso(),
            )

        # EN: In durable mode we inspect the robots verdict before any real fetch is attempted.
        # TR: Durable modda gerçek fetch denenmeden önce robots verdict'ini inceliyoruz.
        robots_verdict = None if robots_allow_decision is None else robots_allow_decision.get("verdict")

        # EN: If robots forbids fetch, we finalize immediately through the minimal
        # EN: robots-block permanent path and commit that durable result.
        # TR: Robots fetch'i yasaklıyorsa minimal robots-block permanent yolu üzerinden
        # TR: hemen finalize ediyor ve bu kalıcı sonucu commit ediyoruz.
        if not robots_verdict_allows_fetch(robots_verdict):
            finalize_result = finalize_robots_block(
                conn,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
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
                observed_at=utc_now_iso(),
            )

        # EN: If robots allows fetch, we execute the minimal real HTTP fetch plus raw-body write.
        # TR: Robots fetch'e izin veriyorsa minimal gerçek HTTP fetch ve ham body yazımını çalıştırıyoruz.
        try:
            fetched_page = fetch_page_to_raw_storage(claimed_url)

            # EN: A successful fetch is finalized through the canonical success wrapper.
            # TR: Başarılı fetch kanonik success wrapper üzerinden finalize edilir.
            finalize_result = finish_fetch_success(
                conn,
                url_id=fetched_page.url_id,
                lease_token=str(claimed_url_value(claimed_url, "lease_token")),
                http_status=fetched_page.http_status,
                content_type=fetched_page.content_type,
                body_bytes=fetched_page.body_bytes,
                etag=fetched_page.etag,
                last_modified=fetched_page.last_modified,
            )

            # EN: We commit so the claim, raw-fetch success finalize, and lease resolution
            # EN: become durable together.
            # TR: Claim, raw-fetch success finalize ve lease çözümü birlikte kalıcı olsun
            # TR: diye commit ediyoruz.
            commit(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=True,
                claimed_url=claimed_url,
                robots_allow_decision=robots_allow_decision,
                storage_plan=storage_plan,
                fetched_page=fetched_page,
                finalize_result=finalize_result,
                observed_at=utc_now_iso(),
            )

        # EN: HTTPError means the server answered with an explicit HTTP failure status.
        # TR: HTTPError sunucunun açık bir HTTP hata durumu ile yanıt verdiği anlamına gelir.
        except HTTPError as exc:
            finalize_result = finalize_http_error(
                conn,
                claimed_url=claimed_url,
                http_status=int(exc.code),
                error_message=f"HTTPError {exc.code}: {exc.reason}",
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
                observed_at=utc_now_iso(),
            )

        # EN: URLError, socket timeout, and timeout-like transport failures are treated
        # EN: as retryable by the minimal first implementation.
        # TR: URLError, socket timeout ve timeout-benzeri taşıma hataları minimal ilk
        # TR: implementasyonda retryable kabul edilir.
        except (URLError, TimeoutError, socket.timeout) as exc:
            finalize_result = finalize_transport_error(
                conn,
                claimed_url=claimed_url,
                error_message=f"{type(exc).__name__}: {exc}",
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
                observed_at=utc_now_iso(),
            )

        # EN: Any other unexpected fetch/runtime failure is finalized as permanent
        # EN: so the minimal layer fails loudly instead of hiding unknown behavior.
        # TR: Diğer tüm beklenmeyen fetch/runtime hataları minimal katman bilinmeyen
        # TR: davranışı gizlemesin diye permanent olarak finalize edilir.
        except Exception as exc:
            finalize_result = finalize_unexpected_runtime_error(
                conn,
                claimed_url=claimed_url,
                error_message=f"{type(exc).__name__}: {exc}",
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
                observed_at=utc_now_iso(),
            )
    finally:
        # EN: We always close the connection even if an error occurs.
        # TR: Hata oluşsa bile bağlantıyı her durumda kapatıyoruz.
        close_db(conn)
