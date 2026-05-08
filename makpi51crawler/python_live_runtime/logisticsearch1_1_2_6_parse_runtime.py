"""
EN:
This file is the parse-runtime child of the worker-runtime family.

EN:
Why this file exists:
- because parse-specific runtime truth should live in one explicit child instead of being hidden inside the main worker hub
- because fetched_page, page_contract_validation, parse_apply_result, taxonomy-facing payloads, candidate shaping, and preranking handoff meaning must remain readable
- because a beginner should be able to find where raw fetched page material stops being only acquisition output and starts becoming structured parse-layer meaning

EN:
What this file DOES:
- expose parse-oriented runtime helper, class, and payload boundaries
- preserve visible parse_apply, validation, extraction, taxonomy-handoff, and degraded branch meaning
- keep parse semantics separate from broader worker orchestration, lease handling, robots policy, and terminal fetch finalization

EN:
What this file DOES NOT do:
- it does not become the full worker orchestrator
- it does not own all acquisition logic
- it does not own all storage-routing logic
- it does not become the taxonomy authority by itself

EN:
Topological role:
- acquisition and fetch-finalize related surfaces produce inputs that can feed this file
- this file turns fetched page material into parse-layer evidence, normalized payloads, taxonomy-facing structures, and downstream handoff meaning
- taxonomy and storage layers sit after this file or consume the explicit outputs shaped here

EN:
Important visible values and shapes:
- fetched_page => the page-level payload entering parse logic
- page_contract_validation => whether fetched_page satisfies the expected parse-side contract
- parse_apply_result => visible parse-layer result package
- taxonomy-oriented payloads => structures forwarded toward taxonomy/runtime application
- candidate/evidence/preranking related payloads => structured parse outputs for later layers
- degraded branch payloads => explicit non-happy parse outcomes that must remain readable

EN:
Accepted architectural identity:
- worker parse runtime child
- narrow parse contract layer
- readable parse/evidence/taxonomy-handoff boundary

EN:
Undesired architectural identity:
- hidden second worker hub
- vague extraction utility dump
- hidden SQL engine
- hidden operator CLI surface

TR:
Bu dosya worker-runtime ailesinin parse-runtime child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü parsee özgü runtime doğrusu ana worker hubının içinde gizlenmek yerine tek ve açık child yüzeyde yaşamalıdır
- çünkü fetched_page, page_contract_validation, parse_apply_result, taxonomyye bakan payloadlar, candidate shaping ve preranking handoff anlamı okunabilir kalmalıdır
- çünkü yeni başlayan biri ham fetched page malzemesinin nerede yalnızca acquisition çıktısı olmaktan çıkıp yapılı parse katmanı anlamına dönüştüğünü bulabilmelidir

TR:
Bu dosya NE yapar:
- parse odaklı runtime helper, class ve payload sınırlarını açığa çıkarır
- parse_apply, validation, extraction, taxonomy-handoff ve degraded dal anlamını görünür tutar
- parse semantiklerini daha geniş worker orkestrasyonundan, lease yönetiminden, robots policy mantığından ve terminal fetch finalization mantığından ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam worker orchestratorun kendisi olmaz
- tüm acquisition mantığının sahibi değildir
- tüm storage-routing mantığının sahibi değildir
- taxonomy authoritynin tek başına kendisi olmaz

TR:
Topolojik rol:
- acquisition ve fetch-finalize ile ilgili yüzeyler bu dosyaya girebilen girdileri üretir
- bu dosya fetched page malzemesini parse katmanı evidence, normalized payload, taxonomyye bakan yapı ve downstream handoff anlamına dönüştürür
- taxonomy ve storage katmanları bu dosyadan sonra gelir veya burada şekillenen açık çıktıları tüketir

TR:
Önemli görünür değerler ve şekiller:
- fetched_page => parse mantığına giren page-level payload
- page_contract_validation => fetched_pagein beklenen parse-side sözleşmeyi sağlayıp sağlamadığı
- parse_apply_result => görünür parse katmanı sonuç paketi
- taxonomy odaklı payloadlar => taxonomy/runtime uygulamasına devredilen yapılar
- candidate/evidence/preranking ile ilgili payloadlar => sonraki katmanlar için yapılı parse çıktıları
- degraded dal payloadları => okunabilir kalması gereken mutlu-yol-dışı parse sonuçları

TR:
Kabul edilen mimari kimlik:
- worker parse runtime child
- dar parse sözleşme katmanı
- okunabilir parse/evidence/taxonomy-handoff sınırı

TR:
İstenmeyen mimari kimlik:
- gizli ikinci worker hubı
- belirsiz extraction utility çöplüğü
- gizli SQL motoru
- gizli operatör CLI yüzeyi
"""

# EN: We enable postponed evaluation of annotations so type hints stay readable
# EN: even when they refer to classes declared later in the file.
# TR: Type hint'ler dosyada daha sonra tanımlanan sınıflara referans verse bile
# TR: okunabilir kalsın diye annotation çözümlemesini erteliyoruz.
# EN: PARSE RUNTIME IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the narrow parse corner of the worker corridor.
# EN: Beginner mental model:
# EN: - acquisition gets material
# EN: - fetch finalization closes the attempt side
# EN: - this file explains how usable meaning is extracted from page material
# EN: - it exists so the crawler can later answer: what was parsed, what was validated, what was extracted, what was handed toward taxonomy or later scoring layers
# EN:
# EN: Accepted architectural meaning:
# EN: - named parse-runtime child
# EN: - focused parse/evidence/validation helper surface
# EN: - readable boundary for raw page material becoming structured parse meaning
# EN:
# EN: Undesired architectural meaning:
# EN: - random extraction helper pile
# EN: - hidden second orchestrator
# EN: - place where validation or parse failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - fetched_page should stay explicit
# EN: - parse validation and apply results should stay structured and readable
# EN: - degraded parse branches must remain visible
# TR: PARSE RUNTIME KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya worker koridorunun dar parse köşesi gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - acquisition malzemeyi alır
# TR: - fetch finalization attempt tarafını kapatır
# TR: - bu dosya page malzemesinden kullanılabilir anlamın nasıl çıkarıldığını açıklar
# TR: - crawlerın daha sonra şu sorulara cevap verebilmesi için vardır: ne parse edildi, ne doğrulandı, ne çıkarıldı, ne taxonomyye veya sonraki scoring katmanlarına devredildi
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli parse-runtime child
# TR: - odaklı parse/evidence/validation yardımcı yüzeyi
# TR: - ham page malzemesinin yapılı parse anlamına dönüşmesi için okunabilir sınır
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele extraction helper yığını
# TR: - gizli ikinci orchestrator
# TR: - validation veya parse hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - fetched_page açık kalmalıdır
# TR: - parse validation ve apply sonuçları yapılı ve okunabilir kalmalıdır
# TR: - degraded parse dalları görünür kalmalıdır

from __future__ import annotations

from .logisticsearch1_1_1_3_frontier_gateway import update_url_crawl_map_metadata

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

from .logisticsearch1_1_2_6_1_taxonomy_runtime import (
    CANONICAL_LANGUAGE_ORDER,
    connect_taxonomy_db,
    search_runtime_taxonomy,
    taxonomy_default_dsn,
)

# EN: This set gives parse_runtime the same canonical 25-language acceptance
# EN: boundary used by taxonomy authority and runtime lookup surfaces.
# TR: Bu küme parse_runtime katmanına taxonomy otoritesi ve runtime lookup
# TR: yüzeyleriyle aynı kanonik 25 dil kabul sınırını verir.
CANONICAL_LANGUAGE_SET = frozenset(CANONICAL_LANGUAGE_ORDER)




# EN: This dataclass stores the structured result of the minimal parse entry step.
# TR: Bu dataclass minimal parse giriş adımının yapılı sonucunu tutar.
@dataclass(slots=True)
# EN: PARSE CLASS PURPOSE MEMORY BLOCK V6 / MinimalParseResult
# EN:
# EN: Why this class exists:
# EN: - because parse-layer truth for 'MinimalParseResult' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand parse-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named parse payload, validation shape, or structured result carrier
# EN: - visible field set currently detected here: url_id, raw_storage_path, input_lang_code, page_title, body_text, payload
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely deals with parse application, contract validation, or parse-result visibility
# EN: - explicit success vs degraded parse meaning may matter here
# EN: - these helpers often define whether later taxonomy/storage layers receive usable payloads
# EN: - visible validation vs rejection distinction is especially important here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no parse contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: PARSE CLASS AMAÇ HAFIZA BLOĞU V6 / MinimalParseResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'MinimalParseResult' için parse katmanı doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip parse tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse payloadı, validation şekli veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: url_id, raw_storage_path, input_lang_code, page_title, body_text, payload
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle parse uygulaması, contract validation veya parse-result görünürlüğü ile ilgilenir
# TR: - açık success vs degraded parse anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki taxonomy/storage katmanlarının kullanılabilir payload alıp almayacağını belirler
# TR: - görünür validation vs rejection ayrımı burada özellikle önemlidir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı parse sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

# EN: PARSE RUNTIME CLASS PURPOSE MEMORY BLOCK V7 / MinimalParseResult
# EN:
# EN: Why this class exists:
# EN: - because parse runtime should carry structured meaning through a named class instead of anonymous dict drift
# EN: - because later taxonomy, preranking, discovery, workflow, and audit surfaces need readable stable field meaning
# EN:
# EN: Accepted role:
# EN: - named parse-runtime class contract
# EN:
# EN: Important contract reminder:
# EN: - this class belongs to the narrow parse-runtime layer and should keep parse-side meaning explicit
# TR: PARSE RUNTIME CLASS AMAÇ HAFIZA BLOĞU V7 / MinimalParseResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü parse runtime anlamı anonim dict dağılması yerine isimli sınıf ile taşınmalıdır
# TR: - çünkü sonraki taxonomy, preranking, discovery, workflow ve denetim yüzeyleri okunabilir ve kararlı alan anlamına ihtiyaç duyar
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime sınıf sözleşmesi
# TR:
# TR: Önemli sözleşme hatırlatması:
# TR: - bu sınıf dar parse-runtime katmanına aittir ve parse-side anlamı açık tutmalıdır
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / normalize_whitespace
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'normalize_whitespace' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: text
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / normalize_whitespace
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'normalize_whitespace' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: text
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / normalize_whitespace
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - text => explicit parse-runtime input parameter of normalize_whitespace; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / normalize_whitespace
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - text => normalize_whitespace fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def normalize_whitespace(text: str) -> str:
    # EN: We collapse all whitespace runs into a single plain space.
    # TR: Tüm boşluk kümelerini tek sade boşluğa indiriyoruz.
    return re.sub(r"\s+", " ", text).strip()


# EN: This helper reads a raw fetch artefact as UTF-8 with replacement so the
# EN: first parse layer never crashes on imperfect byte sequences.
# TR: Bu yardımcı ham fetch artefact'ını replacement ile UTF-8 olarak okur;
# TR: böylece ilk parse katmanı kusurlu byte dizilerinde çökmez.
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / read_raw_body_text
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'read_raw_body_text' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: raw_storage_path
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / read_raw_body_text
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'read_raw_body_text' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: raw_storage_path
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / read_raw_body_text
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - raw_storage_path => explicit parse-runtime input parameter of read_raw_body_text; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / read_raw_body_text
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - raw_storage_path => read_raw_body_text fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def read_raw_body_text(raw_storage_path: str) -> str:
    # EN: We create a Path object first because file inspection is clearer with pathlib.
    # TR: Dosya incelemesi pathlib ile daha açık olduğu için önce Path nesnesi oluşturuyoruz.
    # EN: path is the pathlib wrapper built from raw_storage_path for file existence checks and later disk reads.
    # EN: Expected values are concrete artefact file paths; non-file values are rejected by the next branch.
    # TR: path, dosya varlık kontrolleri ve sonraki disk okumaları için raw_storage_path değerinden üretilen pathlib sarmalayıcısıdır.
    # TR: Beklenen değerler somut artefact dosya yollarıdır; dosya olmayan değerler bir sonraki dalda reddedilir.
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / extract_title_from_html
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'extract_title_from_html' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: html_text
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / extract_title_from_html
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'extract_title_from_html' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: html_text
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / extract_title_from_html
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - html_text => explicit parse-runtime input parameter of extract_title_from_html; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / extract_title_from_html
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - html_text => extract_title_from_html fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def extract_title_from_html(html_text: str) -> str | None:
    # EN: We search case-insensitively and across newlines because title tags may
    # EN: be formatted in different styles.
    # TR: Title etiketleri farklı biçimlerde yazılabildiği için büyük-küçük harf
    # TR: duyarsız ve satırlar arası arama yapıyoruz.
    # EN: match stores the regex search result for the current HTML/text inspection step.
    # EN: Expected values are a regex match object or None when the searched structure is absent.
    # TR: match, mevcut HTML/metin inceleme adımı için regex arama sonucunu taşır.
    # TR: Beklenen değerler regex match nesnesi veya aranan yapı yoksa Nonedir.
    match = re.search(r"<title[^>]*>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)

    # EN: If there is no title tag, we return None explicitly.
    # TR: Title etiketi yoksa açık biçimde None döndürüyoruz.
    if match is None:
        return None

    # EN: We unescape HTML entities and normalize whitespace so the title is ready
    # EN: for later evidence storage.
    # TR: Başlık daha sonra evidence saklamaya hazır olsun diye HTML entity'leri
    # TR: çözüyor ve boşlukları normalize ediyoruz.
    # EN: title_text stores the extracted human-readable title string before and after normalization.
    # EN: Expected values are readable title text or an empty string that later guards can reject.
    # TR: title_text, normalize öncesi ve sonrası çıkarılmış insan-okur başlık metnini taşır.
    # TR: Beklenen değerler okunur başlık metni veya sonraki korumaların reddedebileceği boş stringdir.
    title_text = html.unescape(match.group(1))
    # EN: title_text now stores the whitespace-normalized human title string.
    # EN: Expected values are readable non-empty title text or an empty string that the next branch will reject.
    # TR: title_text artık boşlukları normalize edilmiş insan-okur başlık metnini taşır.
    # TR: Beklenen değerler okunur boş olmayan başlık metni veya bir sonraki dalın reddedeceği boş stringdir.
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / infer_input_lang_code
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'infer_input_lang_code' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: html_text
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / infer_input_lang_code
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'infer_input_lang_code' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: html_text
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / infer_input_lang_code
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - html_text => explicit parse-runtime input parameter of infer_input_lang_code; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / infer_input_lang_code
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - html_text => infer_input_lang_code fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def infer_input_lang_code(html_text: str) -> str:
    # EN: We first inspect the root <html lang=...> marker because it is the
    # EN: simplest first language signal available in minimal parse.
    # TR: Önce kök <html lang=...> işaretine bakıyoruz; çünkü minimal parse içinde
    # TR: eldeki en basit ilk dil sinyali budur.
    # EN: match stores the regex search result for the current HTML/text inspection step.
    # EN: Expected values are a regex match object or None when the searched structure is absent.
    # TR: match, mevcut HTML/metin inceleme adımı için regex arama sonucunu taşır.
    # TR: Beklenen değerler regex match nesnesi veya aranan yapı yoksa Nonedir.
    match = re.search(
        r'<html[^>]*\blang\s*=\s*["\']?([a-zA-Z-]+)',
        html_text,
        flags=re.IGNORECASE,
    )

    # EN: If a language marker exists, we normalize it to the primary two-letter
    # EN: stem before checking canonical membership.
    # TR: Bir dil işareti varsa onu önce birincil iki harfli köke normalize edip
    # TR: sonra kanonik üyeliğini kontrol ediyoruz.
    if match:
        # EN: candidate stores the primary language stem extracted from the HTML lang marker.
        # EN: Expected values are canonical 25-language codes or temporary stems that the next membership check may reject.
        # TR: candidate HTML lang işaretinden çıkarılan birincil dil kökünü taşır.
        # TR: Beklenen değerler kanonik 25 dil kodları veya bir sonraki üyelik kontrolünün reddedebileceği geçici köklerdir.
        candidate = match.group(1).strip().lower().split("-", 1)[0]

        # EN: Only canonical 25-language codes are allowed to flow forward as
        # EN: concrete language truth from this first parse layer.
        # TR: Bu ilk parse katmanından ileriye yalnızca kanonik 25 dil kodları
        # TR: somut dil doğrusu olarak akabilir.
        if candidate in CANONICAL_LANGUAGE_SET:
            return candidate

    # EN: If no canonical language marker exists, we use "und" for undetermined.
    # TR: Kanonik bir dil işareti yoksa belirsiz anlamında "und" kullanıyoruz.
    return "und"

# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / extract_visible_text_from_html
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'extract_visible_text_from_html' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: html_text
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / extract_visible_text_from_html
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'extract_visible_text_from_html' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: html_text
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / extract_visible_text_from_html
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - html_text => explicit parse-runtime input parameter of extract_visible_text_from_html; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / extract_visible_text_from_html
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - html_text => extract_visible_text_from_html fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def extract_visible_text_from_html(html_text: str) -> str:
    # EN: We remove script blocks first because JavaScript is not page meaning.
    # TR: JavaScript sayfa anlamı olmadığı için önce script bloklarını kaldırıyoruz.
    # EN: without_script stores the HTML after script blocks are removed so non-content code does not pollute parsing.
    # EN: Expected values are HTML-like text with script regions replaced by spaces.
    # TR: without_script, script blokları çıkarıldıktan sonraki HTML metnini taşır; böylece içerik dışı kod parse sonucunu kirletmez.
    # TR: Beklenen değerler script bölgeleri boşlukla değiştirilmiş HTML-benzeri metindir.
    without_script = re.sub(
        r"<script\b[^>]*>.*?</script>",
        " ",
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # EN: We remove style blocks second because CSS is not page meaning either.
    # TR: CSS de sayfa anlamı olmadığı için ikinci olarak style bloklarını kaldırıyoruz.
    # EN: without_style stores the HTML after style blocks are removed so CSS does not appear as visible page text.
    # EN: Expected values are HTML-like text with style regions stripped out.
    # TR: without_style, style blokları çıkarıldıktan sonraki HTML metnini taşır; böylece CSS görünür sayfa metni gibi davranmaz.
    # TR: Beklenen değerler style bölgeleri temizlenmiş HTML-benzeri metindir.
    without_style = re.sub(
        r"<style\b[^>]*>.*?</style>",
        " ",
        without_script,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # EN: We replace all remaining tags with spaces to keep visible text boundaries.
    # TR: Görünür metin sınırları korunsun diye kalan tüm etiketleri boşlukla değiştiriyoruz.
    # EN: without_tags stores the intermediate text where remaining HTML tags were replaced by spaces.
    # EN: Expected values are tag-free text that still may contain HTML entities.
    # TR: without_tags, kalan HTML etiketleri boşlukla değiştirildikten sonraki ara metni taşır.
    # TR: Beklenen değerler etiketsiz ama hâlâ HTML entity içerebilen metindir.
    without_tags = re.sub(r"<[^>]+>", " ", without_style)

    # EN: We decode HTML entities because text should be stored in human-readable form.
    # TR: Metin insan-okunur biçimde saklansın diye HTML entity'leri çözüyoruz.
    # EN: unescaped stores the entity-decoded visible text before final whitespace normalization.
    # EN: Expected values are human-readable text fragments that may still contain uneven spacing.
    # TR: unescaped, son boşluk normalizasyonundan önce entity çözülmüş görünür metni taşır.
    # TR: Beklenen değerler insan-okur metin parçalarıdır; bunlar hâlâ düzensiz boşluk içerebilir.
    unescaped = html.unescape(without_tags)

    # EN: We normalize whitespace and return the final simplified visible text.
    # TR: Boşlukları normalize edip son sade görünür metni döndürüyoruz.
    return normalize_whitespace(unescaped)


# EN: This helper builds one small evidence item for a textual field.
# TR: Bu yardımcı metinsel bir alan için küçük bir evidence öğesi üretir.
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / build_query_item
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'build_query_item' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: query_text, field_name
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_query_item
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_query_item' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: query_text, field_name
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / build_query_item
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - query_text => explicit parse-runtime input parameter of build_query_item; this value is part of the visible contract of this function
# EN: - field_name => explicit parse-runtime input parameter of build_query_item; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_query_item
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - query_text => build_query_item fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - field_name => build_query_item fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / build_minimal_parse_payload
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'build_minimal_parse_payload' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: url_id, raw_storage_path, source_run_id, source_note
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely deals with parse application, contract validation, or parse-result visibility
# EN: - explicit success vs degraded parse meaning may matter here
# EN: - these helpers often define whether later taxonomy/storage layers receive usable payloads
# EN: - visible validation vs rejection distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_minimal_parse_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_minimal_parse_payload' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: url_id, raw_storage_path, source_run_id, source_note
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle parse uygulaması, contract validation veya parse-result görünürlüğü ile ilgilenir
# TR: - açık success vs degraded parse anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki taxonomy/storage katmanlarının kullanılabilir payload alıp almayacağını belirler
# TR: - görünür validation vs rejection ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / build_minimal_parse_payload
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - url_id => explicit parse-runtime input parameter of build_minimal_parse_payload; this value is part of the visible contract of this function
# EN: - raw_storage_path => explicit parse-runtime input parameter of build_minimal_parse_payload; this value is part of the visible contract of this function
# EN: - source_run_id => explicit parse-runtime input parameter of build_minimal_parse_payload; this value is part of the visible contract of this function
# EN: - source_note => explicit parse-runtime input parameter of build_minimal_parse_payload; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_minimal_parse_payload
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - url_id => build_minimal_parse_payload fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - raw_storage_path => build_minimal_parse_payload fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - source_run_id => build_minimal_parse_payload fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - source_note => build_minimal_parse_payload fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def build_minimal_parse_payload(
    *,
    url_id: int,
    raw_storage_path: str,
    source_run_id: str | None = None,
    source_note: str | None = None,
) -> MinimalParseResult:
    # EN: We read the raw HTML text first because all later parse signals depend on it.
    # TR: Sonraki tüm parse sinyalleri buna bağlı olduğu için önce ham HTML metnini okuyoruz.
    # EN: html_text stores the durable raw HTML text that the current parse step will inspect and transform.
    # EN: Expected values are decoded page HTML strings read from the controlled raw artefact.
    # TR: html_text, mevcut parse adımının inceleyip dönüştüreceği kalıcı ham HTML metnini taşır.
    # TR: Beklenen değerler kontrollü ham artefact'tan okunmuş decode edilmiş sayfa HTML stringleridir.
    html_text = read_raw_body_text(raw_storage_path)

    # EN: We extract the page title as a separate higher-value signal.
    # TR: Sayfa başlığını daha yüksek değerli ayrı bir sinyal olarak çıkarıyoruz.
    # EN: page_title stores the extracted title signal from the HTML surface.
    # EN: Expected values are a readable title string or None when no usable title exists.
    # TR: page_title, HTML yüzeyinden çıkarılan başlık sinyalini taşır.
    # TR: Beklenen değerler okunur başlık stringi veya kullanılabilir başlık yoksa Nonedir.
    page_title = extract_title_from_html(html_text)

    # EN: We extract visible body text as the first minimal body-content signal.
    # TR: Görünür body metnini ilk minimal body-içerik sinyali olarak çıkarıyoruz.
    # EN: body_text stores the simplified visible text extracted from the HTML body.
    # EN: Expected values are normalized visible text strings, possibly empty for sparse pages.
    # TR: body_text, HTML gövdesinden çıkarılan sadeleştirilmiş görünür metni taşır.
    # TR: Beklenen değerler normalize edilmiş görünür metin stringleridir; seyrek sayfalarda boş olabilir.
    body_text = extract_visible_text_from_html(html_text)

    # EN: We infer a best-effort language code from HTML metadata.
    # TR: HTML metadata üzerinden en iyi çaba dil kodu çıkarıyoruz.
    # EN: input_lang_code stores the best-effort language code inferred from the HTML surface.
    # EN: Expected values are short language codes such as en, tr, de, or the fallback unknown.
    # TR: input_lang_code, HTML yüzeyinden çıkarılan en iyi çaba dil kodunu taşır.
    # TR: Beklenen değerler en, tr, de gibi kısa dil kodları veya fallback unknown değeridir.
    input_lang_code = infer_input_lang_code(html_text)

    # EN: Title evidence contains one item only when a non-empty title exists.
    # TR: Title evidence yalnızca boş olmayan bir başlık varsa tek öğe içerir.
    # EN: title_queries collects title-derived taxonomy search inputs.
    # EN: Expected values are zero or more dict items ready for taxonomy lookup.
    # TR: title_queries, başlıktan türetilen taxonomy arama girdilerini toplar.
    # TR: Beklenen değerler taxonomy lookup için hazır sıfır veya daha fazla dict öğesidir.
    title_queries = []
    if page_title is not None:
        title_queries.append(build_query_item(query_text=page_title, field_name="title"))

    # EN: Body evidence is intentionally truncated so the first payload stays small,
    # EN: predictable, and easy to inspect.
    # TR: İlk payload küçük, öngörülebilir ve incelemesi kolay kalsın diye body
    # TR: evidence bilinçli olarak kısaltılır.
    # EN: body_excerpt stores the deliberately truncated first body-text slice used in the minimal parse payload.
    # EN: Expected values are short visible-text excerpts capped for predictable payload size.
    # TR: body_excerpt, minimal parse payload'ında kullanılan bilinçli olarak kısaltılmış ilk body-text parçasını taşır.
    # TR: Beklenen değerler öngörülebilir payload boyutu için üst sınırla kesilmiş kısa görünür metin alıntılarıdır.
    body_excerpt = body_text[:4000] if body_text else ""

    # EN: Body evidence contains one item only when the excerpt is non-empty.
    # TR: Body evidence yalnızca excerpt boş değilse tek öğe içerir.
    # EN: body_queries collects body-derived taxonomy search inputs.
    # EN: Expected values are zero or more dict items built from the visible body excerpt.
    # TR: body_queries, body metninden türetilen taxonomy arama girdilerini toplar.
    # TR: Beklenen değerler görünür body excerpt'ından üretilmiş sıfır veya daha fazla dict öğesidir.
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / resolve_workflow_linked_snapshot_id
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'resolve_workflow_linked_snapshot_id' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: persist_result
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / resolve_workflow_linked_snapshot_id
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'resolve_workflow_linked_snapshot_id' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: persist_result
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / resolve_workflow_linked_snapshot_id
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - persist_result => explicit parse-runtime input parameter of resolve_workflow_linked_snapshot_id; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / resolve_workflow_linked_snapshot_id
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - persist_result => resolve_workflow_linked_snapshot_id fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
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
# EN: PARSE CLASS PURPOSE MEMORY BLOCK V6 / MinimalParseApplyResult
# EN:
# EN: Why this class exists:
# EN: - because parse-layer truth for 'MinimalParseApplyResult' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand parse-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named parse payload, validation shape, or structured result carrier
# EN: - visible field set currently detected here: persist_result, preranking_snapshot_result, discovery_result, workflow_result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely deals with parse application, contract validation, or parse-result visibility
# EN: - explicit success vs degraded parse meaning may matter here
# EN: - these helpers often define whether later taxonomy/storage layers receive usable payloads
# EN: - visible validation vs rejection distinction is especially important here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no parse contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: PARSE CLASS AMAÇ HAFIZA BLOĞU V6 / MinimalParseApplyResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'MinimalParseApplyResult' için parse katmanı doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip parse tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse payloadı, validation şekli veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: persist_result, preranking_snapshot_result, discovery_result, workflow_result
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle parse uygulaması, contract validation veya parse-result görünürlüğü ile ilgilenir
# TR: - açık success vs degraded parse anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki taxonomy/storage katmanlarının kullanılabilir payload alıp almayacağını belirler
# TR: - görünür validation vs rejection ayrımı burada özellikle önemlidir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı parse sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

# EN: PARSE RUNTIME CLASS PURPOSE MEMORY BLOCK V7 / MinimalParseApplyResult
# EN:
# EN: Why this class exists:
# EN: - because parse runtime should carry structured meaning through a named class instead of anonymous dict drift
# EN: - because later taxonomy, preranking, discovery, workflow, and audit surfaces need readable stable field meaning
# EN:
# EN: Accepted role:
# EN: - named parse-runtime class contract
# EN:
# EN: Important contract reminder:
# EN: - this class belongs to the narrow parse-runtime layer and should keep parse-side meaning explicit
# TR: PARSE RUNTIME CLASS AMAÇ HAFIZA BLOĞU V7 / MinimalParseApplyResult
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü parse runtime anlamı anonim dict dağılması yerine isimli sınıf ile taşınmalıdır
# TR: - çünkü sonraki taxonomy, preranking, discovery, workflow ve denetim yüzeyleri okunabilir ve kararlı alan anlamına ihtiyaç duyar
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime sınıf sözleşmesi
# TR:
# TR: Önemli sözleşme hatırlatması:
# TR: - bu sınıf dar parse-runtime katmanına aittir ve parse-side anlamı açık tutmalıdır
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / minimal_taxonomy_package_version
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'minimal_taxonomy_package_version' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: (no explicit parameters)
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely shapes page-derived evidence, candidate structures, or taxonomy-facing payloads
# EN: - explicit payload structure is often important for audits and later ranking layers
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / minimal_taxonomy_package_version
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'minimal_taxonomy_package_version' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: (açık parametre yok)
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle page kökenli evidence, candidate yapıları veya taxonomyye bakan payloadları şekillendirir
# TR: - açık payload yapısı çoğu zaman denetimler ve sonraki ranking katmanları için önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / minimal_taxonomy_package_version
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / minimal_taxonomy_package_version
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / candidate_score_field_name
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'candidate_score_field_name' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: field_name
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely shapes page-derived evidence, candidate structures, or taxonomy-facing payloads
# EN: - explicit payload structure is often important for audits and later ranking layers
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / candidate_score_field_name
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'candidate_score_field_name' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: field_name
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle page kökenli evidence, candidate yapıları veya taxonomyye bakan payloadları şekillendirir
# TR: - açık payload yapısı çoğu zaman denetimler ve sonraki ranking katmanları için önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / candidate_score_field_name
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - field_name => explicit parse-runtime input parameter of candidate_score_field_name; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / candidate_score_field_name
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - field_name => candidate_score_field_name fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / confidence_band_for_score
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'confidence_band_for_score' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: score
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / confidence_band_for_score
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'confidence_band_for_score' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: score
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / confidence_band_for_score
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - score => explicit parse-runtime input parameter of confidence_band_for_score; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / confidence_band_for_score
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - score => confidence_band_for_score fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / build_taxonomy_search_inputs
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'build_taxonomy_search_inputs' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: parse_result
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely shapes page-derived evidence, candidate structures, or taxonomy-facing payloads
# EN: - explicit payload structure is often important for audits and later ranking layers
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_taxonomy_search_inputs
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_taxonomy_search_inputs' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: parse_result
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle page kökenli evidence, candidate yapıları veya taxonomyye bakan payloadları şekillendirir
# TR: - açık payload yapısı çoğu zaman denetimler ve sonraki ranking katmanları için önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / build_taxonomy_search_inputs
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - parse_result => explicit parse-runtime input parameter of build_taxonomy_search_inputs; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_taxonomy_search_inputs
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - parse_result => build_taxonomy_search_inputs fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def build_taxonomy_search_inputs(parse_result: MinimalParseResult) -> list[dict]:
    # EN: We start from an empty list so each added search input stays explicit.
    # TR: Her eklenen arama girdisi açık kalsın diye boş listeyle başlıyoruz.
    # EN: search_inputs stores the explicit list of taxonomy lookup requests derived from parse evidence.
    # EN: Expected values are ordered dict items that each carry field_name and query_text.
    # TR: search_inputs, parse evidence'dan türetilen açık taxonomy lookup istek listesini taşır.
    # TR: Beklenen değerler field_name ve query_text taşıyan sıralı dict öğeleridir.
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / build_minimal_taxonomy_candidates
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'build_minimal_taxonomy_candidates' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: parse_result, source_run_id, source_note, limit_per_query, max_candidates
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely shapes page-derived evidence, candidate structures, or taxonomy-facing payloads
# EN: - explicit payload structure is often important for audits and later ranking layers
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_minimal_taxonomy_candidates
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_minimal_taxonomy_candidates' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: parse_result, source_run_id, source_note, limit_per_query, max_candidates
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle page kökenli evidence, candidate yapıları veya taxonomyye bakan payloadları şekillendirir
# TR: - açık payload yapısı çoğu zaman denetimler ve sonraki ranking katmanları için önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / build_minimal_taxonomy_candidates
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - parse_result => explicit parse-runtime input parameter of build_minimal_taxonomy_candidates; this value is part of the visible contract of this function
# EN: - source_run_id => explicit parse-runtime input parameter of build_minimal_taxonomy_candidates; this value is part of the visible contract of this function
# EN: - source_note => explicit parse-runtime input parameter of build_minimal_taxonomy_candidates; this value is part of the visible contract of this function
# EN: - limit_per_query => explicit parse-runtime input parameter of build_minimal_taxonomy_candidates; this value is part of the visible contract of this function
# EN: - max_candidates => explicit parse-runtime input parameter of build_minimal_taxonomy_candidates; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_minimal_taxonomy_candidates
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - parse_result => build_minimal_taxonomy_candidates fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - source_run_id => build_minimal_taxonomy_candidates fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - source_note => build_minimal_taxonomy_candidates fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - limit_per_query => build_minimal_taxonomy_candidates fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - max_candidates => build_minimal_taxonomy_candidates fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
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
    # EN: search_inputs stores the explicit list of taxonomy lookup requests derived from parse evidence.
    # EN: Expected values are ordered dict items that each carry field_name and query_text.
    # TR: search_inputs, parse evidence'dan türetilen açık taxonomy lookup istek listesini taşır.
    # TR: Beklenen değerler field_name ve query_text taşıyan sıralı dict öğeleridir.
    search_inputs = build_taxonomy_search_inputs(parse_result)

    # EN: If there is no usable search input, there can be no taxonomy candidates.
    # TR: Kullanılabilir arama girdisi yoksa taxonomy candidate de olamaz.
    if not search_inputs:
        return []

    # EN: We open the dedicated taxonomy connection through the canonical runtime helper.
    # TR: Ayrılmış taxonomy bağlantısını kanonik runtime helper üzerinden açıyoruz.
    # EN: taxonomy_conn stores the dedicated live taxonomy database connection used for runtime lookup work.
    # EN: Expected values are open psycopg connection objects until the surrounding finally/close path runs.
    # TR: taxonomy_conn, runtime lookup işi için kullanılan ayrılmış canlı taxonomy veritabanı bağlantısını taşır.
    # TR: Beklenen değerler çevredeki finally/close yolu çalışana kadar açık psycopg bağlantı nesneleridir.
    taxonomy_conn = connect_taxonomy_db(taxonomy_default_dsn())

    try:
        # EN: We aggregate hits by taxonomy_node_code so multiple field hits enrich
        # EN: one candidate instead of creating noisy duplicates.
        # TR: Birden çok alan vuruşu gürültülü kopyalar üretmesin, tek candidate'i
        # TR: zenginleştirsin diye hit'leri taxonomy_node_code bazında topluyoruz.
        # EN: candidate_map aggregates taxonomy hits by node code so repeated evidence enriches one candidate row.
        # EN: Expected values are dict rows keyed by taxonomy node identifiers.
        # TR: candidate_map, tekrar eden evidence aynı aday satırını zenginleştirsin diye taxonomy hit'lerini node code bazında toplar.
        # TR: Beklenen değerler taxonomy node kimlikleriyle anahtarlanan dict satırlarıdır.
        candidate_map: dict[str, dict] = {}

        # EN: We process each search input one by one.
        # TR: Her arama girdisini tek tek işliyoruz.
        for search_input in search_inputs:
            # EN: We extract the explicit field name.
            # TR: Açık alan adını çıkarıyoruz.
            # EN: field_name stores which parse evidence field produced the current taxonomy search input.
            # EN: Expected values are explicit evidence labels such as title or body_text_excerpt.
            # TR: field_name, mevcut taxonomy arama girdisini hangi parse evidence alanının ürettiğini taşır.
            # TR: Beklenen değerler title veya body_text_excerpt gibi açık evidence etiketleridir.
            field_name = search_input["field_name"]

            # EN: We extract the concrete query text.
            # TR: Somut sorgu metnini çıkarıyoruz.
            # EN: query_text stores the concrete text fragment sent to taxonomy search for the current evidence item.
            # EN: Expected values are non-empty readable strings derived from parse evidence.
            # TR: query_text, mevcut evidence öğesi için taxonomy aramaya gönderilen somut metin parçasını taşır.
            # TR: Beklenen değerler parse evidence'dan türetilmiş boş olmayan okunur stringlerdir.
            query_text = search_input["query_text"]

            # EN: We search the live runtime taxonomy with the same language code
            # EN: inferred from the HTML surface.
            # TR: Canlı runtime taxonomy içinde, HTML yüzeyinden çıkarılan aynı dil
            # TR: koduyla arama yapıyoruz.
            # EN: hits stores taxonomy matches returned for the current search input.
            # EN: Expected values are ordered runtime match objects or an empty list when nothing matched.
            # TR: hits, mevcut arama girdisi için dönen taxonomy eşleşmelerini taşır.
            # TR: Beklenen değerler sıralı runtime match nesneleri veya eşleşme yoksa boş listedir.
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
                # EN: candidate_key stores the taxonomy node code used as the aggregation key for one candidate.
                # EN: Expected values are stable taxonomy node code strings.
                # TR: candidate_key, bir aday için toplama anahtarı olarak kullanılan taxonomy node code değerini taşır.
                # TR: Beklenen değerler kararlı taxonomy node code stringleridir.
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
                # EN: score_field_name stores which candidate score column corresponds to the current evidence field.
                # EN: Expected values are explicit candidate score column names such as title_score or body_score.
                # TR: score_field_name, mevcut evidence alanına karşılık gelen candidate skor sütunu adını taşır.
                # TR: Beklenen değerler title_score veya body_score gibi açık candidate skor sütun adlarıdır.
                score_field_name = candidate_score_field_name(field_name)

                # EN: We convert the returned score into float once.
                # TR: Dönen skoru bir kez float'a çeviriyoruz.
                # EN: match_score stores the numeric score of the current taxonomy hit after one float conversion.
                # EN: Expected values are float score values usually in a bounded matching range.
                # TR: match_score, mevcut taxonomy hit'inin tek seferlik float dönüşümünden sonraki sayısal skorunu taşır.
                # TR: Beklenen değerler genelde sınırlı bir eşleşme aralığında kalan float skor değerleridir.
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
        # EN: ranked_candidates stores the final sorted candidate rows selected for downstream persistence and review.
        # EN: Expected values are candidate dict rows ordered by descending total score.
        # TR: ranked_candidates, downstream persistence ve inceleme için seçilmiş son sıralı aday satırlarını taşır.
        # TR: Beklenen değerler total score'a göre azalan biçimde sıralanmış candidate dict satırlarıdır.
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / build_preranking_candidate_summary
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'build_preranking_candidate_summary' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: candidates
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely shapes page-derived evidence, candidate structures, or taxonomy-facing payloads
# EN: - explicit payload structure is often important for audits and later ranking layers
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_preranking_candidate_summary
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_preranking_candidate_summary' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: candidates
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle page kökenli evidence, candidate yapıları veya taxonomyye bakan payloadları şekillendirir
# TR: - açık payload yapısı çoğu zaman denetimler ve sonraki ranking katmanları için önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / build_preranking_candidate_summary
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - candidates => explicit parse-runtime input parameter of build_preranking_candidate_summary; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_preranking_candidate_summary
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - candidates => build_preranking_candidate_summary fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / extract_candidate_hrefs_from_html
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'extract_candidate_hrefs_from_html' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: html_text
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely shapes page-derived evidence, candidate structures, or taxonomy-facing payloads
# EN: - explicit payload structure is often important for audits and later ranking layers
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / extract_candidate_hrefs_from_html
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'extract_candidate_hrefs_from_html' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: html_text
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle page kökenli evidence, candidate yapıları veya taxonomyye bakan payloadları şekillendirir
# TR: - açık payload yapısı çoğu zaman denetimler ve sonraki ranking katmanları için önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / extract_candidate_hrefs_from_html
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - html_text => explicit parse-runtime input parameter of extract_candidate_hrefs_from_html; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / extract_candidate_hrefs_from_html
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - html_text => extract_candidate_hrefs_from_html fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def extract_candidate_hrefs_from_html(html_text: str) -> list[str]:
    # EN: We collect href values in encounter order first.
    # TR: Önce href değerlerini karşılaşılma sırasıyla topluyoruz.
    # EN: hrefs stores raw href values collected from HTML in encounter order.
    # EN: Expected values are URL-like strings exactly as discovered before normalization.
    # TR: hrefs, HTML içinden karşılaşılma sırasıyla toplanan ham href değerlerini taşır.
    # TR: Beklenen değerler normalize edilmeden önce keşfedilen URL-benzeri stringlerdir.
    hrefs: list[str] = []

    # EN: We scan for simple quoted href attributes because the first discovery
    # EN: bridge should stay easy to audit.
    # TR: İlk discovery köprüsü kolay denetlenebilir kalsın diye basit tırnaklı
    # TR: href niteliklerini tarıyoruz.
    for match in re.finditer(r'href\s*=\s*["\']([^"\']+)["\']', html_text, flags=re.IGNORECASE):
        # EN: href_value is the raw href text extracted from one matched anchor attribute.
        # EN: Expected values are non-empty link texts; blank strings are undesired and filtered out immediately below.
        # TR: href_value eşleşen tek bir anchor niteliğinden çıkarılan ham href metnidir.
        # TR: Beklenen değerler boş olmayan link metinleridir; boş stringler istenmez ve hemen aşağıda elenir.
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / normalize_discovered_href
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'normalize_discovered_href' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: base_url, href_value
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / normalize_discovered_href
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'normalize_discovered_href' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: base_url, href_value
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / normalize_discovered_href
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - base_url => explicit parse-runtime input parameter of normalize_discovered_href; this value is part of the visible contract of this function
# EN: - href_value => explicit parse-runtime input parameter of normalize_discovered_href; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / normalize_discovered_href
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - base_url => normalize_discovered_href fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - href_value => normalize_discovered_href fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def normalize_discovered_href(base_url: str, href_value: str) -> str | None:
    # EN: Empty href values are ignored explicitly.
    # TR: Boş href değerleri açık biçimde yok sayılır.
    if not href_value:
        return None

    # EN: These schemes are intentionally out of scope for the first minimal bridge.
    # TR: Bu şemalar ilk minimal köprü için bilinçli olarak kapsam dışıdır.
    # EN: lowered stores the stripped lowercase href used for quick scheme and fragment rejection checks.
    # EN: Expected values are lowercase href-like strings.
    # TR: lowered, hızlı şema ve fragment red kontrolleri için kullanılan kırpılmış küçük harfli href değerini taşır.
    # TR: Beklenen değerler küçük harfe çevrilmiş href-benzeri stringlerdir.
    lowered = href_value.strip().lower()
    if lowered.startswith(("javascript:", "mailto:", "tel:", "data:", "#")):
        return None

    # EN: We resolve relative links against the parent canonical URL.
    # TR: Göreli linkleri parent kanonik URL'ye göre çözüyoruz.
    # EN: joined stores the base-resolved absolute URL produced from the discovered href.
    # EN: Expected values are joined absolute URL strings before split/authority checks.
    # TR: joined, keşfedilen href'ten üretilen base'e göre çözülmüş mutlak URL'yi taşır.
    # TR: Beklenen değerler split/authority kontrollerinden önceki birleştirilmiş mutlak URL stringleridir.
    joined = urljoin(base_url, href_value.strip())

    # EN: We remove fragments because frontier truth should not duplicate the same
    # EN: resource only due to a fragment.
    # TR: Frontier doğrusu yalnızca fragment yüzünden aynı kaynağı çoğaltmamalıdır;
    # TR: bu yüzden fragment'i kaldırıyoruz.
    # EN: parts stores the split URL structure of the joined discovery candidate.
    # EN: Expected values are urlsplit result objects used for scheme and authority validation.
    # TR: parts, birleştirilmiş discovery adayının ayrıştırılmış URL yapısını taşır.
    # TR: Beklenen değerler şema ve authority doğrulaması için kullanılan urlsplit sonuç nesneleridir.
    parts = urlsplit(joined)
    if parts.scheme.lower() not in {"http", "https"}:
        return None

    # EN: base_parts carries the parsed authority identity of the already-accepted base URL.
    # EN: Expected values are split URL parts with a stable netloc that the next same-authority check can compare against.
    # TR: base_parts daha önce kabul edilmiş base URLnin ayrıştırılmış authority kimliğini taşır.
    # TR: Beklenen değerler bir sonraki same-authority kontrolünün karşılaştırabileceği kararlı netloc alanlarıdır.
    base_parts = urlsplit(base_url)

    # EN: The first bridge stays deliberately narrow: only same-authority links.
    # TR: İlk köprü bilinçli olarak dar kalır: yalnızca aynı authority linkleri.
    if parts.netloc.lower() != base_parts.netloc.lower():
        return None

    # EN: normalized_path stores the canonical path fallback used for discovery normalization.
    # EN: Expected values are a non-empty path string; "/" is the intentional fallback when the raw path is empty.
    # TR: normalized_path discovery normalizasyonunda kullanılan kanonik path fallback değerini taşır.
    # TR: Beklenen değerler boş olmayan path stringidir; ham path boşsa bilinçli fallback "/" olur.
    normalized_path = parts.path or "/"
    # EN: normalized stores the final same-authority normalized discovery URL without fragment noise.
    # EN: Expected values are stable http/https URL texts ready for duplicate suppression and frontier handoff.
    # TR: normalized fragment gürültüsü olmadan son same-authority normalize discovery URL metnini taşır.
    # TR: Beklenen değerler duplicate suppression ve frontier handoff için hazır kararlı http/https URL metinleridir.
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / build_minimal_discovery_targets
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'build_minimal_discovery_targets' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: base_url, html_text, limit
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / build_minimal_discovery_targets
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'build_minimal_discovery_targets' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: base_url, html_text, limit
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / build_minimal_discovery_targets
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - base_url => explicit parse-runtime input parameter of build_minimal_discovery_targets; this value is part of the visible contract of this function
# EN: - html_text => explicit parse-runtime input parameter of build_minimal_discovery_targets; this value is part of the visible contract of this function
# EN: - limit => explicit parse-runtime input parameter of build_minimal_discovery_targets; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / build_minimal_discovery_targets
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - base_url => build_minimal_discovery_targets fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - html_text => build_minimal_discovery_targets fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - limit => build_minimal_discovery_targets fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
def build_minimal_discovery_targets(*, base_url: str, html_text: str, limit: int = 25) -> list[str]:
    # EN: We extract raw href values first.
    # TR: Önce ham href değerlerini çıkarıyoruz.
    # EN: raw_hrefs stores the unnormalized href list extracted from HTML before filtering and canonicalization.
    # EN: Expected values are raw discovered href strings in encounter order.
    # TR: raw_hrefs, filtreleme ve kanonikleştirme öncesinde HTML'den çıkarılan normalize edilmemiş href listesini taşır.
    # TR: Beklenen değerler karşılaşılma sırasındaki ham keşif href stringleridir.
    raw_hrefs = extract_candidate_hrefs_from_html(html_text)

    # EN: We keep unique normalized URLs in encounter order.
    # TR: Tekilleştirilmiş normalize URL'leri karşılaşılma sırasıyla koruyoruz.
    # EN: normalized_urls stores the accepted normalized discovery URLs that survived filtering.
    # EN: Expected values are canonical same-authority http/https URL strings.
    # TR: normalized_urls, filtreleri geçen kabul edilmiş normalize discovery URL'lerini taşır.
    # TR: Beklenen değerler kanonik, aynı authority'ye ait http/https URL stringleridir.
    normalized_urls: list[str] = []
    # EN: seen tracks normalized discovery URLs that were already emitted in this parse pass.
    # EN: Expected values are canonical URL strings; duplicate re-emission is undesired because it inflates discovery noise.
    # TR: seen bu parse geçişinde zaten üretilmiş normalize discovery URLlerini izler.
    # TR: Beklenen değerler kanonik URL stringleridir; duplicate yeniden üretim discovery gürültüsünü şişirdiği için istenmez.
    seen: set[str] = set()

    for href_value in raw_hrefs:
        # EN: normalized stores the current href after same-authority discovery normalization.
        # EN: Expected values are canonical same-authority URLs or None when the href must be rejected by the narrow first bridge.
        # TR: normalized mevcut hrefin same-authority discovery normalizasyonundan geçmiş halini taşır.
        # TR: Beklenen değerler kanonik same-authority URLler veya href dar ilk köprü tarafından reddedilmeliyse Nonedir.
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
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / enqueue_minimal_discovered_links
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'enqueue_minimal_discovered_links' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, url_id, raw_storage_path, source_run_id, source_note, limit
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface exposes one named worker parse contract boundary
# EN: - explicit payload and branch visibility should remain readable here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / enqueue_minimal_discovered_links
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'enqueue_minimal_discovered_links' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, url_id, raw_storage_path, source_run_id, source_note, limit
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey isimli bir worker parse sözleşme sınırını açığa çıkarır
# TR: - açık payload ve dal görünürlüğü burada okunabilir kalmalıdır
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / enqueue_minimal_discovered_links
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - conn => explicit parse-runtime input parameter of enqueue_minimal_discovered_links; this value is part of the visible contract of this function
# EN: - url_id => explicit parse-runtime input parameter of enqueue_minimal_discovered_links; this value is part of the visible contract of this function
# EN: - raw_storage_path => explicit parse-runtime input parameter of enqueue_minimal_discovered_links; this value is part of the visible contract of this function
# EN: - source_run_id => explicit parse-runtime input parameter of enqueue_minimal_discovered_links; this value is part of the visible contract of this function
# EN: - source_note => explicit parse-runtime input parameter of enqueue_minimal_discovered_links; this value is part of the visible contract of this function
# EN: - limit => explicit parse-runtime input parameter of enqueue_minimal_discovered_links; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / enqueue_minimal_discovered_links
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - conn => enqueue_minimal_discovered_links fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - url_id => enqueue_minimal_discovered_links fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - raw_storage_path => enqueue_minimal_discovered_links fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - source_run_id => enqueue_minimal_discovered_links fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - source_note => enqueue_minimal_discovered_links fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - limit => enqueue_minimal_discovered_links fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
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
    # EN: parent_context stores the durable database context of the already-accepted parent URL.
    # EN: Expected values are dict-like rows that include canonical_url and related discovery metadata.
    # TR: parent_context, daha önce kabul edilmiş parent URL'nin kalıcı veritabanı bağlamını taşır.
    # TR: Beklenen değerler canonical_url ve ilgili discovery metadata'sını içeren dict-benzeri satırlardır.
    parent_context = fetch_url_discovery_context(
        conn,
        url_id=url_id,
    )

    # EN: Discovery context no-row must degrade into a visible discovery result
    # EN: instead of crashing the whole parse path.
    # TR: Discovery context no-row durumu tüm parse yolunu çökertmek yerine
    # TR: görünür bir discovery sonucuna degrade olmalıdır.
    if bool(parent_context.get("discovery_degraded")):
        return {
            "parent_url_id": int(url_id),
            "discovery_degraded": True,
            "discovery_degraded_reason": str(parent_context.get("discovery_degraded_reason")),
            "discovery_context_degraded": True,
            "discovery_context": dict(parent_context),
            "discovered_href_count": 0,
            "normalized_url_count": 0,
            "enqueued_url_count": 0,
            "skipped_url_count": 0,
            "degraded_enqueue_count": 0,
            "enqueued_rows": [],
            "degraded_rows": [],
        }

    # EN: We read the raw HTML body from disk because discovery should use the same
    # EN: fetched artefact that parse already trusts.
    # TR: Discovery, parse'ın zaten güvendiği aynı fetch artefact'ını kullansın diye
    # TR: ham HTML body'yi diskten okuyoruz.
    # EN: html_text stores the durable raw HTML text that the current parse step will inspect and transform.
    # EN: Expected values are decoded page HTML strings read from the controlled raw artefact.
    # TR: html_text, mevcut parse adımının inceleyip dönüştüreceği kalıcı ham HTML metnini taşır.
    # TR: Beklenen değerler kontrollü ham artefact'tan okunmuş decode edilmiş sayfa HTML stringleridir.
    html_text = read_raw_body_text(raw_storage_path)

    # EN: We build a conservative list of discovery targets.
    # TR: Muhafazakâr discovery hedefleri listesi kuruyoruz.
    # EN: discovery_targets stores the conservative normalized URLs selected for minimal enqueue work.
    # EN: Expected values are short lists of canonical URLs ready for frontier enqueue attempts.
    # TR: discovery_targets, minimal enqueue işi için seçilmiş muhafazakâr normalize URL'leri taşır.
    # TR: Beklenen değerler frontier enqueue denemelerine hazır kısa kanonik URL listeleridir.
    discovery_targets = build_minimal_discovery_targets(
        base_url=str(parent_context["canonical_url"]),
        html_text=html_text,
        limit=limit,
    )

    # EN: We prepare explicit success and degraded accumulators separately so
    # EN: operator-visible discovery truth stays honest.
    # TR: Operatörün göreceği discovery doğrusu dürüst kalsın diye başarılı ve
    # TR: degrade biriktiricilerini ayrı hazırlıyoruz.
    # EN: enqueued_rows stores visible enqueue success receipts for accepted discovery targets.
    # EN: Expected values are receipt dict rows that describe successful enqueue outcomes.
    # TR: enqueued_rows, kabul edilen discovery hedefleri için görünür enqueue başarı makbuzlarını taşır.
    # TR: Beklenen değerler başarılı enqueue sonuçlarını anlatan makbuz dict satırlarıdır.
    enqueued_rows: list[dict] = []
    # EN: degraded_rows collects visible enqueue receipts that finished in degraded discovery-style branches.
    # EN: Expected values are operator-readable receipt dicts; silently mixing them into success rows is undesired.
    # TR: degraded_rows degrade discovery tarzı dallarda biten görünür enqueue makbuzlarını toplar.
    # TR: Beklenen değerler operatörün okuyabileceği receipt dictleridir; bunları sessizce başarı satırlarına karıştırmak istenmez.
    degraded_rows: list[dict] = []

    for discovered_url in discovery_targets:
        # EN: parts stores the parsed URL components of the current discovered URL candidate.
        # EN: Expected values are split URL parts whose scheme, host, port, path, and query can be forwarded into enqueue truth.
        # TR: parts mevcut discovered URL adayının ayrıştırılmış URL bileşenlerini taşır.
        # TR: Beklenen değerler scheme, host, port, path ve query alanları enqueue doğrusuna aktarılabilen split URL parçalarıdır.
        parts = urlsplit(discovered_url)
        # EN: scheme stores the lowercase transport scheme of the discovered URL.
        # EN: Expected values are "http" or "https"; anything outside the canonical crawl surface would be undesired here.
        # TR: scheme discovered URLnin küçük harfe çevrilmiş taşıma şemasını taşır.
        # TR: Beklenen değerler "http" veya "https"tir; kanonik crawl yüzeyi dışındaki değerler burada istenmez.
        scheme = parts.scheme.lower()
        # EN: host stores the lowercase hostname extracted from the discovered URL.
        # EN: Expected values are non-empty host texts; empty host values would make the enqueue row structurally degraded.
        # TR: host discovered URLden çıkarılan küçük harfli hostname değerini taşır.
        # TR: Beklenen değerler boş olmayan host metinleridir; boş host değerleri enqueue satırını yapısal olarak degrade eder.
        host = (parts.hostname or "").lower()
        # EN: port stores the effective integer port used for authority and frontier identity.
        # EN: Expected values are the explicit URL port or the canonical 443/80 fallback derived from scheme.
        # TR: port authority ve frontier kimliği için kullanılan etkin tamsayı portu taşır.
        # TR: Beklenen değerler URLnin açık portu veya scheme üzerinden türetilen kanonik 443/80 fallback değeridir.
        port = parts.port or (443 if scheme == "https" else 80)
        # EN: authority_key stores the stable host:port identity that the enqueue helper expects.
        # EN: Expected values are deterministic "host:port" texts; mismatched authority identity is undesired because discovery linkage would drift.
        # TR: authority_key enqueue yardımcısının beklediği kararlı host:port kimliğini taşır.
        # TR: Beklenen değerler deterministik "host:port" metinleridir; authority kimliğinin kayması discovery bağlantısını bozacağı için istenmez.
        authority_key = f"{host}:{port}"
        # EN: url_path stores the enqueue-ready path portion of the discovered URL.
        # EN: Expected values are non-empty path texts; "/" is the intentional fallback when the raw path is empty.
        # TR: url_path discovered URLnin enqueueya hazır path bölümünü taşır.
        # TR: Beklenen değerler boş olmayan path metinleridir; ham path boşsa bilinçli fallback "/" olur.
        url_path = parts.path or "/"
        # EN: url_query stores the optional query portion that will be forwarded to enqueue truth.
        # EN: Expected values are a raw query string or None when no query exists; empty-string noise is undesired.
        # TR: url_query enqueue doğrusuna aktarılacak isteğe bağlı query bölümünü taşır.
        # TR: Beklenen değerler ham query stringi veya query yoksa Nonedir; boş-string gürültüsü istenmez.
        url_query = parts.query or None

        # EN: enqueue_row stores the first DB/helper receipt returned for this discovered URL enqueue attempt.
        # EN: Expected values are dict-like success or degraded receipts; silent no-row ambiguity would be undesired.
        # TR: enqueue_row bu discovered URL enqueue denemesi için dönen ilk DB/helper makbuzunu taşır.
        # TR: Beklenen değerler dict-benzeri başarı veya degrade makbuzlarıdır; sessiz no-row belirsizliği istenmez.
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

        # EN: We keep degraded enqueue outcomes visible instead of counting them
        # EN: as successful enqueue rows.
        # TR: Degrade enqueue sonuçlarını başarılı enqueue satırı gibi saymak
        # TR: yerine görünür biçimde ayrı tutuyoruz.
        if enqueue_row is None:
            # EN: A missing enqueue receipt should remain visible as degraded discovery truth.
            # TR: Eksik enqueue makbuzu görünmez kalmamalı, degrade discovery doğrusu olarak görünür kalmalıdır.
            degraded_rows.append(
                {
                    "parent_url_id": int(url_id),
                    "canonical_url": discovered_url,
                    "discovery_degraded": True,
                    "discovery_degraded_reason": "enqueue_discovered_url_returned_none",
                    "error_class": "discovery_enqueue_returned_none",
                    "error_message": "enqueue_discovered_url(...) returned None",
                    "depth": int(parent_context["depth"]) + 1,
                    "priority": max(int(parent_context["priority"]) - 5, 1),
                    "scheme": scheme,
                    "host": host,
                    "port": port,
                    "authority_key": authority_key,
                    "url_path": url_path,
                    "url_query": url_query,
                }
            )
            continue

        # EN: enqueue_row is converted into a plain mutable dict before branch classification continues.
        # EN: Expected values are dict-like receipts that can safely receive later read access and list insertion.
        # TR: enqueue_row dal sınıflandırması sürmeden önce düz ve değiştirilebilir dict haline çevrilir.
        # TR: Beklenen değerler daha sonraki okuma erişimini ve liste eklemeyi güvenle taşıyabilen dict-benzeri makbuzlardır.
        enqueue_row = dict(enqueue_row)
        metadata_update_result: dict = {
            "action": "update_url_crawl_map_metadata",
            "metadata_updated": False,
            "metadata_degraded": True,
            "metadata_skipped": False,
            "error_class": "metadata_target_url_id_missing",
            "error_message": "enqueue row did not include url_id for crawl_map metadata update",
        }

        metadata_update_target_url_id = enqueue_row.get("url_id")
        if metadata_update_target_url_id is not None:
            metadata_update_result = update_url_crawl_map_metadata(
                conn,
                url_id=int(metadata_update_target_url_id),
                root_url_id=int(url_id),
                branch_role="discovered_child",
                branch_label=str(enqueue_row.get("discovery_type") or "html_link"),
                crawl_path_hint="minimal_html_link_discovery_from_parse_runtime",
            )

        enqueue_row["metadata_update_result"] = metadata_update_result


        if bool(enqueue_row.get("discovery_degraded")):
            degraded_rows.append(enqueue_row)
        else:
            enqueued_rows.append(enqueue_row)

    # EN: We return one explicit structured discovery result that keeps both
    # EN: successful and degraded enqueue truth visible.
    # TR: Başarılı ve degrade enqueue doğrularını birlikte görünür tutan açık ve
    # TR: yapılı tek bir discovery sonucu döndürüyoruz.
    return {
        "parent_url_id": int(url_id),
        "discovery_degraded": len(degraded_rows) > 0,
        "discovery_degraded_reason": (
            "enqueue_discovered_url_returned_no_row" if degraded_rows else None
        ),
        "discovery_context_degraded": False,
        "discovered_href_count": len(extract_candidate_hrefs_from_html(html_text)),
        "normalized_url_count": len(discovery_targets),
        "enqueued_url_count": len(enqueued_rows),
        "skipped_url_count": len(extract_candidate_hrefs_from_html(html_text)) - len(discovery_targets),
        "degraded_enqueue_count": len(degraded_rows),
        "metadata_updated_count": sum(
            1
            for row in enqueued_rows
            if isinstance(row.get("metadata_update_result"), dict)
            and bool(row["metadata_update_result"].get("metadata_updated"))
        ),
        "metadata_degraded_count": sum(
            1
            for row in enqueued_rows
            if isinstance(row.get("metadata_update_result"), dict)
            and bool(row["metadata_update_result"].get("metadata_degraded"))
        ),
        "metadata_skipped_count": sum(
            1
            for row in enqueued_rows
            if isinstance(row.get("metadata_update_result"), dict)
            and bool(row["metadata_update_result"].get("metadata_skipped"))
        ),
        "enqueued_rows": enqueued_rows,
        "degraded_rows": degraded_rows,
    }


# EN: This helper is the current canonical repo-contained minimal parse-entry flow.
# EN: It keeps the whole apply path inside tracked code instead of relying on
# EN: ad hoc one-off Python snippets outside the repository surface.
# TR: Bu yardımcı, mevcut kanonik repo-içi minimal parse-entry akışıdır.
# TR: Uygulama yolunun tamamını repository dışında kalan tek kullanımlık Python
# TR: parçaları yerine izlenen kod içinde tutar.
# EN: PARSE FUNCTION PURPOSE MEMORY BLOCK V6 / apply_minimal_parse_entry
# EN:
# EN: Why this function exists:
# EN: - because parse truth for 'apply_minimal_parse_entry' should be exposed through one named top-level helper boundary
# EN: - because parse-side semantics should remain readable instead of being buried in the main worker hub
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, url_id, raw_storage_path, source_run_id, source_note, workflow_state, workflow_state_reason
# EN: - values should match the current Python signature and the parse contract below
# EN:
# EN: Accepted output:
# EN: - a parse-oriented result shape defined by the current function body
# EN: - this may be a validation payload, parse apply result, evidence shape, taxonomy-facing structure, or another explicit parse-side branch result
# EN:
# EN: Common parse meaning hints:
# EN: - this surface likely deals with parse application, contract validation, or parse-result visibility
# EN: - explicit success vs degraded parse meaning may matter here
# EN: - these helpers often define whether later taxonomy/storage layers receive usable payloads
# EN: - visible validation vs rejection distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is parse-side helper logic, not the whole worker corridor
# EN: - parse results must stay explicit so audits can understand success, degraded, rejection, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague parse results that hide branch meaning
# TR: PARSE FUNCTION AMAÇ HAFIZA BLOĞU V6 / apply_minimal_parse_entry
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'apply_minimal_parse_entry' için parse doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü parse tarafı semantiklerinin ana worker hubı içinde gömülü kalmaması gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, url_id, raw_storage_path, source_run_id, source_note, workflow_state, workflow_state_reason
# TR: - değerler aşağıdaki mevcut Python imzası ve parse sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen parse odaklı sonuç şekli
# TR: - bu; validation payloadı, parse apply sonucu, evidence şekli, taxonomyye bakan yapı veya başka açık parse tarafı dal sonucu olabilir
# TR:
# TR: Ortak parse anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle parse uygulaması, contract validation veya parse-result görünürlüğü ile ilgilenir
# TR: - açık success vs degraded parse anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki taxonomy/storage katmanlarının kullanılabilir payload alıp almayacağını belirler
# TR: - görünür validation vs rejection ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon parse tarafı yardımcı mantığıdır, worker koridorunun tamamı değildir
# TR: - parse sonuçları açık kalmalıdır ki denetimler success, degraded, rejection ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz parse sonuçları

# EN: PARSE RUNTIME FUNCTION PURPOSE MEMORY BLOCK V7 / apply_minimal_parse_entry
# EN:
# EN: Why this function exists:
# EN: - because parse runtime needs this helper boundary to stay explicit and auditable
# EN: - because hidden inline parse drift would make taxonomy, discovery, preranking, and workflow behavior harder to verify
# EN:
# EN: Accepted role:
# EN: - named parse-runtime helper boundary
# EN:
# EN: Parameter contract:
# EN: - conn => explicit parse-runtime input parameter of apply_minimal_parse_entry; this value is part of the visible contract of this function
# EN: - url_id => explicit parse-runtime input parameter of apply_minimal_parse_entry; this value is part of the visible contract of this function
# EN: - raw_storage_path => explicit parse-runtime input parameter of apply_minimal_parse_entry; this value is part of the visible contract of this function
# EN: - source_run_id => explicit parse-runtime input parameter of apply_minimal_parse_entry; this value is part of the visible contract of this function
# EN: - source_note => explicit parse-runtime input parameter of apply_minimal_parse_entry; this value is part of the visible contract of this function
# EN: - workflow_state => explicit parse-runtime input parameter of apply_minimal_parse_entry; this value is part of the visible contract of this function
# EN: - workflow_state_reason => explicit parse-runtime input parameter of apply_minimal_parse_entry; this value is part of the visible contract of this function
# TR: PARSE RUNTIME FUNCTION AMAÇ HAFIZA BLOĞU V7 / apply_minimal_parse_entry
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü parse runtime bu helper sınırını açık ve denetlenebilir biçimde tutmalıdır
# TR: - çünkü gizli inline parse dağılması taxonomy, discovery, preranking ve workflow davranışını doğrulamayı zorlaştırır
# TR:
# TR: Kabul edilen rol:
# TR: - isimli parse-runtime helper sınırı
# TR:
# TR: Parametre sözleşmesi:
# TR: - conn => apply_minimal_parse_entry fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - url_id => apply_minimal_parse_entry fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - raw_storage_path => apply_minimal_parse_entry fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - source_run_id => apply_minimal_parse_entry fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - source_note => apply_minimal_parse_entry fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - workflow_state => apply_minimal_parse_entry fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
# TR: - workflow_state_reason => apply_minimal_parse_entry fonksiyonunun açık parse-runtime girdi parametresidir; bu değer fonksiyonun görünür sözleşmesinin parçasıdır
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
    # EN: parse_result stores the structured minimal parse payload derived from the fetched HTML artefact.
    # EN: Expected values are MinimalParseResult instances ready for taxonomy and persistence work.
    # TR: parse_result, fetch edilmiş HTML artefact'ından türetilen yapılı minimal parse payload'ını taşır.
    # TR: Beklenen değerler taxonomy ve persistence işine hazır MinimalParseResult örnekleridir.
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
    # EN: discovery_result stores the visible outcome of the minimal discovered-link enqueue bridge.
    # EN: Expected values are dict-like success or degraded discovery receipts.
    # TR: discovery_result, minimal discovered-link enqueue köprüsünün görünür sonucunu taşır.
    # TR: Beklenen değerler dict-benzeri başarı veya degrade discovery makbuzlarıdır.
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
    # EN: taxonomy_lookup_degraded keeps taxonomy-runtime unavailability visible
    # EN: without rolling back crawler-core fetch/discovery evidence.
    # TR: taxonomy_lookup_degraded, taxonomy-runtime erişilemezliğini görünür tutar;
    # TR: crawler-core fetch/discovery kanıtını rollback ettirmez.
    taxonomy_lookup_degraded = False
    taxonomy_lookup_degraded_reason = None
    taxonomy_lookup_error_class = None
    taxonomy_lookup_error_message = None

    try:
        # EN: raw_taxonomy_candidates stores the unfiltered taxonomy candidates returned by runtime taxonomy search.
        # EN: Expected values are candidate dict rows before SQL-contract filtering.
        # TR: raw_taxonomy_candidates, runtime taxonomy aramasının döndürdüğü filtrelenmemiş taxonomy adaylarını taşır.
        # TR: Beklenen değerler SQL sözleşme filtresinden önceki candidate dict satırlarıdır.
        raw_taxonomy_candidates = build_minimal_taxonomy_candidates(
            parse_result=parse_result,
            source_run_id=source_run_id,
            source_note=source_note,
        )
    except Exception as exc:
        # EN: Taxonomy lookup is intentionally non-fatal for crawler-core validation.
        # EN: Fetch, parse metadata, and discovery truth must remain durable even
        # EN: when the taxonomy DB privilege/runtime seam is not ready yet.
        # TR: Taxonomy lookup crawler-core doğrulaması için bilinçli olarak fatal değildir.
        # TR: Taxonomy DB privilege/runtime sınırı henüz hazır değilse bile fetch,
        # TR: parse metadata ve discovery doğrusu kalıcı kalmalıdır.
        taxonomy_lookup_degraded = True
        taxonomy_lookup_degraded_reason = "taxonomy_runtime_unavailable"
        taxonomy_lookup_error_class = type(exc).__name__
        taxonomy_lookup_error_message = f"{type(exc).__name__}: {str(exc).replace(chr(10), ' ')[:500]}"
        raw_taxonomy_candidates = []

    # EN: We reject candidates that are known-invalid for the current SQL contract
    # EN: before they can abort the surrounding transaction.
    # TR: Mevcut SQL sözleşmesi için geçersiz olduğu bilinen candidate'leri,
    # TR: çevre transaction'ı abort etmeden önce reddediyoruz.
    # EN: persistable_taxonomy_candidates stores only the taxonomy candidates allowed to reach the current SQL contract.
    # EN: Expected values are candidate dict rows that passed persistence safety checks.
    # TR: persistable_taxonomy_candidates, yalnızca mevcut SQL sözleşmesine ulaşmasına izin verilen taxonomy adaylarını taşır.
    # TR: Beklenen değerler persistence güvenlik kontrollerini geçmiş candidate dict satırlarıdır.
    persistable_taxonomy_candidates = []
    # EN: rejected_taxonomy_candidates collects candidates that must not reach the current SQL persistence contract.
    # EN: Expected values are visible rejection receipt dicts; silently dropping these rows would be undesired.
    # TR: rejected_taxonomy_candidates mevcut SQL persistence sözleşmesine ulaşmaması gereken adayları toplar.
    # TR: Beklenen değerler görünür rejection makbuzu dictleridir; bu satırları sessizce düşürmek istenmez.
    rejected_taxonomy_candidates = []

    for candidate in raw_taxonomy_candidates:
        # EN: taxonomy_package_id stores the package identity required by the current taxonomy persistence contract.
        # EN: Expected values are non-empty package identifiers; missing values trigger explicit candidate rejection below.
        # TR: taxonomy_package_id mevcut taxonomy persistence sözleşmesinin istediği paket kimliğini taşır.
        # TR: Beklenen değerler boş olmayan paket kimlikleridir; eksik değerler aşağıda açık candidate reddine yol açar.
        taxonomy_package_id = candidate.get("taxonomy_package_id")

        if taxonomy_package_id in (None, ""):
            rejected_taxonomy_candidates.append(
                {
                    "reason": "missing_taxonomy_package_id",
                    "taxonomy_node_code": candidate.get("taxonomy_node_code"),
                    "taxonomy_concept_key": candidate.get("taxonomy_concept_key"),
                    "input_lang_code": candidate.get("input_lang_code"),
                }
            )
            continue

        persistable_taxonomy_candidates.append(candidate)

    # EN: We enrich the persisted payload in-memory before the DB call so the
    # EN: parse SQL layer receives only persistable candidates.
    # TR: Veritabanı çağrısından önce persist edilecek payload'ı bellekte
    # TR: zenginleştiriyoruz; böylece parse SQL katmanı yalnızca persist edilebilir
    # TR: candidate'ler alır.
    payload = dict(parse_result.payload)
    payload["candidates"] = persistable_taxonomy_candidates

    # EN: We preserve parse metadata produced earlier before adding taxonomy bridge metadata.
    # TR: Taxonomy bridge metadata'sını eklemeden önce daha önce üretilen parse metadata'sını koruyoruz.
    existing_metadata = dict(payload.get("metadata") or {})
    existing_metadata.update(
        {
            "taxonomy_package_version": minimal_taxonomy_package_version(),
            "taxonomy_candidate_count": len(persistable_taxonomy_candidates),
            "taxonomy_candidate_input_count": len(raw_taxonomy_candidates),
            "taxonomy_candidate_rejected_count": len(rejected_taxonomy_candidates),
            "taxonomy_candidate_rejected_sample": rejected_taxonomy_candidates[:10],
            "taxonomy_bridge": "repo_helper_v1",
            "taxonomy_lookup_degraded": taxonomy_lookup_degraded,
            "taxonomy_lookup_degraded_reason": taxonomy_lookup_degraded_reason,
            "taxonomy_lookup_error_class": taxonomy_lookup_error_class,
            "taxonomy_lookup_error_message": taxonomy_lookup_error_message,
        }
    )
    payload["metadata"] = existing_metadata

    # EN: We persist evidence and candidate rows through the existing canonical
    # EN: payload helper.
    # TR: Evidence ve candidate satırlarını mevcut kanonik payload helper'ı
    # TR: üzerinden persist ediyoruz.
    # EN: persist_result stores the DB helper receipt returned after persisting parse/taxonomy payload material.
    # EN: Expected values are dict-like persistence receipts, possibly including degraded flags.
    # TR: persist_result, parse/taxonomy payload malzemesi persist edildikten sonra dönen DB helper makbuzunu taşır.
    # TR: Beklenen değerler dict-benzeri persistence makbuzlarıdır; bunlar degrade bayrakları içerebilir.
    persist_result = persist_taxonomy_preranking_payload(
        conn=conn,
        payload=payload,
    )

    # EN: We normalize persisted-candidate count early so later metadata building
    # EN: stays safe even when the DB wrapper degraded into a no-row payload.
    # TR: Persist edilmiş candidate sayısını erken normalize ediyoruz; böylece DB
    # TR: wrapper no-row degrade payload'ına düşse bile sonraki metadata kurulumları güvenli kalır.
    # EN: persisted_candidate_count stores the normalized count of taxonomy candidates that really persisted.
    # EN: Expected values are non-negative integers.
    # TR: persisted_candidate_count, gerçekten persist edilmiş taxonomy adaylarının normalize edilmiş sayısını taşır.
    # TR: Beklenen değerler negatif olmayan tamsayılardır.
    persisted_candidate_count = int(persist_result.get("persisted_candidate_count", 0) or 0)
    # EN: persist_result_degraded records whether the candidate-persistence helper degraded into a visible no-row style result.
    # EN: Expected values are True or False; hiding this branch would make later workflow reasoning unsafe.
    # TR: persist_result_degraded candidate-persistence yardımcısının görünür no-row tarzı sonuca degrade olup olmadığını kaydeder.
    # TR: Beklenen değerler True veya Falsetur; bu dalı gizlemek sonraki workflow akıl yürütmesini güvensiz hale getirir.
    persist_result_degraded = bool(persist_result.get("preranking_degraded"))

    # EN: We now create the real preranking snapshot row through the dedicated DB
    # EN: wrapper that was already present in SQL but not yet bridged in Python.
    # TR: Artık gerçek preranking snapshot satırını, SQL tarafında zaten var olup
    # TR: Python'da henüz köprülenmemiş dedicated DB wrapper üzerinden oluşturuyoruz.
    # EN: top_score stores the best total taxonomy score that can feed the real preranking snapshot.
    # EN: Expected values are float score values or None when no persistable candidate exists.
    # TR: top_score, gerçek preranking snapshot'ı besleyebilecek en iyi toplam taxonomy skorunu taşır.
    # TR: Beklenen değerler float skor değerleri veya persist edilebilir aday yoksa Nonedir.
    top_score = None
    if persistable_taxonomy_candidates:
        # EN: top_score stores the highest persisted taxonomy score that will feed the real preranking snapshot.
        # EN: Expected values are numeric score values derived from the best persistable candidate.
        # TR: top_score gerçek preranking snapshota girecek en yüksek persisted taxonomy skorunu taşır.
        # TR: Beklenen değerler en iyi persist edilebilir adaydan türetilen sayısal skor değerleridir.
        top_score = float(persistable_taxonomy_candidates[0]["total_score"])

    # EN: pre_ranked is now allowed only when at least one persistable taxonomy
    # EN: candidate exists. Otherwise we intentionally fall back to review_hold.
    # TR: pre_ranked artık yalnızca en az bir persist edilebilir taxonomy
    # TR: candidate varsa mümkündür. Aksi durumda bilinçli olarak review_hold'a düşeriz.
    # EN: effective_workflow_state stores the workflow state after parse-side safety overrides are applied.
    # EN: Expected values are readable workflow state strings such as review_hold or pre_ranked.
    # TR: effective_workflow_state, parse tarafı güvenlik override'ları uygulandıktan sonraki workflow durumunu taşır.
    # TR: Beklenen değerler review_hold veya pre_ranked gibi okunur workflow durum stringleridir.
    effective_workflow_state = workflow_state
    # EN: effective_workflow_state_reason starts from the incoming workflow explanation before parse-side overrides refine it.
    # EN: Expected values are readable reason texts that later branches may replace with more specific truth.
    # TR: effective_workflow_state_reason parse tarafı override dalları onu daraltmadan önce gelen workflow açıklamasından başlar.
    # TR: Beklenen değerler daha sonraki dalların daha özgül doğrularla değiştirebileceği okunur reason metinleridir.
    effective_workflow_state_reason = workflow_state_reason

    if workflow_state == "pre_ranked":
        if persistable_taxonomy_candidates:
            # EN: effective_workflow_state explicitly remains pre_ranked because persistable taxonomy candidates exist.
            # EN: Expected value in this branch is the durable pre_ranked state.
            # TR: effective_workflow_state persist edilebilir taxonomy adayları bulunduğu için açıkça pre_ranked olarak kalır.
            # TR: Bu dalda beklenen değer dayanıklı pre_ranked durumudur.
            effective_workflow_state = "pre_ranked"
            # EN: effective_workflow_state_reason records the precise reason why pre_ranked may remain true here.
            # EN: Expected value is the repo-helper persistence reason token shown below.
            # TR: effective_workflow_state_reason burada pre_ranked durumunun neden geçerli kaldığını kesin biçimde kaydeder.
            # TR: Beklenen değer aşağıda görülen repo-helper persistence reason tokenıdır.
            effective_workflow_state_reason = "taxonomy_candidates_persisted_via_repo_helper"
        elif taxonomy_lookup_degraded:
            # EN: effective_workflow_state is forced to review_hold because taxonomy lookup degraded.
            # EN: Expected value in this branch is review_hold; crawler-core discovery may still be valid.
            # TR: effective_workflow_state taxonomy lookup degrade olduğu için review_holda zorlanır.
            # TR: Bu dalda beklenen değer review_holddur; crawler-core discovery yine geçerli olabilir.
            effective_workflow_state = "review_hold"
            # EN: effective_workflow_state_reason records that review_hold came from taxonomy-runtime unavailability.
            # EN: Expected value is the explicit taxonomy-unavailable manual-review token shown below.
            # TR: effective_workflow_state_reason review_hold sonucunun taxonomy-runtime erişilemezliğinden geldiğini kaydeder.
            # TR: Beklenen değer aşağıda görülen açık taxonomy-unavailable manual-review tokenıdır.
            effective_workflow_state_reason = "taxonomy_lookup_unavailable_manual_review_required"
        elif rejected_taxonomy_candidates:
            # EN: effective_workflow_state is forced to review_hold because the candidate set contains SQL-contract rejections.
            # EN: Expected value in this branch is review_hold, not silent pre_ranked drift.
            # TR: effective_workflow_state candidate kümesi SQL-sözleşme reddi içerdiği için review_holda zorlanır.
            # TR: Bu dalda beklenen değer sessiz pre_ranked kayması değil review_holddur.
            effective_workflow_state = "review_hold"
            # EN: effective_workflow_state_reason records that review_hold came from missing taxonomy package ids.
            # EN: Expected value is the explicit missing-package-id reason token shown below.
            # TR: effective_workflow_state_reason review_hold sonucunun eksik taxonomy package id yüzünden geldiğini kaydeder.
            # TR: Beklenen değer aşağıda görülen açık missing-package-id reason tokenıdır.
            effective_workflow_state_reason = "taxonomy_candidates_rejected_missing_package_id"
        else:
            # EN: effective_workflow_state is forced to review_hold because no persistable taxonomy candidates survived.
            # EN: Expected value in this branch is review_hold for explicit manual inspection.
            # TR: effective_workflow_state persist edilebilir taxonomy adayı kalmadığı için review_holda zorlanır.
            # TR: Bu dalda beklenen değer açık manuel inceleme için review_holddur.
            effective_workflow_state = "review_hold"
            # EN: effective_workflow_state_reason records that the candidate list ended empty after filtering.
            # EN: Expected value is the explicit empty-candidate manual-review token shown below.
            # TR: effective_workflow_state_reason filtreleme sonrasında aday listesinin boş kaldığını kaydeder.
            # TR: Beklenen değer aşağıda görülen açık empty-candidate manual-review tokenıdır.
            effective_workflow_state_reason = "taxonomy_candidates_empty_manual_review_required"

    # EN: preranking_snapshot_result stores the DB receipt returned by real preranking snapshot persistence.
    # EN: Expected values are dict-like success or degraded receipts that later workflow linking can inspect safely.
    # TR: preranking_snapshot_result gerçek preranking snapshot persistence tarafından dönen DB makbuzunu taşır.
    # TR: Beklenen değerler daha sonraki workflow linking adımının güvenle inceleyebileceği dict-benzeri başarı veya degrade makbuzlarıdır.
    preranking_snapshot_result = persist_page_preranking_snapshot(
        conn=conn,
        url_id=url_id,
        input_lang_code=parse_result.input_lang_code,
        taxonomy_package_version=minimal_taxonomy_package_version(),
        top_candidate_count=len(persistable_taxonomy_candidates),
        top_score=top_score,
        candidate_summary=build_preranking_candidate_summary(persistable_taxonomy_candidates),
        snapshot_metadata={
            "taxonomy_package_version": minimal_taxonomy_package_version(),
            "taxonomy_candidate_count": len(persistable_taxonomy_candidates),
            "taxonomy_candidate_input_count": len(raw_taxonomy_candidates),
            "taxonomy_candidate_rejected_count": len(rejected_taxonomy_candidates),
            "taxonomy_candidate_rejected_sample": rejected_taxonomy_candidates[:10],
            "persisted_candidate_count": persisted_candidate_count,
            "persist_result_degraded": persist_result_degraded,
            "taxonomy_bridge": "repo_helper_v1",
            "taxonomy_lookup_degraded": taxonomy_lookup_degraded,
            "taxonomy_lookup_degraded_reason": taxonomy_lookup_degraded_reason,
            "taxonomy_lookup_error_class": taxonomy_lookup_error_class,
            "taxonomy_lookup_error_message": taxonomy_lookup_error_message,
        },
        source_run_id=source_run_id,
        source_note=source_note,
        review_status=effective_workflow_state,
    )

    # EN: The workflow row should link to the real preranking snapshot row when
    # EN: that row exists. If snapshot persistence degraded, we must fall back to a
    # EN: manual-review state instead of crashing on a missing snapshot_id.
    # TR: Workflow satırı gerçek preranking snapshot satırına yalnızca o satır
    # TR: gerçekten varsa bağlanmalıdır. Snapshot persistence degrade olduysa eksik
    # TR: snapshot_id yüzünden çökmek yerine manual-review durumuna düşmeliyiz.
    # EN: preranking_snapshot_degraded records whether real preranking snapshot persistence degraded visibly.
    # EN: Expected values are boolean truth values used for later workflow fallback decisions.
    # TR: preranking_snapshot_degraded, gerçek preranking snapshot persistence'ının görünür biçimde degrade olup olmadığını kaydeder.
    # TR: Beklenen değerler sonraki workflow fallback kararlarında kullanılan boolean doğrulardır.
    preranking_snapshot_degraded = bool(preranking_snapshot_result.get("preranking_degraded"))
    # EN: linked_snapshot_id stores the real snapshot id that the workflow row may link to.
    # EN: Expected values are an integer snapshot id or None when snapshot persistence degraded or failed visibly.
    # TR: linked_snapshot_id workflow satırının bağlanabileceği gerçek snapshot id değerini taşır.
    # TR: Beklenen değerler tamsayı snapshot id veya snapshot persistence görünür biçimde degrade/fail olduysa Nonedir.
    linked_snapshot_id = preranking_snapshot_result.get("snapshot_id")

    if linked_snapshot_id is None:
        # EN: effective_workflow_state is forced to review_hold because there is no snapshot id to link the workflow row to.
        # EN: Expected value in this branch is review_hold for explicit operator follow-up.
        # TR: effective_workflow_state workflow satırının bağlanacağı snapshot id bulunmadığı için review_holda zorlanır.
        # TR: Bu dalda beklenen değer açık operatör takibi için review_holddur.
        effective_workflow_state = "review_hold"
        if preranking_snapshot_degraded:
            # EN: effective_workflow_state_reason records the degraded no-row snapshot branch explicitly.
            # EN: Expected value is the no-row manual-review token shown below.
            # TR: effective_workflow_state_reason degrade no-row snapshot dalını açık biçimde kaydeder.
            # TR: Beklenen değer aşağıda görülen no-row manual-review tokenıdır.
            effective_workflow_state_reason = "preranking_snapshot_no_row_manual_review_required"
        else:
            # EN: effective_workflow_state_reason records the missing snapshot-id branch when no degraded marker exists.
            # EN: Expected value is the explicit missing-snapshot manual-review token shown below.
            # TR: effective_workflow_state_reason degrade işareti yokken eksik snapshot-id dalını açık biçimde kaydeder.
            # TR: Beklenen değer aşağıda görülen açık missing-snapshot manual-review tokenıdır.
            effective_workflow_state_reason = "preranking_snapshot_missing_manual_review_required"

    # EN: We write workflow state through the canonical DB helper and use the real
    # EN: preranking snapshot id.
    # TR: Workflow durumunu kanonik DB helper üzerinden yazıyor ve gerçek
    # TR: preranking snapshot id değerini kullanıyoruz.
    # EN: workflow_result stores the DB helper receipt returned after writing workflow state and snapshot linkage.
    # EN: Expected values are dict-like workflow persistence receipts.
    # TR: workflow_result, workflow durumu ve snapshot bağlantısı yazıldıktan sonra dönen DB helper makbuzunu taşır.
    # TR: Beklenen değerler dict-benzeri workflow persistence makbuzlarıdır.
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
            "taxonomy_candidate_count": len(persistable_taxonomy_candidates),
            "taxonomy_candidate_input_count": len(raw_taxonomy_candidates),
            "taxonomy_candidate_rejected_count": len(rejected_taxonomy_candidates),
            "taxonomy_candidate_rejected_sample": rejected_taxonomy_candidates[:10],
            "persisted_candidate_count": persisted_candidate_count,
            "persist_result_degraded": persist_result_degraded,
            "preranking_snapshot_degraded": preranking_snapshot_degraded,
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
