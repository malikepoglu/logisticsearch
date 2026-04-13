# Host Surface: makpi51crawler
# Host Yüzeyi: makpi51crawler

Documentation hub:
- `hosts/README.md` — host family root
- `README.md` — repository root surface
- `docs/README.md` — documentation hub

Dokümantasyon merkezi:
- `hosts/README.md` — host aile kökü
- `README.md` — repository kök yüzeyi
- `docs/README.md` — dokümantasyon merkezi

## Purpose
## Amaç

This directory is the canonical repository-tracked operational truth surface for the real crawler host `makpi51crawler`.

It is meant to explain the host clearly.

It is **not** a full filesystem dump.

It is **not** the place where shared repository work surfaces such as root `python/`, root `sql/`, or root `crawler_exports/` must be physically relocated.

Bu dizin, gerçek crawler host'u `makpi51crawler` için kanonik repository-tracked operasyon doğrusu yüzeyidir.

Amacı host'u açık biçimde anlatmaktır.

Bu dizin **tam filesystem dump'ı** değildir.

Bu dizin, kök `python/`, kök `sql/` veya kök `crawler_exports/` gibi ortak repository çalışma yüzeylerinin fiziksel olarak taşınması gereken yer **değildir**.

## Current host reading model
## Güncel host okuma modeli

Read this host surface like this:

1. understand what the real machine is
2. understand which real machine paths matter
3. understand access and identity boundaries
4. understand storage and runtime boundaries
5. only then map those truths back to the shared repository root surfaces

Bu host yüzeyini şu sırayla oku:

1. gerçek makinenin ne olduğunu anla
2. hangi gerçek makine yollarının önemli olduğunu anla
3. erişim ve kimlik sınırlarını anla
4. storage ve runtime sınırlarını anla
5. ancak ondan sonra bu doğruları ortak repository kök yüzeylerine geri bağla

## What should be documented here
## Burada ne belgelenmelidir

This surface should later document:

- host identity, hostname, and role truth
- important real paths under `/srv`, the repo checkout path, and related operational boundaries
- SSH/access model
- sparse-checkout or checkout-shape realities if they matter operationally
- local runtime, systemd, crawler, database, export, and storage boundaries
- operator warnings and recovery notes

Bu yüzey daha sonra şunları belgelemelidir:

- host kimliği, hostname ve rol doğrusu
- `/srv` altındaki önemli gerçek yollar, repo checkout yolu ve ilgili operasyon sınırları
- SSH/erişim modeli
- operasyonel olarak önemliyse sparse-checkout veya checkout-shape gerçekleri
- yerel runtime, systemd, crawler, veritabanı, export ve storage sınırları
- operatör uyarıları ve toparlama notları

## What should not be done here
## Burada ne yapılmamalıdır

Do not interpret this host surface as an instruction to relocate shared root project trees under `hosts/makpi51crawler/`.

Do not assume that GitHub-only path moves are harmless for other checkouts of the same branch.

Do not mix host-documentation intent with physical repository-tree relocation without an explicit, separately validated design decision.

Bu host yüzeyini, ortak kök proje ağaçlarının `hosts/makpi51crawler/` altına taşınması talimatı olarak yorumlama.

Aynı branch'in diğer checkout'ları için GitHub-only path taşımalarının zararsız olduğunu varsayma.

Host-dokümantasyon niyetini, açık ve ayrıca doğrulanmış bir tasarım kararı olmadan fiziksel repository-ağacı taşımasıyla karıştırma.

## Current state
## Güncel durum

This host surface is open and active, but still intentionally thin.

The next correct growth direction is stronger host-operational documentation, not blind repository-tree relocation.

Bu host yüzeyi açık ve aktiftir, ancak hâlâ bilinçli olarak incedir.

Bir sonraki doğru büyüme yönü kör repository-ağacı taşıması değil, daha güçlü host-operasyon dokümantasyonudur.
