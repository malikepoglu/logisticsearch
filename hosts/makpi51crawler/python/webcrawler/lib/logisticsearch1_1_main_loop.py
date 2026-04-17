# EN: We enable postponed evaluation of type hints for cleaner forward-friendly
# EN: annotations.
# TR: Daha temiz ve ileriye uyumlu annotation'lar için type hint çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import argparse because this worker/operator surface should be runnable
# EN: from the command line in a controlled and explicit way.
# TR: Bu worker/operatör yüzeyi kontrollü ve açık biçimde komut satırından
# TR: çalıştırılabilsin diye argparse içe aktarıyoruz.
import argparse

# EN: We import json so results can be printed in a structured machine- and
# EN: human-readable format.
# TR: Sonuçlar hem makine hem insan tarafından okunabilir yapılı biçimde
# TR: yazdırılabilsin diye json içe aktarıyoruz.
import json

# EN: We import os so environment variables can be used for DSN and operator
# EN: identity defaults.
# TR: DSN ve operatör kimliği varsayılanları environment variable üzerinden
# TR: alınabilsin diye os içe aktarıyoruz.
import os

# EN: We import time because loop mode needs explicit sleep boundaries between
# EN: controlled worker iterations.
# TR: Loop modu kontrollü worker iterasyonları arasında açık sleep sınırlarına
# TR: ihtiyaç duyduğu için time modülünü içe aktarıyoruz.
import time

# EN: We import asdict because dataclass worker results should be converted into
# EN: plain dictionaries before JSON serialization.
# TR: Dataclass worker sonuçları JSON serileştirmesinden önce düz sözlüklere
# TR: dönüştürülsün diye asdict içe aktarıyoruz.
from dataclasses import asdict

# EN: We import the canonical DB helpers needed by this existing CLI surface.
# TR: Bu mevcut CLI yüzeyinin ihtiyaç duyduğu kanonik DB yardımcılarını içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    connect_db,
    get_webcrawler_runtime_control,
    set_webcrawler_runtime_control,
    webcrawler_runtime_may_claim,
)

# EN: We import the worker runtime helpers that implement the current narrow
# EN: crawler-core execution truth.
# TR: Mevcut dar crawler-core çalışma doğrusunu uygulayan worker runtime
# TR: yardımcılarını içe aktarıyoruz.
from .logisticsearch1_1_2_worker_runtime import WorkerConfig, run_claim_probe


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
    return "makpi51crawler_probe_worker"


# EN: This function reads a control-request identity from the environment and
# EN: falls back to a stable CLI-origin default.
# TR: Bu fonksiyon environment'dan bir control-request kimliği okur ve stabil bir
# TR: CLI-kaynaklı varsayılana geri düşer.
def default_requested_by() -> str:
    # EN: We first check the explicit operator override variable.
    # TR: Önce açık operatör override değişkenine bakıyoruz.
    env_value = os.getenv("LOGISTICSEARCH_CONTROL_REQUESTED_BY")

    # EN: If the operator provided a value, we keep it.
    # TR: Operatör bir değer verdiyse onu koruyoruz.
    if env_value:
        # EN: We return the operator-provided identity.
        # TR: Operatör tarafından verilen kimliği döndürüyoruz.
        return env_value

    # EN: Otherwise we return the stable existing-CLI identity.
    # TR: Aksi durumda stabil mevcut-CLI kimliğini döndürüyoruz.
    return "logisticsearch1_1_main_loop"


# EN: This function builds the command-line parser for the existing operator
# EN: surface without creating any new file surface.
# TR: Bu fonksiyon yeni dosya yüzeyi oluşturmadan mevcut operatör yüzeyi için
# TR: komut satırı parser'ını kurar.
def build_parser() -> argparse.ArgumentParser:
    # EN: We create the parser with a narrow description so current scope stays honest.
    # TR: Güncel kapsam dürüst kalsın diye parser'ı dar bir açıklamayla oluşturuyoruz.
    parser = argparse.ArgumentParser(
        description="Controlled worker probe, runtime-control, and loop operator surface for LogisticSearch crawler_core."
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
    # TR: Operatör geçici claim edilmiş lease'in renewal gerekmeden önce ne kadar
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

    # EN: We add a loop flag so the existing canonical CLI can run repeated
    # EN: worker iterations without creating a new operator file surface.
    # TR: Mevcut kanonik CLI tekrar eden worker iterasyonları çalıştırabilsin ve
    # TR: yeni bir operatör dosya yüzeyi oluşmasın diye loop bayrağı ekliyoruz.
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run repeated worker iterations inside the existing canonical CLI surface.",
    )

    # EN: We add sleep-seconds so the operator can control the normal delay
    # EN: between loop iterations.
    # TR: Operatör loop iterasyonları arasındaki normal gecikmeyi kontrol
    # TR: edebilsin diye sleep-seconds ekliyoruz.
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=5.0,
        help="Normal delay between loop iterations.",
    )

    # EN: We add pause-sleep-seconds so pause state can stay alive with a distinct
    # EN: slower polling cadence.
    # TR: Pause durumu canlı kalsın ve ayrı bir daha yavaş polling temposu
    # TR: kullanılsın diye pause-sleep-seconds ekliyoruz.
    parser.add_argument(
        "--pause-sleep-seconds",
        type=float,
        default=15.0,
        help="Delay between loop iterations while runtime-control is pause.",
    )

    # EN: We add max-iterations so loop mode can be smoke-tested safely.
    # TR: Loop modu güvenli biçimde smoke-test edilebilsin diye max-iterations ekliyoruz.
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=0,
        help="Maximum loop iterations. Zero means no explicit iteration limit.",
    )

    # EN: We add a show-runtime-control flag so the operator can inspect the
    # EN: current durable DB truth without making a claim attempt.
    # TR: Operatör mevcut kalıcı DB doğrusunu claim denemesi yapmadan
    # TR: inceleyebilsin diye show-runtime-control bayrağı ekliyoruz.
    parser.add_argument(
        "--show-runtime-control",
        action="store_true",
        help="Read and print the current runtime-control DB truth.",
    )

    # EN: We add a set-runtime-control choice so the existing CLI can change the
    # EN: crawler state through the sealed DB function surface.
    # TR: Mevcut CLI mühürlü DB fonksiyon yüzeyi üzerinden crawler durumunu
    # TR: değiştirebilsin diye set-runtime-control seçeneğini ekliyoruz.
    parser.add_argument(
        "--set-runtime-control",
        choices=("run", "pause", "stop"),
        help="Set the durable runtime-control state through DB truth.",
    )

    # EN: We add state-reason so every durable control change carries an explicit
    # EN: human-auditable reason.
    # TR: Her kalıcı kontrol değişimi açık ve insan tarafından denetlenebilir bir
    # TR: gerekçe taşısın diye state-reason ekliyoruz.
    parser.add_argument(
        "--state-reason",
        default="operator requested runtime control change via canonical CLI",
        help="Reason text written into ops.webcrawler_runtime_control.",
    )

    # EN: We add requested-by so each durable control change carries an explicit
    # EN: requester identity.
    # TR: Her kalıcı kontrol değişimi açık bir requester kimliği taşısın diye
    # TR: requested-by ekliyoruz.
    parser.add_argument(
        "--requested-by",
        default=default_requested_by(),
        help="Requester identity written into ops.webcrawler_runtime_control.",
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


# EN: This helper decides how long loop mode should sleep before the next
# EN: iteration, based on the visible runtime-control snapshot.
# TR: Bu yardımcı loop modunun sonraki iterasyondan önce ne kadar uyuyacağını
# TR: görünür runtime-control anlık görüntüsüne göre belirler.
def sleep_between_loop_iterations(*, payload: dict, sleep_seconds: float, pause_sleep_seconds: float) -> float:
    # EN: We read the optional runtime-control snapshot from the returned payload.
    # TR: Dönen payload içinden opsiyonel runtime-control anlık görüntüsünü okuyoruz.
    runtime_control = payload.get("runtime_control") or {}

    # EN: We extract the desired state as a normalized text token.
    # TR: desired_state değerini normalize edilmiş metin tokenı olarak çıkarıyoruz.
    desired_state = str(runtime_control.get("desired_state") or "").strip().lower()

    # EN: Pause should keep the process alive but slower.
    # TR: Pause süreci canlı tutmalı ama daha yavaş çalıştırmalıdır.
    if desired_state == "pause":
        return pause_sleep_seconds

    # EN: All remaining states use the normal loop cadence.
    # TR: Kalan tüm durumlar normal loop temposunu kullanır.
    return sleep_seconds


def main() -> int:
    # EN: We construct the parser first.
    # TR: Önce parser'ı kuruyoruz.
    parser = build_parser()

    # EN: We parse the command-line arguments into a namespace.
    # TR: Komut satırı argümanlarını bir namespace içine parse ediyoruz.
    args = parser.parse_args()

    # EN: If runtime-control inspection or mutation was requested, we keep the
    # EN: whole path inside this existing CLI surface instead of creating a new file.
    # TR: Runtime-control inceleme veya değiştirme istendiyse tüm yolu yeni dosya
    # TR: oluşturmadan bu mevcut CLI yüzeyi içinde tutuyoruz.
    if args.show_runtime_control or args.set_runtime_control is not None:
        # EN: We open the crawler DB connection through the canonical helper.
        # TR: Crawler DB bağlantısını kanonik yardımcı üzerinden açıyoruz.
        conn = connect_db(args.dsn)

        try:
            # EN: We start with no set-result because show-only mode may not change anything.
            # TR: Show-only mod hiçbir şeyi değiştirmeyebileceği için başlangıçta set-result yoktur.
            set_result = None

            # EN: If the operator requested a durable state change, we execute it first.
            # TR: Operatör kalıcı durum değişimi istediyse önce onu çalıştırıyoruz.
            if args.set_runtime_control is not None:
                set_result = set_webcrawler_runtime_control(
                    conn,
                    desired_state=args.set_runtime_control,
                    state_reason=args.state_reason,
                    requested_by=args.requested_by,
                )

                # EN: Missing set-result would mean the canonical DB function behaved unexpectedly.
                # TR: Set-result çıkmaması kanonik DB fonksiyonunun beklenmedik davrandığı anlamına gelir.
                if set_result is None:
                    raise RuntimeError("set_webcrawler_runtime_control(...) returned no row")

                # EN: We commit the durable state change before reading the final visible truth.
                # TR: Son görünür doğruluğu okumadan önce kalıcı durum değişimini commit ediyoruz.
                conn.commit()

            # EN: We then read the visible control row.
            # TR: Ardından görünür kontrol satırını okuyoruz.
            runtime_control = get_webcrawler_runtime_control(conn)
            if runtime_control is None:
                raise RuntimeError("get_webcrawler_runtime_control(...) returned no row")

            # EN: We also read the may-claim decision and merge it into the payload.
            # TR: may-claim kararını da okuyup payload içine birleştiriyoruz.
            may_claim_result = webcrawler_runtime_may_claim(conn)
            if may_claim_result is None:
                raise RuntimeError("webcrawler_runtime_may_claim(...) returned no row")

            payload = {
                "mode": "runtime_control",
                "action": "set" if args.set_runtime_control is not None else "show",
                "set_result": set_result,
                "runtime_control": {
                    **dict(runtime_control),
                    "may_claim": may_claim_result.get("may_claim"),
                },
            }

            print(json.dumps(payload, indent=2, default=str))
            return 0
        finally:
            conn.close()

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

    # EN: When loop mode is not requested, we keep the original single-iteration
    # EN: behavior of the existing CLI surface.
    # TR: Loop modu istenmediyse mevcut CLI yüzeyinin orijinal tek-iterasyon
    # TR: davranışını koruyoruz.
    if not args.loop:
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

    # EN: In loop mode we keep iterating until runtime-control says stop or the
    # EN: optional iteration cap is reached.
    # TR: Loop modunda runtime-control stop diyene veya opsiyonel iterasyon sınırına
    # TR: ulaşılana kadar iterasyon yapıyoruz.
    iteration = 0

    while True:
        # EN: We increment the visible iteration counter first.
        # TR: Görünür iterasyon sayacını önce artırıyoruz.
        iteration += 1

        # EN: We execute one controlled worker iteration.
        # TR: Tek bir kontrollü worker iterasyonu çalıştırıyoruz.
        result = run_claim_probe(config)

        # EN: We convert the result into plain data for line-oriented JSON output.
        # TR: Sonucu satır-odaklı JSON çıktısı için düz veriye dönüştürüyoruz.
        payload = asdict(result)

        # EN: We annotate the payload so loop output is self-describing.
        # TR: Loop çıktısı kendi kendini açıklasın diye payload'ı etiketliyoruz.
        payload["mode"] = "worker_loop"
        payload["iteration"] = iteration

        # EN: We print one compact JSON line per iteration so smoke tests and logs stay easy to parse.
        # TR: Smoke testler ve loglar kolay parse edilsin diye her iterasyonda tek satırlık kompakt JSON yazdırıyoruz.
        print(json.dumps(payload, default=str), flush=True)

        # EN: We extract the visible runtime-control desired state from the payload.
        # TR: Payload içinden görünür runtime-control desired state değerini çıkarıyoruz.
        runtime_control = payload.get("runtime_control") or {}
        desired_state = str(runtime_control.get("desired_state") or "").strip().lower()

        # EN: Stop means the loop should exit cleanly and immediately.
        # TR: Stop, loop'un temiz ve hemen çıkması gerektiği anlamına gelir.
        if desired_state == "stop":
            return 0

        # EN: If an explicit iteration cap exists and has been reached, we exit cleanly.
        # TR: Açık bir iterasyon sınırı varsa ve ulaşıldıysa temiz biçimde çıkıyoruz.
        if args.max_iterations > 0 and iteration >= args.max_iterations:
            return 0

        # EN: We sleep according to the visible runtime-control state before the next iteration.
        # TR: Sonraki iterasyondan önce görünür runtime-control durumuna göre uyuyoruz.
        time.sleep(
            sleep_between_loop_iterations(
                payload=payload,
                sleep_seconds=args.sleep_seconds,
                pause_sleep_seconds=args.pause_sleep_seconds,
            )
        )


if __name__ == "__main__":
    # EN: We raise SystemExit with main() so the program exits with the returned
    # EN: process status code in the normal Python CLI style.
    # TR: Program normal Python CLI stilinde dönen süreç durum koduyla çıkabilsin
    # TR: diye main() sonucunu SystemExit ile yükseltiyoruz.
    raise SystemExit(main())
