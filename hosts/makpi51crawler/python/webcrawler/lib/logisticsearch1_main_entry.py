# EN: This module is the canonical root entry surface for the webcrawler runtime.
# TR: Bu modül, webcrawler runtime'ı için kanonik kök giriş yüzeyidir.

# EN: Tree logic says there must be exactly one thin root entry at the top.
# EN: That root entry must not own worker logic, DB logic, or loop policy.
# EN: Its only job is to delegate execution to the next topological level and
# EN: preserve the real process exit code honestly.
# TR: Ağaç mantığına göre en üstte tam olarak tek bir ince kök giriş olmalıdır.
# TR: Bu kök giriş worker mantığına, DB mantığına veya loop politikasına sahip
# TR: olmamalıdır. Tek görevi, çalıştırmayı bir alt topolojik seviyeye devretmek
# TR: ve gerçek süreç çıkış kodunu dürüst biçimde korumaktır.

# EN: We import the real main loop from the next topological level.
# EN: We alias it to run_main_loop so the role of this imported callable stays
# EN: visually explicit at the root-entry layer.
# TR: Gerçek ana loop'u bir alt topolojik seviyeden içe aktarıyoruz.
# TR: Bu içe aktarılan çağrılabilirin rolü kök giriş katmanında görsel olarak
# TR: açık kalsın diye ona run_main_loop takma adını veriyoruz.
from .logisticsearch1_1_main_loop import main as run_main_loop


# EN: This function is the explicit callable root entry.
# EN: It must stay thin and must return the exact integer process status produced
# EN: by the delegated main loop instead of swallowing it.
# TR: Bu fonksiyon açık çağrılabilir kök giriş noktasıdır.
# TR: İnce kalmalı ve devredilen ana loop'un ürettiği tam sayı süreç durum kodunu
# TR: yutmadan aynen geri döndürmelidir.
def main() -> int:
    # EN: We delegate execution to the main continuous loop and return its status
    # EN: unchanged so outer CLI callers can preserve the real result.
    # TR: Çalıştırmayı ana sürekli loop'a devrediyor ve dış CLI çağıranları gerçek
    # TR: sonucu koruyabilsin diye onun durum kodunu değiştirmeden geri döndürüyoruz.
    return run_main_loop()


# EN: This standard guard allows canonical module execution.
# EN: We raise SystemExit with main() so direct module execution preserves the
# EN: returned integer status code in normal Python CLI style.
# TR: Bu standart guard kanonik modül çalıştırmasını sağlar.
# TR: main() ile SystemExit yükseltiyoruz; böylece modül doğrudan çalıştırıldığında
# TR: dönen tam sayı durum kodu normal Python CLI stilinde korunur.
if __name__ == "__main__":
    raise SystemExit(main())
