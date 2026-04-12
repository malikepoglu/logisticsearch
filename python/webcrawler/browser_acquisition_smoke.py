from __future__ import annotations

# EN: We use argparse because this smoke entry must accept explicit operator
# EN: inputs instead of hiding assumptions in hard-coded paths.
# TR: Bu smoke giriş yüzeyi hard-coded varsayımlar yerine açık operatör girdileri
# TR: almalıdır; bu yüzden argparse kullanıyoruz.
import argparse

# EN: We use json because the smoke result must be written as machine-readable evidence.
# TR: Smoke sonucu makine-okunur kanıt olarak yazılacağı için json kullanıyoruz.
import json

# EN: We use datetime only to build deterministic default output paths with timestamps.
# TR: datetime'ı yalnızca zaman damgalı deterministik varsayılan çıktı yolları
# TR: üretmek için kullanıyoruz.
from datetime import UTC, datetime

# EN: We use Path because evidence files are real filesystem artifacts.
# TR: Kanıt dosyaları gerçek dosya-sistemi artıkları olduğu için Path kullanıyoruz.
from pathlib import Path

# EN: We import the canonical browser-acquisition runtime we just created.
# TR: Az önce oluşturduğumuz kanonik browser-acquisition runtime yüzeyini içe aktarıyoruz.
from lib.browser_acquisition_runtime import acquire_public_page_with_browser


# EN: This helper builds timestamped default evidence paths under /tmp.
# TR: Bu yardımcı /tmp altında zaman damgalı varsayılan kanıt yolları üretir.
def build_default_output_paths() -> tuple[Path, Path, Path]:
    # EN: UTC timestamp keeps cross-host comparison simpler.
    # TR: UTC zaman damgası çoklu host karşılaştırmasını daha sade tutar.
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    html_path = Path(f"/tmp/browser_acquisition_rendered_{ts}.html")
    png_path = Path(f"/tmp/browser_acquisition_screenshot_{ts}.png")
    json_path = Path(f"/tmp/browser_acquisition_result_{ts}.json")
    return html_path, png_path, json_path


# EN: This parser defines the explicit CLI contract of the smoke entry.
# TR: Bu parser smoke giriş yüzeyinin açık CLI sözleşmesini tanımlar.
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Controlled browser-acquisition smoke for LogisticSearch webcrawler."
    )
    parser.add_argument("--url", required=True, help="Public target URL to open in the browser.")
    parser.add_argument(
        "--html-out",
        default=None,
        help="Path to write rendered HTML evidence.",
    )
    parser.add_argument(
        "--screenshot-out",
        default=None,
        help="Path to write screenshot evidence.",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Path to write machine-readable JSON result.",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=30000,
        help="Navigation timeout in milliseconds.",
    )
    parser.add_argument(
        "--wait-until",
        default="networkidle",
        choices=["load", "domcontentloaded", "networkidle", "commit"],
        help="Playwright wait-until mode for page.goto(...).",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Launch browser with a visible window instead of headless mode.",
    )
    return parser


# EN: main wires CLI inputs into the canonical browser-acquisition runtime and
# EN: writes the resulting evidence JSON to disk and stdout.
# TR: main, CLI girdilerini kanonik browser-acquisition runtime yüzeyine bağlar
# TR: ve ortaya çıkan kanıt JSON'unu hem diske hem stdout'a yazar.
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    default_html, default_png, default_json = build_default_output_paths()

    html_out = Path(args.html_out) if args.html_out else default_html
    screenshot_out = Path(args.screenshot_out) if args.screenshot_out else default_png
    json_out = Path(args.json_out) if args.json_out else default_json

    result = acquire_public_page_with_browser(
        target_url=args.url,
        html_output_path=html_out,
        screenshot_output_path=screenshot_out,
        headless=not args.headed,
        wait_until=args.wait_until,
        timeout_ms=args.timeout_ms,
    )

    payload = result.to_dict()
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


# EN: This keeps the file executable as a direct CLI entry.
# TR: Bu sayede dosya doğrudan CLI girişi olarak çalıştırılabilir.
if __name__ == "__main__":
    raise SystemExit(main())
