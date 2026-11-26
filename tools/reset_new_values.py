"""Bugün ilk kez değerlenen (henüz yayınlanmamış) oyuncuların donmuş değerini siler; bir sonraki build yeniden hesaplar.
Sadece yeni lig eklerken, yayından önce kullanılır. Eski oyuncuların değerine dokunmaz."""
import json, sys, os
day = sys.argv[1]
R = os.path.join(os.path.dirname(__file__), "..", "data")
s = json.load(open(f"{R}/values.json")); h = json.load(open(f"{R}/value_history.json"))
new = [k for k, v in s["values"].items() if v.get("d") == day]
for k in new:
    del s["values"][k]
    h[k] = [x for x in h.get(k, []) if x["d"] != day]
    if not h[k]: del h[k]
json.dump(s, open(f"{R}/values.json", "w"), ensure_ascii=False, indent=0)
json.dump(h, open(f"{R}/value_history.json", "w"), ensure_ascii=False, indent=0)
print(len(new), "değer sıfırlandı")
