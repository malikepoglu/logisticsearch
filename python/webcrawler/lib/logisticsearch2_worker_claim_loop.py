# EN: We enable postponed evaluation of type hints for cleaner forward-friendly
# EN: annotations.
# TR: Daha temiz ve ileriye uyumlu annotation'lar için type hint çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import argparse because this first worker surface should be runnable
# EN: from the command line in a controlled and explicit way.
# TR: Bu ilk worker yüzeyi kontrollü ve açık biçimde komut satırından
# TR: çalıştırılabilsin diye argparse içe aktarıyoruz.
import argparse

# EN: We import json so the result can be printed in a structured machine- and
# EN: human-readable format.
# TR: Sonuç hem makine hem insan tarafından okunabilir yapılı bir formatta
# TR: yazdırılabilsin diye json içe aktarıyoruz.
import json

# EN: We import os so environment variables can be used for DSN and worker id defaults.
# TR: DSN ve worker id varsayılanları environment variable üzerinden alınabilsin
# TR: diye os içe aktarıyoruz.
import os

# EN: We import asdict because dataclass results should be converted to plain
# EN: dictionaries before JSON serialization.
# TR: Dataclass sonuçları JSON serileştirmesinden önce düz sözlüklere dönüştürülsün
# TR: diye asdict içe aktarıyoruz.
from dataclasses import asdict

# EN: We import the runtime helpers that implement the current narrow worker truth.
# TR: Mevcut dar worker doğrusunu uygulayan runtime yardımcılarını içe aktarıyoruz.
from logisticsearch1_main_worker_runtime import WorkerConfig, run_claim_probe


# EN: This function reads a DSN from the environment and falls back to a
# EN: controlled scratch default for local audit work.
# TR: Bu fonksiyon environment içinden DSN okur ve yerel audit çalışmaları için
# TR: kontrollü bir scratch varsayılanına geri düşer.
def default_dsn() -> str:
    # EN: We first check LOGISTICSEARCH_CRAWLER_DSN because explicit operator
    # EN: configuration is more honest than a hidden hard-coded assumption.
    # TR: Önce LOGISTICSEARCH_CRAWLER_DSN değişkenini kontrol ediyoruz; çünkü
    # TR: açık operatör konfigürasyonu gizli hard-coded varsayımdan daha dürüsttür.
    env_value = os.getenv("LOGISTICSEARCH_CRAWLER_DSN")

    # EN: If the environment variable is present and non-empty, we trust that
    # EN: explicit operator choice.
    # TR: Environment variable mevcut ve boş değilse bu açık operatör tercihini kullanıyoruz.
    if env_value:
        # EN: We return the explicit DSN.
        # TR: Açık DSN değerini geri döndürüyoruz.
        return env_value

    # EN: Otherwise we return a controlled scratch-oriented default.
    # TR: Aksi durumda kontrollü scratch-odaklı bir varsayılan döndürüyoruz.
    return "dbname=logisticsearch_crawler_split_scratch user=postgres"


# EN: This function reads a worker id from the environment and falls back to a
# EN: deterministic demo-friendly default.
# TR: Bu fonksiyon environment'dan worker id okur ve deterministik, demo-dostu
# TR: bir varsayılana geri döner.
def default_worker_id() -> str:
    # EN: We check a dedicated environment variable first.
    # TR: Önce ayrılmış environment variable değerine bakıyoruz.
    env_value = os.getenv("LOGISTICSEARCH_WORKER_ID")

    # EN: If the operator provided a worker id, we keep it.
    # TR: Operatör bir worker id verdiyse onu koruyoruz.
    if env_value:
        # EN: We return the operator-supplied identity.
        # TR: Operatör tarafından verilen kimliği geri döndürüyoruz.
        return env_value

    # EN: Otherwise we use a narrow and explicit default worker identity.
    # TR: Aksi durumda dar ve açık bir varsayılan worker kimliği kullanıyoruz.
    return "ubuntu_desktop_probe_worker"


# EN: This function builds the command-line parser for the first worker surface.
# TR: Bu fonksiyon, ilk worker yüzeyi için komut satırı parser'ını kurar.
def build_parser() -> argparse.ArgumentParser:
    # EN: We create the parser with a narrow description so the current scope
    # EN: remains honest.
    # TR: Güncel kapsam dürüst kalsın diye parser'ı dar bir açıklamayla oluşturuyoruz.
    parser = argparse.ArgumentParser(
        description="Controlled probe-only claim worker for LogisticSearch crawler_core."
    )

    # EN: We add a DSN argument so the operator can override the connection target.
    # TR: Operatör bağlantı hedefini değiştirebilsin diye DSN argümanı ekliyoruz.
    parser.add_argument(
        "--dsn",
        default=default_dsn(),
        help="PostgreSQL DSN. Defaults to LOGISTICSEARCH_CRAWLER_DSN or a local scratch fallback.",
    )

    # EN: We add a worker-id argument because claim semantics depend on a durable
    # EN: textual worker identity.
    # TR: Claim semantiği kalıcı metinsel bir worker kimliğine bağlı olduğu için
    # TR: worker-id argümanı ekliyoruz.
    parser.add_argument(
        "--worker-id",
        default=default_worker_id(),
        help="Worker identity passed into frontier.claim_next_url(...).",
    )

    # EN: We add lease-seconds so the operator can explicitly control how long
    # EN: the temporary claimed lease would last before renewal is required.
    # TR: Operatör geçici claim edilmiş lease'in renewal gerektirmeden önce ne kadar
    # TR: süreceğini açıkça kontrol edebilsin diye lease-seconds ekliyoruz.
    parser.add_argument(
        "--lease-seconds",
        type=int,
        default=600,
        help="Lease duration, in seconds, passed into frontier.claim_next_url(...).",
    )

    # EN: We add a durable-claim flag so the operator can deliberately switch
    # EN: from non-durable probe mode into durable leased-claim mode.
    # TR: Operatör non-durable probe modundan durable leased-claim moduna
    # TR: bilinçli olarak geçebilsin diye durable-claim bayrağı ekliyoruz.
    parser.add_argument(
        "--durable-claim",
        action="store_true",
        help="Commit a successful claim so the lease remains durable in the database.",
    )

    # EN: We add an output mode mainly so structured JSON stays easy to consume.
    # TR: Yapılı JSON çıktısı kolay tüketilebilsin diye özellikle output mode ekliyoruz.
    parser.add_argument(
        "--output",
        choices=("json",),
        default="json",
        help="Current supported output format.",
    )

    # EN: We return the fully prepared parser.
    # TR: Tam hazırlanmış parser'ı geri döndürüyoruz.
    return parser


# EN: This is the main program entry point.
# TR: Bu ana program giriş noktasıdır.
def main() -> int:
    # EN: We construct the parser first.
    # TR: Önce parser'ı kuruyoruz.
    parser = build_parser()

    # EN: We parse the command-line arguments into a namespace.
    # TR: Komut satırı argümanlarını bir namespace içine parse ediyoruz.
    args = parser.parse_args()

    # EN: We build an explicit runtime configuration object so argument meaning
    # EN: stays visible and structured.
    # TR: Argümanların anlamı görünür ve yapılı kalsın diye açık bir runtime
    # TR: konfigürasyon nesnesi kuruyoruz.
    config = WorkerConfig(
        dsn=args.dsn,
        worker_id=args.worker_id,
        lease_seconds=args.lease_seconds,
        # EN: When durable-claim mode is requested, probe_only must become False
        # EN: so a successful claim is committed instead of rolled back.
        # TR: Durable-claim modu istendiğinde probe_only değeri False olmalıdır;
        # TR: böylece başarılı claim rollback yerine commit edilir.
        probe_only=not args.durable_claim,
    )

    # EN: We execute one controlled claim probe according to the current worker truth.
    # TR: Mevcut worker doğrusuna göre tek bir kontrollü claim probe çalıştırıyoruz.
    result = run_claim_probe(config)

    # EN: We convert the dataclass result into plain Python data for JSON output.
    # TR: JSON çıktısı için dataclass sonucunu düz Python verisine dönüştürüyoruz.
    payload = asdict(result)

    # EN: We print JSON with indentation so both humans and tools can inspect it.
    # TR: Hem insanlar hem araçlar inceleyebilsin diye JSON'u girintili yazdırıyoruz.
    print(json.dumps(payload, indent=2, default=str))

    # EN: We return zero because successful structured output means the controlled
    # EN: probe itself completed successfully, even if no claimable row existed.
    # TR: Başarılı yapılı çıktı, claim edilebilir satır olmasa bile kontrollü probe'un
    # TR: başarıyla tamamlandığı anlamına geldiği için sıfır döndürüyoruz.
    return 0


# EN: This standard guard ensures main() runs only when the file is executed
# EN: directly, not when it is imported by another Python file.
# TR: Bu standart koruma, main() fonksiyonunun yalnızca dosya doğrudan
# TR: çalıştırıldığında çalışmasını; başka Python dosyası tarafından import edildiğinde
# TR: otomatik çalışmamasını sağlar.
if __name__ == "__main__":
    # EN: We raise SystemExit with main() so the program exits with the returned
    # EN: process status code in the normal Python CLI style.
    # TR: Program normal Python CLI stilinde dönen süreç durum koduyla çıkabilsin
    # TR: diye main() sonucunu SystemExit ile yükseltiyoruz.
    raise SystemExit(main())
