# Hosts Surface
# Host Yüzeyi

Documentation hub:
- `README.md` — repository root surface
- `docs/README.md` — documentation hub

Dokümantasyon merkezi:
- `README.md` — repository kök yüzeyi
- `docs/README.md` — dokümantasyon merkezi

## Purpose
## Amaç

This directory is the canonical repository-tracked host-operations family.

It exists to describe the operational truth of concrete machines used by the project in a controlled, beginner-readable, and audit-friendly form.

At the current repository point, it also contains explicitly validated host-scoped tracked work surfaces where the repository has intentionally been organized that way.

This family does **not** mean whole-machine byte-for-byte filesystem mirroring.

This family does **not** mean every repository surface for every host must blindly move under `hosts/`.

Bu dizin, kanonik repository-tracked host-operations ailesidir.

Bu aile, projede kullanılan somut makinelerin operasyonel doğrusunu kontrollü, beginner-okunur ve denetim-dostu biçimde açıklamak için vardır.

Mevcut repository noktasında bu aile, repository bilinçli olarak bu şekilde düzenlendiğinde açıkça doğrulanmış host-kapsamlı tracked çalışma yüzeylerini de içerir.

Bu aile, makinelerin tamamının byte-for-byte filesystem aynası anlamına **gelmez**.

Bu aile, her repository yüzeyinin her host için kör biçimde `hosts/` altına taşınması gerektiği anlamına **gelmez**.

## Current canonical rule
## Güncel kanonik kural

At the current repository point, the active crawler-host tracked work surfaces live under:

- `hosts/makpi51crawler/python/`
- `hosts/makpi51crawler/sql/`
- `hosts/makpi51crawler/crawler_exports/`
- `docs/` remains the repository-wide documentation root at repository top level

The `hosts/` family therefore carries both host-operational truth and the explicitly validated host-scoped work surfaces of `makpi51crawler`.

Mevcut repository noktasında aktif crawler-host tracked çalışma yüzeyleri şu yollar altında yaşar:

- `hosts/makpi51crawler/python/`
- `hosts/makpi51crawler/sql/`
- `hosts/makpi51crawler/crawler_exports/`
- `docs/`, repository-geneli dokümantasyon kökü olarak repository üst seviyesinde kalır

Bu nedenle `hosts/` ailesi, hem host-operasyon doğrusunu hem de `makpi51crawler` için açıkça doğrulanmış host-kapsamlı çalışma yüzeylerini taşır.

## What belongs here
## Buraya ne aittir

Typical content for this family includes:

- host identity and naming truth
- access model and authentication notes
- path map of important real machine locations
- storage boundary and mount policy
- runtime and systemd surface map
- sync boundary and operational warnings
- host-specific runbooks
- host-specific prohibitions and operator notes

Bu aileye tipik olarak şunlar aittir:

- host kimliği ve adlandırma doğrusu
- erişim modeli ve kimlik doğrulama notları
- önemli gerçek makine yollarının path map'i
- storage boundary ve mount politikası
- runtime ve systemd yüzey haritası
- senkronizasyon sınırı ve operasyon uyarıları
- host-özel runbook'lar
- host-özel yasaklar ve operatör notları

## What does not belong here
## Buraya ne ait değildir

The following should not be moved here blindly:

- whole-machine dumps or byte-for-byte mirrors
- disposable host-local clutter, caches, virtual environments, and scratch artifacts
- repository-global files like `.gitignore`, root `README.md`, and `docs/README.md`
- unrelated surfaces moved here only because a host happens to use them, without an explicit validated design decision

Aşağıdakiler buraya kör biçimde taşınmamalıdır:

- tam makine dump'ları veya byte-for-byte aynalar
- tek kullanımlık host-yerel dağınık içerikler, cache'ler, sanal ortamlar ve scratch artefact'ları
- `.gitignore`, kök `README.md` ve `docs/README.md` gibi repository-geneli dosyalar
- yalnızca bir host kullanıyor diye, açıkça doğrulanmış bir tasarım kararı olmadan buraya taşınan ilgisiz yüzeyler

## Current scope
## Güncel kapsam

1. `hosts/makpi51crawler/` is the first active host surface because the project is currently focused on the crawler node.
2. `hosts/mak-UbuntuDesktop/` remains only a placeholder until its own turn arrives.
3. `hosts/makpi51crawler/` now intentionally contains the active tracked `python/`, `sql/`, and `crawler_exports/` work surfaces for the crawler host.

1. `hosts/makpi51crawler/` proje şu anda crawler düğümüne odaklandığı için ilk aktif host yüzeyidir.
2. `hosts/mak-UbuntuDesktop/` kendi sırası gelene kadar yalnızca placeholder olarak kalır.
3. `hosts/makpi51crawler/` artık crawler host'u için aktif tracked `python/`, `sql/` ve `crawler_exports/` çalışma yüzeylerini bilinçli olarak içerir.
