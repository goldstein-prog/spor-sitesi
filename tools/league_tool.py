"""Ortak lig içe aktarma aracı: ham ESPN kadro dosyaları + editör seviye puanları -> data/clubs/<lig>/*.json"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools_import import convert

ROOT = os.path.join(os.path.dirname(__file__), "..")


def parse_classes(text):
    out = {}
    for line in text.strip().splitlines():
        slug, rest = line.split(": ", 1)
        d = {}
        for item in rest.split("|"):
            n, c = item.rsplit(" ", 1)
            d[n.strip()] = float(c)
        out[slug] = d
    return out


def run(league, raw_dir, meta, classes_text, source, updated, default=5.0, youth=4.5):
    out_dir = os.path.join(ROOT, "data", "clubs", league)
    os.makedirs(out_dir, exist_ok=True)
    cl = parse_classes(classes_text)
    missing, done = [], []
    for slug, (name, city, stadium) in meta.items():
        raw = os.path.join(raw_dir, f"{slug}.txt")
        if not os.path.exists(raw):
            continue
        names = {l.split("|")[0] for l in open(raw, encoding="utf-8") if l.strip()}
        full = {}
        for k, v in cl.get(slug, {}).items():
            hit = [n for n in names if n == k] or [n for n in names if n.split()[-1] == k or n.startswith(k + " ")]
            if hit:
                full[hit[0]] = v
            else:
                missing.append(f"{slug}: {k}")
        club = convert(raw, {"slug": slug, "name": name, "city": city, "stadium": stadium, "source": source}, full)
        club["updated"] = updated
        for p in club["players"]:
            if p["name"] not in full:
                p["class"] = youth if p["age"] <= 19 else default
        json.dump(club, open(os.path.join(out_dir, f"{slug}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        done.append(slug)
    print(f"{league}: {len(done)} kulüp; eşleşmeyen: {missing or 'yok'}")
