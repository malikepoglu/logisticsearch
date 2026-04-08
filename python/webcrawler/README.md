# Webcrawler Python Surface

This is the first real Python-side worker surface for LogisticSearch.

# Webcrawler Python Yüzeyi

Bu, LogisticSearch için ilk gerçek Python-tarafı worker yüzeyidir.

## Purpose

## Amaç

This directory is the first real Python-side worker surface for the LogisticSearch webcrawler.

Bu dizin, LogisticSearch webcrawler için ilk gerçek Python-tarafı worker yüzeyidir.

Its current scope is intentionally narrow and controlled.

It does not yet provide a real HTTP fetch runtime.

Güncel kapsamı bilinçli olarak dar ve kontrollüdür.

Henüz gerçek bir HTTP fetch runtime'ı sağlamaz.

It exists to do only the first real Python work that the current repository truth safely allows:

Şu anda repository doğrusunun güvenli biçimde izin verdiği ilk gerçek Python işini yapmak için vardır:

1. connect to PostgreSQL
2. call the canonical crawler-core claim entry point
3. represent the claimed row in Python
4. expose lease-aware runtime helpers
5. keep the implementation aligned with the current docs/contracts

1. PostgreSQL’e bağlanmak
2. kanonik crawler-core claim giriş noktasını çağırmak
3. claim edilen satırı Python içinde temsil etmek
4. lease-aware runtime yardımcılarını açmak
5. implementasyonu mevcut dokümanlar/sözleşmeler ile hizalı tutmak

## Current truth boundary

## Güncel gerçeklik sınırı

This surface does **not** yet prove a full crawler runtime.

Bu yüzey henüz tam bir crawler runtime’ını **kanıtlamaz**.

It does **not** yet provide:

Henüz şunları sağlamaz:

- a full HTTP fetch engine
- HTML parsing
- link extraction
- robots cache refresh implementation
- success/retry/permanent finalization wiring
- service-layer service/runtime orchestration
- poweroff/reboot helper implementation

- tam bir HTTP fetch motoru
- HTML parse etme
- link extraction
- robots cache refresh implementasyonu
- success/retry/permanent finalization bağlama yüzeyi
- service-layer servis/runtime orkestrasyonu
- poweroff/reboot helper implementasyonu

## Files

## Dosyalar

- `worker_claim_loop.py`
- `lib/db.py`
- `lib/worker_runtime.py`

## Authoritative basis

## Otoritatif temel

This directory must always be read and evolved together with:

Bu dizin daima şu yüzeylerle birlikte okunmalı ve geliştirilmelidir:

- `docs/SECTION1_WEBCRAWLER_WORKER_OPERATIONAL_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_WORKER_HEARTBEAT_OPERATING_RULE.md`
- `docs/SECTION1_WEBCRAWLER_LEASE_RENEWAL_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_DRAIN_AND_GRACEFUL_SHUTDOWN_CONTRACT.md`
- `docs/SECTION1_WEBCRAWLER_CONTROLS.md`
- `docs/SECTION1_WEBCRAWLER_LIFECYCLE_CONTRACT.md`
- `sql/crawler_core/README.md`

## Working rule

## Çalışma kuralı

Every future change in this Python surface must remain honest about current implementation truth.

Bu Python yüzeyindeki her gelecek değişiklik, güncel implementasyon doğrusu hakkında dürüst kalmalıdır.

The code must not pretend that missing runtime layers already exist.

Kod, eksik runtime katmanları şimdiden varmış gibi davranmamalıdır.


## Controlled dependency surface

This directory now has one tracked dependency surface: `requirements.txt`.

At the current repository truth, it must stay intentionally narrow.

Its purpose is only to define the minimum importable runtime dependency needed by the first probe-only worker surface.

Current controlled dependency rule:

- use `psycopg[binary]==3.3.3`
- do not pretend that HTTP fetch, parsing, or service orchestration dependencies already exist
- keep the future local virtual environment machine-local and untracked
- widen this dependency file only when the GitHub-tracked docs/contracts and real implementation scope genuinely widen

## Kontrollü bağımlılık yüzeyi

Bu dizinin artık bir izlenen bağımlılık yüzeyi vardır: `requirements.txt`.

Güncel repository doğrusunda bu yüzey bilinçli olarak dar kalmalıdır.

Amacı yalnızca ilk probe-only worker yüzeyinin ihtiyaç duyduğu en küçük import edilebilir runtime bağımlılığını tanımlamaktır.

Güncel kontrollü bağımlılık kuralı:

- `psycopg[binary]==3.3.3` kullan
- HTTP fetch, parse veya servis orkestrasyonu bağımlılıkları şimdiden varmış gibi davranma
- gelecekteki yerel sanal ortamı makine-yerel ve izlenmeyen bırak
- bu bağımlılık dosyasını ancak GitHub’da izlenen dokümanlar/sözleşmeler ve gerçek implementasyon kapsamı gerçekten genişlediğinde genişlet
