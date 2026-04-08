# EN: We enable postponed evaluation of type hints so future type references
# EN: remain flexible and readable.
# TR: Gelecekteki type referansları esnek ve okunabilir kalsın diye type hint
# TR: çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import dataclass because configuration and probe result objects are
# EN: easier to understand when their fields are explicit and named.
# TR: Konfigürasyon ve probe sonucu nesneleri alanları açık ve isimli olduğunda
# TR: daha anlaşılır olduğu için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import datetime and timezone so timestamps printed by this worker
# EN: surface remain explicit and timezone-aware.
# TR: Bu worker yüzeyi tarafından yazdırılan zaman damgaları açık ve timezone-aware
# TR: kalsın diye datetime ve timezone içe aktarıyoruz.
from datetime import datetime, timezone

# EN: We import uuid4 so that a runtime instance can generate a unique run id
# EN: without depending on hidden global state.
# TR: Runtime örneği gizli global duruma bağlı kalmadan benzersiz bir run id
# TR: üretebilsin diye uuid4 içe aktarıyoruz.
from uuid import uuid4

# EN: We import the DB helpers that already express the current canonical
# EN: crawler-core interaction points.
# TR: Mevcut kanonik crawler-core etkileşim noktalarını zaten ifade eden
# TR: DB yardımcılarını içe aktarıyoruz.
from .db import claim_next_url, close_db, compute_robots_allow_decision, connect_db, rollback


# EN: This dataclass stores runtime configuration for the first controlled
# EN: Python-side worker surface.
# TR: Bu dataclass, ilk kontrollü Python-tarafı worker yüzeyi için runtime
# TR: konfigürasyonunu tutar.
@dataclass(slots=True)
class WorkerConfig:
    # EN: dsn is the PostgreSQL connection string.
    # TR: dsn, PostgreSQL bağlantı metnidir.
    dsn: str

    # EN: worker_id is the durable textual worker identity passed into
    # EN: frontier.claim_next_url(...).
    # TR: worker_id, frontier.claim_next_url(...) içine verilen kalıcı metinsel
    # TR: worker kimliğidir.
    worker_id: str

    # EN: lease_seconds determines how long the claimed lease should last before
    # EN: renewal becomes necessary.
    # TR: lease_seconds, yenileme gerekmeden önce claim edilen lease'in ne kadar
    # TR: süre geçerli kalacağını belirler.
    lease_seconds: int = 600

    # EN: probe_only keeps the first implementation honest: it proves DB claim
    # EN: interaction without pretending a full fetch/finalize runtime exists.
    # TR: probe_only, ilk implementasyonu dürüst tutar: tam fetch/finalize runtime
    # TR: varmış gibi yapmadan DB claim etkileşimini kanıtlar.
    probe_only: bool = True


# EN: This dataclass stores the result of one controlled claim probe.
# TR: Bu dataclass, tek bir kontrollü claim probe sonucunu tutar.
@dataclass(slots=True)
class ClaimProbeResult:
    # EN: run_id is the unique id of this Python-side runtime execution.
    # TR: run_id, bu Python-tarafı runtime çalıştırmasının benzersiz kimliğidir.
    run_id: str

    # EN: claimed indicates whether a claimable row was returned.
    # TR: claimed, claim edilebilir bir satır dönüp dönmediğini belirtir.
    claimed: bool

    # EN: claimed_url is the actual claimed row object when available.
    # TR: claimed_url, varsa gerçek claim edilmiş satır nesnesidir.
    claimed_url: object | None

    # EN: robots_allow_decision stores the current visible robots allow/block
    # EN: decision mapping when a claim succeeded.
    # TR: robots_allow_decision, claim başarılıysa mevcut görünür robots allow/block
    # TR: karar mapping'ini tutar.
    robots_allow_decision: dict | None

    # EN: observed_at records when the probe result was produced.
    # TR: observed_at, probe sonucunun ne zaman üretildiğini kaydeder.
    observed_at: str


# EN: This helper generates a unique runtime execution id.
# TR: Bu yardımcı, benzersiz bir runtime çalıştırma kimliği üretir.
def new_run_id() -> str:
    # EN: We convert uuid4() to string because string ids are easier to print,
    # EN: log, and inspect in a beginner-facing controlled surface.
    # TR: uuid4() sonucunu metne çeviriyoruz; çünkü metinsel kimlikler beginner
    # TR: odaklı kontrollü yüzeyde yazdırmak, loglamak ve incelemek için daha kolaydır.
    return str(uuid4())


# EN: This helper returns an ISO-8601 UTC timestamp string.
# TR: Bu yardımcı, ISO-8601 biçiminde UTC timestamp metni döndürür.
def utc_now_iso() -> str:
    # EN: We use timezone.utc so the timestamp is explicit and not dependent on
    # EN: whatever local machine timezone may be active.
    # TR: Timestamp aktif yerel makine saat dilimine bağlı kalmasın diye
    # TR: timezone.utc kullanıyoruz.
    return datetime.now(timezone.utc).isoformat()


# EN: This function performs one controlled claim probe and then rolls back.
# TR: Bu fonksiyon tek bir kontrollü claim probe yapar ve ardından rollback eder.
def run_claim_probe(config: WorkerConfig) -> ClaimProbeResult:
    # EN: We generate a unique run id first so the entire probe can be traced.
    # TR: Tüm probe izlenebilir olsun diye önce benzersiz bir run id üretiyoruz.
    run_id = new_run_id()

    # EN: We open a DB connection through the dedicated helper.
    # TR: Ayrı yardımcı üzerinden DB bağlantısı açıyoruz.
    conn = connect_db(config.dsn)

    try:
        # EN: We ask crawler-core for exactly one claimable row.
        # TR: crawler-core'dan tam olarak bir claim edilebilir satır istiyoruz.
        claimed_url = claim_next_url(
            conn=conn,
            worker_id=config.worker_id,
            lease_seconds=config.lease_seconds,
        )

        # EN: If nothing is claimable, we still return a structured result
        # EN: instead of raising an exception.
        # TR: Claim edilebilir hiçbir şey yoksa bile exception yükseltmek yerine
        # TR: yapılı bir sonuç döndürüyoruz.
        if claimed_url is None:
            # EN: We rollback to leave the DB exactly as we found it.
            # TR: DB'yi bulduğumuz gibi bırakmak için rollback yapıyoruz.
            rollback(conn)

            # EN: We return an explicit no-claim result.
            # TR: Açık bir no-claim sonucu döndürüyoruz.
            return ClaimProbeResult(
                run_id=run_id,
                claimed=False,
                claimed_url=None,
                robots_allow_decision=None,
                observed_at=utc_now_iso(),
            )

        # EN: If a row was claimed, we ask for the current visible robots
        # EN: allow/block decision for the claimed host/path pair.
        # TR: Bir satır claim edildiyse, claim edilen host/path çifti için
        # TR: mevcut görünür robots allow/block kararını soruyoruz.
        robots_allow_decision = compute_robots_allow_decision(
            conn=conn,
            host_id=claimed_url.host_id,
            url_path=claimed_url.url_path,
        )

        # EN: This first worker surface is intentionally probe-only, so we roll
        # EN: back rather than leaving a durable lease behind.
        # TR: Bu ilk worker yüzeyi bilinçli olarak probe-only olduğu için kalıcı
        # TR: bir lease bırakmak yerine rollback yapıyoruz.
        rollback(conn)

        # EN: We return a structured success-style probe result.
        # TR: Yapılı bir başarı-benzeri probe sonucu döndürüyoruz.
        return ClaimProbeResult(
            run_id=run_id,
            claimed=True,
            claimed_url=claimed_url,
            robots_allow_decision=robots_allow_decision,
            observed_at=utc_now_iso(),
        )
    finally:
        # EN: We always close the connection even if an error happens.
        # TR: Hata olsa bile bağlantıyı her durumda kapatıyoruz.
        close_db(conn)
