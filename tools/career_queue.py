"""Özelden genele büyüme: oyuncuların kariyerlerinde geçen ama sitede olmayan kulüpleri,
kaç oyuncumuzla bağlantılı olduklarına göre sıralar -> data/expansion_queue.json

Sıradaki kadro eklemeleri bu listenin başından seçilir (en çok bağlantılı kulüp önce)."""
import json, os, re, sys, unicodedata, glob

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
from tools_import import NAT

NT = re.compile(r"\b(u\s?1[5-9]|u\s?2[0-3]|olympic)\b", re.I)
ALIAS = {"internazionale": "inter", "inter milan": "inter", "cologne": "fc-koln", "1 koln": "fc-koln",
         "bayern munchen": "bayern-munich", "athletic bilbao": "athletic-club"}


def norm(x):
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()
    x = re.sub(r"[^a-z0-9 ]", " ", x)
    x = re.sub(r"\b(fc|cf|ac|sc|afc|ssc|as|club|sk|calcio)\b", " ", x)
    return " ".join(x.split())


known = {}
for f in glob.glob(os.path.join(ROOT, "data/clubs/*/*.json")):
    c = json.load(open(f, encoding="utf-8"))
    known[norm(c["name"])] = c["slug"]
    known[norm(c["slug"].replace("-", " "))] = c["slug"]
countries = {norm(k) for k in NAT} | {"turkey", "turkiye", "england", "scotland", "wales", "northern ireland"}

careers = {k: v for k, v in json.load(open(os.path.join(ROOT, "data/careers.json"), encoding="utf-8")).items() if not k.startswith("_")}
queue = {}
for slug, c in careers.items():
    for name, _ in c["clubs"]:
        n = norm(name)
        if NT.search(name) or n in countries or n in known or n in ALIAS:
            continue
        q = queue.setdefault(n, {"club": name, "links": 0, "players": []})
        q["links"] += 1
        q["players"].append(slug)

out = sorted(queue.values(), key=lambda q: -q["links"])
json.dump({"updated": max((c["d"] for c in careers.values()), default=None), "careers": len(careers), "queue": out},
          open(os.path.join(ROOT, "data/expansion_queue.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(careers)} kariyer, {len(out)} bekleyen kulüp")
for q in out[:15]:
    print(f"  {q['links']:>3}  {q['club']}")
