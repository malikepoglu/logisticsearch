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

This family does **not** replace the repository root working surfaces.

This family does **not** mean that tracked Python, SQL, or crawler export trees must physically move under `hosts/`.

This family does **not** mean whole-machine byte-for-byte filesystem mirroring.

Bu dizin, kanonik repository-tracked host-operations ailesidir.

Bu aile, projede kullanılan somut makinelerin operasyonel doğrusunu kontrollü, beginner-okunur ve denetim-dostu biçimde açıklamak için vardır.

Bu aile repository kökündeki çalışma yüzeylerinin yerini **almaz**.

Bu aile, tracked Python, SQL veya crawler export ağaçlarının fiziksel olarak `hosts/` altına taşınması gerektiği anlamına **gelmez**.

Bu aile, makinelerin tamamının byte-for-byte filesystem aynası anlamına **gelmez**.

## Current canonical rule
## Güncel kanonik kural

Repository root remains the canonical location of the shared project work surfaces such as:

- `python/`
- `sql/`
- `crawler_exports/`
- `docs/`

The `hosts/` family is a host-specific operational truth layer that sits beside those root surfaces.

Repository kökü, aşağıdaki ortak proje çalışma yüzeylerinin kanonik yeri olarak kalır:

- `python/`
- `sql/`
- `crawler_exports/`
- `docs/`

`hosts/` ailesi ise bu kök yüzeylerin yanında duran host-özel operasyon doğrusu katmanıdır.

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

The following should not be moved here merely because a host uses them:

- the shared root `python/` project surface
- the shared root `sql/` project surface
- the shared root `crawler_exports/` project surface
- repository-global files like `.gitignore` and root `README.md`

Aşağıdakiler yalnızca bir host kullandığı için buraya taşınmamalıdır:

- ortak kök `python/` proje yüzeyi
- ortak kök `sql/` proje yüzeyi
- ortak kök `crawler_exports/` proje yüzeyi
- `.gitignore` ve kök `README.md` gibi repository-geneli dosyalar

## Current scope
## Güncel kapsam

1. `hosts/makpi51crawler/` is the first active host surface because the project is currently focused on the crawler node.
2. `hosts/mak-UbuntuDesktop/` remains only a placeholder until its own turn arrives.
3. The presence of a host entry does not automatically imply path relocation of project-wide tracked surfaces.

1. `hosts/makpi51crawler/` proje şu anda crawler düğümüne odaklandığı için ilk aktif host yüzeyidir.
2. `hosts/mak-UbuntuDesktop/` kendi sırası gelene kadar yalnızca placeholder olarak kalır.
3. Bir host girdisinin bulunması, proje-geneli tracked yüzeylerin otomatik olarak path taşıması yapılacağı anlamına gelmez.
