"""Serie A içe aktarma (sonradan eklenen kulüpler). Seviye puanları editör (Claude) değerlendirmesi; listede olmayan 5, 19 yaş ve altı 4.5.
Mevcut Serie A kulüplerinin günlük güncellemesi tools/update_squad.py ile yapılır (seviyeler korunur)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from league_tool import run

META = {
    "torino": ("Torino", "Torino", "Stadio Olimpico Grande Torino"),
    "frosinone": ("Frosinone", "Frosinone", "Stadio Benito Stirpe"),
}

C = """
torino: Lucas Perri 6|Franco Israel 5.5|Nathan Patterson 5.5|Cristiano Biraghi 4.5|Eray Cömert 5.5|Ricardo Rodríguez 4.5|Pietro Comuzzo 6.5|Saúl Coco 6|Niccolò Fortini 5.5|Adrian Ismajli 5.5|Rafik Belghali 6|Emirhan Ilkhan 6|Rolando Mandragora 6|Nikola Vlasic 6.5|Gaetano Oristanio 6|Daniel Bragança 6|Cesare Casadei 6.5|Kian Fitz-Jim 6|Gvidas Gineitis 6|Alessio Cacciamani 5|Zakaria Aboukhlal 6|Pietro Pellegri 5|Sandro Kulenovic 6|Giovanni Simeone 6|Ché Adams 6|Duván Zapata 4
frosinone: Lorenzo Palmisani 6|Giorgio Cittadini 5.5|Gabriele Calvani 5.5|Anthony Oyono 5.5|Ilario Monterisi 5.5|Aleksa Terzic 5.5|Gabriele Bracaglia 5.5|Romano Schmid 6|Giacomo Calo 5.5|Matteo Cichella 5.5|Florian Grillitsch 5|Anouar El Azzouzi 5.5|Luis Hasa 5.5|Patrizio Masini 5.5|Farès Ghedjemis 5.5|Antonio Raimondo 6.5|Daniel Birligea 5.5|Giorgi Kvernadze 6|Alessio Zerbin 5.5
"""

if __name__ == "__main__":
    run("serie-a", sys.argv[1] if len(sys.argv) > 1 else "tools/raw/serie-a", META, C,
        "ESPN kadro istatistikleri (Serie A)", "2026-11-27")
