# LogisticSearch

## Overview

**LogisticSearch** is a long-term transportation and logistics data, classification, and search infrastructure project. It is being built to collect, normalize, classify, enrich, transfer, and operationally organize real-world logistics information across a wide domain surface, including freight, warehousing, customs, forwarding, fleet, equipment, service networks, passenger transportation, and selected premium segments such as yachts and private jets. The goal is not to produce a shallow listing site, but to establish a disciplined logistics intelligence foundation that can later power controlled applications, search experiences, and human-supervised decision layers.

## Genel Bakış

**LogisticSearch**, uzun vadeli bir taşımacılık ve lojistik veri, sınıflandırma ve arama altyapısı projesidir. Proje; navlun, depo, gümrük, forwarding, filo, ekipman, servis ağları, yolcu taşımacılığı ve yatlar ile özel jetler gibi seçili premium segmentler dahil olmak üzere geniş bir alan yüzeyindeki gerçek dünya lojistik verilerini toplamak, normalize etmek, sınıflandırmak, zenginleştirmek, taşımak ve operasyonel olarak düzenlemek amacıyla geliştirilmektedir. Amaç yüzeysel bir listeleme sitesi üretmek değil; ileride kontrollü uygulamaları, arama deneyimlerini ve insan denetimli karar katmanlarını besleyebilecek disiplinli bir lojistik istihbarat temeli kurmaktır.
## Project Direction

The project is intentionally evolving as a structured system rather than a quick prototype. Its architecture is being shaped around explicit state transitions, auditable data flow, layered responsibilities, and repository hygiene. Crawling, taxonomy, geospatial enrichment, export packaging, repository synchronization, selectively promoted GitHub-visible export history, removable-media handoff from Pi51 `/srv/data`, desktop-side intake, and later application delivery are treated as separate but connected layers so that the system can remain understandable, maintainable, and extensible as it grows.

## Proje Yönü

Proje, hızlı bir prototip yerine yapısal bir sistem olarak bilinçli şekilde geliştirilmektedir. Mimari; açık durum geçişleri, denetlenebilir veri akışı, katmanlı sorumluluk ayrımı ve repository hijyeni etrafında şekillendirilmektedir. Crawling, taksonomi, coğrafi zenginleştirme, export paketleme, repository senkronizasyonu, seçilerek GitHub üzerinde görünür kılınan export tarihçesi, Pi51 `/srv/data` üzerinden çıkarılabilir medya teslimi, desktop tarafı intake ve daha sonra uygulama sunumu; sistem büyürken anlaşılabilir, sürdürülebilir ve genişletilebilir kalabilsin diye ayrı ama bağlantılı katmanlar olarak ele alınmaktadır.
## Canonical Working Model

The canonical working model is centered on three roles. Ubuntu Desktop is the main development and integration environment. GitHub is the canonical synchronization bridge for repository-tracked code, documentation, SQL, Python surfaces, and operational truth. Pi51crawler is treated as a dedicated crawler and data-origin node rather than an application decision center. In practical terms, the current canonical working model is bidirectional at the repository level: Ubuntu Desktop <> GitHub <> Pi51crawler. For live crawler database/export payload movement, however, the current primary operational path is no longer “Pi51 -> GitHub -> Ubuntu Desktop”. Physical crawler data that must move into Ubuntu Desktop is now expected to travel from Pi51 through `/srv/data` on removable SSD media under controlled operator handling.

## Kanonik Çalışma Modeli

Kanonik çalışma modeli üç rol etrafında kuruludur. Ubuntu Desktop ana geliştirme ve entegrasyon ortamıdır. GitHub; repository’de izlenen kod, dokümantasyon, SQL, Python yüzeyleri ve operasyon doğrusu için kanonik senkronizasyon köprüsüdür. Pi51crawler ise uygulama karar merkezi değil, özel bir crawler ve veri-kaynağı düğümü olarak ele alınmaktadır. Pratikte güncel kanonik çalışma modeli repository seviyesinde çift yönlüdür: Ubuntu Desktop <> GitHub <> Pi51crawler. Ancak canlı crawler verisi / export payload taşımasında birincil operasyon yolu artık “Pi51 -> GitHub -> Ubuntu Desktop” değildir. Ubuntu Desktop’a fiziksel olarak taşınması gereken crawler verisinin, kontrollü operatör işlemi altında Pi51 üzerindeki `/srv/data` üzerinden çıkarılabilir SSD ile gelmesi beklenmektedir.
## Repository Purpose

This repository is the canonical working base of the LogisticSearch project. It is used to define and standardize the crawler export surface, the desktop intake contract, SQL and Python support layers, project structure, data-flow boundaries, and the evolving operational rules around repository cleanliness. The repository is expected to remain useful both as a buildable working tree and as a long-term engineering record of how the system is being shaped.

## Repository Amacı

Bu repository, LogisticSearch projesinin kanonik çalışma tabanıdır. Crawler export yüzeyini, desktop intake sözleşmesini, SQL ve Python destek katmanlarını, proje yapısını, veri akışı sınırlarını ve repository temizliği etrafında gelişen operasyon kurallarını tanımlamak ve standardize etmek için kullanılmaktadır. Repository’nin hem çalıştırılabilir bir çalışma ağacı hem de sistemin nasıl şekillendiğini gösteren uzun vadeli bir mühendislik kaydı olarak faydalı kalması beklenmektedir.
## Reading map for starting from zero

If you are starting from zero, do not read the repository randomly.

Read these first, in this exact order:

1. `docs/TOPIC_BILINGUAL_COMMENT_DENSITY_AUDIT_AND_THRESHOLD_MODEL.md` — universal explanation and recoverability rule
2. `docs/STATUS_STAGE21_PROJECT_CONTINUITY_AND_NEXT_ACTIONS.md` — current project position, continuity truth, and immediate next-action frame
3. `docs/TODO_STAGE21_TIMESTAMPED_EXECUTION_QUEUE.md` — living timestamped execution queue; this file must keep moving as work moves
4. `docs/README.md` — documentation hub and the safest general beginner entry point
5. `makpi51crawler/README.md` — Python surface map

Only after the continuity and hub-level meaning is clear should you continue into lower-level README files and technical source files.

## Sıfırdan başlamak için okuma haritası

Sıfırdan başlıyorsan repository’yi rastgele okuma.

Önce tam olarak şu sırayı oku:

1. `docs/TOPIC_BILINGUAL_COMMENT_DENSITY_AUDIT_AND_THRESHOLD_MODEL.md` — evrensel açıklama ve geri-kurulabilirlik kuralı
2. `docs/STATUS_STAGE21_PROJECT_CONTINUITY_AND_NEXT_ACTIONS.md` — güncel proje konumu, süreklilik doğrusu ve yakın sonraki adım çerçevesi
3. `docs/TODO_STAGE21_TIMESTAMPED_EXECUTION_QUEUE.md` — yaşayan zaman damgalı execution queue; iş ilerledikçe bu dosya da ilerlemelidir
4. `docs/README.md` — dokümantasyon merkezi ve genel başlangıç için en güvenli giriş noktası
5. `makpi51crawler/README.md` — Python yüzey haritası

Süreklilik ve hub-seviyesi anlam netleşmeden alt README dosyalarına ve teknik kaynak dosyalarına geçme.

## Taxonomy and Domain Scope

A major backbone of LogisticSearch is its logistics taxonomy. The taxonomy is intended to cover the transportation and logistics domain broadly and in a way that remains operationally useful. Classification is not treated as a decorative metadata layer; it is one of the core mechanisms that determines how collected entities are interpreted, grouped, enriched, filtered, and prepared for later application use. The long-term scope is intentionally broad and includes both conventional logistics categories and more specialized or premium segments when they are relevant to real-world logistics search and discovery.

## Taksonomi ve Alan Kapsamı

LogisticSearch’in temel omurgalarından biri lojistik taksonomisidir. Bu taksonomi, taşımacılık ve lojistik alanını geniş biçimde ama operasyonel olarak faydalı kalacak şekilde kapsamak üzere tasarlanmaktadır. Sınıflandırma dekoratif bir metadata katmanı olarak görülmez; toplanan varlıkların nasıl yorumlanacağını, gruplanacağını, zenginleştirileceğini, filtreleneceğini ve daha sonra uygulama kullanımına hazırlanacağını belirleyen temel mekanizmalardan biridir. Uzun vadeli kapsam bilinçli olarak geniş tutulmaktadır ve gerçek dünya lojistik arama/keşif ihtiyacına bağlı olarak hem konvansiyonel kategorileri hem de daha uzmanlaşmış veya premium segmentleri içerir.
## Geospatial Model

OpenStreetMap is a mandatory component in the long-term system design. Geographic enrichment is expected to support place normalization, regional interpretation, route and location context, and map-aware logistics intelligence. The geospatial layer is therefore part of the data model itself, not a superficial presentation add-on. This design direction is intended to improve both the quality of classification and the usefulness of future search results.

Map presentation-library choice is intentionally treated as a separate application-surface decision rather than as a direct webcrawler contract. The crawler-side responsibility is geospatial acquisition, normalization, and enrichment truth. The future map-stack decision surface is documented separately in `docs/SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md`.

## Coğrafi Model

OpenStreetMap, uzun vadeli sistem tasarımında zorunlu bir bileşendir. Coğrafi zenginleştirmenin; yer adı normalizasyonu, bölgesel yorumlama, rota ve konum bağlamı ile harita farkındalığına sahip lojistik istihbaratı desteklemesi beklenmektedir. Bu yüzden coğrafi katman, yalnızca görsel bir sunum eklentisi değil, doğrudan veri modelinin parçasıdır. Bu tasarım yönü hem sınıflandırma kalitesini hem de gelecekteki arama sonuçlarının faydasını artırmayı amaçlamaktadır.

Harita gösterim kütüphanesi seçimi, doğrudan webcrawler sözleşmesi olarak değil, ayrı bir uygulama-yüzeyi kararı olarak ele alınır. Crawler tarafının sorumluluğu coğrafi veri edinimi, normalizasyon ve zenginleştirme doğrusudur. Gelecekteki harita-yığını karar yüzeyi ayrı olarak `docs/SECTIONX_MAP_STACK_AND_GEOSPATIAL_APPLICATION_SURFACE.md` dosyasında dokümante edilir.
## Current Repository Focus

The current repository focus is the new `makpi51crawler/` topology.

The active repository-tracked crawler-host surfaces are now:

  * `makpi51crawler/README.md` — crawler-host root explanation and navigation
  * `makpi51crawler/RUNBOOK_SYNC_REPO_AND_RUNTIME.md` — controlled GitHub-to-pi51c repo/runtime synchronization model
  * `makpi51crawler/python_live_runtime/` — Python runtime-family source surface for the crawler loop, controls, catalog loader, taxonomy bridge, acquisition, parsing, storage routing, and diagnostics
  * `makpi51crawler/catalog/` — reviewed source-family and startpoint catalog surface; English currently has 27 source families and 43 English-owned seed URLs
  * `makpi51crawler/taxonomy/` — canonical JSON taxonomy language files and taxonomy schema
  * `docs/` — project contracts, continuity documents, runbooks, and decision records

The current English catalog is intentionally a reviewed candidate catalog, not an automatic crawler_core insertion list. Every source and seed still requires pi51c live probing before DB/frontier insertion.

The immediate repository focus is:

  1. keep the new `makpi51crawler/` root clean and beginner-readable
  2. keep Ubuntu Desktop <> GitHub <> pi51c repository synchronization explicit
  3. verify pi51c `/logisticsearch/repo` as a GitHub mirror before any pi51c runtime/taxonomy/catalog sync
  4. test catalog sources/seeds one by one on pi51c before durable crawler_core insertion
  5. continue crawler_core/webcrawler hardening from the current raw-fetch → parse → taxonomy/catalog boundary

Old repository layouts are not active working surfaces now. Do not plan new work under the removed host-specific legacy tree, old `makpi51crawler/python`, old `makpi51crawler/sql`, old `makpi51crawler/crawler_exports`, or old `makpi51crawler/webcrawler` paths.

## Mevcut Repository Odağı

Güncel repository odağı yeni `makpi51crawler/` topolojisidir.

Aktif repository'de izlenen crawler-host yüzeyleri artık şunlardır:

  * `makpi51crawler/README.md` — crawler-host kök açıklaması ve navigasyon
  * `makpi51crawler/RUNBOOK_SYNC_REPO_AND_RUNTIME.md` — kontrollü GitHub'dan pi51c repo/runtime senkronizasyon modeli
  * `makpi51crawler/python_live_runtime/` — crawler döngüsü, kontroller, catalog loader, taxonomy bridge, acquisition, parse, storage routing ve diagnostik için Python runtime-aile kaynak yüzeyi
  * `makpi51crawler/catalog/` — incelenmiş source-family ve startpoint catalog yüzeyi; İngilizce şu anda 27 source family ve 43 İngilizceye ait seed URL içerir
  * `makpi51crawler/taxonomy/` — kanonik JSON taxonomy dil dosyaları ve taxonomy schema
  * `docs/` — proje sözleşmeleri, süreklilik dokümanları, runbook'lar ve karar kayıtları

Güncel English catalog bilinçli olarak incelenmiş aday catalog'dur; otomatik crawler_core insert listesi değildir. Her source ve seed, DB/frontier insert öncesinde yine pi51c canlı probe ile doğrulanmalıdır.

Yakın repository odağı:

  1. yeni `makpi51crawler/` kökünü temiz ve başlangıç seviyesinde okunabilir tutmak
  2. Ubuntu Desktop <> GitHub <> pi51c repository senkronizasyonunu açık tutmak
  3. pi51c üzerinde herhangi runtime/taxonomy/catalog sync öncesinde `/logisticsearch/repo` klasörünü GitHub aynası olarak doğrulamak
  4. catalog source/seed kayıtlarını kalıcı crawler_core insert öncesinde pi51c üzerinde tek tek test etmek
  5. crawler_core/webcrawler hardening hattına mevcut raw-fetch → parse → taxonomy/catalog sınırından devam etmek

Eski repository yerleşimleri artık aktif çalışma yüzeyi değildir. Yeni işi kaldırılmış host-özel legacy tree, eski `makpi51crawler/python`, eski `makpi51crawler/sql`, eski `makpi51crawler/crawler_exports` veya eski `makpi51crawler/webcrawler` yolları altında planlama.

## Engineering Principles

The project is developed with a strong preference for explicitness, auditability, reversibility, and clean standardization. Large blind cleanups are avoided. Instead, the system is improved step by step, with each meaningful change expected to be understandable, reviewable, and operationally justified. Repository hygiene is treated as part of the engineering work itself rather than as an afterthought.

## Mühendislik İlkeleri

Proje; açıklık, denetlenebilirlik, geri alınabilirlik ve temiz standardizasyon yönünde güçlü bir tercihle geliştirilmektedir. Büyük ve kör temizliklerden kaçınılmaktadır. Bunun yerine sistem adım adım iyileştirilir; her anlamlı değişikliğin anlaşılabilir, gözden geçirilebilir ve operasyonel olarak gerekçelendirilebilir olması beklenir. Repository hijyeni de sonradan düşünülen bir ayrıntı değil, doğrudan mühendislik işinin parçası olarak ele alınır.
## Near-Term Priorities

The near-term priorities are clear. First, the repository root will be standardized without disturbing validated flows. Second, the supporting SQL and Python surfaces will be shaped into a more intentional structure. Third, local-only surfaces will be given explicit policy boundaries so that the repository remains clean and portable. After that, the next data-flow layer can be expanded on a more stable and better-documented foundation.

## Yakın Vadeli Öncelikler

Yakın vadeli öncelikler nettir. İlk olarak repository kökü, doğrulanmış akışları bozmadan standardize edilecektir. İkinci olarak destekleyici SQL ve Python yüzeyleri daha bilinçli bir yapıya kavuşturulacaktır. Üçüncü olarak local-only yüzeyler için açık politika sınırları belirlenecektir; böylece repository temiz ve taşınabilir kalacaktır. Bundan sonra bir sonraki veri akışı katmanı, daha istikrarlı ve daha iyi dokümante edilmiş bir temel üzerinde genişletilebilecektir.
## Status Notice

This repository is under active architectural and operational refinement. Paths, module boundaries, and support surfaces may evolve as the system becomes cleaner and more mature. The direction, however, is stable: first build a disciplined logistics data infrastructure, then build polished application layers on top of it.

## Durum Notu

Bu repository aktif mimari ve operasyon iyileştirmesi altındadır. Yollar, modül sınırları ve destek yüzeyleri sistem temizlenip olgunlaştıkça evrilebilir. Buna rağmen yön stabildir: önce disiplinli bir lojistik veri altyapısı kurmak, sonra bunun üzerine cilalı uygulama katmanları inşa etmek.

## Current repository structure rule

The current canonical repository structure rule is simple:

  * repository-global entry and governance surfaces such as `README.md`, `docs/`, and `.gitignore` remain at repository root
  * the active crawler-host tracked work surfaces live under `makpi51crawler/`
  * Python runtime-family code lives under `makpi51crawler/python_live_runtime/`
  * source/startpoint catalog JSON lives under `makpi51crawler/catalog/`
  * taxonomy JSON lives under `makpi51crawler/taxonomy/`
  * pi51c runtime synchronization must start from a verified GitHub mirror at `/logisticsearch/repo`
  * live runtime, DB, systemd, and data directories on pi51c are separate operational surfaces and must not be silently confused with the repository tree

The main active crawler-host repository surfaces are:

  * `makpi51crawler/README.md`
  * `makpi51crawler/RUNBOOK_SYNC_REPO_AND_RUNTIME.md`
  * `makpi51crawler/python_live_runtime/README.md`
  * `makpi51crawler/catalog/schema/startpoint_catalog_v2.schema.json`
  * `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
  * `makpi51crawler/taxonomy/README.md`
  * `makpi51crawler/taxonomy/schema/logisticsearch_taxonomy_language_schema_v1.json`
  * `makpi51crawler/taxonomy/languages/`

## Güncel repository yapı kuralı

Güncel kanonik repository yapı kuralı basittir:

  * `README.md`, `docs/` ve `.gitignore` gibi repository-geneli giriş ve yönetişim yüzeyleri repository kökünde kalır
  * aktif crawler-host izlenen çalışma yüzeyleri `makpi51crawler/` altında yaşar
  * Python runtime-aile kodu `makpi51crawler/python_live_runtime/` altında yaşar
  * source/startpoint catalog JSON `makpi51crawler/catalog/` altında yaşar
  * taxonomy JSON `makpi51crawler/taxonomy/` altında yaşar
  * pi51c runtime senkronizasyonu, önce `/logisticsearch/repo` klasörünün GitHub aynası olarak doğrulanmasıyla başlamalıdır
  * pi51c üzerindeki live runtime, DB, systemd ve data klasörleri ayrı operasyon yüzeyleridir; repository ağacıyla sessizce karıştırılmamalıdır

Ana aktif crawler-host repository yüzeyleri şunlardır:

  * `makpi51crawler/README.md`
  * `makpi51crawler/RUNBOOK_SYNC_REPO_AND_RUNTIME.md`
  * `makpi51crawler/python_live_runtime/README.md`
  * `makpi51crawler/catalog/schema/startpoint_catalog_v2.schema.json`
  * `makpi51crawler/catalog/startpoints/en/english_source_families_v2.json`
  * `makpi51crawler/taxonomy/README.md`
  * `makpi51crawler/taxonomy/schema/logisticsearch_taxonomy_language_schema_v1.json`
  * `makpi51crawler/taxonomy/languages/`

## Future deferred note: Pi51 semi-automatic sync model

This is only a short reminder note for later. It is not active now.

Planned later direction:

  * controlled push from the relevant Ubuntu Desktop working surface
  * controlled or semi-automatic fast-forward pull from GitHub into the pi51c repository
  * controlled synchronization from the pi51c repository tree into the live runtime tree
  * this model will later be documented separately as a detailed guide and runbook

Current priority remains bringing up webcrawler and crawler_core first.

## Geleceğe ertelenmiş not: Pi51 yarı otomatik senkron modeli

Bu bölüm şimdilik yalnızca kısa bir hatırlatma notudur. Şu anda aktif değildir.

Gelecekte düşünülmesi planlanan yön:

  * Ubuntu Desktop tarafında ilgili klasörden kontrollü push komutu
  * pi51c repo tarafında GitHub'dan kontrollü veya yarı otomatik fast-forward pull
  * pi51c runtime tarafında repo ağacından canlı runtime ağacına kontrollü senkron
  * bu model daha sonra ayrıca ayrıntılı rehber ve runbook olarak yazılacaktır

Mevcut öncelik önce webcrawler ve crawler_core'u ayağa kaldırmaktır.
