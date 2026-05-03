#!/usr/bin/env python3
"""Project sync dispatcher with safe coreutils passthrough.

EN:
This file intentionally shares the command name "sync" only as a project-level
dispatcher source. It must never replace /usr/bin/sync. Unknown, empty, or
coreutils-style invocations pass through to /usr/bin/sync unchanged.

Supported project subcommands:
- sync repo
- sync runtime
- sync makpi51crawler

TR:
Bu dosya "sync" adını yalnızca proje-seviyesi dispatcher source olarak kullanır.
/usr/bin/sync asla değiştirilmez. Bilinmeyen, boş veya coreutils tarzı çağrılar
değiştirilmeden /usr/bin/sync komutuna aktarılır.

Desteklenen proje alt komutları:
- sync repo
- sync runtime
- sync makpi51crawler
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


COREUTILS_SYNC = "/usr/bin/sync"
PROJECT_SUBCOMMANDS = {"repo", "runtime", "makpi51crawler"}


try:
    from . import sync_makpi51crawler, sync_repo, sync_runtime
except ImportError:  # pragma: no cover - direct script/importlib fallback
    # EN: When loaded directly with importlib.spec_from_file_location or executed
    # as a script, sibling modules may not be on sys.path. Add this directory.
    #
    # TR: Bu dosya doğrudan script/importlib ile yüklendiğinde kardeş modüller
    # sys.path içinde olmayabilir. Bu klasörü açıkça ekle.
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

    import sync_makpi51crawler  # type: ignore[no-redef]
    import sync_repo  # type: ignore[no-redef]
    import sync_runtime  # type: ignore[no-redef]


def _exec_coreutils_sync(argv: list[str]) -> None:
    """Exec /usr/bin/sync with original arguments.

    EN: os.execv replaces the current process; it returns only on failure.
    TR: os.execv mevcut sürecin yerine geçer; yalnızca hata olursa geri döner.
    """

    os.execv(COREUTILS_SYNC, ["sync", *argv])


def _print_help() -> None:
    print("Project sync dispatcher")
    print()
    print("Project subcommands:")
    print("  sync repo [args...]")
    print("  sync runtime [args...]")
    print("  sync makpi51crawler [args...]")
    print()
    print("Safety:")
    print("  Unknown/no-arg/coreutils-style calls pass through to /usr/bin/sync.")
    print("  This dispatcher must not replace /usr/bin/sync.")
    print()
    print("Examples:")
    print("  sync repo --help")
    print("  sync runtime --help")
    print("  sync makpi51crawler --help")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if args and args[0] in {"-h", "--help"}:
        _print_help()
        return 0

    if not args:
        _exec_coreutils_sync(args)
        return 0

    subcommand = args[0]
    subcommand_args = args[1:]

    if subcommand == "repo":
        return sync_repo.main(subcommand_args)

    if subcommand == "runtime":
        return sync_runtime.main(subcommand_args)

    if subcommand == "makpi51crawler":
        return sync_makpi51crawler.main(subcommand_args)

    _exec_coreutils_sync(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
