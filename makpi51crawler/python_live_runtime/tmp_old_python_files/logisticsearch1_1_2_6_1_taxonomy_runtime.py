"""
EN:
This file is the taxonomy-runtime child directly beneath the broader parse-runtime surface.

EN:
Why this file exists:
- because taxonomy-specific runtime truth should live in one explicit child instead of being diluted across the broader parse layer
- because canonical language order, taxonomy authority lookups, runtime matching, and taxonomy-facing selection/enrichment meaning must remain readable
- because a beginner should be able to find where parse-layer material becomes taxonomy-layer classification or tagging meaning without digging through unrelated parse helpers

EN:
What this file DOES:
- expose taxonomy-oriented runtime helper, class, and payload boundaries
- preserve visible taxonomy lookup, authority usage, language-aware matching, and degraded branch meaning
- keep taxonomy semantics separate from broader parse orchestration and separate from later storage/ranking layers

EN:
What this file DOES NOT do:
- it does not become the full parse runtime hub
- it does not become the full worker orchestrator
- it does not replace the canonical taxonomy database authority by itself
- it does not become the final ranking or outreach-decision layer

EN:
Topological role:
- parse runtime prepares or shapes material that can flow into this taxonomy child
- this file applies taxonomy-facing interpretation, matching, normalization, and language-aware structure
- later layers may consume taxonomy-shaped outputs for enrichment, selection, scoring, or other downstream decisions

EN:
Important visible values and shapes:
- taxonomy payloads => structured data prepared for taxonomy-aware runtime use
- language or locale-aware values => explicit indicators used to keep 25-language behavior readable
- authority-facing or match-facing structures => visible runtime shapes that explain how taxonomy was consulted
- degraded branch payloads => explicit non-happy taxonomy outcomes that must remain readable

EN:
Accepted architectural identity:
- taxonomy runtime child
- narrow taxonomy contract layer
- readable parse-to-taxonomy boundary

EN:
Undesired architectural identity:
- hidden second parse hub
- vague language helper dump
- hidden SQL engine
- hidden operator CLI surface

TR:
Bu dosya daha geniş parse-runtime yüzeyinin hemen altında duran taxonomy-runtime child yüzeyidir.

TR:
Bu dosya neden var:
- çünkü taxonomyye özgü runtime doğrusu daha geniş parse katmanı içinde dağılmak yerine tek ve açık child yüzeyde yaşamalıdır
- çünkü kanonik dil sırası, taxonomy authority lookup mantığı, runtime matching ve taxonomyye bakan selection/enrichment anlamı okunabilir kalmalıdır
- çünkü yeni başlayan biri parse katmanı malzemesinin nerede taxonomy katmanı sınıflandırma veya etiketleme anlamına dönüştüğünü ilgisiz parse yardımcıları arasında kaybolmadan bulabilmelidir

TR:
Bu dosya NE yapar:
- taxonomy odaklı runtime helper, class ve payload sınırlarını açığa çıkarır
- taxonomy lookup, authority kullanımı, language-aware matching ve degraded dal anlamını görünür tutar
- taxonomy semantiklerini daha geniş parse orkestrasyonundan ve sonraki storage/ranking katmanlarından ayrı tutar

TR:
Bu dosya NE yapmaz:
- tam parse runtime hubının kendisi olmaz
- tam worker orchestratorun kendisi olmaz
- kanonik taxonomy database authoritynin tek başına yerine geçmez
- final ranking veya outreach-decision katmanının kendisi olmaz

TR:
Topolojik rol:
- parse runtime bu taxonomy child yüzeyine akabilecek malzemeyi hazırlar veya şekillendirir
- bu dosya taxonomyye bakan yorumlama, matching, normalization ve language-aware yapı kurar
- sonraki katmanlar enrichment, selection, scoring veya başka downstream kararlar için taxonomy şekillendirilmiş çıktıları tüketebilir

TR:
Önemli görünür değerler ve şekiller:
- taxonomy payloadları => taxonomy-aware runtime kullanımına hazırlanan yapılı veri
- language veya locale-aware değerler => 25 dilli davranışı okunabilir tutmak için kullanılan açık göstergeler
- authority-facing veya match-facing yapılar => taxonomyye nasıl bakıldığını açıklayan görünür runtime şekilleri
- degraded dal payloadları => okunabilir kalması gereken mutlu-yol-dışı taxonomy sonuçları

TR:
Kabul edilen mimari kimlik:
- taxonomy runtime child
- dar taxonomy sözleşme katmanı
- okunabilir parse-to-taxonomy sınırı

TR:
İstenmeyen mimari kimlik:
- gizli ikinci parse hubı
- belirsiz dil yardımcıları çöplüğü
- gizli SQL motoru
- gizli operatör CLI yüzeyi
"""

# EN: We enable postponed evaluation of annotations so type hints stay readable
# EN: and forward references do not need eager runtime resolution.
# TR: Type hint'ler okunabilir kalsın ve forward reference'lar anında çözülmek
# TR: zorunda olmasın diye annotation çözümlemesini erteliyoruz.
# EN: TAXONOMY RUNTIME IDENTITY MEMORY BLOCK V6
# EN:
# EN: This file should be read as the narrow taxonomy corner of the parse corridor.
# EN: Beginner mental model:
# EN: - parse runtime extracts meaning from fetched material
# EN: - this child explains how that meaning is aligned with canonical taxonomy truth
# EN: - it exists so the crawler can later answer: which language-aware taxonomy signals were consulted, matched, or prepared
# EN:
# EN: Accepted architectural meaning:
# EN: - named taxonomy-runtime child
# EN: - focused language-aware taxonomy helper surface
# EN: - readable boundary for parse meaning becoming taxonomy-shaped meaning
# EN:
# EN: Undesired architectural meaning:
# EN: - random multilingual helper pile
# EN: - hidden second parse orchestrator
# EN: - place where taxonomy matching failures become invisible
# EN:
# EN: Important value-shape reminders:
# EN: - taxonomy-facing payloads should stay explicit
# EN: - language-aware matching results should stay structured and readable
# EN: - degraded taxonomy branches must remain visible
# TR: TAXONOMY RUNTIME KIMLIK HAFIZA BLOĞU V6
# TR:
# TR: Bu dosya parse koridorunun dar taxonomy köşesi gibi okunmalıdır.
# TR: Başlangıç seviyesi zihinsel model:
# TR: - parse runtime fetched malzemeden anlam çıkarır
# TR: - bu child o anlamın kanonik taxonomy doğrusu ile nasıl hizalandığını açıklar
# TR: - crawlerın daha sonra şu sorulara cevap verebilmesi için vardır: hangi language-aware taxonomy sinyalleri kullanıldı, eşleşti veya hazırlandı
# TR:
# TR: Kabul edilen mimari anlam:
# TR: - isimli taxonomy-runtime child
# TR: - odaklı language-aware taxonomy yardımcı yüzeyi
# TR: - parse anlamının taxonomy şekilli anlama dönüşmesi için okunabilir sınır
# TR:
# TR: İstenmeyen mimari anlam:
# TR: - rastgele multilingual helper yığını
# TR: - gizli ikinci parse orchestrator
# TR: - taxonomy matching hatalarının görünmez olduğu yer
# TR:
# TR: Önemli değer-şekli hatırlatmaları:
# TR: - taxonomyye bakan payloadlar açık kalmalıdır
# TR: - language-aware matching sonuçları yapılı ve okunabilir kalmalıdır
# TR: - degraded taxonomy dalları görünür kalmalıdır

from __future__ import annotations

# EN: We import dataclass because taxonomy match rows should travel through the
# EN: runtime as explicit, named, beginner-readable structured objects.
# TR: Taxonomy eşleşme satırları runtime içinde açık, isimli ve beginner-okunur
# TR: yapılı nesneler olarak taşınsın diye dataclass içe aktarıyoruz.
from dataclasses import dataclass

# EN: We import Any because some PostgreSQL-returned numeric/text fields may stay
# EN: lightly flexible until the scoring surface is sealed more tightly.
# TR: Bazı PostgreSQL dönen sayısal/metinsel alanlar skor yüzeyi daha sıkı
# TR: mühürlenene kadar hafif esnek kalabileceği için Any içe aktarıyoruz.
from typing import Any

# EN: We import os because the taxonomy DSN should be overridable explicitly from
# EN: the environment rather than hidden in code only.
# TR: Taxonomy DSN değeri yalnızca kod içinde gizli kalmasın, environment'dan da
# TR: açıkça override edilebilsin diye os içe aktarıyoruz.
import os

# EN: We import psycopg because taxonomy runtime reads are performed directly from
# EN: PostgreSQL through a second controlled read-only connection.
# TR: Taxonomy runtime okumaları ikinci kontrollü read-only bağlantı üzerinden
# TR: doğrudan PostgreSQL'den yapılacağı için psycopg içe aktarıyoruz.
import psycopg

# EN: We import dict_row so query results arrive as dictionary-like mappings with
# EN: explicit column names instead of positional tuples.
# TR: Sorgu sonuçları pozisyonel tuple yerine açık sütun adlarıyla dict-benzeri
# TR: mapping olarak gelsin diye dict_row içe aktarıyoruz.
from psycopg.rows import dict_row

# EN: This tuple is the explicit canonical 25-language order consumed by the
# EN: crawler/taxonomy runtime contract. It must stay byte-for-byte aligned with
# EN: the SQL taxonomy authority surface.
# TR: Bu tuple crawler/taxonomy runtime sözleşmesinin kullandığı açık kanonik
# TR: 25 dil sırasıdır. SQL taxonomy otorite yüzeyi ile byte-for-byte hizalı
# TR: kalmalıdır.
CANONICAL_LANGUAGE_ORDER: tuple[str, ...] = (
    "ar", "bg", "cs", "de", "el", "en", "es", "fr", "hu", "it",
    "ja", "ko", "nl", "pt", "ro", "ru", "tr", "zh", "hi", "bn",
    "ur", "uk", "id", "vi", "he",
)


# EN: This dataclass represents one runtime taxonomy match returned by the narrow
# EN: read-only lookup seam.
# TR: Bu dataclass dar read-only lookup seam'i tarafından döndürülen tek bir
# TR: runtime taxonomy eşleşmesini temsil eder.
@dataclass(slots=True)
# EN: TAXONOMY CLASS PURPOSE MEMORY BLOCK V6 / TaxonomyRuntimeMatch
# EN:
# EN: Why this class exists:
# EN: - because taxonomy-layer truth for 'TaxonomyRuntimeMatch' should be carried by a named structure instead of anonymous loose payload passing
# EN: - because beginners should be able to inspect field names and understand taxonomy-side role meaning directly
# EN:
# EN: Accepted role:
# EN: - named taxonomy payload, match shape, authority-facing structure, or structured result carrier
# EN: - visible field set currently detected here: node_id, node_code, domain_type, node_kind, lang_code, matched_surface, matched_text, match_score, lang_priority
# EN:
# EN: Common taxonomy meaning hints:
# EN: - this surface likely deals with taxonomy lookup, taxonomy matching, or language-aware runtime meaning
# EN: - explicit success vs degraded taxonomy meaning may matter here
# EN: - these helpers often decide whether later layers receive usable taxonomy-shaped payloads
# EN: - visible matched vs unmatched distinction is especially important here
# EN:
# EN: Undesired misunderstanding:
# EN: - treating this class as random container text with no taxonomy contract meaning
# EN: - collapsing its named shape into anonymous dict drift everywhere
# TR: TAXONOMY CLASS AMAÇ HAFIZA BLOĞU V6 / TaxonomyRuntimeMatch
# TR:
# TR: Bu sınıf neden var:
# TR: - çünkü 'TaxonomyRuntimeMatch' için taxonomy katmanı doğrusu isimsiz gevşek payload dolaştırmak yerine isimli yapı ile taşınmalıdır
# TR: - çünkü yeni başlayan biri alan isimlerini inceleyip taxonomy tarafı rol anlamını doğrudan anlayabilmelidir
# TR:
# TR: Kabul edilen rol:
# TR: - isimli taxonomy payloadı, match şekli, authorityye bakan yapı veya yapılı sonuç taşıyıcısı
# TR: - burada şu an tespit edilen görünür alan kümesi: node_id, node_code, domain_type, node_kind, lang_code, matched_surface, matched_text, match_score, lang_priority
# TR:
# TR: Ortak taxonomy anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle taxonomy lookup, taxonomy matching veya language-aware runtime anlamı ile ilgilenir
# TR: - açık success vs degraded taxonomy anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir taxonomy şekilli payload alıp almayacağını belirler
# TR: - görünür matched vs unmatched ayrımı burada özellikle önemlidir
# TR:
# TR: İstenmeyen yanlış anlama:
# TR: - bu sınıfı taxonomy sözleşme anlamı olmayan rastgele kap gibi görmek
# TR: - isimli şeklini yok sayıp her şeyi anonim dict driftine ezmek

# EN: STAGE21-AUTO-COMMENT :: TaxonomyRuntimeMatch is a top-level taxonomy runtime class in this file.
# EN: STAGE21-AUTO-COMMENT :: TaxonomyRuntimeMatch keeps an explicit runtime shape so taxonomy-facing data remains readable and auditable.
# TR: STAGE21-AUTO-COMMENT :: TaxonomyRuntimeMatch, bu dosyadaki ust-seviye taxonomy runtime class yuzeyidir.
# TR: STAGE21-AUTO-COMMENT :: TaxonomyRuntimeMatch, taxonomyye bakan runtime verisinin okunabilir ve denetlenebilir kalmasi icin acik bir sekil tasir.
class TaxonomyRuntimeMatch:
    # EN: node_id is the durable numeric identity of the matched taxonomy node.
    # TR: node_id eşleşen taxonomy düğümünün kalıcı sayısal kimliğidir.
    node_id: int

    # EN: node_code is the human-inspectable stable taxonomy code.
    # TR: node_code insan tarafından incelenebilir stabil taxonomy kodudur.
    node_code: str

    # EN: domain_type stores the major domain family of the matched node.
    # TR: domain_type eşleşen düğümün büyük alan ailesini tutar.
    domain_type: str

    # EN: node_kind stores the narrower runtime kind of the matched node.
    # TR: node_kind eşleşen düğümün daha dar runtime türünü tutar.
    node_kind: str

    # EN: lang_code stores which language row actually matched.
    # TR: lang_code gerçekte hangi dil satırının eşleştiğini tutar.
    lang_code: str

    # EN: matched_surface tells whether the hit came from translations or keywords.
    # TR: matched_surface vuruşun translations mı keywords mü yüzeyinden geldiğini söyler.
    matched_surface: str

    # EN: matched_text stores the exact runtime text that matched.
    # TR: matched_text eşleşen tam runtime metnini tutar.
    matched_text: str

    # EN: match_score is the current narrow numeric score used only for ordering.
    # TR: match_score şu an yalnızca sıralama için kullanılan dar sayısal skordur.
    match_score: Any

    # EN: lang_priority stores the explicit language-priority bucket used by the query.
    # TR: lang_priority sorgu tarafından kullanılan açık dil-öncelik kovasını tutar.
    lang_priority: int


# EN: This helper returns the default taxonomy DSN. The runtime should prefer an
# EN: explicit environment value and only then fall back to the controlled local default.
# TR: Bu yardımcı varsayılan taxonomy DSN değerini döndürür. Runtime önce açık
# TR: environment değerini tercih etmeli, ancak sonra kontrollü yerel varsayılana düşmelidir.
# EN: TAXONOMY FUNCTION PURPOSE MEMORY BLOCK V6 / taxonomy_default_dsn
# EN:
# EN: Why this function exists:
# EN: - because taxonomy truth for 'taxonomy_default_dsn' should be exposed through one named top-level helper boundary
# EN: - because taxonomy-side semantics should remain readable instead of being diluted inside broader parse orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: (no explicit parameters)
# EN: - values should match the current Python signature and the taxonomy contract below
# EN:
# EN: Accepted output:
# EN: - a taxonomy-oriented result shape defined by the current function body
# EN: - this may be a match result, prepared payload, authority-facing structure, language-aware shape, or another explicit taxonomy-side branch result
# EN:
# EN: Common taxonomy meaning hints:
# EN: - this surface likely deals with taxonomy lookup, taxonomy matching, or language-aware runtime meaning
# EN: - explicit success vs degraded taxonomy meaning may matter here
# EN: - these helpers often decide whether later layers receive usable taxonomy-shaped payloads
# EN: - visible matched vs unmatched distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is taxonomy-side helper logic, not the whole parse corridor
# EN: - taxonomy results must stay explicit so audits can understand success, degraded, unmatched, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague taxonomy results that hide branch meaning
# TR: TAXONOMY FUNCTION AMAÇ HAFIZA BLOĞU V6 / taxonomy_default_dsn
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'taxonomy_default_dsn' için taxonomy doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü taxonomy tarafı semantiklerinin daha geniş parse orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: (açık parametre yok)
# TR: - değerler aşağıdaki mevcut Python imzası ve taxonomy sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen taxonomy odaklı sonuç şekli
# TR: - bu; match sonucu, hazırlanmış payload, authorityye bakan yapı, language-aware şekil veya başka açık taxonomy tarafı dal sonucu olabilir
# TR:
# TR: Ortak taxonomy anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle taxonomy lookup, taxonomy matching veya language-aware runtime anlamı ile ilgilenir
# TR: - açık success vs degraded taxonomy anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir taxonomy şekilli payload alıp almayacağını belirler
# TR: - görünür matched vs unmatched ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon taxonomy tarafı yardımcı mantığıdır, parse koridorunun tamamı değildir
# TR: - taxonomy sonuçları açık kalmalıdır ki denetimler success, degraded, unmatched ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz taxonomy sonuçları

# EN: STAGE21-AUTO-COMMENT :: taxonomy_default_dsn is a top-level taxonomy runtime function in this file.
# EN: STAGE21-AUTO-COMMENT :: taxonomy_default_dsn must keep its runtime contract explicit so taxonomy-side meaning does not become vague.
# TR: STAGE21-AUTO-COMMENT :: taxonomy_default_dsn, bu dosyadaki ust-seviye taxonomy runtime fonksiyonudur.
# TR: STAGE21-AUTO-COMMENT :: taxonomy_default_dsn, taxonomy tarafi anlamin belirsizlesmemesi icin runtime sozlesmesini acik tutmalidir.
def taxonomy_default_dsn() -> str:
    # EN: We first check the dedicated taxonomy DSN variable because a second DB
    # EN: connection should be explicit at operator level.
    # TR: Önce ayrılmış taxonomy DSN değişkenini kontrol ediyoruz; çünkü ikinci DB
    # TR: bağlantısı operatör seviyesinde açık olmalıdır.
# EN: STAGE21-AUTO-COMMENT :: env_value is a function-local value inside taxonomy_default_dsn.
# EN: STAGE21-AUTO-COMMENT :: We keep env_value explicit so later readers can trace how taxonomy_default_dsn shapes intermediate taxonomy runtime state.
# TR: STAGE21-AUTO-COMMENT :: env_value, taxonomy_default_dsn icindeki function-local degerdir.
# TR: STAGE21-AUTO-COMMENT :: env_value adini acik tutuyoruz; boylece sonraki okuyucular taxonomy_default_dsn fonksiyonunun ara taxonomy runtime durumunu nasil sekillendirdigini izleyebilir.
    env_value = os.getenv("LOGISTICSEARCH_TAXONOMY_DSN")

    # EN: If the operator provided a non-empty DSN, we trust and return it.
    # TR: Operatör boş olmayan bir DSN verdiyse ona güvenip geri döndürüyoruz.
    if env_value:
        return env_value

    # EN: Otherwise we use the current controlled live-runtime default.
    # TR: Aksi durumda mevcut kontrollü canlı-runtime varsayımını kullanıyoruz.
    return "dbname=logisticsearch_taxonomy user=makpi51"


# EN: This helper opens one read-only-style taxonomy connection using psycopg.
# EN: We keep autocommit disabled and transaction control explicit for auditability.
# TR: Bu yardımcı psycopg ile tek bir read-only-tarzı taxonomy bağlantısı açar.
# TR: Denetlenebilirlik için autocommit kapalı ve transaction kontrolü açık kalır.
# EN: TAXONOMY FUNCTION PURPOSE MEMORY BLOCK V6 / connect_taxonomy_db
# EN:
# EN: Why this function exists:
# EN: - because taxonomy truth for 'connect_taxonomy_db' should be exposed through one named top-level helper boundary
# EN: - because taxonomy-side semantics should remain readable instead of being diluted inside broader parse orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: dsn
# EN: - values should match the current Python signature and the taxonomy contract below
# EN:
# EN: Accepted output:
# EN: - a taxonomy-oriented result shape defined by the current function body
# EN: - this may be a match result, prepared payload, authority-facing structure, language-aware shape, or another explicit taxonomy-side branch result
# EN:
# EN: Common taxonomy meaning hints:
# EN: - this surface likely deals with taxonomy lookup, taxonomy matching, or language-aware runtime meaning
# EN: - explicit success vs degraded taxonomy meaning may matter here
# EN: - these helpers often decide whether later layers receive usable taxonomy-shaped payloads
# EN: - visible matched vs unmatched distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is taxonomy-side helper logic, not the whole parse corridor
# EN: - taxonomy results must stay explicit so audits can understand success, degraded, unmatched, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague taxonomy results that hide branch meaning
# TR: TAXONOMY FUNCTION AMAÇ HAFIZA BLOĞU V6 / connect_taxonomy_db
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'connect_taxonomy_db' için taxonomy doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü taxonomy tarafı semantiklerinin daha geniş parse orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: dsn
# TR: - değerler aşağıdaki mevcut Python imzası ve taxonomy sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen taxonomy odaklı sonuç şekli
# TR: - bu; match sonucu, hazırlanmış payload, authorityye bakan yapı, language-aware şekil veya başka açık taxonomy tarafı dal sonucu olabilir
# TR:
# TR: Ortak taxonomy anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle taxonomy lookup, taxonomy matching veya language-aware runtime anlamı ile ilgilenir
# TR: - açık success vs degraded taxonomy anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir taxonomy şekilli payload alıp almayacağını belirler
# TR: - görünür matched vs unmatched ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon taxonomy tarafı yardımcı mantığıdır, parse koridorunun tamamı değildir
# TR: - taxonomy sonuçları açık kalmalıdır ki denetimler success, degraded, unmatched ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz taxonomy sonuçları

# EN: STAGE21-AUTO-COMMENT :: connect_taxonomy_db is a top-level taxonomy runtime function in this file.
# EN: STAGE21-AUTO-COMMENT :: connect_taxonomy_db must keep its runtime contract explicit so taxonomy-side meaning does not become vague.
# TR: STAGE21-AUTO-COMMENT :: connect_taxonomy_db, bu dosyadaki ust-seviye taxonomy runtime fonksiyonudur.
# TR: STAGE21-AUTO-COMMENT :: connect_taxonomy_db, taxonomy tarafi anlamin belirsizlesmemesi icin runtime sozlesmesini acik tutmalidir.
# EN: STAGE21-AUTO-COMMENT :: Parameter dsn is an explicit input of connect_taxonomy_db and should stay visible in the function contract.
# TR: STAGE21-AUTO-COMMENT :: dsn parametresi, connect_taxonomy_db fonksiyonunun acik girdisidir ve fonksiyon sozlesmesinde gorunur kalmalidir.
def connect_taxonomy_db(dsn: str) -> psycopg.Connection:
    # EN: We connect with dict_row so callers can read by column name.
    # TR: Çağıranlar sütun adına göre okuyabilsin diye dict_row ile bağlanıyoruz.
# EN: STAGE21-AUTO-COMMENT :: conn is a function-local value inside connect_taxonomy_db.
# EN: STAGE21-AUTO-COMMENT :: We keep conn explicit so later readers can trace how connect_taxonomy_db shapes intermediate taxonomy runtime state.
# TR: STAGE21-AUTO-COMMENT :: conn, connect_taxonomy_db icindeki function-local degerdir.
# TR: STAGE21-AUTO-COMMENT :: conn adini acik tutuyoruz; boylece sonraki okuyucular connect_taxonomy_db fonksiyonunun ara taxonomy runtime durumunu nasil sekillendirdigini izleyebilir.
    conn = psycopg.connect(dsn, row_factory=dict_row)

    # EN: We return the open connection to the caller.
    # TR: Açık bağlantıyı çağırana döndürüyoruz.
    return conn


# EN: This helper normalizes incoming query text before it is compared against the
# EN: normalized runtime translation/keyword surfaces.
# TR: Bu yardımcı gelen sorgu metnini normalize eder; sonra bu metin normalize edilmiş
# TR: runtime translation/keyword yüzeylerine karşı karşılaştırılır.
# EN: TAXONOMY FUNCTION PURPOSE MEMORY BLOCK V6 / normalize_taxonomy_query_text
# EN:
# EN: Why this function exists:
# EN: - because taxonomy truth for 'normalize_taxonomy_query_text' should be exposed through one named top-level helper boundary
# EN: - because taxonomy-side semantics should remain readable instead of being diluted inside broader parse orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: query_text
# EN: - values should match the current Python signature and the taxonomy contract below
# EN:
# EN: Accepted output:
# EN: - a taxonomy-oriented result shape defined by the current function body
# EN: - this may be a match result, prepared payload, authority-facing structure, language-aware shape, or another explicit taxonomy-side branch result
# EN:
# EN: Common taxonomy meaning hints:
# EN: - this surface likely deals with taxonomy lookup, taxonomy matching, or language-aware runtime meaning
# EN: - explicit success vs degraded taxonomy meaning may matter here
# EN: - these helpers often decide whether later layers receive usable taxonomy-shaped payloads
# EN: - visible matched vs unmatched distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is taxonomy-side helper logic, not the whole parse corridor
# EN: - taxonomy results must stay explicit so audits can understand success, degraded, unmatched, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague taxonomy results that hide branch meaning
# TR: TAXONOMY FUNCTION AMAÇ HAFIZA BLOĞU V6 / normalize_taxonomy_query_text
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'normalize_taxonomy_query_text' için taxonomy doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü taxonomy tarafı semantiklerinin daha geniş parse orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: query_text
# TR: - değerler aşağıdaki mevcut Python imzası ve taxonomy sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen taxonomy odaklı sonuç şekli
# TR: - bu; match sonucu, hazırlanmış payload, authorityye bakan yapı, language-aware şekil veya başka açık taxonomy tarafı dal sonucu olabilir
# TR:
# TR: Ortak taxonomy anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle taxonomy lookup, taxonomy matching veya language-aware runtime anlamı ile ilgilenir
# TR: - açık success vs degraded taxonomy anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir taxonomy şekilli payload alıp almayacağını belirler
# TR: - görünür matched vs unmatched ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon taxonomy tarafı yardımcı mantığıdır, parse koridorunun tamamı değildir
# TR: - taxonomy sonuçları açık kalmalıdır ki denetimler success, degraded, unmatched ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz taxonomy sonuçları

# EN: STAGE21-AUTO-COMMENT :: normalize_taxonomy_query_text is a top-level taxonomy runtime function in this file.
# EN: STAGE21-AUTO-COMMENT :: normalize_taxonomy_query_text must keep its runtime contract explicit so taxonomy-side meaning does not become vague.
# TR: STAGE21-AUTO-COMMENT :: normalize_taxonomy_query_text, bu dosyadaki ust-seviye taxonomy runtime fonksiyonudur.
# TR: STAGE21-AUTO-COMMENT :: normalize_taxonomy_query_text, taxonomy tarafi anlamin belirsizlesmemesi icin runtime sozlesmesini acik tutmalidir.
# EN: STAGE21-AUTO-COMMENT :: Parameter query_text is an explicit input of normalize_taxonomy_query_text and should stay visible in the function contract.
# TR: STAGE21-AUTO-COMMENT :: query_text parametresi, normalize_taxonomy_query_text fonksiyonunun acik girdisidir ve fonksiyon sozlesmesinde gorunur kalmalidir.
def normalize_taxonomy_query_text(query_text: str) -> str:
    # EN: We strip outer whitespace first because surrounding spaces carry no meaning.
    # TR: Dış boşluklar anlam taşımadığı için önce onları kırpıyoruz.
# EN: STAGE21-AUTO-COMMENT :: normalized_text is a function-local value inside normalize_taxonomy_query_text.
# EN: STAGE21-AUTO-COMMENT :: We keep normalized_text explicit so later readers can trace how normalize_taxonomy_query_text shapes intermediate taxonomy runtime state.
# TR: STAGE21-AUTO-COMMENT :: normalized_text, normalize_taxonomy_query_text icindeki function-local degerdir.
# TR: STAGE21-AUTO-COMMENT :: normalized_text adini acik tutuyoruz; boylece sonraki okuyucular normalize_taxonomy_query_text fonksiyonunun ara taxonomy runtime durumunu nasil sekillendirdigini izleyebilir.
    normalized_text = query_text.strip()

    # EN: We lower-case the text because current runtime normalized columns are
    # EN: designed for case-insensitive comparison.
    # TR: Mevcut runtime normalize sütunları büyük/küçük harf duyarsız karşılaştırma
    # TR: için tasarlandığı için metni küçük harfe indiriyoruz.
# EN: STAGE21-AUTO-COMMENT :: normalized_text is a function-local value inside normalize_taxonomy_query_text.
# EN: STAGE21-AUTO-COMMENT :: We keep normalized_text explicit so later readers can trace how normalize_taxonomy_query_text shapes intermediate taxonomy runtime state.
# TR: STAGE21-AUTO-COMMENT :: normalized_text, normalize_taxonomy_query_text icindeki function-local degerdir.
# TR: STAGE21-AUTO-COMMENT :: normalized_text adini acik tutuyoruz; boylece sonraki okuyucular normalize_taxonomy_query_text fonksiyonunun ara taxonomy runtime durumunu nasil sekillendirdigini izleyebilir.
    normalized_text = normalized_text.lower()

    # EN: We collapse repeated whitespace so the query shape becomes more stable.
    # TR: Tekrarlayan boşlukları indiriyoruz; böylece sorgu şekli daha stabil oluyor.
# EN: STAGE21-AUTO-COMMENT :: normalized_text is a function-local value inside normalize_taxonomy_query_text.
# EN: STAGE21-AUTO-COMMENT :: We keep normalized_text explicit so later readers can trace how normalize_taxonomy_query_text shapes intermediate taxonomy runtime state.
# TR: STAGE21-AUTO-COMMENT :: normalized_text, normalize_taxonomy_query_text icindeki function-local degerdir.
# TR: STAGE21-AUTO-COMMENT :: normalized_text adini acik tutuyoruz; boylece sonraki okuyucular normalize_taxonomy_query_text fonksiyonunun ara taxonomy runtime durumunu nasil sekillendirdigini izleyebilir.
    normalized_text = " ".join(normalized_text.split())

    # EN: We return the final normalized form.
    # TR: Son normalize edilmiş biçimi döndürüyoruz.
    return normalized_text


# EN: This helper fetches one compact identity/count snapshot from the runtime
# EN: taxonomy database so callers can prove they connected to the expected surface.
# TR: Bu yardımcı runtime taxonomy veritabanından tek bir kompakt kimlik/sayım
# TR: özeti çeker; böylece çağıranlar beklenen yüzeye bağlandığını kanıtlayabilir.
# EN: TAXONOMY FUNCTION PURPOSE MEMORY BLOCK V6 / fetch_taxonomy_runtime_identity_counts
# EN:
# EN: Why this function exists:
# EN: - because taxonomy truth for 'fetch_taxonomy_runtime_identity_counts' should be exposed through one named top-level helper boundary
# EN: - because taxonomy-side semantics should remain readable instead of being diluted inside broader parse orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn
# EN: - values should match the current Python signature and the taxonomy contract below
# EN:
# EN: Accepted output:
# EN: - a taxonomy-oriented result shape defined by the current function body
# EN: - this may be a match result, prepared payload, authority-facing structure, language-aware shape, or another explicit taxonomy-side branch result
# EN:
# EN: Common taxonomy meaning hints:
# EN: - this surface likely deals with taxonomy lookup, taxonomy matching, or language-aware runtime meaning
# EN: - explicit success vs degraded taxonomy meaning may matter here
# EN: - these helpers often decide whether later layers receive usable taxonomy-shaped payloads
# EN: - visible matched vs unmatched distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is taxonomy-side helper logic, not the whole parse corridor
# EN: - taxonomy results must stay explicit so audits can understand success, degraded, unmatched, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague taxonomy results that hide branch meaning
# TR: TAXONOMY FUNCTION AMAÇ HAFIZA BLOĞU V6 / fetch_taxonomy_runtime_identity_counts
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'fetch_taxonomy_runtime_identity_counts' için taxonomy doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü taxonomy tarafı semantiklerinin daha geniş parse orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn
# TR: - değerler aşağıdaki mevcut Python imzası ve taxonomy sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen taxonomy odaklı sonuç şekli
# TR: - bu; match sonucu, hazırlanmış payload, authorityye bakan yapı, language-aware şekil veya başka açık taxonomy tarafı dal sonucu olabilir
# TR:
# TR: Ortak taxonomy anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle taxonomy lookup, taxonomy matching veya language-aware runtime anlamı ile ilgilenir
# TR: - açık success vs degraded taxonomy anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir taxonomy şekilli payload alıp almayacağını belirler
# TR: - görünür matched vs unmatched ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon taxonomy tarafı yardımcı mantığıdır, parse koridorunun tamamı değildir
# TR: - taxonomy sonuçları açık kalmalıdır ki denetimler success, degraded, unmatched ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz taxonomy sonuçları

# EN: STAGE21-AUTO-COMMENT :: fetch_taxonomy_runtime_identity_counts is a top-level taxonomy runtime function in this file.
# EN: STAGE21-AUTO-COMMENT :: fetch_taxonomy_runtime_identity_counts must keep its runtime contract explicit so taxonomy-side meaning does not become vague.
# TR: STAGE21-AUTO-COMMENT :: fetch_taxonomy_runtime_identity_counts, bu dosyadaki ust-seviye taxonomy runtime fonksiyonudur.
# TR: STAGE21-AUTO-COMMENT :: fetch_taxonomy_runtime_identity_counts, taxonomy tarafi anlamin belirsizlesmemesi icin runtime sozlesmesini acik tutmalidir.
# EN: STAGE21-AUTO-COMMENT :: Parameter conn is an explicit input of fetch_taxonomy_runtime_identity_counts and should stay visible in the function contract.
# TR: STAGE21-AUTO-COMMENT :: conn parametresi, fetch_taxonomy_runtime_identity_counts fonksiyonunun acik girdisidir ve fonksiyon sozlesmesinde gorunur kalmalidir.
def fetch_taxonomy_runtime_identity_counts(conn: psycopg.Connection) -> dict[str, Any]:
    # EN: We open one cursor for the compact read-only snapshot query.
    # TR: Kompakt read-only özet sorgusu için tek bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We select the current DB identity and the main runtime counts together
        # EN: so the proof stays compact and explicit.
        # TR: Kanıt kompakt ve açık kalsın diye mevcut DB kimliğini ve ana runtime
        # TR: sayımlarını birlikte seçiyoruz.
        cur.execute(
            """
            SELECT
              current_database() AS db_name,
              current_user AS db_user,
              (SELECT count(*)::bigint FROM logistics.supported_languages)        AS supported_languages,
              (SELECT count(*)::bigint FROM logistics.taxonomy_nodes)             AS taxonomy_nodes,
              (SELECT count(*)::bigint FROM logistics.taxonomy_node_translations) AS taxonomy_node_translations,
              (SELECT count(*)::bigint FROM logistics.taxonomy_keywords)          AS taxonomy_keywords,
              (SELECT count(*)::bigint FROM logistics.taxonomy_closure)           AS taxonomy_closure
            """
        )

        # EN: We fetch exactly one row because this proof query returns one compact snapshot.
        # TR: Bu kanıt sorgusu tek bir kompakt özet döndürdüğü için tam bir satır çekiyoruz.
        row = cur.fetchone()

    # EN: We return the raw mapping directly because its shape is already explicit.
    # TR: Şekli zaten açık olduğu için ham mapping'i doğrudan döndürüyoruz.
    return row


# EN: This helper performs one deliberately narrow runtime lookup against the 25-language
# EN: taxonomy surfaces. It is not final ranking logic. It is only the first controlled seam.
# TR: Bu yardımcı 25 dilli taxonomy yüzeylerine karşı bilinçli olarak dar bir runtime
# TR: lookup yapar. Bu nihai ranking mantığı değildir. Yalnızca ilk kontrollü seam'dir.
# EN: TAXONOMY FUNCTION PURPOSE MEMORY BLOCK V6 / search_runtime_taxonomy
# EN:
# EN: Why this function exists:
# EN: - because taxonomy truth for 'search_runtime_taxonomy' should be exposed through one named top-level helper boundary
# EN: - because taxonomy-side semantics should remain readable instead of being diluted inside broader parse orchestration
# EN:
# EN: Accepted input:
# EN: - the explicit parameters of this function are: conn, query_text, input_lang_code, limit
# EN: - values should match the current Python signature and the taxonomy contract below
# EN:
# EN: Accepted output:
# EN: - a taxonomy-oriented result shape defined by the current function body
# EN: - this may be a match result, prepared payload, authority-facing structure, language-aware shape, or another explicit taxonomy-side branch result
# EN:
# EN: Common taxonomy meaning hints:
# EN: - this surface likely deals with taxonomy lookup, taxonomy matching, or language-aware runtime meaning
# EN: - explicit success vs degraded taxonomy meaning may matter here
# EN: - these helpers often decide whether later layers receive usable taxonomy-shaped payloads
# EN: - visible matched vs unmatched distinction is especially important here
# EN:
# EN: Important beginner reminder:
# EN: - this function is taxonomy-side helper logic, not the whole parse corridor
# EN: - taxonomy results must stay explicit so audits can understand success, degraded, unmatched, and downstream handoff meaning
# EN:
# EN: Undesired behavior:
# EN: - silent payload mutation
# EN: - vague taxonomy results that hide branch meaning
# TR: TAXONOMY FUNCTION AMAÇ HAFIZA BLOĞU V6 / search_runtime_taxonomy
# TR:
# TR: Bu fonksiyon neden var:
# TR: - çünkü 'search_runtime_taxonomy' için taxonomy doğrusu tek ve isimli top-level yardımcı sınırı üzerinden açığa çıkmalıdır
# TR: - çünkü taxonomy tarafı semantiklerinin daha geniş parse orkestrasyonu içinde seyrelmemesi gerekir
# TR:
# TR: Kabul edilen girdi:
# TR: - bu fonksiyonun açık parametreleri şunlardır: conn, query_text, input_lang_code, limit
# TR: - değerler aşağıdaki mevcut Python imzası ve taxonomy sözleşmesi ile uyumlu olmalıdır
# TR:
# TR: Kabul edilen çıktı:
# TR: - mevcut fonksiyon gövdesi tarafından belirlenen taxonomy odaklı sonuç şekli
# TR: - bu; match sonucu, hazırlanmış payload, authorityye bakan yapı, language-aware şekil veya başka açık taxonomy tarafı dal sonucu olabilir
# TR:
# TR: Ortak taxonomy anlam ipuçları:
# TR: - bu yüzey büyük ihtimalle taxonomy lookup, taxonomy matching veya language-aware runtime anlamı ile ilgilenir
# TR: - açık success vs degraded taxonomy anlamı burada önemli olabilir
# TR: - bu tür yardımcılar çoğu zaman sonraki katmanların kullanılabilir taxonomy şekilli payload alıp almayacağını belirler
# TR: - görünür matched vs unmatched ayrımı burada özellikle önemlidir
# TR:
# TR: Önemli başlangıç hatırlatması:
# TR: - bu fonksiyon taxonomy tarafı yardımcı mantığıdır, parse koridorunun tamamı değildir
# TR: - taxonomy sonuçları açık kalmalıdır ki denetimler success, degraded, unmatched ve downstream handoff anlamını anlayabilsin
# TR:
# TR: İstenmeyen davranış:
# TR: - sessiz payload değişimi
# TR: - dal anlamını gizleyen belirsiz taxonomy sonuçları

# EN: STAGE21-AUTO-COMMENT :: search_runtime_taxonomy is a top-level taxonomy runtime function in this file.
# EN: STAGE21-AUTO-COMMENT :: search_runtime_taxonomy must keep its runtime contract explicit so taxonomy-side meaning does not become vague.
# TR: STAGE21-AUTO-COMMENT :: search_runtime_taxonomy, bu dosyadaki ust-seviye taxonomy runtime fonksiyonudur.
# TR: STAGE21-AUTO-COMMENT :: search_runtime_taxonomy, taxonomy tarafi anlamin belirsizlesmemesi icin runtime sozlesmesini acik tutmalidir.
# EN: STAGE21-AUTO-COMMENT :: Parameter conn is an explicit input of search_runtime_taxonomy and should stay visible in the function contract.
# TR: STAGE21-AUTO-COMMENT :: conn parametresi, search_runtime_taxonomy fonksiyonunun acik girdisidir ve fonksiyon sozlesmesinde gorunur kalmalidir.
# EN: STAGE21-AUTO-COMMENT :: Parameter query_text is an explicit input of search_runtime_taxonomy and should stay visible in the function contract.
# TR: STAGE21-AUTO-COMMENT :: query_text parametresi, search_runtime_taxonomy fonksiyonunun acik girdisidir ve fonksiyon sozlesmesinde gorunur kalmalidir.
# EN: STAGE21-AUTO-COMMENT :: Parameter input_lang_code is an explicit input of search_runtime_taxonomy and should stay visible in the function contract.
# TR: STAGE21-AUTO-COMMENT :: input_lang_code parametresi, search_runtime_taxonomy fonksiyonunun acik girdisidir ve fonksiyon sozlesmesinde gorunur kalmalidir.
# EN: STAGE21-AUTO-COMMENT :: Parameter limit is an explicit input of search_runtime_taxonomy and should stay visible in the function contract.
# TR: STAGE21-AUTO-COMMENT :: limit parametresi, search_runtime_taxonomy fonksiyonunun acik girdisidir ve fonksiyon sozlesmesinde gorunur kalmalidir.
def search_runtime_taxonomy(
    conn: psycopg.Connection,
    *,
    query_text: str,
    input_lang_code: str | None = None,
    limit: int = 20,
) -> list[TaxonomyRuntimeMatch]:
    # EN: We normalize the external query first so runtime matching stays stable.
    # TR: Runtime eşleşmesi stabil kalsın diye dış sorguyu önce normalize ediyoruz.
# EN: STAGE21-AUTO-COMMENT :: normalized_query_text is a function-local value inside search_runtime_taxonomy.
# EN: STAGE21-AUTO-COMMENT :: We keep normalized_query_text explicit so later readers can trace how search_runtime_taxonomy shapes intermediate taxonomy runtime state.
# TR: STAGE21-AUTO-COMMENT :: normalized_query_text, search_runtime_taxonomy icindeki function-local degerdir.
# TR: STAGE21-AUTO-COMMENT :: normalized_query_text adini acik tutuyoruz; boylece sonraki okuyucular search_runtime_taxonomy fonksiyonunun ara taxonomy runtime durumunu nasil sekillendirdigini izleyebilir.
    normalized_query_text = normalize_taxonomy_query_text(query_text)

    # EN: Empty normalized text must not hit the DB because that would be noisy and misleading.
    # TR: Boş normalize metin DB'ye gitmemelidir; aksi gürültülü ve yanıltıcı olur.
    if normalized_query_text == "":
        return []

    # EN: We clamp the limit into a safe narrow range so callers cannot accidentally
    # EN: request a huge uncontrolled result set.
    # TR: Çağıranlar kazara devasa ve kontrolsüz sonuç kümesi istemesin diye limit
    # TR: değerini güvenli ve dar aralığa sıkıştırıyoruz.
# EN: STAGE21-AUTO-COMMENT :: safe_limit is a function-local value inside search_runtime_taxonomy.
# EN: STAGE21-AUTO-COMMENT :: We keep safe_limit explicit so later readers can trace how search_runtime_taxonomy shapes intermediate taxonomy runtime state.
# TR: STAGE21-AUTO-COMMENT :: safe_limit, search_runtime_taxonomy icindeki function-local degerdir.
# TR: STAGE21-AUTO-COMMENT :: safe_limit adini acik tutuyoruz; boylece sonraki okuyucular search_runtime_taxonomy fonksiyonunun ara taxonomy runtime durumunu nasil sekillendirdigini izleyebilir.
    safe_limit = max(1, min(limit, 100))

    # EN: We build one contains-pattern once because both translation and keyword
    # EN: surfaces use the same normalized contains check.
    # TR: Hem translation hem keyword yüzeyi aynı normalize contains kontrolünü
    # TR: kullandığı için contains-pattern değerini bir kez kuruyoruz.
# EN: STAGE21-AUTO-COMMENT :: contains_pattern is a function-local value inside search_runtime_taxonomy.
# EN: STAGE21-AUTO-COMMENT :: We keep contains_pattern explicit so later readers can trace how search_runtime_taxonomy shapes intermediate taxonomy runtime state.
# TR: STAGE21-AUTO-COMMENT :: contains_pattern, search_runtime_taxonomy icindeki function-local degerdir.
# TR: STAGE21-AUTO-COMMENT :: contains_pattern adini acik tutuyoruz; boylece sonraki okuyucular search_runtime_taxonomy fonksiyonunun ara taxonomy runtime durumunu nasil sekillendirdigini izleyebilir.
    contains_pattern = f"%{normalized_query_text}%"

    # EN: We open a cursor for the single narrow search query.
    # TR: Tek dar arama sorgusu için bir cursor açıyoruz.
    with conn.cursor() as cur:
        # EN: We query translations and keywords together, but still keep the SQL
        # EN: intentionally simple and inspectable.
        # TR: Translation ve keyword yüzeylerini birlikte sorguluyoruz; ama SQL'i
        # TR: yine de bilinçli olarak sade ve incelenebilir tutuyoruz.
        cur.execute(
            """
            WITH language_priority AS (
                SELECT %(input_lang_code)s::text AS lang_code, 0 AS lang_priority
                WHERE %(input_lang_code)s::text IS NOT NULL
                  AND btrim(%(input_lang_code)s::text) <> ''

                UNION ALL
                SELECT 'en'::text, 1
                UNION ALL
                SELECT 'tr'::text, 2
                UNION ALL
                SELECT 'de'::text, 3
            ),
            translation_hits AS (
                SELECT
                    n.id AS node_id,
                    n.node_code,
                    n.domain_type,
                    n.node_kind,
                    t.lang_code,
                    'translation'::text AS matched_surface,
                    t.title AS matched_text,
                    CASE
                        WHEN t.title_normalized = %(normalized_query_text)s THEN 100.0::numeric
                        WHEN t.title_normalized LIKE %(contains_pattern)s THEN 80.0::numeric
                        ELSE round((similarity(t.title_normalized, %(normalized_query_text)s) * 100.0)::numeric, 4)
                    END AS match_score,
                    COALESCE(lp.lang_priority, 50) AS lang_priority
                FROM logistics.taxonomy_nodes AS n
                JOIN logistics.taxonomy_node_translations AS t
                  ON t.node_id = n.id
                LEFT JOIN language_priority AS lp
                  ON lp.lang_code = t.lang_code
                WHERE n.is_active = true
                  AND (
                        t.title_normalized = %(normalized_query_text)s
                     OR t.title_normalized LIKE %(contains_pattern)s
                     OR similarity(t.title_normalized, %(normalized_query_text)s) >= 0.35
                  )
            ),
            keyword_hits AS (
                SELECT
                    n.id AS node_id,
                    n.node_code,
                    n.domain_type,
                    n.node_kind,
                    k.lang_code,
                    'keyword'::text AS matched_surface,
                    k.keyword AS matched_text,
                    CASE
                        WHEN k.keyword_normalized = %(normalized_query_text)s THEN 100.0::numeric
                        WHEN k.keyword_normalized LIKE %(contains_pattern)s THEN 80.0::numeric
                        ELSE round((similarity(k.keyword_normalized, %(normalized_query_text)s) * 100.0)::numeric, 4)
                    END AS match_score,
                    COALESCE(lp.lang_priority, 50) AS lang_priority
                FROM logistics.taxonomy_nodes AS n
                JOIN logistics.taxonomy_keywords AS k
                  ON k.node_id = n.id
                LEFT JOIN language_priority AS lp
                  ON lp.lang_code = k.lang_code
                WHERE n.is_active = true
                  AND (
                        k.keyword_normalized = %(normalized_query_text)s
                     OR k.keyword_normalized LIKE %(contains_pattern)s
                     OR similarity(k.keyword_normalized, %(normalized_query_text)s) >= 0.35
                  )
            ),
            combined_hits AS (
                SELECT * FROM translation_hits
                UNION ALL
                SELECT * FROM keyword_hits
            ),
            ranked_hits AS (
                SELECT
                    node_id,
                    node_code,
                    domain_type,
                    node_kind,
                    lang_code,
                    matched_surface,
                    matched_text,
                    match_score,
                    lang_priority,
                    row_number() OVER (
                        PARTITION BY node_id, lang_code, matched_surface, matched_text
                        ORDER BY match_score DESC, lang_priority ASC, node_id ASC
                    ) AS dedupe_rank
                FROM combined_hits
            )
            SELECT
                node_id,
                node_code,
                domain_type,
                node_kind,
                lang_code,
                matched_surface,
                matched_text,
                match_score,
                lang_priority
            FROM ranked_hits
            WHERE dedupe_rank = 1
            ORDER BY
                match_score DESC,
                lang_priority ASC,
                node_id ASC,
                matched_surface ASC,
                lang_code ASC
            LIMIT %(safe_limit)s
            """,
            {
                "input_lang_code": input_lang_code,
                "normalized_query_text": normalized_query_text,
                "contains_pattern": contains_pattern,
                "safe_limit": safe_limit,
            },
        )

        # EN: We fetch all rows because the limit is already clamped and explicit.
        # TR: Limit zaten sıkıştırılmış ve açık olduğu için tüm satırları çekiyoruz.
        rows = cur.fetchall()

    # EN: We convert every row into the shaped dataclass so later runtime layers do
    # EN: not depend on loose dict shapes.
    # TR: Sonraki runtime katmanları gevşek dict şekillerine bağlı kalmasın diye her
    # TR: satırı şekilli dataclass nesnesine dönüştürüyoruz.
    return [
        TaxonomyRuntimeMatch(
            node_id=row["node_id"],
            node_code=row["node_code"],
            domain_type=row["domain_type"],
            node_kind=row["node_kind"],
            lang_code=row["lang_code"],
            matched_surface=row["matched_surface"],
            matched_text=row["matched_text"],
            match_score=row["match_score"],
            lang_priority=row["lang_priority"],
        )
        for row in rows
    ]
