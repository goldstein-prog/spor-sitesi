"""Mevcut kulüp JSON'unu yeni ham ESPN kadrosuyla günceller (seviye puanları korunur).
Kullanım: python3 tools/update_squad.py <lig> <kulüp-slug> <ham.txt> [varsayılan=5] [genç=4.5]
- Mevcut oyuncu: no, mevki, yaş, uyruk, maç, yedek, gol, asist güncellenir; ad ve seviye korunur.
- Ham listede olmayan oyuncu kadrodan çıkarılır (ayrıldı).
- Yeni oyuncu: en az bir maça çıkmışsa ya da 21 yaşından büyükse eklenir (altyapı listeleri dışarıda kalır);
  seviye: 19 yaş ve altı genç değeri, diğerleri varsayılan."""
import json, os, re, sys, unicodedata, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools_import import NAT, P, num

ROOT = os.path.join(os.path.dirname(__file__), "..")
ALIAS = {"tasos douvikas": "anastasios douvikas"}


def key(n):
    n = n.replace("ı", "i").replace("İ", "I").replace("ł", "l").replace("Ł", "L").replace("’", "'")
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    n = re.sub(r"[^a-z ]", "", n)
    n = " ".join(n.split())
    return ALIAS.get(n, n)


def update(league, slug, raw, default=5.0, youth=4.5):
    path = os.path.join(ROOT, "data", "clubs", league, f"{slug}.json")
    club = json.load(open(path, encoding="utf-8"))
    old = {key(p["name"]): p for p in club["players"]}
    out, added, kept = [], [], set()
    for line in open(raw, encoding="utf-8"):
        if not line.strip():
            continue
        n, no, pos, age, nat, apps, sub, g, a = (line.rstrip("\n").split("|") + [""] * 9)[:9]
        age = num(age)
        if age is None:
            continue
        rec = {"num": num(no), "pos": P[pos], "age": age, "nat": NAT.get(nat, nat or "-"),
               "apps": num(apps), "sub": num(sub), "goals": num(g) if pos != "G" else None,
               "assists": num(a) if pos != "G" else None}
        k = key(n)
        if k in old:
            p = old[k]
            p.update(rec)
            out.append(p)
            kept.add(k)
        elif (rec["apps"] or 0) + (rec["sub"] or 0) > 0 or age > 21:
            p = {"name": n, **rec, "minutes": None, "class": youth if age <= 19 else default}
            out.append(p)
            added.append(n)
    gone = [p["name"] for k, p in old.items() if k not in kept]
    club["players"] = out
    club["updated"] = datetime.date.today().isoformat()
    json.dump(club, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{league}/{slug}: {len(out)} oyuncu; yeni: {added or '-'}; ayrılan: {gone or '-'}")


if __name__ == "__main__":
    a = sys.argv[1:]
    update(a[0], a[1], a[2], *(float(x) for x in a[3:5]))
