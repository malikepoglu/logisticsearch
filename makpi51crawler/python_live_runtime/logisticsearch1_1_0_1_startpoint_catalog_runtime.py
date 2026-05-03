# =============================================================================
# STRICT_STARTPOINT_RUNTIME_VARIABLE_CONTRACT_EN_TR
# =============================================================================
# EN: This block is a beginner-first variable contract for this startpoint runtime
# EN: module. It explains the important variable names, what values they are
# EN: expected to carry, and which values must raise errors or be rejected.
# TR: Bu blok, bu startpoint runtime modülü için başlangıç seviyesine uygun bir
# TR: değişken sözleşmesidir. Önemli değişken adlarını, hangi değerleri taşımaları
# TR: gerektiğini ve hangi değerlerin hata veya red üretmesi gerektiğini açıklar.
#
# EN: catalog_path
# EN:   Meaning: filesystem path of one canonical startpoint catalog JSON file.
# EN:   Expected good values: str or pathlib.Path pointing to an existing UTF-8 JSON file.
# EN:   Error values: empty string, missing file, directory path, non-JSON file,
# EN:   unreadable file, or JSON that does not match the catalog schema.
# TR: catalog_path
# TR:   Anlamı: tek bir canonical startpoint catalog JSON dosyasının dosya yolu.
# TR:   Beklenen doğru değerler: mevcut bir UTF-8 JSON dosyasını gösteren str veya
# TR:   pathlib.Path.
# TR:   Hata değerleri: boş string, var olmayan dosya, klasör yolu, JSON olmayan
# TR:   dosya, okunamayan dosya veya catalog şemasına uymayan JSON.
#
# EN: catalog
# EN:   Meaning: decoded Python dictionary loaded from catalog_path.
# EN:   Expected good values: dict with catalog_version, catalog_status,
# EN:   catalog_scope, seed_contract_basis, and source_families keys.
# EN:   Error values: list/string/null root, missing required keys, wrong key types,
# EN:   duplicate source family codes, or empty source_families.
# TR: catalog
# TR:   Anlamı: catalog_path içinden okunmuş Python dict nesnesi.
# TR:   Beklenen doğru değerler: catalog_version, catalog_status, catalog_scope,
# TR:   seed_contract_basis ve source_families alanlarını içeren dict.
# TR:   Hata değerleri: kökte liste/string/null, eksik zorunlu alan, yanlış tip,
# TR:   tekrar eden source family kodu veya boş source_families.
#
# EN: source_families
# EN:   Meaning: top-level source families such as associations, directories, or
# EN:   logistics networks. A source family is not a single random URL; it is a
# EN:   coherent source ecosystem/host family.
# EN:   Expected good values: non-empty list of dict objects.
# EN:   Error values: non-list value, empty list, non-dict entries, duplicate
# EN:   source_family_code values, missing source_root_url, or missing source_host.
# TR: source_families
# TR:   Anlamı: dernek, dizin veya lojistik ağ gibi üst seviye kaynak aileleri.
# TR:   Source family rastgele tek URL değildir; tutarlı bir kaynak ekosistemi /
# TR:   host ailesidir.
# TR:   Beklenen doğru değerler: dict nesnelerinden oluşan boş olmayan liste.
# TR:   Hata değerleri: liste olmayan değer, boş liste, dict olmayan eleman,
# TR:   tekrar eden source_family_code, eksik source_root_url veya eksik source_host.
#
# EN: family
# EN:   Meaning: one source family entry inside source_families.
# EN:   Expected good values: dict with source_family_code, source_family_name,
# EN:   source_status, source_root_url, source_host, source_category, family_metadata,
# EN:   and seed_surfaces.
# EN:   Error values: missing identity fields, blank strings, invalid metadata type,
# EN:   or seed_surfaces that is not a list.
# TR: family
# TR:   Anlamı: source_families içindeki tek bir kaynak ailesi kaydı.
# TR:   Beklenen doğru değerler: source_family_code, source_family_name,
# TR:   source_status, source_root_url, source_host, source_category,
# TR:   family_metadata ve seed_surfaces alanlarını içeren dict.
# TR:   Hata değerleri: eksik kimlik alanları, boş stringler, yanlış metadata tipi
# TR:   veya liste olmayan seed_surfaces.
#
# EN: seed_surfaces
# EN:   Meaning: reviewed discovery surfaces under one source family. A surface can
# EN:   be a directory page, member search page, country/language section, or
# EN:   structured startpoint group.
# EN:   Expected good values: non-empty list of dict objects with stable surface codes.
# EN:   Error values: non-list value, empty list, missing surface_code, duplicate
# EN:   surface_code, or missing seed_urls.
# TR: seed_surfaces
# TR:   Anlamı: bir source family altındaki incelenmiş keşif yüzeyleri. Bir surface
# TR:   dizin sayfası, üye arama sayfası, ülke/dil bölümü veya yapılandırılmış
# TR:   startpoint grubu olabilir.
# TR:   Beklenen doğru değerler: kararlı surface_code içeren dict nesnelerinden
# TR:   oluşan boş olmayan liste.
# TR:   Hata değerleri: liste olmayan değer, boş liste, eksik surface_code, tekrar
# TR:   eden surface_code veya eksik seed_urls.
#
# EN: seed_urls
# EN:   Meaning: exact canonical URLs that can later become reviewed seeds.
# EN:   Expected good values: non-empty list of dict objects; each seed URL should
# EN:   be absolute HTTP/HTTPS, stable, relevant to logistics discovery, and not a
# EN:   login-only or blocked page unless explicitly marked for review.
# EN:   Error values: non-list value, empty list, relative URL, non-HTTP scheme,
# EN:   duplicate URL, blank URL, or URL that belongs to a different source host
# EN:   without an explicit cross-host policy.
# TR: seed_urls
# TR:   Anlamı: daha sonra incelenmiş seed olabilecek tam canonical URL'ler.
# TR:   Beklenen doğru değerler: dict nesnelerinden oluşan boş olmayan liste; her
# TR:   seed URL mutlak HTTP/HTTPS olmalı, kararlı olmalı, lojistik keşif ile
# TR:   ilgili olmalı ve özel review işareti yoksa login-only / blocked olmamalıdır.
# TR:   Hata değerleri: liste olmayan değer, boş liste, relative URL, HTTP dışı
# TR:   şema, tekrar eden URL, boş URL veya açık cross-host policy olmadan başka
# TR:   host'a ait URL.
#
# EN: priority
# EN:   Meaning: numeric review/execution priority used for ordering candidate seeds.
# EN:   Expected good values: integer or numeric value where lower/higher meaning is
# EN:   defined by the catalog contract and used consistently.
# EN:   Error values: missing priority when required, non-numeric text, negative value
# EN:   if forbidden by catalog policy, or inconsistent priority scale.
# TR: priority
# TR:   Anlamı: candidate seed sıralaması için kullanılan sayısal inceleme/çalıştırma
# TR:   önceliği.
# TR:   Beklenen doğru değerler: catalog contract içinde anlamı tanımlanmış ve
# TR:   tutarlı kullanılan integer veya numeric değer.
# TR:   Hata değerleri: zorunlu yerde eksik priority, sayısal olmayan metin, policy
# TR:   yasaklıyorsa negatif değer veya tutarsız priority ölçeği.
#
# EN: lang_code
# EN:   Meaning: language code associated with a source/seed surface.
# EN:   Expected good values: one of the canonical 25 language codes when the field
# EN:   identifies taxonomy/search language coverage; for English startpoints this
# EN:   is usually "en".
# EN:   Error values: unknown code, blank code, mixed locale string without mapping,
# EN:   or language code that is used to fake equal source counts across languages.
# TR: lang_code
# TR:   Anlamı: source/seed surface ile ilişkili dil kodu.
# TR:   Beklenen doğru değerler: alan taxonomy/search dil kapsamını gösteriyorsa
# TR:   canonical 25 dil kodundan biri; İngilizce startpoint için genellikle "en".
# TR:   Hata değerleri: bilinmeyen kod, boş kod, eşlemesi olmayan karma locale
# TR:   string veya diller arasında sahte eşit source sayısı üretmek için kullanılan
# TR:   dil kodu.
#
# EN: Important design rule
# EN:   Source and seed counts do not need to be equal across all 25 languages.
# EN:   English may be richer. The all-25 equality rule applies to taxonomy nodes,
# EN:   not to startpoint/source/seed counts.
# TR: Önemli tasarım kuralı
# TR:   Source ve seed sayıları 25 dilde eşit olmak zorunda değildir. İngilizce daha
# TR:   zengin olabilir. 25 dil eşitliği taxonomy node'ları için geçerlidir;
# TR:   startpoint/source/seed sayıları için geçerli değildir.
# =============================================================================

# EN: This module is the first canonical runtime bridge for the source-family startpoint
# EN: model. It makes the model executable on pi51c instead of leaving it as documentation
# EN: only.
# TR: Bu modül, source-family startpoint modeli için ilk kanonik runtime köprüsüdür.
# TR: Bu modeli yalnızca dokümanda bırakmak yerine pi51c üzerinde çalıştırılabilir
# TR: hale getirir.

from __future__ import annotations

# EN: We import json because catalogs are stored as JSON documents inside the repo and
# EN: runtime tree.
# TR: Kataloglar repo ve runtime ağacı içinde JSON dokümanları olarak tutulduğu için
# TR: json içe aktarılır.
import json

# EN: We import dataclass because explicit structured runtime results are easier to audit
# EN: than loose dictionaries alone.
# TR: Açık yapılı runtime sonuçları gevşek sözlüklerden daha kolay denetlendiği için
# TR: dataclass içe aktarılır.
from dataclasses import asdict, dataclass

# EN: We import Path because catalog files are filesystem-backed artefacts.
# TR: Katalog dosyaları dosya sistemi tabanlı artefact'lar olduğu için Path içe
# TR: aktarılır.
from pathlib import Path

# EN: We import Any because JSON-derived structures remain heterogeneous at the runtime
# EN: boundary.
# TR: JSON'dan türetilen yapılar runtime sınırında heterojen kaldığı için Any içe
# TR: aktarılır.
from typing import Any


# EN: This dataclass represents one flattened review candidate derived from a
# EN: source-family catalog.
# TR: Bu dataclass, source-family kataloğundan türetilen tek bir düzleştirilmiş
# TR: inceleme adayını temsil eder.
@dataclass(slots=True)
class ReviewCandidate:
    # EN: source_family_code identifies the top-level source ecosystem.
    # TR: source_family_code üst düzey kaynak ekosistemini tanımlar.
    source_family_code: str

    # EN: source_host identifies the host-level pacing domain.
    # TR: source_host host-level pacing alanını tanımlar.
    source_host: str

    # EN: host_budget_group groups same-host or same-budget surfaces together.
    # TR: host_budget_group aynı host veya aynı bütçe grubundaki yüzeyleri birlikte
    # TR: gruplar.
    host_budget_group: str

    # EN: surface_code identifies the discovery surface under the source family.
    # TR: surface_code source family altındaki keşif yüzeyini tanımlar.
    surface_code: str

    # EN: surface_type stores the surface class such as directory or search_surface.
    # TR: surface_type directory veya search_surface gibi yüzey sınıfını saklar.
    surface_type: str

    # EN: canonical_url is the exact URL that would be reviewed or inserted as a seed.
    # TR: canonical_url inceleme yapılacak veya seed olarak eklenecek tam URL'dir.
    canonical_url: str

    # EN: priority is the effective seed priority used for ordering.
    # TR: priority sıralama için kullanılan etkili seed önceliğidir.
    priority: int

    # EN: manual_review_priority is the human-controlled review urgency. Lower is more
    # EN: important.
    # TR: manual_review_priority insan kontrollü inceleme önceliğidir. Daha düşük değer
    # TR: daha önemlidir.
    manual_review_priority: int

    # EN: trust_tier stores the review trust tier such as A, B, or C.
    # TR: trust_tier A, B veya C gibi inceleme güven katmanını saklar.
    trust_tier: str

    # EN: lang_code stores the catalog language code.
    # TR: lang_code katalog dil kodunu saklar.
    lang_code: str


# EN: This helper reads one JSON file from disk.
# TR: Bu yardımcı diskten tek bir JSON dosyası okur.
def _read_json_file(path: Path) -> dict[str, Any]:
    # EN: We decode with UTF-8 because repo-tracked catalog artefacts are canonical UTF-8
    # EN: text files.
    # TR: Repo-izlenen katalog artefact'ları kanonik UTF-8 metin dosyaları olduğu için
    # TR: UTF-8 ile çözüyoruz.
    return json.loads(path.read_text(encoding="utf-8"))


# EN: This helper enforces the presence of required keys at one runtime boundary.
# TR: Bu yardımcı tek bir runtime sınırında gerekli anahtarların varlığını zorunlu
# TR: kılar.
def _require_keys(obj: dict[str, Any], required_keys: tuple[str, ...], context: str) -> None:
    # EN: We scan each required key one by one so the resulting error stays precise.
    # TR: Oluşacak hata açık ve kesin kalsın diye her gerekli anahtarı tek tek tararız.
    for key in required_keys:
        if key not in obj:
            raise ValueError(f"{context}: missing required key: {key}")


# EN: This helper loads a source-family catalog from disk.
# TR: Bu yardımcı diskten bir source-family kataloğu yükler.
def load_startpoint_catalog(catalog_path: str | Path) -> dict[str, Any]:
    # EN: We normalize to Path first so both str and Path callers are accepted.
    # TR: Hem str hem Path çağıranları kabul etmek için önce Path'e normalize ediyoruz.
    normalized_path = Path(catalog_path)

    # EN: The file must exist because a missing catalog is an operator error, not a
    # EN: silent runtime condition.
    # TR: Eksik katalog sessiz bir runtime durumu değil, operatör hatasıdır; bu yüzden
    # TR: dosya mevcut olmalıdır.
    if not normalized_path.is_file():
        raise FileNotFoundError(f"catalog file not found: {normalized_path}")

    # EN: We read the JSON payload and then validate the catalog shape explicitly.
    # TR: JSON payload'ını okuyor ve sonra katalog şeklini açık biçimde doğruluyoruz.
    catalog = _read_json_file(normalized_path)
    validate_startpoint_catalog(catalog)
    return catalog


# EN: This helper validates the high-level V2 catalog shape.
# TR: Bu yardımcı üst düzey V2 katalog şeklini doğrular.
def validate_startpoint_catalog(catalog: dict[str, Any]) -> None:
    # EN: The catalog root must expose the expected top-level structure.
    # TR: Katalog kökü beklenen üst düzey yapıyı sağlamalıdır.
    _require_keys(
        catalog,
        (
            "catalog_version",
            "catalog_status",
            "catalog_scope",
            "seed_contract_basis",
            "source_families",
        ),
        "catalog_root",
    )

    # EN: source_families must be a list because the whole model is built around multiple
    # EN: families each containing surfaces and seeds.
    # TR: source_families bir liste olmalıdır; çünkü tüm model surface ve seed içeren
    # TR: çoklu family'ler etrafında kuruludur.
    source_families = catalog["source_families"]
    if not isinstance(source_families, list):
        raise ValueError("catalog_root: source_families must be a list")

    # EN: We track family codes so duplicate top-level identities are rejected early.
    # TR: Yinelenen üst düzey kimlikler erken reddedilsin diye family kodlarını izliyoruz.
    seen_family_codes: set[str] = set()

    # EN: We now validate each family independently.
    # TR: Artık her family'yi bağımsız biçimde doğruluyoruz.
    for family_index, family in enumerate(source_families):
        if not isinstance(family, dict):
            raise ValueError(f"source_family[{family_index}]: family entry must be an object")

        _require_keys(
            family,
            (
                "source_family_code",
                "source_family_name",
                "source_status",
                "source_root_url",
                "source_host",
                "source_category",
                "allowed_schemes",
                "default_priority",
                "default_recrawl_interval",
                "default_max_depth",
                "family_metadata",
                "seed_surfaces",
            ),
            f"source_family[{family_index}]",
        )

        family_code = str(family["source_family_code"])
        if family_code in seen_family_codes:
            raise ValueError(f"duplicate source_family_code: {family_code}")
        seen_family_codes.add(family_code)

        family_metadata = family["family_metadata"]
        if not isinstance(family_metadata, dict):
            raise ValueError(f"source_family[{family_index}].family_metadata must be an object")

        _require_keys(
            family_metadata,
            (
                "lang_code",
                "trust_tier",
                "discovery_value",
                "noise_risk",
                "manual_review_priority",
                "live_check_required",
                "family_review_state",
                "host_budget_group",
                "cross_seed_traversal_allowed",
                "cross_language_traversal_allowed",
            ),
            f"source_family[{family_index}].family_metadata",
        )

        seed_surfaces = family["seed_surfaces"]
        if not isinstance(seed_surfaces, list):
            raise ValueError(f"source_family[{family_index}].seed_surfaces must be a list")

        seen_surface_codes: set[str] = set()

        for surface_index, surface in enumerate(seed_surfaces):
            if not isinstance(surface, dict):
                raise ValueError(
                    f"source_family[{family_index}].seed_surfaces[{surface_index}] must be an object"
                )

            _require_keys(
                surface,
                (
                    "surface_code",
                    "surface_type",
                    "surface_name",
                    "seed_urls",
                ),
                f"source_family[{family_index}].seed_surfaces[{surface_index}]",
            )

            surface_code = str(surface["surface_code"])
            if surface_code in seen_surface_codes:
                raise ValueError(
                    f"duplicate surface_code within family {family_code}: {surface_code}"
                )
            seen_surface_codes.add(surface_code)

            seed_urls = surface["seed_urls"]
            if not isinstance(seed_urls, list):
                raise ValueError(
                    f"source_family[{family_index}].seed_surfaces[{surface_index}].seed_urls must be a list"
                )

            if len(seed_urls) == 0:
                raise ValueError(
                    f"source_family[{family_index}].seed_surfaces[{surface_index}] has no seed_urls"
                )

            seen_seed_urls: set[str] = set()

            for seed_index, seed in enumerate(seed_urls):
                if not isinstance(seed, dict):
                    raise ValueError(
                        f"source_family[{family_index}].seed_surfaces[{surface_index}].seed_urls[{seed_index}] must be an object"
                    )

                _require_keys(
                    seed,
                    (
                        "seed_type",
                        "submitted_url",
                        "canonical_url",
                        "is_enabled",
                        "priority",
                        "max_depth",
                        "recrawl_interval",
                        "seed_metadata",
                    ),
                    f"source_family[{family_index}].seed_surfaces[{surface_index}].seed_urls[{seed_index}]",
                )

                canonical_url = str(seed["canonical_url"])
                if canonical_url in seen_seed_urls:
                    raise ValueError(
                        f"duplicate canonical_url within family {family_code} surface {surface_code}: {canonical_url}"
                    )
                seen_seed_urls.add(canonical_url)


# EN: This helper projects the source-family catalog into rows that are close to the
# EN: current seed.source and seed.seed_url reality.
# TR: Bu yardımcı, source-family kataloğunu mevcut seed.source ve seed.seed_url
# TR: gerçeğine yakın satırlara dönüştürür.
def project_catalog_to_seed_rows(catalog: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    # EN: We validate first so projection works only on trusted structure.
    # TR: Dönüştürme yalnızca güvenilir yapı üzerinde çalışsın diye önce doğrularız.
    validate_startpoint_catalog(catalog)

    # EN: projected_sources collects one projected source row per family.
    # TR: projected_sources her family için tek bir projeksiyon source satırı toplar.
    projected_sources: list[dict[str, Any]] = []

    # EN: projected_seed_urls collects one projected seed row per catalog seed URL.
    # TR: projected_seed_urls her katalog seed URL'si için tek bir projeksiyon seed
    # TR: satırı toplar.
    projected_seed_urls: list[dict[str, Any]] = []

    # EN: We now flatten family -> surface -> seed into the two row groups.
    # TR: Şimdi family -> surface -> seed yapısını iki satır grubuna düzleştiriyoruz.
    for family in catalog["source_families"]:
        family_metadata = dict(family["family_metadata"])

        projected_sources.append(
            {
                "source_code": family["source_family_code"],
                "source_name": family["source_family_name"],
                "source_status": family["source_status"],
                "homepage_url": family["source_root_url"],
                "source_category": family["source_category"],
                "allowed_schemes": list(family["allowed_schemes"]),
                "default_priority": int(family["default_priority"]),
                "default_recrawl_interval": str(family["default_recrawl_interval"]),
                "default_max_depth": int(family["default_max_depth"]),
                "notes": family.get("notes"),
                "projected_family_metadata": family_metadata,
            }
        )

        for surface in family["seed_surfaces"]:
            surface_metadata = dict(surface.get("surface_metadata", {}))

            for seed in surface["seed_urls"]:
                merged_seed_metadata = dict(seed["seed_metadata"])

                # EN: We enrich seed_metadata with family and surface identity so the
                # EN: current seed table can carry richer runtime truth without waiting
                # EN: for an immediate database redesign.
                # TR: Seed tablosu hemen yeniden tasarlanmadan daha zengin runtime
                # TR: doğrusu taşınabilsin diye seed_metadata'yı family ve surface
                # TR: kimliği ile zenginleştiriyoruz.
                merged_seed_metadata.setdefault("source_family_code", family["source_family_code"])
                merged_seed_metadata.setdefault("source_host", family["source_host"])
                merged_seed_metadata.setdefault("host_budget_group", family_metadata["host_budget_group"])
                merged_seed_metadata.setdefault("surface_code", surface["surface_code"])
                merged_seed_metadata.setdefault("surface_type", surface["surface_type"])
                merged_seed_metadata.setdefault("surface_name", surface["surface_name"])
                merged_seed_metadata.setdefault("family_trust_tier", family_metadata["trust_tier"])
                merged_seed_metadata.setdefault("family_discovery_value", family_metadata["discovery_value"])
                merged_seed_metadata.setdefault("family_noise_risk", family_metadata["noise_risk"])
                merged_seed_metadata.setdefault("family_review_state", family_metadata["family_review_state"])
                merged_seed_metadata.setdefault("surface_metadata", surface_metadata)

                projected_seed_urls.append(
                    {
                        "source_code": family["source_family_code"],
                        "seed_type": seed["seed_type"],
                        "submitted_url": seed["submitted_url"],
                        "canonical_url": seed["canonical_url"],
                        "is_enabled": bool(seed["is_enabled"]),
                        "priority": int(seed["priority"]),
                        "max_depth": int(seed["max_depth"]),
                        "recrawl_interval": str(seed["recrawl_interval"]),
                        "seed_metadata": merged_seed_metadata,
                        "notes": seed.get("notes"),
                    }
                )

    return {
        "projected_sources": projected_sources,
        "projected_seed_urls": projected_seed_urls,
    }


# EN: This helper flattens all seed URLs into review candidates.
# TR: Bu yardımcı tüm seed URL'lerini inceleme adaylarına düzleştirir.
def build_review_candidates(catalog: dict[str, Any]) -> list[ReviewCandidate]:
    # EN: We validate first so candidate generation uses trusted structure.
    # TR: Aday üretimi güvenilir yapı kullansın diye önce doğrularız.
    validate_startpoint_catalog(catalog)

    # EN: candidates stores every flattened review candidate before ordering.
    # TR: candidates sıralama öncesindeki tüm düzleştirilmiş inceleme adaylarını
    # TR: saklar.
    candidates: list[ReviewCandidate] = []

    for family in catalog["source_families"]:
        family_metadata = family["family_metadata"]

        for surface in family["seed_surfaces"]:
            for seed in surface["seed_urls"]:
                candidates.append(
                    ReviewCandidate(
                        source_family_code=str(family["source_family_code"]),
                        source_host=str(family["source_host"]),
                        host_budget_group=str(family_metadata["host_budget_group"]),
                        surface_code=str(surface["surface_code"]),
                        surface_type=str(surface["surface_type"]),
                        canonical_url=str(seed["canonical_url"]),
                        priority=int(seed["priority"]),
                        manual_review_priority=int(family_metadata["manual_review_priority"]),
                        trust_tier=str(family_metadata["trust_tier"]),
                        lang_code=str(family_metadata["lang_code"]),
                    )
                )

    return candidates


# EN: This helper builds a host-spaced review queue. The goal is to avoid back-to-back
# EN: same-host review pressure when multiple host budget groups exist.
# TR: Bu yardımcı host-spaced bir inceleme kuyruğu kurar. Amaç, birden fazla host
# TR: bütçe grubu varsa art arda aynı host baskısını önlemektir.
def build_host_spaced_review_queue(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    # EN: We first flatten all review candidates.
    # TR: Önce tüm inceleme adaylarını düzleştiriyoruz.
    candidates = build_review_candidates(catalog)

    # EN: grouped stores candidates bucketed by host_budget_group.
    # TR: grouped adayları host_budget_group bazında kovalar.
    grouped: dict[str, list[ReviewCandidate]] = {}

    for candidate in candidates:
        grouped.setdefault(candidate.host_budget_group, []).append(candidate)

    # EN: We sort each group so more urgent manual-review and higher-priority seeds come
    # EN: first within that group.
    # TR: Her grubu, daha acil manuel inceleme ve daha yüksek öncelikli seed'ler grup
    # TR: içinde önce gelecek şekilde sıralıyoruz.
    for group_key, items in grouped.items():
        grouped[group_key] = sorted(
            items,
            key=lambda item: (
                item.manual_review_priority,
                -item.priority,
                item.source_family_code,
                item.surface_code,
                item.canonical_url,
            ),
        )

    # EN: active_group_keys stores the stable group ordering used by round-robin.
    # TR: active_group_keys round-robin için kullanılan kararlı grup sırasını saklar.
    active_group_keys = sorted(grouped.keys())

    # EN: review_queue stores the final host-spaced queue as serializable dictionaries.
    # TR: review_queue nihai host-spaced kuyruğu serileştirilebilir sözlükler olarak
    # TR: saklar.
    review_queue: list[dict[str, Any]] = []

    # EN: We repeatedly take one candidate from each still-non-empty group.
    # TR: Boşalmamış her gruptan tekrar tekrar bir aday alıyoruz.
    while True:
        made_progress = False

        for group_key in active_group_keys:
            items = grouped[group_key]
            if not items:
                continue

            next_item = items.pop(0)
            review_queue.append(asdict(next_item))
            made_progress = True

        if not made_progress:
            break

    return review_queue


# EN: This helper builds a compact runtime summary for smoke tests and audits.
# TR: Bu yardımcı smoke testler ve denetimler için kompakt bir runtime özeti kurar.
def build_catalog_runtime_summary(catalog: dict[str, Any]) -> dict[str, Any]:
    # EN: We derive review candidates and projected rows from the same validated catalog.
    # TR: Aynı doğrulanmış katalogdan hem inceleme adaylarını hem projeksiyon satırlarını
    # TR: türetiyoruz.
    candidates = build_review_candidates(catalog)
    queue = build_host_spaced_review_queue(catalog)
    projection = project_catalog_to_seed_rows(catalog)

    # EN: We compute a few compact counters so operators can verify the shape quickly.
    # TR: Operatörler şekli hızlıca doğrulayabilsin diye birkaç kompakt sayaç hesaplarız.
    unique_hosts = sorted({candidate.source_host for candidate in candidates})
    unique_budget_groups = sorted({candidate.host_budget_group for candidate in candidates})

    return {
        "catalog_version": catalog["catalog_version"],
        "source_family_count": len(catalog["source_families"]),
        "projected_source_count": len(projection["projected_sources"]),
        "projected_seed_url_count": len(projection["projected_seed_urls"]),
        "review_candidate_count": len(candidates),
        "review_queue_count": len(queue),
        "unique_host_count": len(unique_hosts),
        "unique_hosts": unique_hosts,
        "unique_budget_group_count": len(unique_budget_groups),
        "unique_budget_groups": unique_budget_groups,
        "first_review_queue_items": queue[:10],
    }


# EN: This explicit export list defines the public runtime surface of this module.
# TR: Bu açık export listesi bu modülün public runtime yüzeyini tanımlar.
__all__ = [
    "ReviewCandidate",
    "load_startpoint_catalog",
    "validate_startpoint_catalog",
    "project_catalog_to_seed_rows",
    "build_review_candidates",
    "build_host_spaced_review_queue",
    "build_catalog_runtime_summary",
]
