# EN: This module is the canonical root entry surface for the webcrawler runtime.
# TR: Bu modül, webcrawler runtime'ı için kanonik kök giriş yüzeyidir.

# EN: Tree logic says there must be a single root entry at the top.
# EN: That root entry should stay thin and should hand control to the main loop below it.
# TR: Ağaç mantığına göre en üstte tek bir kök giriş olmalıdır.
# TR: Bu kök giriş ince kalmalı ve kontrolü altındaki ana loop'a devretmelidir.

# EN: We import the real main loop from the next topological level.
# TR: Gerçek ana loop'u bir alt topolojik seviyeden içeri aktarıyoruz.
from .logisticsearch1_1_main_loop import main as run_main_loop


# EN: This function is the explicit callable root entry.
# TR: Bu fonksiyon açık çağrılabilir kök giriş noktasıdır.
def main() -> None:
    # EN: Delegate execution to the main continuous loop.
    # TR: Çalıştırmayı ana sürekli loop'a devret.
    run_main_loop()


# EN: This standard guard allows canonical module execution.
# TR: Bu standart guard kanonik modül çalıştırmasını sağlar.
if __name__ == "__main__":
    # EN: Start from the canonical root entry.
    # TR: Kanonik kök girişten başlat.
    main()
