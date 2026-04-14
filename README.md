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

If you are starting from zero, do **not** read the repository randomly.

Use this order:

1. `docs/README.md` — documentation hub and the safest beginner entry point
2. `hosts/makpi51crawler/python/README.md` — Python surface map
3. `hosts/makpi51crawler/sql/README.md` — SQL surface map
4. `hosts/makpi51crawler/crawler_exports/README.md` — export and data-flow surface map

Only after the hub-level meaning is clear should you continue into the lower-level README files inside those surfaces.

## Sıfırdan başlamak için okuma haritası

Sıfırdan başlıyorsan repository'yi rastgele okuma.

Şu sırayı kullan:

1. `docs/README.md` — dokümantasyon merkezi ve başlangıç için en güvenli giriş noktası
2. `hosts/makpi51crawler/python/README.md` — Python yüzey haritası
3. `hosts/makpi51crawler/sql/README.md` — SQL yüzey haritası
4. `hosts/makpi51crawler/crawler_exports/README.md` — export ve veri akışı yüzey haritası

Bu yüzeylerin içindeki alt README dosyalarına ancak hub seviyesindeki anlam netleştikten sonra geç.

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

At the current stage, the project has already established repository synchronization and crawler-side operational surfaces across Ubuntu Desktop, GitHub, and Pi51crawler. A repository-visible GitHub batch export path also exists as a controlled transport/audit surface, but it is no longer the canonical primary path for moving Pi51 database payload into Ubuntu Desktop. The present focus is to keep the working model explicit: Ubuntu Desktop <> GitHub <> Pi51crawler for code/docs/system truth, while removable-media transfer from Pi51 `/srv/data` into Ubuntu Desktop is the current primary path for physical crawler data movement. In concrete terms, the next standardization work is centered on `hosts/makpi51crawler/crawler_exports/`, `hosts/makpi51crawler/sql/`, `hosts/makpi51crawler/python/`, and the policy decisions for machine-local surfaces such as `_imports/` and `_build/`.

## Mevcut Repository Odağı

Mevcut aşamada proje, Ubuntu Desktop, GitHub ve Pi51crawler arasında repository senkronizasyonunu ve crawler tarafı operasyon yüzeylerini zaten kurmuş durumdadır. Repository’de görünür bir GitHub batch export yolu da kontrollü bir taşıma/audit yüzeyi olarak vardır; ancak Pi51 veritabanı payload’ını Ubuntu Desktop’a taşımak için artık kanonik birincil yol değildir. Şu anki odak; kod/doküman/sistem doğrusu için Ubuntu Desktop <> GitHub <> Pi51crawler modelini açık tutmak ve fiziksel crawler veri hareketi için Pi51 `/srv/data` -> çıkarılabilir medya -> Ubuntu Desktop yolunu birincil operasyon doğrusu olarak netleştirmektir. Somut olarak sıradaki standardizasyon çalışması `hosts/makpi51crawler/crawler_exports/`, `hosts/makpi51crawler/sql/`, `hosts/makpi51crawler/python/` ve `_imports/` ile `_build/` gibi makineye özel yüzeyler için politika kararları etrafında şekillenmektedir.
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
## Güncel repository yapı kuralı

The current canonical repository rule is simple:

- repository-global entry and governance surfaces such as `README.md`, `docs/`, and `.gitignore` remain at repository root
- the active crawler-host tracked work surfaces now live under `hosts/makpi51crawler/`
- `hosts/` therefore acts as both a host-operations family and, where explicitly validated, the home of host-scoped tracked work surfaces

In the current repository point, the main active crawler-host work surfaces are:

- `hosts/makpi51crawler/python/README.md`
- `hosts/makpi51crawler/sql/README.md`
- `hosts/makpi51crawler/crawler_exports/README.md`
- `hosts/README.md`

Güncel kanonik repository kuralı basittir:

- `README.md`, `docs/` ve `.gitignore` gibi repository-geneli giriş ve yönetişim yüzeyleri repository kökünde kalır
- aktif crawler-host izlenen çalışma yüzeyleri artık `hosts/makpi51crawler/` altında yaşar
- bu nedenle `hosts/`, hem host-operasyon ailesi hem de açıkça doğrulanmış durumlarda host-kapsamlı izlenen çalışma yüzeylerinin evi olarak görev yapar

Mevcut repository noktasında ana aktif crawler-host çalışma yüzeyleri şunlardır:

- `hosts/makpi51crawler/python/README.md`
- `hosts/makpi51crawler/sql/README.md`
- `hosts/makpi51crawler/crawler_exports/README.md`
- `hosts/README.md`
