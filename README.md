# LogisticSearch

**LogisticSearch** is a long-term transportation and logistics data, classification, and search infrastructure project. It is being built to collect, normalize, classify, enrich, transfer, and operationally organize real-world logistics information across a wide domain surface, including freight, warehousing, customs, forwarding, fleet, equipment, service networks, passenger transportation, and selected premium segments such as yachts and private jets. The goal is not to produce a shallow listing site, but to establish a disciplined logistics intelligence foundation that can later power controlled applications, search experiences, and human-supervised decision layers.

**LogisticSearch**, uzun vadeli bir taşımacılık ve lojistik veri, sınıflandırma ve arama altyapısı projesidir. Proje; navlun, depo, gümrük, forwarding, filo, ekipman, servis ağları, yolcu taşımacılığı ve yatlar ile özel jetler gibi seçili premium segmentler dahil olmak üzere geniş bir alan yüzeyindeki gerçek dünya lojistik verilerini toplamak, normalize etmek, sınıflandırmak, zenginleştirmek, taşımak ve operasyonel olarak düzenlemek amacıyla geliştirilmektedir. Amaç yüzeysel bir listeleme sitesi üretmek değil; ileride kontrollü uygulamaları, arama deneyimlerini ve insan denetimli karar katmanlarını besleyebilecek disiplinli bir lojistik istihbarat temeli kurmaktır.

## Project Direction

The project is intentionally evolving as a structured system rather than a quick prototype. Its architecture is being shaped around explicit state transitions, auditable data flow, layered responsibilities, and repository hygiene. Crawling, taxonomy, geospatial enrichment, export packaging, GitHub-mediated transfer, desktop-side intake, and later application delivery are treated as separate but connected layers so that the system can remain understandable, maintainable, and extensible as it grows.

Proje, hızlı bir prototip yerine yapısal bir sistem olarak bilinçli şekilde geliştirilmektedir. Mimari; açık durum geçişleri, denetlenebilir veri akışı, katmanlı sorumluluk ayrımı ve repository hijyeni etrafında şekillendirilmektedir. Crawling, taksonomi, coğrafi zenginleştirme, export paketleme, GitHub aracılı aktarım, desktop tarafı intake ve daha sonra uygulama sunumu; sistem büyürken anlaşılabilir, sürdürülebilir ve genişletilebilir kalabilsin diye ayrı ama bağlantılı katmanlar olarak ele alınmaktadır.

## Canonical Working Model

The canonical working model is centered on three roles. Ubuntu Desktop is the main development and integration environment. GitHub is the canonical synchronization and transport bridge. Pi51 is treated as a dedicated crawler and data-origin node rather than an application decision center. In practical terms, the project currently follows this flow: collect on the crawler, package structured batches, push them to GitHub, pull them into Ubuntu Desktop, import them into PostgreSQL, and continue processing from there under controlled operational rules.

Kanonik çalışma modeli üç rol etrafında kuruludur. Ubuntu Desktop ana geliştirme ve entegrasyon ortamıdır. GitHub kanonik senkronizasyon ve taşıma köprüsüdür. Pi51 ise uygulama karar merkezi değil, özel bir crawler ve veri-kaynağı düğümü olarak ele alınmaktadır. Pratikte proje şu akışı izlemektedir: veriyi crawler üzerinde topla, yapısal batch’ler halinde paketle, GitHub’a gönder, Ubuntu Desktop’a çek, PostgreSQL içine al ve oradan kontrollü operasyon kurallarıyla işlemeye devam et.

## Repository Purpose

This repository is the canonical working base of the LogisticSearch project. It is used to define and standardize the crawler export surface, the desktop intake contract, SQL and Python support layers, project structure, data-flow boundaries, and the evolving operational rules around repository cleanliness. The repository is expected to remain useful both as a buildable working tree and as a long-term engineering record of how the system is being shaped.

Bu repository, LogisticSearch projesinin kanonik çalışma tabanıdır. Crawler export yüzeyini, desktop intake sözleşmesini, SQL ve Python destek katmanlarını, proje yapısını, veri akışı sınırlarını ve repository temizliği etrafında gelişen operasyon kurallarını tanımlamak ve standardize etmek için kullanılmaktadır. Repository’nin hem çalıştırılabilir bir çalışma ağacı hem de sistemin nasıl şekillendiğini gösteren uzun vadeli bir mühendislik kaydı olarak faydalı kalması beklenmektedir.

## Taxonomy and Domain Scope

A major backbone of LogisticSearch is its logistics taxonomy. The taxonomy is intended to cover the transportation and logistics domain broadly and in a way that remains operationally useful. Classification is not treated as a decorative metadata layer; it is one of the core mechanisms that determines how collected entities are interpreted, grouped, enriched, filtered, and prepared for later application use. The long-term scope is intentionally broad and includes both conventional logistics categories and more specialized or premium segments when they are relevant to real-world logistics search and discovery.

LogisticSearch’in temel omurgalarından biri lojistik taksonomisidir. Bu taksonomi, taşımacılık ve lojistik alanını geniş biçimde ama operasyonel olarak faydalı kalacak şekilde kapsamak üzere tasarlanmaktadır. Sınıflandırma dekoratif bir metadata katmanı olarak görülmez; toplanan varlıkların nasıl yorumlanacağını, gruplanacağını, zenginleştirileceğini, filtreleneceğini ve daha sonra uygulama kullanımına hazırlanacağını belirleyen temel mekanizmalardan biridir. Uzun vadeli kapsam bilinçli olarak geniş tutulmaktadır ve gerçek dünya lojistik arama/keşif ihtiyacına bağlı olarak hem konvansiyonel kategorileri hem de daha uzmanlaşmış veya premium segmentleri içerir.

## Geospatial Model

OpenStreetMap is a mandatory component in the long-term system design. Geographic enrichment is expected to support place normalization, regional interpretation, route and location context, and map-aware logistics intelligence. The geospatial layer is therefore part of the data model itself, not a superficial presentation add-on. This design direction is intended to improve both the quality of classification and the usefulness of future search results.

OpenStreetMap, uzun vadeli sistem tasarımında zorunlu bir bileşendir. Coğrafi zenginleştirmenin; yer adı normalizasyonu, bölgesel yorumlama, rota ve konum bağlamı ile harita farkındalığına sahip lojistik istihbaratı desteklemesi beklenmektedir. Bu yüzden coğrafi katman, yalnızca görsel bir sunum eklentisi değil, doğrudan veri modelinin parçasıdır. Bu tasarım yönü hem sınıflandırma kalitesini hem de gelecekteki arama sonuçlarının faydasını artırmayı amaçlamaktadır.

## Current Repository Focus

At the current stage, the project has already established a working crawler export flow from Pi51 to GitHub and from GitHub into Ubuntu Desktop. Structured batch export, guarded push behavior, desktop-side intake, and initial PostgreSQL loading are already functioning. The present focus is to make the repository root more coherent and professional without breaking validated live surfaces. In concrete terms, the next standardization work is centered on `crawler_exports/`, `sql/`, `python/`, and the policy decisions for machine-local surfaces such as `_imports/` and `_build/`.

Mevcut aşamada proje, Pi51’den GitHub’a ve GitHub’dan Ubuntu Desktop’a çalışan bir crawler export akışını zaten kurmuş durumdadır. Yapısal batch export, korumalı push davranışı, desktop tarafı intake ve ilk PostgreSQL yükleme adımları halihazırda çalışmaktadır. Şu anki odak, doğrulanmış canlı yüzeyleri bozmadan repository kökünü daha tutarlı ve daha profesyonel hale getirmektir. Somut olarak sıradaki standardizasyon çalışması `crawler_exports/`, `sql/`, `python/` ve `_imports/` ile `_build/` gibi makineye özel yüzeyler için politika kararları etrafında şekillenmektedir.

## Engineering Principles

The project is developed with a strong preference for explicitness, auditability, reversibility, and clean standardization. Large blind cleanups are avoided. Instead, the system is improved step by step, with each meaningful change expected to be understandable, reviewable, and operationally justified. Repository hygiene is treated as part of the engineering work itself rather than as an afterthought.

Proje; açıklık, denetlenebilirlik, geri alınabilirlik ve temiz standardizasyon yönünde güçlü bir tercihle geliştirilmektedir. Büyük ve kör temizliklerden kaçınılmaktadır. Bunun yerine sistem adım adım iyileştirilir; her anlamlı değişikliğin anlaşılabilir, gözden geçirilebilir ve operasyonel olarak gerekçelendirilebilir olması beklenir. Repository hijyeni de sonradan düşünülen bir ayrıntı değil, doğrudan mühendislik işinin parçası olarak ele alınır.

## Near-Term Priorities

The near-term priorities are clear. First, the repository root will be standardized without disturbing validated flows. Second, the supporting SQL and Python surfaces will be shaped into a more intentional structure. Third, local-only surfaces will be given explicit policy boundaries so that the repository remains clean and portable. After that, the next data-flow layer can be expanded on a more stable and better-documented foundation.

Yakın vadeli öncelikler nettir. İlk olarak repository kökü, doğrulanmış akışları bozmadan standardize edilecektir. İkinci olarak destekleyici SQL ve Python yüzeyleri daha bilinçli bir yapıya kavuşturulacaktır. Üçüncü olarak local-only yüzeyler için açık politika sınırları belirlenecektir; böylece repository temiz ve taşınabilir kalacaktır. Bundan sonra bir sonraki veri akışı katmanı, daha istikrarlı ve daha iyi dokümante edilmiş bir temel üzerinde genişletilebilecektir.

## Status Notice

This repository is under active architectural and operational refinement. Paths, module boundaries, and support surfaces may evolve as the system becomes cleaner and more mature. The direction, however, is stable: first build a disciplined logistics data infrastructure, then build polished application layers on top of it.

Bu repository aktif mimari ve operasyon iyileştirmesi altındadır. Yollar, modül sınırları ve destek yüzeyleri sistem temizlenip olgunlaştıkça evrilebilir. Buna rağmen yön stabildir: önce disiplinli bir lojistik veri altyapısı kurmak, sonra bunun üzerine cilalı uygulama katmanları inşa etmek.
