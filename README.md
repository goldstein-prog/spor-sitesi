# Kramponomi

Futbolcu piyasa değerleri, kulüp kadro değerleri, transferler ve puan durumları.
Şu an: Trendyol Süper Lig (18), Premier Lig (20), La Liga (20), Serie A (20), Bundesliga (18) ve Ligue 1 (18 kulüp).

## Yapı
- `data/leagues.json` ligler (lig tabanı katsayısı dahil)
- `data/clubs/<lig>/<kulüp>.json` kadrolar: ad, no, mevki, yaş, uyruk, maç, yedek, gol, asist, dakika, seviye (1-10)
- `data/standings/<lig>.json` puan durumu
- `tools/update_squad.py` mevcut kulübü yeni ham kadroyla günceller (seviyeler korunur); `tools/<lig>.py` lig içe aktarma betikleri
- `data/editor_log.json` olay bazlı seviye değişiklikleri, `data/editor_notes.json` olay sayılmayan notlar, `data/transfers.json` transferler
- `data/values.json` dondurulmuş piyasa değerleri. Değerler yılda iki kez, transfer dönemi öncesi gece `python3 build.py --revalue` ile yeniden hesaplanır; normal derleme değerleri değiştirmez
- `data/value_history.json` her değer güncellemesinin kaydı (değer grafiği)
- `valuation.py` değer formülü, `build.py` site üretici, `tools_import.py` ham kadro dönüştürücü

## Derleme
`python3 build.py` → `docs/` (GitHub Pages buradan yayınlar)

## Olay bazlı değerleme
Her oyuncu siteye eklendiği gün ilk değerini alır. Sonra değer sadece iki durumda değişir:
1. **Transfer dönemlerinden önceki gece** tüm oyuncular (`python3 build.py --revalue`).
2. **Önemli bir olayda** sadece o oyuncu: `data/revalue_requests.json` dosyasına `{"slug": "...", "reason": "kısa Türkçe gerekçe"}` eklenir, sonraki normal `python3 build.py` sadece o oyuncunun değerini yeniden hesaplar, değer geçmişine nedeniyle birlikte yazar ve talebi siler.

Geçerli olaylar (iki kaynakla doğrulanmış olmalı):
- Resmîleşmiş transfer veya kiralık (oyuncu yeni kulübüne taşınır, değer yeni ligin tabanıyla hesaplanır).
- Resmî açıklamayla en az 3 ay sürecek sakatlık (seviye en fazla -0,5).
- Kariyer değiştiren gelişme: ilk A milli takım çağrısı, emeklilik kararı (seviye en fazla ±0,5).
Form dalgalanması, söylenti ve tek maçlık performans olay sayılmaz; transfer dönemini bekler. Transfer dışında bir oyuncu 30 günde en fazla bir kez olayla yeniden değerlenir. Seviye değişiklikleri `data/editor_log.json`'a yazılır.
