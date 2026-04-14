# Python Surface: makpi51crawler
# Python Yüzeyi: makpi51crawler

Documentation hub:

* `hosts/makpi51crawler/README.md` — host root for makpi51crawler
* `hosts/README.md` — host family root
* `README.md` — repository root surface
* `docs/README.md` — documentation hub

Dokümantasyon merkezi:

* `hosts/makpi51crawler/README.md` — makpi51crawler host kökü
* `hosts/README.md` — host aile kökü
* `README.md` — repository kök yüzeyi
* `docs/README.md` — dokümantasyon merkezi

## Purpose
## Amaç

This directory is the host-scoped Python surface for `makpi51crawler`.

Bu dizin, `makpi51crawler` için host-kapsamlı Python yüzeyidir.

It exists to hold repository-worthy Python material that belongs to the crawler host line and must remain reviewable, versioned, and reproducible.

Amacı, crawler host hattına ait olan ve gözden geçirilebilir, versiyonlanabilir ve tekrar üretilebilir kalması gereken repository-değerindeki Python materyalini barındırmaktır.

## Current tracked sub-surfaces
## Güncel izlenen alt yüzeyler

* `hosts/makpi51crawler/python/desktop_import/README.md` — narrow Desktop-import helper line kept under the host-scoped Python family
* `hosts/makpi51crawler/python/webcrawler/README.md` — current controlled Python-side crawler runtime surface
* `hosts/makpi51crawler/python/webcrawler/lib/README.md` — crawler runtime library family and internal module layout

* `hosts/makpi51crawler/python/desktop_import/README.md` — host-kapsamlı Python ailesi altında tutulan dar Desktop-import yardımcı hattı
* `hosts/makpi51crawler/python/webcrawler/README.md` — mevcut kontrollü Python-tarafı crawler runtime yüzeyi
* `hosts/makpi51crawler/python/webcrawler/lib/README.md` — crawler runtime kütüphane ailesi ve iç modül yerleşimi

## Current judgement
## Güncel değerlendirme

At the current repository point, this directory must no longer be read as a `desktop_import`-only area.

Mevcut repository noktasında bu dizin artık yalnızca `desktop_import` alanı gibi okunmamalıdır.

The current truth is that this Python surface contains two distinct lines:

* a narrow helper/import line
* an active webcrawler runtime line

Güncel gerçek, bu Python yüzeyinin iki ayrı hattı içerdiğidir:

* dar kapsamlı bir yardımcı/import hattı
* aktif bir webcrawler runtime hattı

The webcrawler line is the more active engineering direction and should be treated as the primary live runtime family under this host-scoped Python surface.

Webcrawler hattı daha aktif mühendislik yönüdür ve bu host-kapsamlı Python yüzeyi altındaki birincil canlı runtime ailesi olarak ele alınmalıdır.

## Boundary
## Sınır

Only durable and repository-worthy Python content should live here.

Burada yalnızca kalıcı ve repository’ye girmeye değer Python içerikleri yer almalıdır.

Machine-local virtual environments, cache directories, throwaway experiments, temporary outputs, and other disposable artifacts must stay outside Git or remain ignored.

Makineye özel sanal ortamlar, cache dizinleri, tek kullanımlık denemeler, geçici çıktılar ve diğer atıl artefact’lar Git dışında kalmalı veya ignore edilmelidir.
