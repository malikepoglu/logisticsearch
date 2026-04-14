# EN: We enable postponed evaluation of annotations so type hints stay readable
# EN: even when they refer to classes declared later in the file.
# TR: Type hint'ler dosyada daha sonra tanımlanan sınıflara referans verse bile
# TR: okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
from __future__ import annotations

# EN: We import dataclass because small structured parse result objects are
# EN: easier to inspect when every field is explicit and named.
# TR: Küçük yapılı parse sonuç nesneleri her alan açık ve isimli olduğunda
# TR: incelemek daha kolay olduğu için dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import html because HTML entity decoding should happen explicitly in the
# EN: first minimal parse implementation.
# TR: HTML entity çözümlemesi ilk minimal parse implementasyonunda açık biçimde
# TR: yapılmalı diye html modülünü içe aktarıyoruz.
import html

# EN: We import re because this minimal first parse layer intentionally uses
# EN: narrow standard-library regex extraction instead of a larger parser stack.
# TR: Bu minimal ilk parse katmanı daha büyük bir parser stack yerine bilinçli
# TR: olarak dar standart-kütüphane regex extraction kullandığı için re içe aktarıyoruz.
import re

# EN: We import Path because raw fetch artefact paths are easier and safer to
# EN: inspect with pathlib than with loose string handling.
# TR: Ham fetch artefact path'lerini pathlib ile incelemek gevşek metin
# TR: kullanımına göre daha kolay ve daha güvenli olduğu için Path içe aktarıyoruz.
from pathlib import Path


# EN: These DB helpers are imported here because the canonical minimal parse-apply
# EN: path must now live inside repository-tracked code instead of ad hoc snippets.
# TR: Kanonik minimal parse-apply yolu artık tek kullanımlık parçalar yerine
# TR: repository içinde izlenen kodda yaşamalı olduğu için bu DB yardımcılarını
# TR: burada içe aktarıyoruz.
from .logisticsearch1_4_db import persist_taxonomy_preranking_payload, upsert_page_workflow_status


# EN: This dataclass stores the structured result of the minimal parse entry step.
# TR: Bu dataclass minimal parse giriş adımının yapılı sonucunu tutar.
@dataclass(slots=True)
class MinimalParseResult:
    # EN: url_id is the frontier.url identifier being parsed.
    # TR: url_id parse edilen frontier.url kimliğidir.
    url_id: int

    # EN: raw_storage_path is the on-disk raw body file used as parse input.
    # TR: raw_storage_path parse girdisi olarak kullanılan disk üzerindeki ham body dosyasıdır.
    raw_storage_path: str

    # EN: input_lang_code is the best-effort language code inferred by this minimal layer.
    # TR: input_lang_code bu minimal katman tarafından tahmin edilen en iyi çaba dil kodudur.
    input_lang_code: str

    # EN: page_title is the extracted HTML title when available.
    # TR: page_title varsa çıkarılmış HTML başlığıdır.
    page_title: str | None

    # EN: body_text is the simplified visible text extracted from the HTML body.
    # TR: body_text HTML gövdesinden çıkarılan sadeleştirilmiş görünür metindir.
    body_text: str

    # EN: payload is the JSON-serializable structure that will later be sent into
    # EN: parse.persist_taxonomy_preranking_payload(...).
    # TR: payload daha sonra parse.persist_taxonomy_preranking_payload(...)
    # TR: içine gönderilecek JSON-serileştirilebilir yapıdır.
    payload: dict


# EN: This helper normalizes whitespace so downstream parse evidence is smaller,
# EN: cleaner, and easier to compare.
# TR: Bu yardımcı boşlukları normalize eder; böylece sonraki parse evidence daha
# TR: küçük, daha temiz ve karşılaştırması daha kolay olur.
def normalize_whitespace(text: str) -> str:
    # EN: We collapse all whitespace runs into a single plain space.
    # TR: Tüm boşluk kümelerini tek sade boşluğa indiriyoruz.
    return re.sub(r"\s+", " ", text).strip()


# EN: This helper reads a raw fetch artefact as UTF-8 with replacement so the
# EN: first parse layer never crashes on imperfect byte sequences.
# TR: Bu yardımcı ham fetch artefact'ını replacement ile UTF-8 olarak okur;
# TR: böylece ilk parse katmanı kusurlu byte dizilerinde çökmez.
def read_raw_body_text(raw_storage_path: str) -> str:
    # EN: We create a Path object first because file inspection is clearer with pathlib.
    # TR: Dosya incelemesi pathlib ile daha açık olduğu için önce Path nesnesi oluşturuyoruz.
    path = Path(raw_storage_path)

    # EN: The raw file must exist because parse entry depends on a real fetch artefact.
    # TR: Parse girişi gerçek bir fetch artefact'ına dayandığı için ham dosya mevcut olmalıdır.
    if not path.is_file():
        raise FileNotFoundError(f"raw fetch artefact is missing: {raw_storage_path}")

    # EN: We decode as UTF-8 with replacement because this first implementation
    # EN: chooses robustness over strict byte-perfect rejection.
    # TR: Bu ilk implementasyon katı byte-mükemmelliği reddetmek yerine dayanıklılığı
    # TR: seçtiği için replacement ile UTF-8 decode ediyoruz.
    return path.read_text(encoding="utf-8", errors="replace")


# EN: This helper extracts the first HTML <title> content when it exists.
# TR: Bu yardımcı HTML içindeki ilk <title> içeriğini, varsa, çıkarır.
def extract_title_from_html(html_text: str) -> str | None:
    # EN: We search case-insensitively and across newlines because title tags may
    # EN: be formatted in different styles.
    # TR: Title etiketleri farklı biçimlerde yazılabildiği için büyük-küçük harf
    # TR: duyarsız ve satırlar arası arama yapıyoruz.
    match = re.search(r"<title[^>]*>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)

    # EN: If there is no title tag, we return None explicitly.
    # TR: Title etiketi yoksa açık biçimde None döndürüyoruz.
    if match is None:
        return None

    # EN: We unescape HTML entities and normalize whitespace so the title is ready
    # EN: for later evidence storage.
    # TR: Başlık daha sonra evidence saklamaya hazır olsun diye HTML entity'leri
    # TR: çözüyor ve boşlukları normalize ediyoruz.
    title_text = html.unescape(match.group(1))
    title_text = normalize_whitespace(title_text)

    # EN: Empty titles should behave like missing titles.
    # TR: Boş başlıklar eksik başlık gibi davranmalıdır.
    if not title_text:
        return None

    # EN: We return the cleaned title.
    # TR: Temizlenmiş başlığı döndürüyoruz.
    return title_text


# EN: This helper infers a minimal language code from the root <html lang=...>
# EN: attribute when it exists.
# TR: Bu yardımcı kök <html lang=...> niteliğinden, varsa, minimal bir dil kodu çıkarır.
def infer_input_lang_code(html_text: str) -> str:
    # EN: We look for the HTML lang attribute because it is the cheapest and
    # EN: simplest first language signal.
    # TR: HTML lang niteliğine bakıyoruz; çünkü bu en ucuz ve en basit ilk dil sinyalidir.
    match = re.search(r"<html[^>]*\blang=[\"']?([a-zA-Z0-9_-]+)", html_text, flags=re.IGNORECASE)

    # EN: If no language marker exists, we use "und" for undetermined.
    # TR: Dil işareti yoksa undetermined anlamında "und" kullanıyoruz.
    if match is None:
        return "und"

    # EN: We normalize to lowercase because later matching becomes simpler.
    # TR: Sonraki eşleşmeler daha kolay olsun diye küçük harfe normalize ediyoruz.
    return match.group(1).strip().lower()


# EN: This helper removes script/style blocks and strips remaining tags to build
# EN: a simple visible-text approximation.
# TR: Bu yardımcı script/style bloklarını kaldırır ve kalan etiketleri sıyırarak
# TR: basit bir görünür-metin yaklaşımı üretir.
def extract_visible_text_from_html(html_text: str) -> str:
    # EN: We remove script blocks first because JavaScript is not page meaning.
    # TR: JavaScript sayfa anlamı olmadığı için önce script bloklarını kaldırıyoruz.
    without_script = re.sub(
        r"<script\b[^>]*>.*?</script>",
        " ",
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # EN: We remove style blocks second because CSS is not page meaning either.
    # TR: CSS de sayfa anlamı olmadığı için ikinci olarak style bloklarını kaldırıyoruz.
    without_style = re.sub(
        r"<style\b[^>]*>.*?</style>",
        " ",
        without_script,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # EN: We replace all remaining tags with spaces to keep visible text boundaries.
    # TR: Görünür metin sınırları korunsun diye kalan tüm etiketleri boşlukla değiştiriyoruz.
    without_tags = re.sub(r"<[^>]+>", " ", without_style)

    # EN: We decode HTML entities because text should be stored in human-readable form.
    # TR: Metin insan-okunur biçimde saklansın diye HTML entity'leri çözüyoruz.
    unescaped = html.unescape(without_tags)

    # EN: We normalize whitespace and return the final simplified visible text.
    # TR: Boşlukları normalize edip son sade görünür metni döndürüyoruz.
    return normalize_whitespace(unescaped)


# EN: This helper builds one small evidence item for a textual field.
# TR: Bu yardımcı metinsel bir alan için küçük bir evidence öğesi üretir.
def build_query_item(*, query_text: str, field_name: str) -> dict:
    # EN: We keep the structure deliberately simple and explicit for the first parse layer.
    # TR: İlk parse katmanı için yapıyı bilinçli olarak sade ve açık tutuyoruz.
    return {
        "query_text": query_text,
        "field_name": field_name,
        "source": "minimal_parse_runtime",
    }


# EN: This function converts one fetched raw HTML artefact into the minimal
# EN: JSON payload expected by the parse persistence layer.
# TR: Bu fonksiyon fetch edilmiş tek bir ham HTML artefact'ını parse persistence
# TR: katmanının beklediği minimal JSON payload'ına çevirir.
def build_minimal_parse_payload(
    *,
    url_id: int,
    raw_storage_path: str,
    source_run_id: str | None = None,
    source_note: str | None = None,
) -> MinimalParseResult:
    # EN: We read the raw HTML text first because all later parse signals depend on it.
    # TR: Sonraki tüm parse sinyalleri buna bağlı olduğu için önce ham HTML metnini okuyoruz.
    html_text = read_raw_body_text(raw_storage_path)

    # EN: We extract the page title as a separate higher-value signal.
    # TR: Sayfa başlığını daha yüksek değerli ayrı bir sinyal olarak çıkarıyoruz.
    page_title = extract_title_from_html(html_text)

    # EN: We extract visible body text as the first minimal body-content signal.
    # TR: Görünür body metnini ilk minimal body-içerik sinyali olarak çıkarıyoruz.
    body_text = extract_visible_text_from_html(html_text)

    # EN: We infer a best-effort language code from HTML metadata.
    # TR: HTML metadata üzerinden en iyi çaba dil kodu çıkarıyoruz.
    input_lang_code = infer_input_lang_code(html_text)

    # EN: Title evidence contains one item only when a non-empty title exists.
    # TR: Title evidence yalnızca boş olmayan bir başlık varsa tek öğe içerir.
    title_queries = []
    if page_title is not None:
        title_queries.append(build_query_item(query_text=page_title, field_name="title"))

    # EN: Body evidence is intentionally truncated so the first payload stays small,
    # EN: predictable, and easy to inspect.
    # TR: İlk payload küçük, öngörülebilir ve incelemesi kolay kalsın diye body
    # TR: evidence bilinçli olarak kısaltılır.
    body_excerpt = body_text[:4000] if body_text else ""

    # EN: Body evidence contains one item only when the excerpt is non-empty.
    # TR: Body evidence yalnızca excerpt boş değilse tek öğe içerir.
    body_queries = []
    if body_excerpt:
        body_queries.append(build_query_item(query_text=body_excerpt, field_name="body_text_excerpt"))

    # EN: We build the minimal payload structure expected by the parse SQL layer.
    # EN: Candidate list is intentionally empty in this first entry step.
    # TR: Parse SQL katmanının beklediği minimal payload yapısını kuruyoruz.
    # TR: Candidate list bu ilk giriş adımında bilinçli olarak boştur.
    payload = {
        "url_id": url_id,
        "input_lang_code": input_lang_code,
        "url_queries": [],
        "title_queries": title_queries,
        "h1_queries": [],
        "breadcrumb_queries": [],
        "structured_data_queries": [],
        "anchor_queries": [],
        "body_queries": body_queries,
        "candidates": [],
        "source_run_id": source_run_id,
        "source_note": source_note or "minimal parse entry flow from raw fetch artefact",
        "metadata": {
            "parse_mode": "minimal_stdlib_html",
            "raw_storage_path": raw_storage_path,
            "page_title": page_title,
            "body_text_chars": len(body_text),
        },
    }

    # EN: We return both the human-useful extracted fields and the final payload.
    # TR: Hem insan için faydalı çıkarılmış alanları hem de son payload'ı döndürüyoruz.
    return MinimalParseResult(
        url_id=url_id,
        raw_storage_path=raw_storage_path,
        input_lang_code=input_lang_code,
        page_title=page_title,
        body_text=body_text,
        payload=payload,
    )

# EN: This helper decides what value is currently safe to place into
# EN: parse.page_workflow_status.linked_snapshot_id.
# TR: Bu yardımcı, parse.page_workflow_status.linked_snapshot_id alanına şu anda
# TR: hangi değerin güvenli biçimde yazılabileceğini belirler.
def resolve_workflow_linked_snapshot_id(persist_result: dict | None) -> int | None:
    # EN: We intentionally return None in the current minimal parse-entry stage.
    # TR: Mevcut minimal parse-entry aşamasında bilinçli olarak None döndürüyoruz.

    # EN: Current live Pi51 proof showed that persist_taxonomy_preranking_payload(...)
    # EN: returns a field named snapshot_id, but that field is not yet proven to be
    # EN: parse.page_preranking_snapshot.snapshot_id.
    # TR: Mevcut canlı Pi51 kanıtı, persist_taxonomy_preranking_payload(...)
    # TR: fonksiyonunun snapshot_id adlı bir alan döndürdüğünü gösterdi; ancak bu
    # TR: alanın parse.page_preranking_snapshot.snapshot_id olduğu henüz kanıtlanmadı.

    # EN: The linked_snapshot_id column has a foreign-key constraint that points
    # EN: specifically to parse.page_preranking_snapshot(snapshot_id).
    # TR: linked_snapshot_id sütunu özellikle
    # TR: parse.page_preranking_snapshot(snapshot_id) tablosuna giden bir foreign-key
    # TR: kısıtına sahiptir.

    # EN: Blindly reusing persist_result["snapshot_id"] here would therefore risk
    # EN: foreign-key violations and incorrect semantic linking.
    # TR: Bu yüzden persist_result["snapshot_id"] değerini burada körlemesine
    # TR: yeniden kullanmak foreign-key ihlali ve yanlış semantik bağlama riski taşır.

    # EN: Until an explicit, tested, and sealed mapping to a real preranking snapshot
    # EN: exists, the only safe value is None.
    # TR: Gerçek bir preranking snapshot'ına giden açık, test edilmiş ve mühürlenmiş
    # TR: bir mapping oluşana kadar tek güvenli değer None'dır.
    return None


# EN: This dataclass stores the two durable DB results produced by the canonical
# EN: minimal parse-apply helper.
# TR: Bu dataclass, kanonik minimal parse-apply yardımcısının ürettiği iki kalıcı
# TR: DB sonucunu tutar.
@dataclass(slots=True)
class MinimalParseApplyResult:
    # EN: persist_result stores the row returned by
    # EN: parse.persist_taxonomy_preranking_payload(...).
    # TR: persist_result, parse.persist_taxonomy_preranking_payload(...)
    # TR: tarafından dönen satırı tutar.
    persist_result: dict

    # EN: workflow_result stores the row returned by
    # EN: parse.upsert_page_workflow_status(...).
    # TR: workflow_result, parse.upsert_page_workflow_status(...)
    # TR: tarafından dönen satırı tutar.
    workflow_result: dict


# EN: This helper is the current canonical repo-contained minimal parse-entry flow.
# EN: It keeps the whole apply path inside tracked code instead of relying on
# EN: ad hoc one-off Python snippets outside the repository surface.
# TR: Bu yardımcı, mevcut kanonik repo-içi minimal parse-entry akışıdır.
# TR: Uygulama yolunun tamamını repository dışında kalan tek kullanımlık Python
# TR: parçaları yerine izlenen kod içinde tutar.
def apply_minimal_parse_entry(
    *,
    conn,
    url_id: int,
    raw_storage_path: str,
    source_run_id: str,
    source_note: str | None = None,
    workflow_state: str = "pre_ranked",
    workflow_state_reason: str = "minimal_parse_entry_flow_committed_via_repo_helper",
) -> MinimalParseApplyResult:
    # EN: We first build the structured minimal parse payload from the raw HTML
    # EN: artefact because payload construction and DB persistence must stay aligned.
    # TR: Önce ham HTML artefact'ından yapılı minimal parse payload'ını kuruyoruz;
    # TR: çünkü payload üretimi ile DB persistence aynı hizada kalmalıdır.
    parse_result = build_minimal_parse_payload(
        url_id=url_id,
        raw_storage_path=raw_storage_path,
        source_run_id=source_run_id,
        source_note=source_note,
    )

    # EN: We persist the payload through the canonical DB helper so the current
    # EN: narrow parse persistence truth stays centralized.
    # TR: Payload'ı kanonik DB yardımcısı üzerinden persist ediyoruz; böylece
    # TR: mevcut dar parse persistence doğrusu merkezî kalır.
    persist_result = persist_taxonomy_preranking_payload(
        conn=conn,
        payload=parse_result.payload,
    )

    # EN: We resolve linked_snapshot_id only through the dedicated safe-policy
    # EN: helper so blind snapshot reuse cannot silently reappear.
    # TR: linked_snapshot_id değerini yalnızca dedicated güvenli-politika
    # TR: yardımcısı üzerinden çözüyoruz; böylece kör snapshot yeniden kullanımı
    # TR: sessizce geri dönemez.
    linked_snapshot_id = resolve_workflow_linked_snapshot_id(persist_result)

    # EN: We write workflow state through the canonical DB helper and pass the
    # EN: safe linked_snapshot_id result exactly as resolved above.
    # TR: Workflow durumunu kanonik DB yardımcısı üzerinden yazıyoruz ve güvenli
    # TR: linked_snapshot_id sonucunu yukarıda çözüldüğü haliyle aynen iletiyoruz.
    workflow_result = upsert_page_workflow_status(
        conn=conn,
        url_id=url_id,
        workflow_state=workflow_state,
        state_reason=workflow_state_reason,
        linked_snapshot_id=linked_snapshot_id,
        source_run_id=source_run_id,
        source_note=source_note,
        status_metadata={
            "parse_mode": "minimal_stdlib_html",
            "linked_snapshot_policy": "safe_repo_helper",
            "linked_snapshot_id": linked_snapshot_id,
            "raw_storage_path": raw_storage_path,
        },
    )

    # EN: We return both durable DB results together so callers can audit exactly
    # EN: what the parse apply step changed.
    # TR: Çağıran taraf parse apply adımının tam olarak neyi değiştirdiğini audit
    # TR: edebilsin diye iki kalıcı DB sonucunu birlikte döndürüyoruz.
    return MinimalParseApplyResult(
        persist_result=persist_result,
        workflow_result=workflow_result,
    )
