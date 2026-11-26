"""Ham kadro dosyalarını (ad|no|mevki|yaş|uyruk|maç|yedek|gol|asist) kulüp JSON'una çevirir."""
import json, sys
NAT = {"Greece":"Yunanistan","Türkiye":"Türkiye","Brazil":"Brezilya","Tunisia":"Tunus","Denmark":"Danimarka","Congo":"Kongo","Romania":"Romanya",
"Bosnia and Herzegovina":"Bosna-Hersek","Iceland":"İzlanda","Sweden":"İsveç","Germany":"Almanya","France":"Fransa","Poland":"Polonya","Mali":"Mali",
"Ghana":"Gana","Ivory Coast":"Fildişi Sahili","Senegal":"Senegal","Georgia":"Gürcistan","Cameroon":"Kamerun","Uzbekistan":"Özbekistan","Croatia":"Hırvatistan",
"Tanzania":"Tanzanya","Gambia":"Gambiya","England":"İngiltere","Switzerland":"İsviçre","Ireland":"İrlanda","Republic of Ireland":"İrlanda","Jordan":"Ürdün",
"Scotland":"İskoçya","Portugal":"Portekiz","Netherlands":"Hollanda","Serbia":"Sırbistan","Guinea":"Gine","Italy":"İtalya","Kosovo":"Kosova","Austria":"Avusturya",
"Madagascar":"Madagaskar","Israel":"İsrail","Nigeria":"Nijerya","Suriname":"Surinam","Spain":"İspanya","Angola":"Angola","Norway":"Norveç","Honduras":"Honduras",
"Albania":"Arnavutluk","Morocco":"Fas","Hungary":"Macaristan","Curaçao":"Curaçao","Jamaica":"Jamaika","Venezuela":"Venezuela","Belgium":"Belçika","Chile":"Şili",
"Azerbaijan":"Azerbaycan","Congo DR":"Kongo DC","South Korea":"Güney Kore","North Macedonia":"Kuzey Makedonya","Egypt":"Mısır","Liberia":"Liberya","Ecuador":"Ekvador","USA":"ABD","Bulgaria":"Bulgaristan","Armenia":"Ermenistan","Argentina":"Arjantin","Colombia":"Kolombiya","Uruguay":"Uruguay","Slovakia":"Slovakya","Slovenia":"Slovenya","Montenegro":"Karadağ","Mexico":"Meksika","Latvia":"Letonya","Lithuania":"Litvanya","Finland":"Finlandiya","Czechia":"Çekya","Niger":"Nijer","Japan":"Japonya","Zambia":"Zambiya","Guinea-Bissau":"Gine-Bissau","Indonesia":"Endonezya","Australia":"Avustralya","Canada":"Kanada","Togo":"Togo","Mauritania":"Moritanya","Gabon":"Gabon","Ukraine":"Ukrayna","Equatorial Guinea":"Ekvator Ginesi"}
P = {"G":"KL","D":"DF","M":"OS","F":"FV"}

def num(x):
    x = x.strip()
    return int(x) if x not in ("", "-", "--") else None

def convert(raw, meta, classes):
    players = []
    for line in open(raw, encoding="utf-8"):
        if not line.strip(): continue
        n, no, pos, age, nat, apps, sub, g, a = (line.rstrip("\n").split("|") + [""] * 9)[:9]
        age = num(age)
        if age is None: continue
        cls = classes.get(n, 4.5 if age <= 19 else 5)
        players.append({"name": n, "num": num(no), "pos": P[pos], "age": age, "nat": NAT.get(nat, nat or "-"),
                        "apps": num(apps), "sub": num(sub), "goals": num(g) if pos != "G" else None,
                        "assists": num(a) if pos != "G" else None, "minutes": None, "class": cls})
    meta.update({"updated": "2026-11-26", "players": players})
    return meta
