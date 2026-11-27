"""Kullanım: python3 tools/add_careers.py < satırlar
Satır: slug|Kulüp:sezon;Kulüp:sezon:Lig/st/sub/g/a/yc/rc;...   (en yeni önce, milli/genç takımlar hariç; sub bilinmiyorsa boş)
Satır slug yerine "+slug" ile başlarsa mevcut kariyere sadece istatistik eklenir."""
import json, sys, datetime
p = "data/careers.json"; d = json.load(open(p))
today = datetime.date.today().isoformat()
n = 0
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("#"): continue
    slug, rest = line.split("|", 1)
    clubs = []
    for part in rest.split(";"):
        bits = part.split(":")
        row = [bits[0].strip(), int(bits[1]) if len(bits) > 1 and bits[1].strip().isdigit() else None]
        if len(bits) > 2:
            comp, *nums = bits[2].split("/")
            nums = [int(x) if x.strip() != "" else None for x in nums]
            row.append(dict(comp=comp, **dict(zip(["st", "sub", "g", "a", "yc", "rc"], nums))))
        clubs.append(row)
    if slug.startswith("+"):
        slug = slug[1:]
        byname = {c[0]: c for c in d[slug]["clubs"]}
        for row in clubs:
            if row[0] in byname and len(row) > 2:
                byname[row[0]][2:] = [row[2]]
        n += 1; continue
    old = d.get(slug, {})
    d[slug] = {"d": today, "src": "ESPN", "clubs": clubs, **({"nt": old["nt"]} if "nt" in old else {})}
    n += 1
json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
print(n, "kariyer yazıldı; toplam", len([k for k in d if not k.startswith("_")]))
