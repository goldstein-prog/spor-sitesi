#!/usr/bin/env python3
"""SporDurak statik site üreticisi.

Kullanım: python3 build.py
data/ ve i18n/ klasörlerindeki JSON dosyalarından docs/ klasörüne site üretir.
Yeni dil eklemek: i18n/<dil>.json oluştur, config.json -> languages listesine ekle.
"""
import json, os, shutil, html
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
CONFIG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
CATALOG = json.load(open(os.path.join(ROOT, "data/catalog.json"), encoding="utf-8"))
BASE = CONFIG["base_path"].rstrip("/")  # ör. "/spor-sitesi" veya "" (kendi alan adında)
SITE_URL = CONFIG["site_url"].rstrip("/")
e = html.escape
sitemap = []


def load(path):
    p = os.path.join(ROOT, "data", path)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def fmt_date(iso, T):
    d = datetime.fromisoformat(iso)
    return f"{d.day} {T['months'][d.month-1]} {T['days'][d.weekday()]}, {d:%H:%M}"


def url(lang, *parts):
    return BASE + "/" + "/".join([lang, *parts]) + ("/" if parts or True else "")


def write(rel, content, lang, indexable=True):
    path = os.path.join(OUT, rel.strip("/"), "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)
    if indexable:
        sitemap.append(SITE_URL + "/" + rel.strip("/") + "/")


def page(lang, T, title, desc, body, crumbs, path, noindex=False):
    nav = "".join(f'<a href="{url(lang, s["slug"][lang])}">{s["icon"]} {e(s["name"][lang])}</a>' for s in CATALOG["sports"])
    bc = " › ".join(f'<a href="{h}">{e(n)}</a>' if h else e(n) for n, h in crumbs)
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}/{l}/">' for l in CONFIG["languages"])
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | {e(T['site_name'])}</title>
<meta name="description" content="{e(desc)}">{robots}
<link rel="canonical" href="{SITE_URL}/{path.strip('/')}/">{alts}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<link rel="stylesheet" href="{BASE}/assets/style.css">
</head><body>
<header><div class="wrap"><a class="logo" href="{url(lang)}">🏆 {e(T['site_name'])}</a><nav>{nav}</nav></div></header>
<main class="wrap"><div class="crumbs">{bc}</div>{body}</main>
<footer><div class="wrap">{e(T['footer'])} · © {datetime.now().year} {e(T['site_name'])}</div></footer>
</body></html>"""


def standings_table(data, T):
    if data["type"] == "football":
        rows = "".join(
            f'<tr class="{ "top" if i < 4 else ("low" if i >= len(data["rows"])-3 else "")}"><td>{i+1}</td><td class="t">{e(r["team"])}</td>'
            f'<td>{r["w"]+r["d"]+r["l"]}</td><td>{r["w"]}</td><td>{r["d"]}</td><td>{r["l"]}</td><td><b>{r["pts"]}</b></td></tr>'
            for i, r in enumerate(data["rows"]))
        return f'<table><thead><tr><th>#</th><th class="t">{T["team"]}</th><th>{T["played"]}</th><th>{T["won"]}</th><th>{T["drawn"]}</th><th>{T["lost"]}</th><th>{T["points"]}</th></tr></thead><tbody>{rows}</tbody></table>'
    out = ""
    for g in data["groups"]:
        rows = "".join(
            f'<tr><td>{i+1}</td><td class="t">{e(r["team"])}</td><td>{r["w"]}</td><td>{r["l"]}</td><td>{r["w"]/(r["w"]+r["l"]):.3f}</td></tr>'
            for i, r in enumerate(g["rows"]))
        out += f'<h2>{e(g["name"])}</h2><table><thead><tr><th>#</th><th class="t">{T["team"]}</th><th>{T["won"]}</th><th>{T["lost"]}</th><th>{T["pct"]}</th></tr></thead><tbody>{rows}</tbody></table>'
    return out


def match_list(matches, T):
    def item(m):
        tr = any(k in m["home"] + m["away"] for k in T["turkish_keywords"])
        score = f'{m["hs"]} - {m["as"]}' if m["hs"] is not None else T["vs"]
        return (f'<li class="{"tr" if tr else ""}"><span class="d">{fmt_date(m["time"], T)}</span>'
                f'<span class="h">{e(m["home"])}</span><span class="s">{score}</span><span class="a">{e(m["away"])}</span></li>')
    return '<ul class="matches">' + "".join(item(m) for m in matches) + "</ul>"


def build_lang(lang):
    T = json.load(open(os.path.join(ROOT, "i18n", f"{lang}.json"), encoding="utf-8"))
    home = [(T["home"], url(lang))]
    featured = ""

    for s in CATALOG["sports"]:
        sname, sslug = s["name"][lang], s["slug"][lang]
        cards = ""
        for L in s["leagues"]:
            lname = L["name"][lang]
            links = []
            if L.get("standings"):
                data = load(f"standings/{L['standings']}.json")
                p = f"{lang}/{sslug}/{L['id']}/puan-durumu"
                body = f'<h1>{e(T["standings_title"].format(league=lname))}</h1><p class="upd">{T["updated"]}: {data["updated"]}</p>{standings_table(data, T)}'
                write(p, page(lang, T, T["standings_title"].format(league=lname), T["standings_desc"].format(league=lname), body,
                              home + [(sname, url(lang, sslug)), (lname, None)], p), lang)
                links.append(f'<a href="{BASE}/{p}/">{T["standings"]}</a>')
            if L.get("matches"):
                data = load(f"matches/{L['matches']}.json")
                past = [m for m in data["matches"] if m["hs"] is not None]
                fut = [m for m in data["matches"] if m["hs"] is None]
                p = f"{lang}/{sslug}/{L['id']}/fikstur"
                body = (f'<h1>{e(T["fixtures_title"].format(league=lname))}</h1><p class="upd">{T["updated"]}: {data["updated"]} · {T["time_note"]}</p>'
                        f'<h2>{T["results"]}</h2>{match_list(past[::-1], T)}<h2>{T["upcoming"]}</h2>{match_list(fut, T)}')
                write(p, page(lang, T, T["fixtures_title"].format(league=lname), T["fixtures_desc"].format(league=lname), body,
                              home + [(sname, url(lang, sslug)), (lname, None)], p), lang)
                links.append(f'<a href="{BASE}/{p}/">{T["fixtures"]}</a>')
                featured += f'<section class="card wide"><h2>{s["icon"]} {e(lname)}: {T["results"]}</h2>{match_list(past[::-1][:6], T)}<a class="more" href="{BASE}/{p}/">{T["fixtures"]} →</a></section>'
            inner = " · ".join(links) if links else f'<span class="soon">{T["soon"]}</span>'
            cards += f'<div class="card"><small>{e(L["country"][lang])}</small><h3>{e(lname)}</h3>{inner}</div>'
        p = f"{lang}/{sslug}"
        has_data = any(L.get("standings") or L.get("matches") for L in s["leagues"])
        body = f'<h1>{s["icon"]} {e(sname)}</h1><h2>{T["leagues"]}</h2><div class="grid">{cards}</div>'
        write(p, page(lang, T, T["sport_title"].format(sport=sname), T["sport_desc"].format(sport=sname), body,
                      home + [(sname, None)], p, noindex=not has_data), lang, indexable=has_data)

    tiles = "".join(f'<a class="tile" href="{url(lang, s["slug"][lang])}"><span>{s["icon"]}</span>{e(s["name"][lang])}</a>' for s in CATALOG["sports"])
    body = f'<section class="hero"><h1>{e(T["site_name"])}</h1><p>{e(T["tagline"])}</p></section><div class="tiles">{tiles}</div>{featured}'
    write(lang, page(lang, T, T["tagline"], T["tagline"], body, [(T["home"], None)], lang), lang)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for lang in CONFIG["languages"]:
        build_lang(lang)
    d = CONFIG["languages"][0]
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        f'<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={BASE}/{d}/"><link rel="canonical" href="{SITE_URL}/{d}/">')
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{u}</loc></url>" for u in sitemap) + "</urlset>")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print(f"{len(sitemap)} sayfa üretildi -> docs/")


if __name__ == "__main__":
    main()
