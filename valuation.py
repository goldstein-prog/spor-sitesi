"""PiyasaDeğeri oyuncu değer formülü.

Değer (milyon €) = LİG_TABANI x yaş x mevki x süre x performans x seviye

- yaş: zirve 24-28; gençlerde gelişim primi, 29 sonrası düşüş
- mevki: forvet > orta saha > defans > kaleci
- süre: kulübündeki en çok oynayan oyuncuya göre oynama payı
- performans: maç başı gol katkısının mevkinin beklentisine oranı (veri yoksa nötr)
- seviye (class, 1-10): oyuncunun kalitesi, geçmişi, milli takım ve itibar.
  Editör (Claude) tarafından belirlenir ve haberlerle güncellenir. 5 = ortalama Süper Lig oyuncusu.
"""


AGE = {16: .55, 17: .65, 18: .75, 19: .9, 20: 1.0, 21: 1.08, 22: 1.12, 23: 1.12, 24: 1.1, 25: 1.08, 26: 1.05,
       27: 1.0, 28: .94, 29: .85, 30: .74, 31: .62, 32: .5, 33: .4, 34: .32, 35: .25, 36: .2}
POS = {"FV": 1.3, "OS": 1.15, "DF": .95, "KL": .75}
EXPECTED_GA = {"FV": .55, "OS": .3, "DF": .08, "KL": 0}
POS_NAME = {"KL": "Kaleci", "DF": "Defans", "OS": "Orta saha", "FV": "Forvet"}


def age_f(age):
    return AGE.get(max(16, min(36, age)), .2)


def time_f(p, club):
    pl = club["players"]
    if p.get("minutes") is not None:
        mx = max((x.get("minutes") or 0) for x in pl) or 1
        share = p["minutes"] / mx
    elif p.get("apps") is None:
        share = .35  # maç sayısı doğrulanamadı: temkinli varsayım
    else:
        mx = max(x["apps"] or 0 for x in pl) or 1
        sub = p.get("sub") or 0
        share = ((p["apps"] or 0) - .5 * sub) / mx
    share = max(0, min(1, share))
    return .6 + .6 * share, share


def perf_f(p, club=None):
    if club and club.get("apps_scope") == "all":
        return 1.0  # maç sayısı tüm turnuvalar, gol sadece lig: karşılaştırma adil olmaz
    exp = EXPECTED_GA[p["pos"]]
    if not exp or p.get("goals") is None or not p["apps"]:
        return 1.0
    ga = (p["goals"] or 0) + .7 * (p.get("assists") or 0)
    if p["apps"] < 3:
        return 1.0
    ratio = (ga / p["apps"]) / exp
    return max(.8, min(1.6, 1 + .45 * (ratio - 1)))


def class_f(c):
    return 1.75 ** (c - 5)


def value(p, club, base):
    t, share = time_f(p, club)
    parts = {
        "Lig tabanı": base,
        "Yaş": age_f(p["age"]),
        "Mevki": POS[p["pos"]],
        "Oynama süresi": t,
        "Performans": perf_f(p, club),
        "Seviye": class_f(p["class"]),
    }
    v = 1.0
    for x in parts.values():
        v *= x
    return round_value(v), parts, share


def round_value(v):
    if v >= 20: step = 1.0
    elif v >= 5: step = .5
    elif v >= 1: step = .1
    else: step = .05
    return max(.1, round(round(v / step) * step, 2))


def fmt(v):
    if v >= 1000:
        return f"€{v/1000:.2f} mlr".replace(".", ",")
    if v >= 1:
        s = f"{v:.1f}".replace(".", ",").replace(",0", "")
        return f"€{s} mn"
    return f"€{int(round(v * 1000))} bin"
