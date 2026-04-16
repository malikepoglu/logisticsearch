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

# EN: We import hashlib because discovered canonical URLs should be hashed in the same explicit way before DB enqueue.
# TR: Keşfedilmiş kanonik URL'ler DB enqueue öncesinde aynı açık biçimde hash'lensin diye hashlib içe aktarıyoruz.
import hashlib

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

# EN: We import URL helpers because minimal discovery must normalize relative and absolute HTML links.
# TR: Minimal discovery göreli ve mutlak HTML linklerini normalize etmelidir; bu yüzden URL yardımcılarını içe aktarıyoruz.
from urllib.parse import urljoin, urlsplit, urlunsplit


# EN: These DB helpers are imported here because the canonical minimal parse-apply
# EN: path must now live inside repository-tracked code instead of ad hoc snippets.
# TR: Kanonik minimal parse-apply yolu artık tek kullanımlık parçalar yerine
# TR: repository içinde izlenen kodda yaşamalı olduğu için bu DB yardımcılarını
# TR: burada içe aktarıyoruz.
from .logisticsearch1_1_1_state_db_gateway import (
    enqueue_discovered_url,
    fetch_url_discovery_context,
    persist_page_preranking_snapshot,
    persist_taxonomy_preranking_payload,
    upsert_page_workflow_status,
)

from .logisticsearch1_1_2_3_1_taxonomy_runtime import (
    connect_taxonomy_db,
    search_runtime_taxonomy,
    taxonomy_default_dsn,
)



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

    # EN: preranking_snapshot_result stores the row returned by
    # EN: parse.persist_page_preranking_snapshot(...).
    # TR: preranking_snapshot_result, parse.persist_page_preranking_snapshot(...)
    # TR: tarafından dönen satırı tutar.
    preranking_snapshot_result: dict

    # EN: discovery_result stores the structured result of the minimal HTML-link
    # EN: discovery enqueue bridge.
    # TR: discovery_result, minimal HTML-link discovery enqueue köprüsünün
    # TR: yapılı sonucunu tutar.
    discovery_result: dict

    # EN: workflow_result stores the row returned by
    # EN: parse.upsert_page_workflow_status(...).
    # TR: workflow_result, parse.upsert_page_workflow_status(...)
    # TR: tarafından dönen satırı tutar.
    workflow_result: dict


# EN: This helper returns the current taxonomy package-version text used by the
# EN: minimal repo-contained taxonomy bridge.
# TR: Bu yardımcı, minimal repo-içi taxonomy köprüsünün kullandığı güncel
# TR: taxonomy package-version metnini döndürür.
def minimal_taxonomy_package_version() -> str:
    # EN: We keep the package version explicit and stable so persisted parse rows
    # EN: can later be audited without guessing.
    # TR: Persist edilen parse satırları daha sonra tahmin yürütmeden audit
    # TR: edilebilsin diye package version değerini açık ve stabil tutuyoruz.
    return "pi51_taxonomy_runtime_v1"


# EN: This helper maps parse evidence field names onto the score-column names
# EN: expected by the parse candidate contract.
# TR: Bu yardımcı parse evidence alan adlarını, parse candidate sözleşmesinin
# TR: beklediği skor sütunu adlarına eşler.
def candidate_score_field_name(field_name: str) -> str:
    # EN: Title evidence contributes to title_score.
    # TR: Title evidence, title_score alanına katkı verir.
    if field_name == "title":
        return "title_score"

    # EN: All remaining minimal evidence currently contributes through body_score.
    # TR: Kalan tüm minimal evidence şu anda body_score üzerinden katkı verir.
    return "body_score"


# EN: This helper converts a numeric score into a small explicit confidence band.
# TR: Bu yardımcı sayısal bir skoru küçük ve açık bir confidence band değerine çevirir.
def confidence_band_for_score(score: float) -> str:
    # EN: Very high scores become high-confidence candidates.
    # TR: Çok yüksek skorlar high-confidence candidate olur.
    if score >= 90.0:
        return "high"

    # EN: Mid-high scores become medium-confidence candidates.
    # TR: Orta-yüksek skorlar medium-confidence candidate olur.
    if score >= 60.0:
        return "medium"

    # EN: Positive but weaker scores remain low-confidence.
    # TR: Pozitif ama daha zayıf skorlar low-confidence olarak kalır.
    if score > 0.0:
        return "low"

    # EN: Zero-score rows stay unreviewed.
    # TR: Sıfır-skor satırlar unreviewed olarak kalır.
    return "unreviewed"


# EN: This helper builds the minimal search-input list sent into the runtime
# EN: taxonomy helper.
# TR: Bu yardımcı runtime taxonomy helper'ına gönderilecek minimal arama girdisi
# TR: listesini kurar.
def build_taxonomy_search_inputs(parse_result: MinimalParseResult) -> list[dict]:
    # EN: We start from an empty list so each added search input stays explicit.
    # TR: Her eklenen arama girdisi açık kalsın diye boş listeyle başlıyoruz.
    search_inputs: list[dict] = []

    # EN: A non-empty page title is the strongest first query source.
    # TR: Boş olmayan page title ilk ve en güçlü sorgu kaynağıdır.
    if parse_result.page_title:
        search_inputs.append(
            {
                "field_name": "title",
                "query_text": parse_result.page_title,
            }
        )

    # EN: A non-empty body excerpt is used as the second weaker query source.
    # TR: Boş olmayan body excerpt ikinci ve daha zayıf sorgu kaynağı olarak kullanılır.
    if parse_result.body_text:
        search_inputs.append(
            {
                "field_name": "body_text_excerpt",
                "query_text": parse_result.body_text[:1000],
            }
        )

    # EN: We return the fully prepared search-input list.
    # TR: Tam hazırlanmış arama girdisi listesini döndürüyoruz.
    return search_inputs


# EN: This helper builds minimal parse candidate rows from the live runtime
# EN: taxonomy database by using the already-proven second-connection helper.
# TR: Bu yardımcı, zaten kanıtlanmış ikinci-bağlantı helper'ını kullanarak canlı
# TR: runtime taxonomy veritabanından minimal parse candidate satırları üretir.
def build_minimal_taxonomy_candidates(
    *,
    parse_result: MinimalParseResult,
    source_run_id: str,
    source_note: str | None = None,
    limit_per_query: int = 5,
    max_candidates: int = 10,
) -> list[dict]:
    # EN: We first derive the concrete search inputs from the parse result.
    # TR: Önce parse sonucundan somut arama girdilerini türetiyoruz.
    search_inputs = build_taxonomy_search_inputs(parse_result)

    # EN: If there is no usable search input, there can be no taxonomy candidates.
    # TR: Kullanılabilir arama girdisi yoksa taxonomy candidate de olamaz.
    if not search_inputs:
        return []

    # EN: We open the dedicated taxonomy connection through the canonical runtime helper.
    # TR: Ayrılmış taxonomy bağlantısını kanonik runtime helper üzerinden açıyoruz.
    taxonomy_conn = connect_taxonomy_db(taxonomy_default_dsn())

    try:
        # EN: We aggregate hits by taxonomy_node_code so multiple field hits enrich
        # EN: one candidate instead of creating noisy duplicates.
        # TR: Birden çok alan vuruşu gürültülü kopyalar üretmesin, tek candidate'i
        # TR: zenginleştirsin diye hit'leri taxonomy_node_code bazında topluyoruz.
        candidate_map: dict[str, dict] = {}

        # EN: We process each search input one by one.
        # TR: Her arama girdisini tek tek işliyoruz.
        for search_input in search_inputs:
            # EN: We extract the explicit field name.
            # TR: Açık alan adını çıkarıyoruz.
            field_name = search_input["field_name"]

            # EN: We extract the concrete query text.
            # TR: Somut sorgu metnini çıkarıyoruz.
            query_text = search_input["query_text"]

            # EN: We search the live runtime taxonomy with the same language code
            # EN: inferred from the HTML surface.
            # TR: Canlı runtime taxonomy içinde, HTML yüzeyinden çıkarılan aynı dil
            # TR: koduyla arama yapıyoruz.
            hits = search_runtime_taxonomy(
                taxonomy_conn,
                query_text=query_text,
                input_lang_code=parse_result.input_lang_code,
                limit=limit_per_query,
            )

            # EN: We fold each returned hit into the candidate map.
            # TR: Dönen her hit'i candidate map içine katlıyoruz.
            for hit in hits:
                # EN: One node_code corresponds to one aggregated candidate row.
                # TR: Bir node_code tek bir toplanmış candidate satırına karşılık gelir.
                candidate_key = hit.node_code

                # EN: If this node has not been seen yet, we create its base row.
                # TR: Bu node daha önce görülmediyse temel satırını oluşturuyoruz.
                if candidate_key not in candidate_map:
                    candidate_map[candidate_key] = {
                        "taxonomy_source_db": "logisticsearch_taxonomy",
                        "taxonomy_package_version": minimal_taxonomy_package_version(),
                        "taxonomy_package_id": None,
                        "taxonomy_concept_id": None,
                        "taxonomy_node_code": hit.node_code,
                        "taxonomy_concept_key": f"{hit.node_code}:{hit.lang_code}",
                        "input_lang_code": parse_result.input_lang_code,
                        "matched_lang_codes": [],
                        "matched_fields": [],
                        "matched_queries": [],
                        "domain_type": hit.domain_type,
                        "node_kind": hit.node_kind,
                        "url_score": 0.0,
                        "title_score": 0.0,
                        "h1_score": 0.0,
                        "breadcrumb_score": 0.0,
                        "structured_data_score": 0.0,
                        "anchor_score": 0.0,
                        "body_score": 0.0,
                        "total_score": 0.0,
                        "evidence_count": 0,
                        "confidence_band": "unreviewed",
                        "source_run_id": source_run_id,
                        "source_note": source_note or "taxonomy runtime bridge from minimal parse entry",
                        "candidate_metadata": {
                            "taxonomy_node_id": hit.node_id,
                            "lang_priority": hit.lang_priority,
                            "matched_surfaces": [],
                            "matched_texts": [],
                        },
                    }

                # EN: We work on the aggregated candidate row.
                # TR: Toplanmış candidate satırı üzerinde çalışıyoruz.
                candidate = candidate_map[candidate_key]

                # EN: We map the current evidence field to its score column.
                # TR: Mevcut evidence alanını kendi skor sütununa eşliyoruz.
                score_field_name = candidate_score_field_name(field_name)

                # EN: We convert the returned score into float once.
                # TR: Dönen skoru bir kez float'a çeviriyoruz.
                match_score = float(hit.match_score)

                # EN: We keep the best score seen for that field.
                # TR: O alan için görülen en iyi skoru koruyoruz.
                candidate[score_field_name] = max(float(candidate[score_field_name]), match_score)

                # EN: We keep a unique sorted language list.
                # TR: Tekilleştirilmiş ve sıralı dil listesini koruyoruz.
                candidate["matched_lang_codes"] = sorted(
                    set(candidate["matched_lang_codes"]) | {hit.lang_code}
                )

                # EN: We keep a unique field list.
                # TR: Tekilleştirilmiş alan listesini koruyoruz.
                if field_name not in candidate["matched_fields"]:
                    candidate["matched_fields"].append(field_name)

                # EN: We append the concrete query-evidence item.
                # TR: Somut sorgu-evidence öğesini ekliyoruz.
                candidate["matched_queries"].append(
                    {
                        "field_name": field_name,
                        "query_text": query_text,
                        "matched_surface": hit.matched_surface,
                        "matched_text": hit.matched_text,
                        "match_score": match_score,
                        "lang_code": hit.lang_code,
                    }
                )

                # EN: We increase the explicit evidence counter.
                # TR: Açık evidence sayacını artırıyoruz.
                candidate["evidence_count"] = int(candidate["evidence_count"]) + 1

                # EN: We keep track of matched surfaces in metadata.
                # TR: Eşleşen yüzeyleri metadata içinde takip ediyoruz.
                candidate["candidate_metadata"]["matched_surfaces"] = sorted(
                    set(candidate["candidate_metadata"]["matched_surfaces"]) | {hit.matched_surface}
                )

                # EN: We keep track of matched texts in metadata without duplication.
                # TR: Eşleşen metinleri metadata içinde tekrar olmadan takip ediyoruz.
                if hit.matched_text not in candidate["candidate_metadata"]["matched_texts"]:
                    candidate["candidate_metadata"]["matched_texts"].append(hit.matched_text)

                # EN: We recompute total_score from the explicit score columns only.
                # TR: total_score değerini yalnızca açık skor sütunlarından yeniden hesaplıyoruz.
                candidate["total_score"] = round(
                    float(candidate["url_score"])
                    + float(candidate["title_score"])
                    + float(candidate["h1_score"])
                    + float(candidate["breadcrumb_score"])
                    + float(candidate["structured_data_score"])
                    + float(candidate["anchor_score"])
                    + float(candidate["body_score"]),
                    4,
                )

        # EN: We rank aggregated candidates by descending total_score and then by node code.
        # TR: Toplanmış candidate'leri azalan total_score ve sonra node code ile sıralıyoruz.
        ranked_candidates = sorted(
            candidate_map.values(),
            key=lambda item: (-float(item["total_score"]), item["taxonomy_node_code"]),
        )[:max_candidates]

        # EN: We assign the final confidence band after sorting.
        # TR: Son confidence band değerini sıralama sonrası atıyoruz.
        for candidate in ranked_candidates:
            candidate["confidence_band"] = confidence_band_for_score(float(candidate["total_score"]))

        # EN: We return the ranked candidate list.
        # TR: Sıralanmış candidate listesini döndürüyoruz.
        return ranked_candidates

    finally:
        # EN: We always close the second taxonomy connection explicitly.
        # TR: İkinci taxonomy bağlantısını her durumda açık biçimde kapatıyoruz.
        taxonomy_conn.close()


# EN: This helper builds the compact candidate summary stored in the preranking
# EN: snapshot row.
# TR: Bu yardımcı, preranking snapshot satırında saklanan kompakt candidate
# TR: özetini kurar.
def build_preranking_candidate_summary(candidates: list[dict]) -> list[dict]:
    # EN: We keep the summary intentionally small and top-ranked only.
    # TR: Özeti bilinçli olarak küçük ve yalnızca en üst sıralı adaylarla tutuyoruz.
    return [
        {
            "taxonomy_node_code": candidate["taxonomy_node_code"],
            "taxonomy_concept_key": candidate["taxonomy_concept_key"],
            "domain_type": candidate["domain_type"],
            "node_kind": candidate["node_kind"],
            "matched_lang_codes": candidate["matched_lang_codes"],
            "matched_fields": candidate["matched_fields"],
            "total_score": candidate["total_score"],
            "confidence_band": candidate["confidence_band"],
        }
        for candidate in candidates[:5]
    ]




# EN: This helper extracts raw href attribute values from HTML in a deliberately
# EN: narrow stdlib-only way.
# TR: Bu yardımcı HTML içindeki ham href değerlerini bilinçli olarak dar ve
# TR: yalnızca stdlib kullanan bir yöntemle çıkarır.
def extract_candidate_hrefs_from_html(html_text: str) -> list[str]:
    # EN: We collect href values in encounter order first.
    # TR: Önce href değerlerini karşılaşılma sırasıyla topluyoruz.
    hrefs: list[str] = []

    # EN: We scan for simple quoted href attributes because the first discovery
    # EN: bridge should stay easy to audit.
    # TR: İlk discovery köprüsü kolay denetlenebilir kalsın diye basit tırnaklı
    # TR: href niteliklerini tarıyoruz.
    for match in re.finditer(r'href\s*=\s*["\']([^"\']+)["\']', html_text, flags=re.IGNORECASE):
        href_value = match.group(1).strip()
        if href_value:
            hrefs.append(href_value)

    # EN: We return the raw href list.
    # TR: Ham href listesini döndürüyoruz.
    return hrefs


# EN: This helper normalizes one discovered href against a base URL and keeps the
# EN: first bridge conservative by allowing only same-authority http/https links.
# TR: Bu yardımcı keşfedilmiş tek bir href değerini base URL'ye göre normalize eder
# TR: ve ilk köprüyü muhafazakâr tutmak için yalnızca aynı authority'deki
# TR: http/https linklere izin verir.
def normalize_discovered_href(base_url: str, href_value: str) -> str | None:
    # EN: Empty href values are ignored explicitly.
    # TR: Boş href değerleri açık biçimde yok sayılır.
    if not href_value:
        return None

    # EN: These schemes are intentionally out of scope for the first minimal bridge.
    # TR: Bu şemalar ilk minimal köprü için bilinçli olarak kapsam dışıdır.
    lowered = href_value.strip().lower()
    if lowered.startswith(("javascript:", "mailto:", "tel:", "data:", "#")):
        return None

    # EN: We resolve relative links against the parent canonical URL.
    # TR: Göreli linkleri parent kanonik URL'ye göre çözüyoruz.
    joined = urljoin(base_url, href_value.strip())

    # EN: We remove fragments because frontier truth should not duplicate the same
    # EN: resource only due to a fragment.
    # TR: Frontier doğrusu yalnızca fragment yüzünden aynı kaynağı çoğaltmamalıdır;
    # TR: bu yüzden fragment'i kaldırıyoruz.
    parts = urlsplit(joined)
    if parts.scheme.lower() not in {"http", "https"}:
        return None

    base_parts = urlsplit(base_url)

    # EN: The first bridge stays deliberately narrow: only same-authority links.
    # TR: İlk köprü bilinçli olarak dar kalır: yalnızca aynı authority linkleri.
    if parts.netloc.lower() != base_parts.netloc.lower():
        return None

    normalized_path = parts.path or "/"
    normalized = urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            normalized_path,
            parts.query,
            "",
        )
    )

    # EN: We return the normalized discovered URL.
    # TR: Normalize edilmiş keşif URL'sini döndürüyoruz.
    return normalized


# EN: This helper builds a small unique list of normalized discovery targets.
# TR: Bu yardımcı normalize edilmiş discovery hedeflerinden küçük ve tekilleşmiş
# TR: bir liste kurar.
def build_minimal_discovery_targets(*, base_url: str, html_text: str, limit: int = 25) -> list[str]:
    # EN: We extract raw href values first.
    # TR: Önce ham href değerlerini çıkarıyoruz.
    raw_hrefs = extract_candidate_hrefs_from_html(html_text)

    # EN: We keep unique normalized URLs in encounter order.
    # TR: Tekilleştirilmiş normalize URL'leri karşılaşılma sırasıyla koruyoruz.
    normalized_urls: list[str] = []
    seen: set[str] = set()

    for href_value in raw_hrefs:
        normalized = normalize_discovered_href(base_url, href_value)
        if normalized is None:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        normalized_urls.append(normalized)
        if len(normalized_urls) >= limit:
            break

    # EN: We return the final limited target list.
    # TR: Son sınırlı hedef listesini döndürüyoruz.
    return normalized_urls


# EN: This helper performs the minimal HTML-link discovery enqueue bridge inside
# EN: the current parse transaction.
# TR: Bu yardımcı, mevcut parse transaction'ı içinde minimal HTML-link discovery
# TR: enqueue köprüsünü çalıştırır.
def enqueue_minimal_discovered_links(
    *,
    conn,
    url_id: int,
    raw_storage_path: str,
    source_run_id: str,
    source_note: str | None = None,
    limit: int = 25,
) -> dict:
    # EN: We first read the durable parent URL context from the DB.
    # TR: Önce kalıcı parent URL bağlamını DB'den okuyoruz.
    parent_context = fetch_url_discovery_context(
        conn,
        url_id=url_id,
    )
    if parent_context is None:
        raise RuntimeError("fetch_url_discovery_context(...) returned no row")

    # EN: We read the raw HTML body from disk because discovery should use the same
    # EN: fetched artefact that parse already trusts.
    # TR: Discovery, parse'ın zaten güvendiği aynı fetch artefact'ını kullansın diye
    # TR: ham HTML body'yi diskten okuyoruz.
    html_text = read_raw_body_text(raw_storage_path)

    # EN: We build a conservative list of discovery targets.
    # TR: Muhafazakâr discovery hedefleri listesi kuruyoruz.
    discovery_targets = build_minimal_discovery_targets(
        base_url=str(parent_context["canonical_url"]),
        html_text=html_text,
        limit=limit,
    )

    # EN: We prepare the result accumulator.
    # TR: Sonuç biriktiricisini hazırlıyoruz.
    enqueued_rows: list[dict] = []

    for discovered_url in discovery_targets:
        parts = urlsplit(discovered_url)
        scheme = parts.scheme.lower()
        host = (parts.hostname or "").lower()
        port = parts.port or (443 if scheme == "https" else 80)
        authority_key = f"{host}:{port}"
        url_path = parts.path or "/"
        url_query = parts.query or None

        enqueue_row = enqueue_discovered_url(
            conn,
            parent_url_id=int(url_id),
            canonical_url=discovered_url,
            canonical_url_sha256=hashlib.sha256(discovered_url.encode("utf-8")).hexdigest(),
            port=port,
            scheme=scheme,
            host=host,
            authority_key=authority_key,
            registrable_domain=host,
            url_path=url_path,
            url_query=url_query,
            discovery_type="html_link",
            depth=int(parent_context["depth"]) + 1,
            priority=max(int(parent_context["priority"]) - 5, 1),
            enqueue_reason="minimal_html_link_discovery_from_parse_runtime",
        )

        if enqueue_row is not None:
            enqueued_rows.append(dict(enqueue_row))

    # EN: We return one explicit structured discovery result.
    # TR: Açık ve yapılı tek bir discovery sonucu döndürüyoruz.
    return {
        "parent_url_id": int(url_id),
        "discovered_href_count": len(extract_candidate_hrefs_from_html(html_text)),
        "normalized_url_count": len(discovery_targets),
        "enqueued_url_count": len(enqueued_rows),
        "skipped_url_count": len(extract_candidate_hrefs_from_html(html_text)) - len(discovery_targets),
        "enqueued_rows": enqueued_rows,
    }


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

    # EN: We run the minimal HTML-link discovery enqueue bridge before final
    # EN: workflow state is written, so the same transaction can carry both parse
    # EN: and discovery side effects.
    # TR: Son workflow durumu yazılmadan önce minimal HTML-link discovery enqueue
    # TR: köprüsünü çalıştırıyoruz; böylece aynı transaction hem parse hem discovery
    # TR: yan etkilerini taşıyabilir.
    discovery_result = enqueue_minimal_discovered_links(
        conn=conn,
        url_id=url_id,
        raw_storage_path=raw_storage_path,
        source_run_id=source_run_id,
        source_note=source_note,
    )

    # EN: We build minimal taxonomy candidates through the already-proven runtime
    # EN: taxonomy helper and its second database connection.
    # TR: Minimal taxonomy candidate'lerini, zaten kanıtlanmış runtime taxonomy
    # TR: helper'ı ve onun ikinci veritabanı bağlantısı üzerinden kuruyoruz.
    taxonomy_candidates = build_minimal_taxonomy_candidates(
        parse_result=parse_result,
        source_run_id=source_run_id,
        source_note=source_note,
    )

    # EN: We enrich the persisted payload in-memory before the DB call so the
    # EN: parse SQL layer receives real candidates instead of an always-empty list.
    # TR: Veritabanı çağrısından önce persist edilecek payload'ı bellekte
    # TR: zenginleştiriyoruz; böylece parse SQL katmanı sürekli boş liste yerine
    # TR: gerçek candidate'ler alır.
    payload = dict(parse_result.payload)
    payload["candidates"] = taxonomy_candidates
    payload["metadata"] = {
        "taxonomy_package_version": minimal_taxonomy_package_version(),
        "taxonomy_candidate_count": len(taxonomy_candidates),
        "taxonomy_bridge": "repo_helper_v1",
    }

    # EN: We persist evidence and candidate rows through the existing canonical
    # EN: payload helper.
    # TR: Evidence ve candidate satırlarını mevcut kanonik payload helper'ı
    # TR: üzerinden persist ediyoruz.
    persist_result = persist_taxonomy_preranking_payload(
        conn=conn,
        payload=payload,
    )

    # EN: We now create the real preranking snapshot row through the dedicated DB
    # EN: wrapper that was already present in SQL but not yet bridged in Python.
    # TR: Artık gerçek preranking snapshot satırını, SQL tarafında zaten var olup
    # TR: Python'da henüz köprülenmemiş dedicated DB wrapper üzerinden oluşturuyoruz.
    top_score = None
    if taxonomy_candidates:
        top_score = float(taxonomy_candidates[0]["total_score"])

    # EN: pre_ranked is now allowed only when at least one taxonomy candidate exists.
    # EN: Otherwise we intentionally fall back to review_hold.
    # TR: pre_ranked artık yalnızca en az bir taxonomy candidate varsa mümkündür.
    # TR: Aksi durumda bilinçli olarak review_hold durumuna düşüyoruz.
    effective_workflow_state = workflow_state
    effective_workflow_state_reason = workflow_state_reason

    if workflow_state == "pre_ranked":
        if taxonomy_candidates:
            effective_workflow_state = "pre_ranked"
            effective_workflow_state_reason = "taxonomy_candidates_persisted_via_repo_helper"
        else:
            effective_workflow_state = "review_hold"
            effective_workflow_state_reason = "taxonomy_candidates_empty_manual_review_required"

    preranking_snapshot_result = persist_page_preranking_snapshot(
        conn=conn,
        url_id=url_id,
        input_lang_code=parse_result.input_lang_code,
        taxonomy_package_version=minimal_taxonomy_package_version(),
        top_candidate_count=len(taxonomy_candidates),
        top_score=top_score,
        candidate_summary=build_preranking_candidate_summary(taxonomy_candidates),
        snapshot_metadata={
            "taxonomy_package_version": minimal_taxonomy_package_version(),
            "taxonomy_candidate_count": len(taxonomy_candidates),
            "persisted_candidate_count": persist_result["persisted_candidate_count"],
            "taxonomy_bridge": "repo_helper_v1",
        },
        source_run_id=source_run_id,
        source_note=source_note,
        review_status=effective_workflow_state,
    )

    # EN: The workflow row must now link to the real preranking snapshot row,
    # EN: not to the evidence snapshot placeholder.
    # TR: Workflow satırı artık evidence snapshot placeholder'ına değil,
    # TR: gerçek preranking snapshot satırına bağlanmalıdır.
    linked_snapshot_id = preranking_snapshot_result["snapshot_id"]

    # EN: We write workflow state through the canonical DB helper and use the real
    # EN: preranking snapshot id.
    # TR: Workflow durumunu kanonik DB helper üzerinden yazıyor ve gerçek
    # TR: preranking snapshot id değerini kullanıyoruz.
    workflow_result = upsert_page_workflow_status(
        conn=conn,
        url_id=url_id,
        workflow_state=effective_workflow_state,
        state_reason=effective_workflow_state_reason,
        linked_snapshot_id=linked_snapshot_id,
        source_run_id=source_run_id,
        source_note=source_note,
        status_metadata={
            "parse_mode": "minimal_stdlib_html",
            "linked_snapshot_policy": "preranking_snapshot_only",
            "linked_snapshot_id": linked_snapshot_id,
            "raw_storage_path": raw_storage_path,
            "taxonomy_package_version": minimal_taxonomy_package_version(),
            "taxonomy_candidate_count": len(taxonomy_candidates),
            "persisted_candidate_count": persist_result["persisted_candidate_count"],
        },
    )

    # EN: We return all durable DB results together so callers can audit exactly
    # EN: what the parse apply step changed.
    # TR: Çağıran taraf parse apply adımının tam olarak neyi değiştirdiğini audit
    # TR: edebilsin diye tüm kalıcı DB sonuçlarını birlikte döndürüyoruz.
    return MinimalParseApplyResult(
        persist_result=persist_result,
        preranking_snapshot_result=preranking_snapshot_result,
        discovery_result=discovery_result,
        workflow_result=workflow_result,
    )
