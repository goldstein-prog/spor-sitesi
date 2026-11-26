"""Forma avatarları: kulüp renklerinden çizilen, telifsiz basit forma SVG'leri."""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
KITS = json.load(open(os.path.join(ROOT, "data", "kits.json"), encoding="utf-8"))

BODY = "M38 10 L30 13 L28 18 L28 92 L72 92 L72 18 L70 13 L62 10 Q50 21 38 10 Z"
SLEEVE_L = "M30 13 L8 27 L16 45 L28 38 L28 18 Z"
SLEEVE_R = "M70 13 L92 27 L84 45 L72 38 L72 18 Z"
OUTLINE = "M38 10 L30 13 L8 27 L16 45 L28 38 L28 92 L72 92 L72 38 L84 45 L92 27 L70 13 L62 10 Q50 21 38 10 Z"


def lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kit_for(club_slug, gk=False):
    if gk:
        return KITS["_kaleci"]
    return KITS.get(club_slug, KITS["_varsayilan"])


def svg(kit, uid="k", number=None, size=None):
    a, b, pat = kit
    sz = f' width="{size}" height="{size}"' if size else ""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"{sz} role="img" aria-hidden="true">',
             f'<defs><clipPath id="{uid}"><path d="{BODY}"/></clipPath></defs>']
    if pat == "cizgili":
        parts.append(f'<path d="{BODY}" fill="{a}"/><g clip-path="url(#{uid})" fill="{b}">' +
                     "".join(f'<rect x="{x}" y="0" width="7" height="100"/>' for x in (33, 46.5, 60)) + "</g>")
        parts.append(f'<path d="{SLEEVE_L}" fill="{a}"/><path d="{SLEEVE_R}" fill="{a}"/>')
    elif pat == "yarim":
        parts.append(f'<g clip-path="url(#{uid})"><rect x="0" y="0" width="50" height="100" fill="{a}"/>'
                     f'<rect x="50" y="0" width="50" height="100" fill="{b}"/></g>')
        parts.append(f'<path d="{SLEEVE_L}" fill="{b}"/><path d="{SLEEVE_R}" fill="{a}"/>')
    else:
        parts.append(f'<path d="{BODY}" fill="{a}"/><path d="{SLEEVE_L}" fill="{b}"/><path d="{SLEEVE_R}" fill="{b}"/>')
    collar = b if pat == "duz" else ("#111111" if lum(a) > .6 else "#ffffff")
    parts.append(f'<path d="M38 10 Q50 21 62 10" fill="none" stroke="{collar}" stroke-width="3"/>')
    parts.append(f'<path d="{OUTLINE}" fill="none" stroke="rgba(0,0,0,.28)" stroke-width="1.2" stroke-linejoin="round"/>')
    if number not in (None, "", "-"):
        ref = a if pat != "yarim" else b
        fg, st = ("#111111", "#ffffff") if lum(ref) > .55 else ("#ffffff", "#111111")
        fs = 30 if len(str(number)) < 3 else 24
        parts.append(f'<text x="50" y="68" text-anchor="middle" font-family="Montserrat,DM Sans,sans-serif" font-weight="800" '
                     f'font-size="{fs}" fill="{fg}" stroke="{st}" stroke-width="2.2" paint-order="stroke">{number}</text>')
    parts.append("</svg>")
    return "".join(parts)


def write_club_files(out_dir, club_slugs):
    os.makedirs(out_dir, exist_ok=True)
    for s in list(club_slugs) + ["_kaleci"]:
        kit = KITS["_kaleci"] if s == "_kaleci" else kit_for(s)
        name = "kaleci" if s == "_kaleci" else s
        open(os.path.join(out_dir, f"{name}.svg"), "w", encoding="utf-8").write(svg(kit, uid="c"))
