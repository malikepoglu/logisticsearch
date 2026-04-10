# SECTIONX Map Stack and Geospatial Application Surface

Documentation hub:
- `docs/README.md` — use this as the root reading map for the documentation set.

Dokümantasyon merkezi:
- `docs/README.md` — dokümantasyon setinin kök okuma haritası olarak bunu kullan.

## Overview

This document records the current design truth for the future map-stack and geospatial application surface of LogisticSearch.

It is intentionally **not** a crawler-core runtime contract.

Its job is to preserve the architectural separation between:

1. crawler-side geospatial data acquisition and enrichment
2. application-side map rendering, live position display, and operator-facing geospatial interaction

## Genel Bakış

Bu belge, LogisticSearch’in gelecekteki harita yığını ve coğrafi uygulama yüzeyi için mevcut tasarım doğrusunu kaydeder.

Bilinçli olarak bir crawler-core runtime sözleşmesi **değildir**.

Görevi, şu iki alan arasındaki mimari ayrımı korumaktır:

1. crawler tarafındaki coğrafi veri edinimi ve zenginleştirme
2. uygulama tarafındaki harita gösterimi, canlı konum görünümü ve operatör-yüzlü coğrafi etkileşim

## Purpose

This document exists so that map-library choice does not accidentally leak into the wrong technical section.

The project needs one explicit home for:

- future map-library choice
- screen-by-screen geospatial UI role separation
- live-tracking transport choice
- shared database truth for map-facing data
- the boundary between crawler-acquired coordinates and application-rendered map views

## Amaç

Bu doküman, harita kütüphanesi seçiminin yanlış teknik bölüme sızmaması için vardır.

Projenin şu konular için tek açık bir dokümantasyon evine ihtiyacı vardır:

- gelecekteki harita kütüphanesi seçimi
- ekran bazlı coğrafi UI rol ayrımı
- canlı takip taşıma tercihi
- harita-yüzlü veri için ortak veritabanı doğrusu
- crawler tarafından toplanan koordinatlar ile uygulama tarafından gösterilen harita görünümleri arasındaki sınır

## Current truth boundary

Current truth:

- OpenStreetMap remains a mandatory geospatial data/enrichment component in the long-term system design.
- PostgreSQL/PostGIS remains the canonical geospatial data truth for storage and querying.
- Map presentation-library choice is **not** part of the current SECTION1 webcrawler contract.
- The current application-surface direction is a split-by-purpose map stack rather than a forced single-library rule.

## Güncel doğruluk sınırı

Güncel doğruluk:

- OpenStreetMap, uzun vadeli sistem tasarımında zorunlu coğrafi veri/zenginleştirme bileşeni olarak kalır.
- Depolama ve sorgulama için kanonik coğrafi veri doğrusu PostgreSQL/PostGIS olarak kalır.
- Harita gösterim kütüphanesi seçimi mevcut SECTION1 webcrawler sözleşmesinin parçası **değildir**.
- Mevcut uygulama-yüzeyi yönü, tek kütüphane zorlaması yerine amaca göre ayrılmış bir harita yığınıdır.

## Canonical current decision

The current design direction is:

  * MapLibre GL JS for live operational map views such as vehicle/device/fleet tracking screens
  * MapLibre GL JS as the default public presentation library for firm/branch address maps on the main application surface
  * OpenLayers for technical or analytical map screens where more advanced drawing, measurement, or operator-side spatial tooling may later be needed
  * PostgreSQL/PostGIS as the shared geospatial truth below all surfaces
  * API/service delivery as the controlled application-facing boundary above PostgreSQL/PostGIS
  * GeoJSON-shaped application delivery as the practical interchange surface from backend/API layers into map-facing screens

Default public firm/branch address chain:

  * PostgreSQL/PostGIS -> API -> GeoJSON -> MapLibre GL JS
## Kanonik güncel karar

Mevcut tasarım yönü şudur:

  * araç/cihaz/filo takibi gibi canlı operasyon harita görünümleri için MapLibre GL JS
  * ana uygulama yüzeyindeki firma/şube adres haritaları için varsayılan kamuya-açık gösterim kütüphanesi olarak MapLibre GL JS
  * ileride daha gelişmiş çizim, ölçüm veya operatör-tarafı uzamsal araçlar gerekebilecek teknik/analitik harita ekranları için OpenLayers
  * tüm yüzeylerin altında ortak coğrafi doğruluk olarak PostgreSQL/PostGIS
  * PostgreSQL/PostGIS üzerinde kontrollü uygulama-yüzlü sınır olarak API/service teslimi
  * backend/API katmanlarından harita-yüzlü ekranlara pratik aktarım yüzeyi olarak GeoJSON şekilli veri teslimi

Varsayılan kamuya-açık firma/şube adres zinciri:

  * PostgreSQL/PostGIS -> API -> GeoJSON -> MapLibre GL JS
## Live update transport direction

The current direction is also purpose-split here.

### Live operational tracking screens

For truly live position updates, the preferred direction is:

- backend state from PostgreSQL/PostGIS
- push/update delivery through Socket.IO style live transport
- MapLibre GL JS on the receiving screen when continuous motion and rapid refresh visibility matter

### Technical analysis screens

For analytical or operator-tool screens, the default direction is:

- backend/API query
- GeoJSON response
- OpenLayers-based rendering and interaction

If a later technical screen genuinely needs live updates too, that can be added deliberately. But live streaming is not assumed as the default for every map screen.

## Canlı güncelleme taşıma yönü

Bu alanda da güncel yön amaca göre ayrılmıştır.

### Canlı operasyon takip ekranları

Gerçekten canlı konum güncellemeleri için tercih edilen yön şudur:

- PostgreSQL/PostGIS tabanlı backend durumu
- Socket.IO benzeri canlı taşıma ile push/update teslimi
- sürekli hareket ve hızlı yenileme görünürlüğünün önemli olduğu ekranda MapLibre GL JS

### Teknik analiz ekranları

Analitik veya operatör-aracı ekranları için varsayılan yön şudur:

- backend/API sorgusu
- GeoJSON yanıtı
- OpenLayers tabanlı gösterim ve etkileşim

İleride gerçekten canlı güncelleme gerektiren teknik bir ekran olursa bu ayrıca eklenebilir. Ancak canlı akış her harita ekranı için varsayılan kabul edilmez.

### Live client-side motion rendering rule

For live tracking screens, incoming position updates do not need to arrive at animation-frame frequency.

A backend or transport layer may legitimately deliver vehicle/device/fleet updates every few seconds or even at longer controlled intervals.

The receiving application screen may still render smoother visible motion between confirmed updates.

The current preferred direction is:

- keep durable position truth in backend/database layers
- deliver live updates through Socket.IO style transport when the screen is a real live-tracking surface
- interpolate on the client side between confirmed points with `requestAnimationFrame`
- update the visible map source in place through source-level data refresh such as `map.getSource('vehicles').setData(...)` or an equivalent direct source-update path
- avoid full map reinitialization or coarse full-screen refresh just to move a live marker

This rule is a rendering and interaction policy.

It must not be misread as permission to invent location truth beyond the most recent confirmed backend updates.

### Canlı istemci-tarafı hareket gösterim kuralı

Canlı takip ekranlarında gelen konum güncellemelerinin animation-frame frekansında gelmesi gerekmez.

Backend veya taşıma katmanı, araç/cihaz/filo güncellemelerini meşru olarak birkaç saniyede bir hatta daha uzun kontrollü aralıklarla teslim edebilir.

Buna rağmen alıcı uygulama ekranı, doğrulanmış güncellemeler arasındaki görünür hareketi daha yumuşak biçimde gösterebilir.

Güncel tercih edilen yön şudur:

- kalıcı konum doğrusunu backend/veritabanı katmanlarında tutmak
- ekran gerçekten canlı takip yüzeyiyse güncellemeleri Socket.IO benzeri taşıma ile vermek
- doğrulanmış noktalar arasında istemci tarafında `requestAnimationFrame` ile interpolation yapmak
- görünür harita kaynağını `map.getSource('vehicles').setData(...)` gibi source-seviyesinde veri güncellemesiyle veya eşdeğer doğrudan kaynak-güncelleme yolu ile yerinde güncellemek
- canlı marker hareketi için haritanın tamamını yeniden başlatmamak ve kaba tam-ekran yenileme yapmamak

Bu kural bir gösterim ve etkileşim politikasıdır.

En son doğrulanmış backend güncellemelerinin ötesinde konum doğrusu uydurma izni gibi okunmamalıdır.

## Boundary against SECTION1 webcrawler

This topic belongs outside SECTION1 because SECTION1 is responsible for crawler/runtime/data-acquisition truth, not UI-library choice.

SECTION1 may still document geospatial items such as:

- whether the crawler acquires coordinates
- how address-to-coordinate enrichment is handled
- what GeoJSON-ready or PostGIS-ready geospatial truth is emitted
- what OSM-facing acquisition limits, service boundaries, or enrichment constraints exist

But SECTION1 should not become the place that decides:

- MapLibre GL JS vs OpenLayers
- live dashboard rendering choice
- operator-facing map interaction choice
- application-screen transport choice by itself

## SECTION1 webcrawler ile sınır

Bu konu SECTION1 dışında yer alır; çünkü SECTION1’in görevi UI-kütüphanesi seçimi değil, crawler/runtime/veri-edinim doğrusudur.

SECTION1 yine de şu coğrafi konuları dokümante edebilir:

- crawler’ın koordinat toplayıp toplamadığı
- adresten koordinata zenginleştirmenin nasıl ele alındığı
- hangi GeoJSON-hazır veya PostGIS-hazır coğrafi doğrunun üretildiği
- OSM’e bakan veri edinim limitleri, servis sınırları veya enrichment kısıtları

Ama SECTION1 şu kararların yeri olmamalıdır:

- MapLibre GL JS mi OpenLayers mı
- canlı dashboard gösterim tercihi
- operatör-yüzlü harita etkileşim tercihi
- uygulama ekranı taşıma tercihi

## Current implementation honesty

This document records a design direction, not a claim that the full map stack is already implemented.

Current truth is only this:

- the direction has been chosen
- the boundary has been clarified
- the repository now has an explicit place to preserve that decision without polluting SECTION1

## Mevcut implementasyon dürüstlüğü

Bu doküman tam harita yığınının zaten uygulanmış olduğunu iddia etmez; yalnızca tasarım yönünü kaydeder.

Güncel doğruluk yalnızca şudur:

- yön seçilmiştir
- sınır netleştirilmiştir
- repository artık bu kararı SECTION1’i kirletmeden koruyacak açık bir yere sahiptir
