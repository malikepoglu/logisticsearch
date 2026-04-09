# EN: We enable postponed evaluation of annotations so type hints stay readable
# EN: even when they refer to classes declared later in the file.
# TR: Type hint'ler dosyada daha sonra tanımlanan sınıflara referans verse bile
# TR: okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import dataclass because configuration and result objects are much
# EN: easier to understand when every field is explicit and named.
# TR: Konfigürasyon ve sonuç nesneleri her alan açık ve isimli olduğunda çok
# TR: daha anlaşılır olduğu için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import datetime and timezone so observed timestamps are explicit and UTC-based.
# TR: Gözlenen zaman damgaları açık ve UTC tabanlı olsun diye datetime ve timezone
# TR: içe aktarıyoruz.
from datetime import datetime, timezone

# EN: We import uuid4 so every probe execution can get its own unique run id.
# TR: Her probe çalıştırması kendine ait benzersiz bir run id alabilsin diye
# TR: uuid4 içe aktarıyoruz.
from uuid import uuid4

# EN: These DB helpers already express the current canonical crawler-core
# EN: interaction points for the narrow probe worker surface.
# TR: Bu DB yardımcıları dar probe worker yüzeyi için mevcut kanonik crawler-core
# TR: etkileşim noktalarını zaten ifade ediyor.
from .db import claim_next_url, close_db, commit, compute_robots_allow_decision, connect_db, rollback

# EN: We import the minimal storage routing helper because worker runtime must
# EN: now become storage-aware before it tries to claim new work.
# TR: Worker runtime artık yeni iş claim etmeye çalışmadan önce storage-aware
# TR: hale gelmek zorunda olduğu için minimal storage routing yardımcısını içe aktarıyoruz.
from .storage_routing import ProcessedOutputPlan, choose_processed_output_plan


# EN: This dataclass stores runtime configuration for the current narrow worker surface.
# TR: Bu dataclass mevcut dar worker yüzeyi için runtime konfigürasyonunu tutar.
@dataclass(slots=True)
class WorkerConfig:
    # EN: dsn is the PostgreSQL connection string used by this worker runtime.
    # TR: dsn bu worker runtime tarafından kullanılan PostgreSQL bağlantı metnidir.
    dsn: str

    # EN: worker_id is the textual worker identity passed into frontier.claim_next_url(...).
    # TR: worker_id frontier.claim_next_url(...) içine verilen metinsel worker kimliğidir.
    worker_id: str

    # EN: lease_seconds says how long a claimed lease should stay valid before
    # EN: renewal would become necessary.
    # TR: lease_seconds claim edilmiş bir lease'in renewal gerekmeden önce ne kadar
    # TR: süre geçerli kalacağını söyler.
    lease_seconds: int = 600

    # EN: probe_only keeps the worker in non-durable verification mode when
    # EN: it is True. When it is False, a successful claim is committed and left
    # EN: leased in the database for the current worker.
    # TR: probe_only True olduğunda worker'ı kalıcı olmayan doğrulama modunda
    # TR: tutar. False olduğunda başarılı claim commit edilir ve mevcut worker
    # TR: için veritabanında leased olarak bırakılır.
    probe_only: bool = True


# EN: This dataclass stores the result of one controlled claim probe.
# TR: Bu dataclass tek bir kontrollü claim probe sonucunu tutar.
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


# EN: This function performs one controlled claim probe.
# EN: It is now storage-aware: before it tries to claim work, it asks the
# EN: storage-routing surface whether normal processed-output flow should pause.
# TR: Bu fonksiyon tek bir kontrollü claim probe yapar.
# TR: Artık storage-aware'dir: iş claim etmeye çalışmadan önce storage-routing
# TR: yüzeyine normal işlenmiş-çıktı akışının pause olup olmaması gerektiğini sorar.
def run_claim_probe(config: WorkerConfig) -> ClaimProbeResult:
    # EN: We create a unique run id first so the full probe execution can be traced.
    # TR: Tüm probe çalıştırması izlenebilir olsun diye önce benzersiz bir run id üretiyoruz.
    run_id = new_run_id()

    # EN: We compute the current storage plan before touching the DB because the
    # EN: crawler must not claim new work when storage policy says it should pause.
    # TR: DB'ye dokunmadan önce mevcut storage planı hesaplıyoruz; çünkü storage
    # TR: politikası pause diyorsa crawler yeni iş claim etmemelidir.
    storage_plan = choose_processed_output_plan()

    # EN: If storage plan says pause, we stop here deliberately.
    # EN: We return a structured result instead of claiming new work.
    # TR: Storage plan pause diyorsa bilinçli olarak burada duruyoruz.
    # TR: Yeni iş claim etmek yerine yapılı bir sonuç döndürüyoruz.
    if storage_plan.pause_crawler:
        return ClaimProbeResult(
            run_id=run_id,
            claimed=False,
            claimed_url=None,
            robots_allow_decision=None,
            storage_plan=storage_plan,
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

        # EN: If nothing is currently claimable, we still return a structured result.
        # EN: We also rollback so DB state remains exactly as we found it.
        # TR: Şu anda claim edilebilir hiçbir şey yoksa yine yapılı bir sonuç
        # TR: döndürüyoruz. Ayrıca DB durumunu bulduğumuz gibi bırakmak için rollback yapıyoruz.
        if claimed_url is None:
            rollback(conn)

            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=None,
                storage_plan=storage_plan,
                observed_at=utc_now_iso(),
            )

        # EN: If a row was claimed, we also ask for the current visible robots
        # EN: allow/block decision for that claimed host/path pair.
        # TR: Bir satır claim edildiyse, o claim edilen host/path çifti için mevcut
        # TR: görünür robots allow/block kararını da soruyoruz.
        robots_allow_decision = compute_robots_allow_decision(
            conn=conn,
            host_id=claimed_url.host_id,
            url_path=claimed_url.url_path,
        )

        # EN: In probe-only mode we deliberately rollback so claim proof does
        # EN: not leave durable queue state behind.
        # TR: Probe-only modda claim kanıtı kalıcı kuyruk durumu bırakmasın diye
        # TR: bilinçli olarak rollback yapıyoruz.
        if config.probe_only:
            rollback(conn)

        # EN: In durable-claim mode we deliberately commit so the claimed URL
        # EN: remains leased in the database for the current worker.
        # TR: Durable-claim modda claim edilen URL mevcut worker için veritabanında
        # TR: leased olarak kalsın diye bilinçli olarak commit yapıyoruz.
        else:
            commit(conn)

        # EN: We return one structured success-style probe result.
        # TR: Tek bir yapılı başarı-benzeri probe sonucu döndürüyoruz.
        return ClaimProbeResult(
            run_id=run_id,
            claimed=True,
            claimed_url=claimed_url,
            robots_allow_decision=robots_allow_decision,
            storage_plan=storage_plan,
            observed_at=utc_now_iso(),
        )
    finally:
        # EN: We always close the connection even if an error occurs.
        # TR: Hata oluşsa bile bağlantıyı her durumda kapatıyoruz.
        close_db(conn)
