# Kramponomi

Futbolcu piyasa değerleri, kulüp kadro değerleri, transferler ve puan durumları.
Şu an: Trendyol Süper Lig (18 kulüp) ve Serie A (18/20 kulüp).

## Yapı
- `data/leagues.json` ligler (lig tabanı katsayısı dahil)
- `data/clubs/<lig>/<kulüp>.json` kadrolar: ad, no, mevki, yaş, uyruk, maç, yedek, gol, asist, dakika, seviye (1-10)
- `data/standings/<lig>.json` puan durumu, `data/transfers.json` transferler
- `data/values.json` dondurulmuş piyasa değerleri. Değerler yılda iki kez, transfer dönemi öncesi gece `python3 build.py --revalue` ile yeniden hesaplanır; normal derleme değerleri değiştirmez
- `data/value_history.json` her değer güncellemesinin kaydı (değer grafiği)
- `valuation.py` değer formülü, `build.py` site üretici, `tools_import.py` ham kadro dönüştürücü

## Derleme
`python3 build.py` → `docs/` (GitHub Pages buradan yayınlar)
