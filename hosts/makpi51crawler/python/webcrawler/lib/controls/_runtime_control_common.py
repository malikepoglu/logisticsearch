# EN: We enable postponed annotation evaluation so type hints remain readable.
# TR: Type hint'ler okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import getpass because the current control surface must verify which
# EN: OS user is invoking the command, just like the old shell wrappers did.
# TR: Mevcut control yüzeyi komutu hangi OS kullanıcısının çağırdığını
# TR: doğrulamalıdır; eski shell wrapper'lar da bunu yaptığı için getpass
# TR: içe aktarıyoruz.
import getpass

# EN: We import json because control results should be printed in a structured
# EN: machine-readable form.
# TR: Kontrol sonuçları yapılı ve makine-okunur biçimde yazdırılmalıdır; bu
# TR: yüzden json içe aktarıyoruz.
import json

# EN: We import os because environment variables still participate in DSN
# EN: resolution.
# TR: DSN çözümünde environment variable'lar hâlâ rol oynadığı için os içe
# TR: aktarıyoruz.
import os

# EN: We import Path because filesystem path handling is clearer with pathlib.
# TR: Dosya yolu işlemleri pathlib ile daha açık olduğu için Path içe aktarıyoruz.
from pathlib import Path

# EN: We import the canonical runtime-control DB helpers directly, because the
# EN: interpreted controls surface should talk to the sealed DB gateway rather
# EN: than shelling out into a stale CLI string.
# TR: Yorumlanan controls yüzeyi stale CLI metnine shell ile gitmek yerine
# TR: mühürlü DB gateway ile doğrudan konuşmalıdır; bu yüzden kanonik
# TR: runtime-control DB yardımcılarını içe aktarıyoruz.
from ..logisticsearch1_1_1_state_db_gateway import (
    connect_db,
    get_webcrawler_runtime_control,
    set_webcrawler_runtime_control,
    webcrawler_runtime_may_claim,
)

# EN: The current live controls contract expects the non-root makpi51 user.
# TR: Güncel canlı controls sözleşmesi root olmayan makpi51 kullanıcısını bekler.
EXPECTED_USER = "makpi51"


# EN: This helper resolves the webcrawler root from this file location.
# EN: controls/_runtime_control_common.py -> controls -> lib -> webcrawler
# TR: Bu yardımcı webcrawler kökünü bu dosyanın konumundan çözer.
# TR: controls/_runtime_control_common.py -> controls -> lib -> webcrawler
def webcrawler_root() -> Path:
    # EN: parents[2] lands at the webcrawler directory.
    # TR: parents[2] bizi webcrawler dizinine getirir.
    return Path(__file__).resolve().parents[2]


# EN: This helper returns the canonical live env-file path.
# TR: Bu yardımcı kanonik canlı env dosyası yolunu döndürür.
def env_file_path() -> Path:
    # EN: Runtime env truth currently lives under webcrawler/config/webcrawler.env.
    # TR: Runtime env doğrusu şu anda webcrawler/config/webcrawler.env altında yaşar.
    return webcrawler_root() / "config" / "webcrawler.env"


# EN: This helper enforces the same user policy the old shell wrappers used.
# TR: Bu yardımcı eski shell wrapper'ların kullandığı aynı kullanıcı politikasını
# TR: uygular.
def ensure_expected_user() -> None:
    # EN: We read the visible current username through getpass.
    # TR: Mevcut kullanıcı adını getpass üzerinden okuyoruz.
    current_user = getpass.getuser()

    # EN: Root is intentionally forbidden for these operator controls.
    # TR: Bu operatör kontrolleri için root bilinçli olarak yasaktır.
    if current_user == "root":
        raise RuntimeError(f"control must be run as {EXPECTED_USER}, not root")

    # EN: Any non-root but wrong user is also rejected explicitly.
    # TR: Root olmayan ama yanlış kullanıcı da açık biçimde reddedilir.
    if current_user != EXPECTED_USER:
        raise RuntimeError(
            f"control must be run as {EXPECTED_USER}; current user is {current_user}"
        )


# EN: This helper reads a very small .env-like file format in a conservative way.
# EN: We support the current webcrawler.env style without trying to implement a
# EN: full shell parser.
# TR: Bu yardımcı çok küçük bir .env-benzeri formatı muhafazakâr biçimde okur.
# TR: Tam bir shell parser yazmaya çalışmadan mevcut webcrawler.env stilini
# TR: destekliyoruz.
def read_simple_env_file(path: Path) -> dict[str, str]:
    # EN: Missing env file is a hard failure because the old controls surface also
    # EN: required it explicitly.
    # TR: Eksik env dosyası sert hatadır; çünkü eski controls yüzeyi de bunu açıkça
    # TR: zorunlu tutuyordu.
    if not path.is_file():
        raise RuntimeError(f"missing env file: {path}")

    # EN: This dictionary accumulates parsed key/value pairs.
    # TR: Bu sözlük parse edilen anahtar/değer çiftlerini biriktirir.
    parsed: dict[str, str] = {}

    # EN: We iterate line by line because the accepted format is line-oriented.
    # TR: Kabul edilen biçim satır-odaklı olduğu için satır satır ilerliyoruz.
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        # EN: We strip outer whitespace first.
        # TR: Önce dış boşlukları kırpıyoruz.
        line = raw_line.strip()

        # EN: Empty lines and comment lines carry no runtime value here.
        # TR: Boş satırlar ve yorum satırları burada runtime değeri taşımaz.
        if not line or line.startswith("#"):
            continue

        # EN: We tolerate an optional leading export prefix.
        # TR: İsteğe bağlı baştaki export önekini tolere ediyoruz.
        if line.startswith("export "):
            line = line[len("export "):].strip()

        # EN: Lines without '=' are ignored because they do not fit the narrow
        # EN: accepted contract.
        # TR: '=' içermeyen satırlar dar kabul sözleşmesine uymadığı için yok sayılır.
        if "=" not in line:
            continue

        # EN: We split only once so the value may still contain '=' characters.
        # TR: Değer içinde '=' bulunabilsin diye yalnızca bir kez bölüyoruz.
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        # EN: We remove one matching pair of surrounding quotes when present.
        # TR: Varsa eşleşen tek çift dış tırnağı kaldırıyoruz.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]

        # EN: We keep only non-empty keys.
        # TR: Yalnızca boş olmayan anahtarları tutuyoruz.
        if key:
            parsed[key] = value

    # EN: We return the parsed environment mapping.
    # TR: Parse edilmiş environment eşlemesini döndürüyoruz.
    return parsed


# EN: This helper resolves the crawler DSN using current environment first and
# EN: env-file fallback second.
# TR: Bu yardımcı crawler DSN değerini önce mevcut environment'dan, sonra env
# TR: dosyası fallback'inden çözer.
def resolve_crawler_dsn() -> str:
    # EN: Current process environment gets first priority.
    # TR: İlk öncelik mevcut süreç environment'ıdır.
    env_dsn = (os.getenv("LOGISTICSEARCH_CRAWLER_DSN") or "").strip()
    if env_dsn:
        return env_dsn

    # EN: If process environment is empty, we read the canonical env file.
    # TR: Süreç environment'ı boşsa kanonik env dosyasını okuyoruz.
    file_values = read_simple_env_file(env_file_path())
    file_dsn = (file_values.get("LOGISTICSEARCH_CRAWLER_DSN") or "").strip()
    if file_dsn:
        return file_dsn

    # EN: Missing DSN is a hard failure because controls cannot talk to DB truth
    # EN: without it.
    # TR: DSN eksikse sert hata veririz; çünkü controls DB doğrusu ile onsuz
    # TR: konuşamaz.
    raise RuntimeError("missing LOGISTICSEARCH_CRAWLER_DSN in environment and env file")


# EN: This helper executes one durable runtime-control state change and prints
# EN: the final visible truth as JSON.
# TR: Bu yardımcı tek bir kalıcı runtime-control durum değişimini çalıştırır ve
# TR: son görünür doğruluğu JSON olarak yazdırır.
def apply_runtime_control(
    *,
    desired_state: str,
    state_reason: str,
    requested_by: str,
) -> int:
    # EN: We enforce the current user policy first.
    # TR: Önce güncel kullanıcı politikasını uygularız.
    ensure_expected_user()

    # EN: We resolve the crawler DSN before opening the DB connection.
    # TR: DB bağlantısını açmadan önce crawler DSN değerini çözüyoruz.
    dsn = resolve_crawler_dsn()

    # EN: We connect through the canonical DB gateway.
    # TR: Kanonik DB gateway üzerinden bağlanıyoruz.
    conn = connect_db(dsn)

    try:
        # EN: We execute the durable state change through the sealed DB function.
        # TR: Kalıcı durum değişimini mühürlü DB fonksiyonu üzerinden çalıştırıyoruz.
        set_result = set_webcrawler_runtime_control(
            conn,
            desired_state=desired_state,
            state_reason=state_reason,
            requested_by=requested_by,
        )

        # EN: A degraded set-result means the lower mutation wrapper returned no
        # EN: row. We must surface that payload honestly instead of crashing.
        # TR: Degrade olmuş set-result alt mutation wrapper'ın satır döndürmediği
        # TR: anlamına gelir. Bunu çökmeden dürüstçe görünür kılmalıyız.
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

        # EN: The durable state change must be committed before the visible truth is
        # EN: re-read.
        # TR: Görünür doğruluk yeniden okunmadan önce kalıcı durum değişimi commit
        # TR: edilmelidir.
        conn.commit()

        # EN: We read back the visible runtime-control row.
        # TR: Görünür runtime-control satırını geri okuyoruz.
        runtime_control = get_webcrawler_runtime_control(conn)

        # EN: A degraded runtime-control read after commit must stay operator-visible
        # EN: instead of turning into an exception.
        # TR: Commit sonrası degrade runtime-control okuması istisnaya dönüşmek
        # TR: yerine operatöre görünür kalmalıdır.
        if bool(runtime_control.get("runtime_control_degraded")):
            payload = {
                "mode": "runtime_control",
                "action": "set",
                "set_result": dict(set_result),
                "runtime_control": dict(runtime_control),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 2

        # EN: We also read back the visible may-claim decision.
        # TR: Görünür may-claim kararını da geri okuyoruz.
        may_claim_result = webcrawler_runtime_may_claim(conn)

        # EN: A degraded may-claim read must be surfaced explicitly instead of
        # EN: pretending the final control snapshot is complete.
        # TR: Degrade olmuş may-claim okuması nihai kontrol görüntüsü tamamlanmış
        # TR: gibi davranmak yerine açıkça görünür kılınmalıdır.
        if bool(may_claim_result.get("runtime_control_degraded")):
            payload = {
                "mode": "runtime_control",
                "action": "set",
                "set_result": dict(set_result),
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

        # EN: We build one final structured payload.
        # TR: Tek bir nihai yapılı payload kuruyoruz.
        payload = {
            "mode": "runtime_control",
            "action": "set",
            "set_result": set_result,
            "runtime_control": {
                **dict(runtime_control),
                "may_claim": may_claim_result.get("may_claim"),
            },
        }

        # EN: We print JSON for both humans and tools.
        # TR: JSON çıktısını hem insanlar hem araçlar için yazdırıyoruz.
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return 0
    finally:
        # EN: We always close the DB connection.
        # TR: DB bağlantısını her durumda kapatıyoruz.
        conn.close()
