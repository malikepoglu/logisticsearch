"""\
EN:
This module is the canonical operator-facing CLI/control surface that sits
directly under the thin root entry.

Scope contract:
- It is allowed to parse CLI arguments and print structured JSON.
- It is allowed to inspect or mutate runtime-control state through the gateway.
- It is allowed to execute one worker probe iteration or a repeated loop of
  worker probe iterations.
- It is not the place where low-level claim/fetch/parse logic is implemented;
  that logic lives in the worker runtime family.

Important payload shapes surfaced here:
- runtime_control: dict-like snapshot returned by gateway helpers.
- may_claim_result: dict returned by runtime-control policy evaluation.
- config: WorkerConfig dataclass passed into run_claim_probe(...).
- payload: JSON-serializable dict printed to stdout.
- desired_state: normalized text token such as play/pause/stop.
- probe_only: bool routed into WorkerConfig; True means rollback-style probe,
  False means durable claim path.

TR:
Bu modül ince kök girişin hemen altında duran kanonik operatör-yüzlü CLI/kontrol
yüzeyidir.

Kapsam sözleşmesi:
- CLI argümanlarını parse etmesine ve yapılı JSON basmasına izin verilir.
- Gateway üzerinden runtime-control durumunu inceleyebilir veya değiştirebilir.
- Tek worker probe iterasyonu veya tekrar eden worker probe iterasyonları
  çalıştırabilir.
- Düşük seviye claim/fetch/parse mantığının sahibi değildir; bu mantık worker
  runtime ailesinde yaşar.

Burada görünür olan önemli payload şekilleri:
- runtime_control: gateway yardımcılarından dönen dict-benzeri anlık görüntü.
- may_claim_result: runtime-control policy değerlendirmesinden dönen dict.
- config: run_claim_probe(...) içine verilen WorkerConfig dataclass nesnesi.
- payload: stdout'a basılan JSON-serileştirilebilir dict.
- desired_state: play/pause/stop gibi normalize edilmiş metin tokenı.
- probe_only: WorkerConfig içine taşınan bool; True rollback-benzeri probe,
  False durable claim yolu demektir.
"""

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
    """\
    EN:
    Resolve the crawler DSN for this CLI surface.

    Branch contract:
    - Returns str from LOGISTICSEARCH_CRAWLER_DSN when that variable is present
      and non-empty.
    - Otherwise returns a controlled local scratch fallback string.
    - This helper never returns None.

    TR:
    Bu CLI yüzeyi için crawler DSN değerini çözer.

    Dal sözleşmesi:
    - LOGISTICSEARCH_CRAWLER_DSN varsa ve boş değilse oradaki str değeri döner.
    - Aksi durumda kontrollü yerel scratch fallback str değeri döner.
    - Bu yardımcı asla None döndürmez.
    """
    # EN: We first check LOGISTICSEARCH_CRAWLER_DSN because explicit operator
    # EN: configuration is more honest than a hidden hard-coded assumption.
    # TR: Önce LOGISTICSEARCH_CRAWLER_DSN değişkenini kontrol ediyoruz; çünkü
    # TR: açık operatör konfigürasyonu gizli hard-coded varsayımdan daha dürüsttür.
    # EN: env_value is either a non-empty DSN string chosen by the operator or
    # EN: None/empty when no explicit DSN override exists in the environment.
    # TR: env_value ya operatör tarafından seçilmiş boş olmayan DSN metnidir ya da
    # TR: environment içinde açık bir DSN override yoksa None/boş değerdir.
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
    """\
    EN:
    Resolve the visible worker identity used in claim-oriented calls.

    Return contract:
    - str from LOGISTICSEARCH_WORKER_ID when explicitly provided.
    - Otherwise deterministic fallback worker id.
    - Never returns None.

    TR:
    Claim-odaklı çağrılarda kullanılan görünür worker kimliğini çözer.

    Dönüş sözleşmesi:
    - LOGISTICSEARCH_WORKER_ID açıkça verilmişse oradaki str değer döner.
    - Aksi durumda deterministik fallback worker id döner.
    - Asla None döndürmez.
    """
    # EN: We check a dedicated environment variable first.
    # TR: Önce ayrılmış environment variable değerine bakıyoruz.
    # EN: env_value carries the visible worker identity override. It is expected
    # EN: to be text because downstream claim surfaces use textual worker ids.
    # TR: env_value görünür worker identity override değerini taşır. Aşağı akış
    # TR: claim yüzeyleri metinsel worker id kullandığı için burada metin beklenir.
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
    """\
    EN:
    Resolve the operator/requester identity written into runtime-control rows.

    Return contract:
    - str from LOGISTICSEARCH_CONTROL_REQUESTED_BY when present.
    - Otherwise stable CLI-origin fallback identity.
    - Never returns None.

    TR:
    Runtime-control satırlarına yazılan operatör/istekçi kimliğini çözer.

    Dönüş sözleşmesi:
    - LOGISTICSEARCH_CONTROL_REQUESTED_BY varsa oradaki str değeri döner.
    - Aksi durumda stabil CLI-kaynaklı fallback kimliği döner.
    - Asla None döndürmez.
    """
    # EN: We first check the explicit operator override variable.
    # TR: Önce açık operatör override değişkenine bakıyoruz.
    # EN: env_value is the optional text identity written into runtime-control
    # EN: audit fields such as requested_by.
    # TR: env_value requested_by gibi runtime-control audit alanlarına yazılan
    # TR: opsiyonel metinsel kimliktir.
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
    """\
    EN:
    Build the current CLI parser for runtime-control and worker-probe operations.

    Return contract:
    - Returns argparse.ArgumentParser.
    - The parser exposes DSN, worker_id, lease_seconds, probe_only-related
      durable-claim selection, loop cadence, and runtime-control inspection/
      mutation flags.

    TR:
    Runtime-control ve worker-probe işlemleri için mevcut CLI parser'ını kurar.

    Dönüş sözleşmesi:
    - argparse.ArgumentParser döndürür.
    - Parser; DSN, worker_id, lease_seconds, probe_only ile ilişkili
      durable-claim seçimi, loop temposu ve runtime-control inceleme/değiştirme
      bayraklarını dışa açar.
    """
    # EN: We create the parser with a narrow description so current scope stays honest.
    # TR: Güncel kapsam dürüst kalsın diye parser'ı dar bir açıklamayla oluşturuyoruz.
    # EN: parser is the single ArgumentParser instance for this module. It stays
    # EN: local to keep the file surface simple and to avoid hidden global CLI state.
    # TR: parser bu modülün tek ArgumentParser örneğidir. Dosya yüzeyi sade kalsın
    # TR: ve gizli global CLI durumu oluşmasın diye yerel tutulur.
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
    """\
    EN:
    Choose the next loop sleep duration from the visible runtime-control payload.

    Input contract:
    - payload: dict expected to possibly contain payload["runtime_control"].
    - sleep_seconds: normal cadence when no pause state is visible.
    - pause_sleep_seconds: slower cadence used when desired_state == "pause".

    Return branches:
    - float pause_sleep_seconds when desired_state resolves to "pause".
    - float sleep_seconds for all remaining branches, including missing or empty
      runtime_control payload.

    TR:
    Görünür runtime-control payload'ından bir sonraki loop uyku süresini seçer.

    Girdi sözleşmesi:
    - payload: muhtemelen payload["runtime_control"] içeren dict.
    - sleep_seconds: görünür pause durumu yoksa normal tempo.
    - pause_sleep_seconds: desired_state == "pause" olduğunda kullanılan daha yavaş tempo.

    Dönüş dalları:
    - desired_state "pause" ise float pause_sleep_seconds.
    - Eksik/boş runtime_control dahil kalan tüm dallarda float sleep_seconds.
    """
    # EN: We read the optional runtime-control snapshot from the returned payload.
    # TR: Dönen payload içinden opsiyonel runtime-control anlık görüntüsünü okuyoruz.
    # EN: runtime_control is expected to be a dict-like snapshot. Missing/None
    # EN: branches are normalized to an empty dict so downstream .get(...) calls
    # EN: remain branch-safe.
    # TR: runtime_control dict-benzeri anlık görüntü olarak beklenir. Eksik/None
    # TR: dallar boş dict'e normalize edilir; böylece aşağıdaki .get(...) çağrıları
    # TR: dal-güvenli kalır.
    runtime_control = payload.get("runtime_control") or {}

    # EN: We extract the desired state as a normalized text token.
    # TR: desired_state değerini normalize edilmiş metin tokenı olarak çıkarıyoruz.
    # EN: desired_state is always normalized into lowercase text. Typical visible
    # EN: values here include "pause", "play", "stop", or empty string when the
    # EN: upstream payload did not expose a desired_state field.
    # TR: desired_state her zaman küçük harfli metne normalize edilir. Buradaki
    # TR: tipik görünür değerler "pause", "play", "stop" veya upstream payload
    # TR: desired_state alanı taşımıyorsa boş metindir.
    desired_state = str(runtime_control.get("desired_state") or "").strip().lower()

    # EN: Pause should keep the process alive but slower.
    # TR: Pause süreci canlı tutmalı ama daha yavaş çalıştırmalıdır.
    if desired_state == "pause":
        return pause_sleep_seconds

    # EN: All remaining states use the normal loop cadence.
    # TR: Kalan tüm durumlar normal loop temposunu kullanır.
    return sleep_seconds


def main() -> int:
    """\
    EN:
    Execute the canonical CLI surface for one of three broad corridors:
    1) runtime-control inspection/mutation,
    2) single worker probe,
    3) repeated worker loop.

    Return contract:
    - 0 on successful structured execution.
    - 2 when runtime-control or may-claim reads/writes are explicitly degraded
      but still rendered as visible JSON.
    - Unexpected exceptions are not swallowed here.

    Important visible variables:
    - config: WorkerConfig forwarded to run_claim_probe(...).
    - runtime_control: dict snapshot read from gateway helpers.
    - may_claim_result: dict explaining whether claims are currently permitted.
    - payload: final JSON-serializable dict printed to stdout.
    - probe_only: bool embedded inside config via durable-claim inversion.

    TR:
    Üç ana koridordan birini çalıştıran kanonik CLI yüzeyidir:
    1) runtime-control inceleme/değiştirme,
    2) tek worker probe,
    3) tekrar eden worker loop.

    Dönüş sözleşmesi:
    - Yapılı çalıştırma başarılıysa 0.
    - Runtime-control veya may-claim okuma/yazma açıkça degrade olup yine de
      görünür JSON olarak basılıyorsa 2.
    - Beklenmeyen istisnalar burada yutulmaz.

    Önemli görünür değişkenler:
    - config: run_claim_probe(...) içine iletilen WorkerConfig.
    - runtime_control: gateway yardımcılarından okunan dict anlık görüntü.
    - may_claim_result: claim izni verilip verilmediğini açıklayan dict.
    - payload: stdout'a basılan son JSON-serileştirilebilir dict.
    - probe_only: durable-claim terslenmesiyle config içine gömülen bool.
    """
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
            # EN: set_result starts as None because show-only runtime-control mode
            # EN: may inspect state without writing anything. Later it becomes a dict
            # EN: when set_webcrawler_runtime_control(...) actually runs.
            # TR: set_result başlangıçta None'dır; çünkü yalnızca gösterim yapan
            # TR: runtime-control modu hiçbir şey yazmadan durumu inceleyebilir.
            # TR: set_webcrawler_runtime_control(...) çalışırsa daha sonra dict olur.
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

                # EN: A degraded set-result must stay operator-visible instead of
                # EN: crashing this CLI surface.
                # TR: Degrade olmuş set-result bu CLI yüzeyinde çökme üretmek
                # TR: yerine operatöre görünür kalmalıdır.
                if bool(set_result.get("runtime_control_degraded")):
                    payload = {
                        "mode": "runtime_control",
                        "action": "set",
                        "set_result": dict(set_result),
                        "runtime_control": dict(set_result),
                    }
                    conn.rollback()
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                    return 2

                # EN: We commit the durable state change before reading the final visible truth.
                # TR: Son görünür doğruluğu okumadan önce kalıcı durum değişimini commit ediyoruz.
                conn.commit()

            # EN: We then read the visible control row.
            # TR: Ardından görünür kontrol satırını okuyoruz.
            runtime_control = get_webcrawler_runtime_control(conn)

            # EN: A degraded runtime-control read must be surfaced explicitly instead
            # EN: of turning into a hard failure.
            # TR: Degrade olmuş runtime-control okuması sert hataya dönüşmek yerine
            # TR: açıkça görünür kılınmalıdır.
            if bool(runtime_control.get("runtime_control_degraded")):
                payload = {
                    "mode": "runtime_control",
                    "action": "set" if args.set_runtime_control is not None else "show",
                    "set_result": set_result,
                    "runtime_control": dict(runtime_control),
                }
                print(json.dumps(payload, ensure_ascii=False, indent=2))
                return 2

            # EN: We also read the may-claim decision and merge it into the payload.
            # TR: may-claim kararını da okuyup payload içine birleştiriyoruz.
            # EN: may_claim_result is the policy-evaluation dict returned by the
            # EN: gateway. It normally carries a bool-like may_claim field and may also
            # EN: carry degraded markers when the control surface cannot be trusted fully.
            # TR: may_claim_result gateway tarafından dönen policy değerlendirme
            # TR: dict'idir. Normalde bool-benzeri may_claim alanı taşır; ayrıca kontrol
            # TR: yüzeyi tam güvenilir değilse degraded işaretleri de taşıyabilir.
            may_claim_result = webcrawler_runtime_may_claim(conn)

            # EN: A degraded may-claim read must stay visible instead of pretending
            # EN: the final snapshot is complete.
            # TR: Degrade olmuş may-claim okuması nihai görüntü tamamlanmış gibi
            # TR: davranmak yerine görünür kalmalıdır.
            if bool(may_claim_result.get("runtime_control_degraded")):
                payload = {
                    "mode": "runtime_control",
                    "action": "set" if args.set_runtime_control is not None else "show",
                    "set_result": set_result,
                    "may_claim_result": dict(may_claim_result),
                    "runtime_control": {
                        **dict(runtime_control),
                        "may_claim": may_claim_result.get("may_claim"),
                        "may_claim_degraded": True,
                        "may_claim_degraded_reason": may_claim_result.get("runtime_control_degraded_reason"),
                    },
                }
                print(json.dumps(payload, ensure_ascii=False, indent=2))
                return 2

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
    # EN: config is the structured runtime contract forwarded into run_claim_probe.
    # EN: It contains the DSN text, textual worker_id, integer lease duration, and
    # EN: the probe_only bool that decides rollback-style vs durable claim behavior.
    # TR: config run_claim_probe içine iletilen yapılandırılmış runtime sözleşmesidir.
    # TR: DSN metnini, metinsel worker_id değerini, tamsayı lease süresini ve
    # TR: rollback-benzeri probe ile durable claim davranışını belirleyen probe_only
    # TR: bool alanını taşır.
    config = WorkerConfig(
        dsn=args.dsn,
        worker_id=args.worker_id,
        lease_seconds=args.lease_seconds,
        # EN: When durable-claim mode is requested, probe_only must become False
        # EN: so a successful claim is committed instead of rolled back.
        # TR: Durable-claim modu istendiğinde probe_only değeri False olmalıdır;
        # TR: böylece başarılı claim rollback yerine commit edilir.
        # EN: probe_only is False only when --durable-claim was explicitly chosen.
        # EN: Typical branches: True -> probe/rollback corridor, False -> durable
        # EN: leased-claim corridor.
        # TR: probe_only yalnızca --durable-claim açıkça seçildiğinde False olur.
        # TR: Tipik dallar: True -> probe/rollback koridoru, False -> durable
        # TR: leased-claim koridoru.
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
        # EN: payload becomes a plain dict copy of the worker result dataclass so
        # EN: JSON serialization is deterministic and explicit.
        # TR: payload worker sonuç dataclass'ının düz dict kopyasına dönüşür; böylece
        # TR: JSON serileştirmesi deterministik ve açık olur.
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
    # EN: iteration is the visible loop counter. It stays integer-typed and starts
    # EN: at 0 so the first executed loop body reports iteration 1.
    # TR: iteration görünür loop sayacıdır. Tamsayı tipinde kalır ve 0'dan başlar;
    # TR: böylece ilk çalıştırılan loop gövdesi iteration 1 olarak raporlanır.
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
        # EN: runtime_control is re-read from the just-produced payload so loop exit
        # EN: and sleep decisions are based on the same visible snapshot the operator
        # EN: sees in stdout.
        # TR: runtime_control yeni üretilen payload içinden tekrar okunur; böylece loop
        # TR: çıkış ve uyku kararları operatörün stdout'ta gördüğü aynı anlık görüntüye
        # TR: dayanır.
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
