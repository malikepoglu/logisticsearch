"""\
EN:
This file is the single canonical root entry for the current webcrawler runtime tree.

Topological contract:
1) This file is intentionally thin.
2) It must not own crawler policy, worker state, DB access, or loop branching.
3) It imports exactly one next-level callable and returns that callable's integer
   process status unchanged.
4) Its only observable payload is the delegated exit code.

TR:
Bu dosya mevcut webcrawler runtime ağacının tek kanonik kök giriş noktasıdır.

Topolojik sözleşme:
1) Bu dosya bilinçli olarak ince tutulur.
2) Crawler policy, worker state, DB access veya loop branching sahipliği yapmaz.
3) Tam olarak bir alt-seviye çağrılabilir içe aktarır ve onun ürettiği tamsayı
   süreç durum kodunu değiştirmeden geri döndürür.
4) Dışarıya görünen tek payload delege edilen çıkış kodudur.
"""

# EN: The root entry imports the next topological layer and gives it a visually
# EN: explicit alias. This alias is always expected to be a callable that accepts
# EN: no arguments here and returns an integer process-style exit status.
# TR: Kök giriş bir alt topolojik katmanı içe aktarır ve ona görsel olarak açık
# TR: bir takma ad verir. Buradaki beklenti bu takma adın parametresiz çağrılabilen
# TR: ve tamsayı süreç-benzeri çıkış kodu döndüren bir callable olmasıdır.
from .logisticsearch1_1_main_loop import main as run_main_loop


def main() -> int:
    """\
    EN:
    Execute the next topological runtime layer and return its status unchanged.

    Return contract:
    - int: delegated process exit status from logisticsearch1_1_main_loop.main().
    - No dict/payload/None branch exists at this layer.
    - Unexpected exceptions are intentionally not swallowed here; they should
      remain visible to the outer Python process.

    TR:
    Bir alt topolojik runtime katmanını çalıştırır ve onun durum kodunu aynen döndürür.

    Dönüş sözleşmesi:
    - int: logisticsearch1_1_main_loop.main() tarafından üretilen delege süreç
      çıkış kodu.
    - Bu katmanda dict/payload/None dalı yoktur.
    - Beklenmeyen istisnalar burada özellikle yutulmaz; dış Python sürecine görünür
      kalmalıdır.
    """

    # EN: There is no local branch logic here. We delegate immediately so this
    # EN: file stays a truthful root-entry wrapper instead of becoming a second
    # EN: hidden control layer.
    # TR: Burada yerel branch mantığı yoktur. Bu dosya gizli ikinci bir kontrol
    # TR: katmanına dönüşmesin diye hemen delegasyon yapıyoruz.
    return run_main_loop()


if __name__ == "__main__":
    # EN: SystemExit(main()) preserves the delegated integer exit code when the
    # EN: module is executed directly with Python.
    # TR: SystemExit(main()) modül Python ile doğrudan çalıştırıldığında delege
    # TR: edilen tamsayı çıkış kodunu korur.
    raise SystemExit(main())
