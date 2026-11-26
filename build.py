#!/usr/bin/env python3
"""Kramponomi statik site üreticisi.  Kullanım: python3 build.py [--revalue]

--revalue: piyasa değerlerini yeniden hesaplar (sadece transfer dönemi öncesi kullanılır).

data/clubs/*.json  -> kulüp kadroları (oyuncu: name,num,pos,age,nat,apps,sub,goals,assists,minutes,class)
data/standings.json, data/transfers.json
data/value_history.json -> her derlemede bugünün değerleri eklenir (değer geçmişi grafiği)
Çıktı: docs/  (GitHub Pages)
"""
import json, os, re, shutil, sys, unicodedata, html
from datetime import date
from valuation import value, fmt, POS_NAME
import kits

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
C = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
BASE, URL, L, SN = C["base_path"].rstrip("/"), C["site_url"].rstrip("/"), C["lang"], C["site_name"]
TODAY = date.today().isoformat()
e = html.escape
sitemap = []
TRMAP = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


MONTHS = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]


def fmt_d(d):
    y, m, dd = d.split("-")
    return f"{int(dd)} {MONTHS[int(m)-1]} {y}"


def slug(s):
    s = unicodedata.normalize("NFKD", s.translate(TRMAP)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load(p):
    return json.load(open(os.path.join(ROOT, "data", p), encoding="utf-8"))


def link(*parts):
    return f"{BASE}/{L}/" + "".join(p + "/" for p in parts)


def write(parts, title, desc, body, crumbs=(), jsonld=None, noindex=False):
    rel = "/".join([L, *parts])
    path = os.path.join(OUT, rel, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bc = "" if not crumbs else '<div class="crumbs">' + " › ".join(
        f'<a href="{h}">{e(n)}</a>' if h else e(n) for n, h in [("Ana Sayfa", link()), *crumbs]) + "</div>"
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    nav = "".join(f'<a href="{link(*p)}">{n}</a>' for n, p in [(f"{lg['flag']} {lg['short']}", ["lig", lg["id"]]) for lg in leagues] + [
        ("Oyuncular", ["en-degerli-oyuncular"]), ("Kulüpler", ["kulupler"]), ("Genç Yetenekler", ["genc-yetenekler"]),
        ("Transferler", ["transferler"]), ("Nasıl Hesaplıyoruz?", ["nasil-hesapliyoruz"])])
    open(path, "w", encoding="utf-8").write(f"""<!DOCTYPE html><html lang="{L}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | {SN}</title><meta property="og:site_name" content="{SN}"><meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if noindex else ''}<link rel="canonical" href="{URL}/{rel}/">
<link rel="alternate" hreflang="{L}" href="{URL}/{rel}/">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">
<link rel="preload" href="{BASE}/assets/fonts/dmsans.woff" as="font" type="font/woff" crossorigin><link rel="stylesheet" href="{BASE}/assets/style.css"><link rel="icon" type="image/png" href="{BASE}/assets/favicon-32.png"><link rel="apple-touch-icon" href="{BASE}/assets/apple-touch-icon.png"><meta property="og:image" content="{URL}/assets/icon-512.png"><meta name="theme-color" content="#0d0d0d">{ld}</head><body>
<header><div class="wrap top"><a class="logo" href="{link()}"><img src="{BASE}/assets/logo-light.png" alt="{SN}" width="157" height="55"></a>
<div class="search"><input id="q" type="search" placeholder="Oyuncu veya kulüp ara..." autocomplete="off"><div id="res"></div></div></div>
<nav class="wrap">{nav}</nav></header>
<main class="wrap">{bc}{body}</main>
<footer><div class="wrap"><p><b>{SN}</b> · Futbolcu piyasa değerleri, kadrolar ve transferler: {", ".join(lg["name"] for lg in leagues)}.</p>
<p>Değerler, açık formülümüz ve editör değerlendirmesiyle hesaplanan <b>tahminlerdir</b>; resmi transfer bedeli değildir. <a href="{link('nasil-hesapliyoruz')}">Nasıl hesaplıyoruz?</a></p>
<p>Son değer güncellemesi: {fmt_d(VALUE_DATE)} · Sonraki: {C["next_revalue"]} · Veriler son güncelleme: {fmt_d(TODAY)}</p></div></footer>
<script>window.BASE="{BASE}";window.LANG="{L}";</script><script src="{BASE}/assets/search.js" defer></script>
</body></html>""")
    if not noindex:
        sitemap.append(f"{URL}/{rel}/")


# ---------- veri hazırlığı ----------
leagues = load("leagues.json")
clubs = []
for lg in leagues:
    d = os.path.join(ROOT, "data/clubs", lg["id"])
    lg["clubs"] = []
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        c = load(f"clubs/{lg['id']}/{f}")
        c["league"] = lg
        for p in c["players"]:
            p["value"], p["parts"], p["share"] = value(p, c, lg["base"])
            p["slug"] = slug(p["name"])
            p["club"] = c
        c["total"] = round(sum(p["value"] for p in c["players"]), 1)
        c["avg_age"] = round(sum(p["age"] for p in c["players"]) / len(c["players"]), 1)
        c["foreign"] = sum(1 for p in c["players"] if p["nat"] != lg["country"])
        clubs.append(c)
        lg["clubs"].append(c)
    lg["clubs"].sort(key=lambda c: -c["total"])
leagues = [lg for lg in leagues if lg["clubs"]]
clubs.sort(key=lambda c: -c["total"])
seen = {}
_h = os.path.join(ROOT, "data/value_history.json")
_owner = {k: v[-1]["club"] for k, v in (json.load(open(_h, encoding="utf-8")) if os.path.exists(_h) else {}).items() if v}
_has = {(c["slug"], p["slug"]) for c in clubs for p in c["players"]}
for c in sorted(clubs, key=lambda c: c["slug"]):  # aynı isimli oyuncular için benzersiz ve kalıcı adres
    for p in c["players"]:
        o = _owner.get(p["slug"])
        if p["slug"] in seen or (o and o != c["slug"] and (o, p["slug"]) in _has):
            p["slug"] += "-" + c["slug"]
        seen[p["slug"]] = 1
# ---------- değer dondurma ----------
# Piyasa değerleri sadece transfer dönemlerinden önceki gece (--revalue) yeniden hesaplanır.
# Arada kadro/istatistik güncellense bile sitede gösterilen değer sabit kalır.
snap_path = os.path.join(ROOT, "data/values.json")
snap = json.load(open(snap_path, encoding="utf-8")) if os.path.exists(snap_path) else {"date": None, "values": {}}
hist_path = os.path.join(ROOT, "data/value_history.json")
hist = json.load(open(hist_path, encoding="utf-8")) if os.path.exists(hist_path) else {}
REVALUE = "--revalue" in sys.argv or not snap["values"]
all_players = [p for c in clubs for p in c["players"]]
if REVALUE:
    snap = {"date": TODAY, "values": {}}
for p in all_players:
    s = snap["values"].get(p["slug"])
    if s and not REVALUE:
        p["value"], p["parts"] = s["v"], s["parts"]
        p["valued"] = s.get("d", snap["date"])
    else:  # yeniden değerleme ya da yeni eklenen oyuncu
        snap["values"][p["slug"]] = {"v": p["value"], "parts": p["parts"], "d": TODAY}
        p["valued"] = TODAY
        h = hist.setdefault(p["slug"], [])
        if not h or h[-1]["d"] != TODAY:
            h.append({"d": TODAY, "v": p["value"], "club": p["club"]["slug"]})
        else:
            h[-1]["v"] = p["value"]
json.dump(snap, open(snap_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(hist, open(hist_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
VALUE_DATE = snap["date"]
for c in clubs:
    c["total"] = round(sum(p["value"] for p in c["players"]), 1)
for lg in leagues:
    lg["clubs"].sort(key=lambda c: -c["total"])
clubs.sort(key=lambda c: -c["total"])
players = sorted(all_players, key=lambda p: -p["value"])
for i, p in enumerate(players):
    p["rank"] = i + 1


# ---------- bileşenler ----------
def plink(p):
    return f'<a href="{link("oyuncu", p["slug"])}">{e(p["name"])}</a>'


def kiticon(p):
    k = "kaleci" if p["pos"] == "KL" else p["club"]["slug"]
    return f'<img class="kit" src="{BASE}/assets/kits/{k}.svg" alt="" width="22" height="22" loading="lazy">'


def clink(c):
    return f'<span title="{e(c["league"]["name"])}">{c["league"]["flag"]}</span> <a href="{link("kulup", c["slug"])}">{e(c["name"])}</a>'


def player_table(ps, show_club=True, rank=True, compact=False):
    hx = " style='display:none'" if compact else ""
    head = ("<th>#</th>" if rank else "") + "<th class='l'>Oyuncu</th>" + ("<th class='l'>Kulüp</th>" if show_club else "") + \
        f"<th>Mevki</th><th>Yaş</th><th class='l hide-s'{hx}>Uyruk</th><th{hx}>Maç</th><th{hx}>Gol</th><th class='r'>Piyasa Değeri</th>"
    rows = ""
    for i, p in enumerate(ps):
        g = "-" if p.get("goals") is None else p["goals"]
        rows += ("<tr>" + (f"<td>{i+1}</td>" if rank else "") + f"<td class='l'><b>{kiticon(p)}{plink(p)}</b></td>" +
                 (f"<td class='l'>{clink(p['club'])}</td>" if show_club else "") +
                 f"<td><span class='pos {p['pos']}'>{p['pos']}</span></td><td>{p['age']}</td><td class='l hide-s'{hx}>{e(p['nat'])}</td>"
                 f"<td{hx}>{'-' if p['apps'] is None else p['apps']}</td><td{hx}>{g}</td><td class='r val'>{fmt(p['value'])}</td></tr>")
    return f"<div class='tbl'><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>"


def club_table(cs, compact=False):
    hx = " style='display:none'" if compact else ""
    rows = "".join(f"<tr><td>{i+1}</td><td class='l'><b>{clink(c)}</b></td><td>{len(c['players'])}</td><td{hx}>{c['avg_age']}</td>"
                   f"<td class='hide-s'{hx}>{c['foreign']}</td><td class='r val'>{fmt(c['total'])}</td><td class='r hide-s'{hx}>{fmt(c['total']/len(c['players']))}</td></tr>"
                   for i, c in enumerate(cs))
    return (f"<div class='tbl'><table><thead><tr><th>#</th><th class='l'>Kulüp</th><th>Kadro</th><th{hx}>Yaş ort.</th><th class='hide-s'{hx}>Yabancı</th>"
            f"<th class='r'>Toplam Değer</th><th class='r hide-s'{hx}>Ortalama</th></tr></thead><tbody>{rows}</tbody></table></div>")


def chart(h):
    if len(h) < 2:
        return "<p class='muted'>Değer geçmişi bugünden itibaren kaydediliyor; her değişiklik bu grafikte görünecek.</p>"
    vs = [x["v"] for x in h]
    lo, hi = min(vs) * .9, max(vs) * 1.1
    W, H, n = 600, 180, len(h)
    pts = [(30 + i * (W - 60) / (n - 1), H - 25 - (x["v"] - lo) / (hi - lo or 1) * (H - 50)) for i, x in enumerate(h)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4"><title>{h[i]["d"]}: {fmt(h[i]["v"])}</title></circle>' for i, (x, y) in enumerate(pts))
    lbl = f'<text x="30" y="{H-5}">{h[0]["d"]}</text><text x="{W-30}" y="{H-5}" text-anchor="end">{h[-1]["d"]}</text>'
    return f'<svg class="chart" viewBox="0 0 {W} {H}"><polyline points="{line}"/>{dots}{lbl}</svg>'


# ---------- sayfalar ----------
def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    kits.write_club_files(os.path.join(OUT, "assets", "kits"), [c["slug"] for c in clubs])
    tr = load("transfers.json")
    young = [p for p in players if p["age"] <= 21]
    for lg in leagues:
        lg["players"] = [p for p in players if p["club"]["league"] is lg]
        for i, p in enumerate(lg["players"]):
            p["lrank"] = i + 1
        sp = os.path.join(ROOT, "data/standings", lg["id"] + ".json")
        lg["standings"] = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else None

    def standings_rows(lg, n=None):
        st, known = lg["standings"], {c["name"]: c for c in lg["clubs"]}
        z = lg.get("zones", {"cl": 2, "el": 5, "rel": 3})
        rows = st["rows"][:n] if n else st["rows"]
        out = ""
        for i, r in enumerate(rows):
            cls = "cl" if i < z["cl"] else "el" if i < z["el"] else "rel" if i >= len(st["rows"]) - z["rel"] else ""
            name = clink(known[r["team"]]) if r["team"] in known else e(r["team"])
            wdl = f"<td>{r['w']}</td><td>{r['d']}</td><td>{r['l']}</td>" if "w" in r else ""
            av = f"<td>{r['av']:+d}</td>" if "av" in r else ""
            out += f"<tr class='{cls}'><td>{i+1}</td><td class='l'><b>{name}</b></td><td>{r['o']}</td>{wdl}{av}<td><b>{r['p']}</b></td></tr>"
        r0 = st["rows"][0]
        head = "<th>O</th>" + ("<th>G</th><th>B</th><th>M</th>" if "w" in r0 else "") + ("<th>Av</th>" if "av" in r0 else "") + "<th>P</th>"
        return f"<div class='tbl'><table><thead><tr><th>#</th><th class='l'>Takım</th>{head}</tr></thead><tbody>{out}</tbody></table></div>"

    # oyuncu sayfaları
    for p in players:
        c = p["club"]
        lg = c["league"]
        parts = "".join(f"<tr><td class='l'>{k}</td><td class='r'>×{v:.2f}</td></tr>" for k, v in p["parts"].items())
        stats = [("Maç", p["apps"]), ("Gol", p.get("goals")), ("Asist", p.get("assists")), ("Dakika", p.get("minutes"))]
        stats = "".join(f"<div><b>{'-' if v is None else v}</b><small>{k}</small></div>" for k, v in stats)
        near = sorted((x for x in players if x["pos"] == p["pos"] and x is not p), key=lambda x: abs(x["value"] - p["value"]))[:6]
        kit = kits.svg(kits.kit_for(c["slug"], p["pos"] == "KL"), uid="pk", number=p.get("num"))
        body = f"""<section class="profile"><div class="kitbig" title="Forma çizimi: kulüp renkleri">{kit}</div><div class="pinfo"><small class="muted">#{p['num'] or '-'} · {POS_NAME[p['pos']]}</small><h1>{e(p['name'])}</h1>
<p>{clink(c)} · {p['age']} yaş · {e(p['nat'])}</p></div>
<div class="bigval"><small>Piyasa Değeri</small><b>{fmt(p['value'])}</b><small>{e(lg['short'])}'de {p['lrank']}. · Genelde {p['rank']}. sırada</small><small>Değer tarihi: {fmt_d(p['valued'])}</small></div></section>
<div class="cards">{stats}</div>
<div class="two"><section class="card"><h2>Değer geçmişi</h2>{chart(hist.get(p['slug'], []))}</section>
<section class="card"><h2>Değer nasıl hesaplandı?</h2><table class="mini">{parts}</table>
<p class="muted">Formülün tamamı: <a href="{link('nasil-hesapliyoruz')}">Nasıl hesaplıyoruz?</a></p></section></div>
<section class="card"><h2>Benzer değerdeki {POS_NAME[p['pos']].lower()} oyuncuları</h2>{player_table(near)}</section>
<p class="muted">Sezon istatistikleri ({'tüm turnuvalar' if c.get('apps_scope') == 'all' else 'lig maçları'}): {e(c['source'])}, {c['updated']}.</p>"""
        ld = {"@context": "https://schema.org", "@type": "Person", "name": p["name"], "nationality": p["nat"],
              "affiliation": {"@type": "SportsTeam", "name": c["name"]}}
        write(["oyuncu", p["slug"]], f"{p['name']} Piyasa Değeri ({fmt(p['value'])}) - {c['name']}",
              f"{p['name']} güncel piyasa değeri {fmt(p['value'])}. {c['name']} oyuncusu {p['name']}: yaş, mevki, maç, gol ve değer geçmişi.",
              body, [(lg["short"], link("lig", lg["id"])), (c["name"], link("kulup", c["slug"])), (p["name"], None)], ld)

    # kulüp sayfaları
    for c in clubs:
        lg = c["league"]
        byp = ""
        for pos in ["KL", "DF", "OS", "FV"]:
            ps = sorted((p for p in c["players"] if p["pos"] == pos), key=lambda p: -p["value"])
            if ps:
                byp += f"<h2>{POS_NAME[pos]}</h2>{player_table(ps, show_club=False, rank=False)}"
        top = max(c["players"], key=lambda p: p["value"])
        ckit = kits.svg(kits.kit_for(c["slug"]), uid="ck")
        body = f"""<section class="profile"><div class="kitbig">{ckit}</div><div class="pinfo"><h1>{e(c['name'])} Kadro Değeri</h1><p>{lg['flag']} <a href="{link('lig', lg['id'])}">{e(lg['name'])}</a> · {e(c['city'])}{' · ' + e(c['stadium']) if c.get('stadium') else ''}</p></div>
<div class="bigval"><small>Toplam Kadro Değeri</small><b>{fmt(c['total'])}</b><small>{e(lg['short'])}'de {lg['clubs'].index(c)+1}. sırada</small></div></section>
<div class="cards"><div><b>{len(c['players'])}</b><small>Oyuncu</small></div><div><b>{c['avg_age']}</b><small>Yaş ortalaması</small></div>
<div><b>{c['foreign']}</b><small>Yabancı</small></div><div><b>{e(top['name'])}</b><small>En değerli oyuncu</small></div></div>{byp}
<p class="muted">Kaynak: {e(c['source'])}, {c['updated']}.</p>"""
        write(["kulup", c["slug"]], f"{c['name']} Kadro Değeri ve Oyuncuları {C['season']}",
              f"{c['name']} {C['season']} kadrosu ve piyasa değerleri: toplam {fmt(c['total'])}. En değerli oyuncu {top['name']} ({fmt(top['value'])}).",
              body, [(lg["short"], link("lig", lg["id"])), (c["name"], None)],
              {"@context": "https://schema.org", "@type": "SportsTeam", "name": c["name"], "sport": "Football"})

    # lig sayfaları
    for lg in leagues:
        stp = ""
        if lg["standings"]:
            st = lg["standings"]
            write(["lig", lg["id"], "puan-durumu"], f"{lg['name']} Puan Durumu {C['season']}", f"{lg['name']} {C['season']} güncel puan durumu ({st['week']}. hafta).",
                  f"<h1>{lg['flag']} {e(lg['name'])} Puan Durumu</h1><p class='muted'>{st['week']}. hafta sonu · güncelleme {st['updated']}</p>{standings_rows(lg)}",
                  [(lg["short"], link("lig", lg["id"])), ("Puan Durumu", None)])
            stp = f"<h2>Puan durumu</h2>{standings_rows(lg, 8)}<a class='more' href='{link('lig', lg['id'], 'puan-durumu')}'>Tam tablo →</a>"
        lyoung = [p for p in lg["players"] if p["age"] <= 21]
        body = f"""<section class="profile"><div><h1>{lg['flag']} {e(lg['name'])} Piyasa Değerleri</h1><p>{e(lg['country'])} · {len(lg['clubs'])} kulüp · {len(lg['players'])} oyuncu</p></div>
<div class="bigval"><small>Toplam Değer</small><b>{fmt(sum(c['total'] for c in lg['clubs']))}</b><small>eklenen kulüplerin toplamı</small></div></section>
<div class="two"><section class="card"><h2>En değerli oyuncular</h2>{player_table(lg['players'][:15], compact=True)}</section>
<section class="card"><h2>Kulüp değerleri</h2>{club_table(lg['clubs'], compact=True)}{stp}</section></div>
<section class="card"><h2>En değerli genç yetenekler (21 yaş altı)</h2>{player_table(lyoung[:10])}</section>"""
        write(["lig", lg["id"]], f"{lg['name']} Oyuncu Piyasa Değerleri ve Kadro Değerleri {C['season']}",
              f"{lg['name']} en değerli oyuncular, kulüplerin kadro değerleri ve puan durumu.", body, [(lg["short"], None)])

    write(["en-degerli-oyuncular"], f"En Değerli Futbolcular {C['season']}",
          "En değerli futbolcular: güncel piyasa değeri sıralaması, yaş, mevki ve sezon istatistikleri.",
          f"<h1>En Değerli Futbolcular</h1><p class='muted'>{len(players)} oyuncu · {len(clubs)} kulüp · {len(leagues)} lig</p>{player_table(players)}",
          [("Oyuncular", None)])
    write(["genc-yetenekler"], "En Değerli Genç Yetenekler (21 yaş altı)",
          "21 yaş ve altındaki en değerli genç futbolcular.",
          f"<h1>En Değerli Genç Yetenekler</h1><p class='muted'>21 yaş ve altı</p>{player_table(young)}", [("Genç Yetenekler", None)])
    write(["kulupler"], f"Kulüplerin Kadro Değerleri {C['season']}",
          "Kulüplerin toplam kadro değerleri, yaş ortalamaları ve yabancı oyuncu sayıları.",
          f"<h1>Kulüplerin Kadro Değerleri</h1>{club_table(clubs)}"
          f"<p class='muted'>Kulüpler doğrulandıkça ekleniyor.</p>", [("Kulüpler", None)])

    trs = "".join(f"<tr><td>{t['date']}</td><td class='l'><b>{e(t['player'])}</b></td><td class='l'>{e(t['from'])}</td><td class='l'>{e(t['to'])}</td>"
                  f"<td class='l hide-s'>{e(t['type'])}{' · ' + e(t['fee']) if t.get('fee') else ''}</td></tr>" for t in tr["items"])
    write(["transferler"], f"Transferler {C['season']}", "2026-27 sezonu gelen ve giden transferler.",
          f"<h1>Transferler</h1><div class='tbl'><table><thead><tr><th>Tarih</th><th class='l'>Oyuncu</th><th class='l'>Eski kulüp</th>"
          f"<th class='l'>Yeni kulüp</th><th class='l hide-s'>Tür</th></tr></thead><tbody>{trs}</tbody></table></div>", [("Transferler", None)])

    write(["nasil-hesapliyoruz"], "Piyasa Değerlerini Nasıl Hesaplıyoruz?", "Kramponomi oyuncu değer formülü: lig, yaş, mevki, oynama süresi, performans ve seviye.",
          METHOD, [("Nasıl Hesaplıyoruz?", None)])

    # ana sayfa
    lcards = "".join(f"<a class='tile' href='{link('lig', lg['id'])}'><span>{lg['flag']}</span><b>{e(lg['name'])}</b><small>{len(lg['clubs'])} kulüp · {len(lg['players'])} oyuncu</small></a>" for lg in leagues)
    body = f"""<section class="hero"><h1>Kramponomi: futbolun ekonomisi</h1>
<p>{len(players)} oyuncunun piyasa değeri, kulüplerin kadro değerleri ve transferler. Açık formül, şeffaf hesap.</p>
<p class="vdate">Son değer güncellemesi: <b>{fmt_d(VALUE_DATE)}</b> · Sonraki güncelleme: <b>{C["next_revalue"]}</b></p></section>
<div class="tiles">{lcards}</div>
<div class="two"><section class="card"><h2>En değerli 10 oyuncu</h2>{player_table(players[:10], compact=True)}<a class="more" href="{link('en-degerli-oyuncular')}">Tüm liste →</a></section>
<section class="card"><h2>En değerli kulüpler</h2>{club_table(clubs[:10], compact=True)}<a class="more" href="{link('kulupler')}">Tüm kulüpler →</a></section></div>
<div class="two"><section class="card"><h2>En değerli genç yetenekler</h2>{player_table(young[:8], compact=True)}<a class="more" href="{link('genc-yetenekler')}">Tümü →</a></section>
<section class="card"><h2>Son transferler</h2><div class='tbl'><table><tbody>{''.join(trs.split('</tr>')[i] + '</tr>' for i in range(min(8, len(tr['items']))))}</tbody></table></div>
<a class="more" href="{link('transferler')}">Tüm transferler →</a></section></div>"""
    write([], "Futbolcu Piyasa Değerleri, Kadro Değerleri ve Transferler", "Süper Lig ve Avrupa liglerinde futbolcuların güncel piyasa değerleri, kulüp kadro değerleri ve transferler.", body)

    # arama dizini, yönlendirme, sitemap
    idx = [{"n": p["name"], "u": link("oyuncu", p["slug"]), "c": p["club"]["name"], "v": fmt(p["value"])} for p in players] + \
          [{"n": c["name"], "u": link("kulup", c["slug"]), "c": "Kulüp", "v": fmt(c["total"])} for c in clubs]
    json.dump(idx, open(os.path.join(OUT, "assets", "index.json"), "w", encoding="utf-8"), ensure_ascii=False)
    open(os.path.join(OUT, "index.html"), "w").write(f'<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={link()}"><link rel="canonical" href="{URL}/{L}/">')
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                                       + "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in sitemap) + "</urlset>")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {URL}/sitemap.xml\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print(f"{len(players)} oyuncu, {len(clubs)} kulüp, {len(sitemap)} sayfa -> docs/")


METHOD = """<h1>Piyasa değerlerini nasıl hesaplıyoruz?</h1>
<p>Kramponomi'deki her değer, herkesin görebileceği bir formülle hesaplanır. Bir oyuncunun sayfasında değerin hangi çarpanlardan oluştuğunu tek tek görebilirsiniz.</p>
<div class="card formula">Değer = Lig tabanı × Yaş × Mevki × Oynama süresi × Performans × Seviye</div>
<h2>Çarpanlar</h2><ul>
<li><b>Lig tabanı:</b> Ligin ekonomik büyüklüğü ve transfer piyasası: Süper Lig 2,0 · Serie A 5,5. Yeni ligler eklendikçe her ligin kendi tabanı olur.</li>
<li><b>Yaş:</b> Değer 22-26 yaş arasında zirve yapar. 21 yaş altına gelişim primi verilir, 29 yaştan sonra her yıl belirgin düşüş uygulanır.</li>
<li><b>Mevki:</b> Transfer piyasasında forvetler en, kaleciler en düşük fiyatlanır: Forvet 1,30 · Orta saha 1,15 · Defans 0,95 · Kaleci 0,75.</li>
<li><b>Oynama süresi:</b> Oyuncunun kulübündeki en çok oynayan oyuncuya göre süre payı. Hiç oynamayan oyuncu 0,60, takımın vazgeçilmezi 1,20 alır.</li>
<li><b>Performans:</b> Maç başına gol ve asist katkısının, mevkisinden beklenene oranı (forvet için maç başı 0,55 katkı beklenir). En az 3 maç gerekir; veri yoksa ya da maç ve gol sayıları farklı turnuvaları kapsıyorsa nötr (1,00) kalır. Sınırlar: 0,80 - 1,60.</li>
<li><b>Seviye (1-10):</b> Oyuncunun gerçek kalitesi: geçmiş kulüpleri, milli takım düzeyi, uluslararası itibar ve gelişim potansiyeli. 5, kendi liginin ortalama oyuncusudur; her +1 puan değeri yaklaşık 1,75 katına çıkarır. Bu puanı editörümüz belirler ve sakatlık, form ve haberlere göre günceller.</li></ul>
<h2>Değerler ne zaman güncellenir?</h2>
<p>Piyasa değerleri her gün değişmez. Tek maçlık bir form patlaması ya da düşüşü değeri yanıltıcı şekilde oynatmasın diye değerleri yılda iki kez, <b>transfer dönemleri açılmadan önceki gece</b> toplu olarak güncelliyoruz: yaz transfer dönemi öncesi (Haziran sonu) ve kış transfer dönemi öncesi (Aralık sonu). Kadrolar, maç, gol ve asist sayıları ile puan durumları ise düzenli olarak güncellenir; bir sonraki değer güncellemesinde bu veriler hesaba katılır. Sezon ortasında kadroya eklenen yeni bir oyuncu ilk değerini eklendiği gün alır.</p>
<h2>Bu değerler ne değildir?</h2>
<p><b>Neden Kramponomi?</b> Krampon ve ekonomi kelimelerinden doğdu: sahadaki performansı piyasadaki karşılığıyla buluşturuyoruz.</p>
<p>Bu değerler bir transfer bedeli ya da kulüplerin açıkladığı rakamlar değildir. Bir oyuncunun bugünkü piyasada yaklaşık ne edeceğine dair tahminimizdir. Sözleşme süresi, maaş ve kulübün satma isteği gibi etkenler gerçek bedeli değiştirebilir.</p>
<h2>Veriler</h2><p>Kadro ve sezon istatistikleri, birden fazla açık kaynakla karşılaştırılarak düzenli güncellenir. Her kulüp sayfasının altında kaynağı ve güncelleme tarihi yazar. Bir hata görürseniz bize bildirin.</p>"""

if __name__ == "__main__":
    build()
