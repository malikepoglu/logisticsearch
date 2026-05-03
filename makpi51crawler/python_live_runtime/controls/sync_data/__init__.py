"""LogisticSearch controlled repository/runtime synchronization helpers.

EN:
This package replaces the old live-only /logisticsearch/bin sync surface with
tracked Python controls. The helpers are intentionally operator-triggered and
verification-heavy. They do not start the crawler service by default and do not
touch PostgreSQL.

TR:
Bu paket eski live-only /logisticsearch/bin sync yüzeyinin yerine tracked Python
kontrolleri sağlar. Yardımcılar bilinçli olarak operatör tetikli ve doğrulama
ağırlıklıdır. Varsayılan olarak crawler servisini başlatmaz ve PostgreSQL'e
dokunmaz.
"""

from __future__ import annotations

__all__ = [
    "sync_repo",
    "sync_runtime",
    "sync_all",
]
