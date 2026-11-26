"""Premier Lig kulüplerini ham ESPN kadro dosyalarından üretir (bir kerelik içe aktarma).
Seviye (class) puanları editör (Claude) değerlendirmesidir; listede olmayan oyuncu 5.5, 19 yaş ve altı 4.5."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools_import import convert

RAW = sys.argv[1] if len(sys.argv) > 1 else "/tmp/raw/premier-lig"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "clubs", "premier-lig")

META = {
    "arsenal": ("Arsenal", "Londra", "Emirates Stadium"),
    "manchester-city": ("Manchester City", "Manchester", "Etihad Stadium"),
    "liverpool": ("Liverpool", "Liverpool", "Anfield"),
    "chelsea": ("Chelsea", "Londra", "Stamford Bridge"),
    "brighton": ("Brighton", "Brighton", "Amex Stadium"),
    "bournemouth": ("Bournemouth", "Bournemouth", "Vitality Stadium"),
    "brentford": ("Brentford", "Londra", "Gtech Community Stadium"),
    "leeds-united": ("Leeds United", "Leeds", "Elland Road"),
    "everton": ("Everton", "Liverpool", "Hill Dickinson Stadium"),
    "tottenham-hotspur": ("Tottenham Hotspur", "Londra", "Tottenham Hotspur Stadium"),
    "hull-city": ("Hull City", "Hull", "MKM Stadium"),
    "aston-villa": ("Aston Villa", "Birmingham", "Villa Park"),
    "newcastle-united": ("Newcastle United", "Newcastle", "St James' Park"),
    "coventry-city": ("Coventry City", "Coventry", "Coventry Building Society Arena"),
    "fulham": ("Fulham", "Londra", "Craven Cottage"),
    "ipswich-town": ("Ipswich Town", "Ipswich", "Portman Road"),
    "nottingham-forest": ("Nottingham Forest", "Nottingham", "City Ground"),
    "sunderland": ("Sunderland", "Sunderland", "Stadium of Light"),
    "manchester-united": ("Manchester United", "Manchester", "Old Trafford"),
    "crystal-palace": ("Crystal Palace", "Londra", "Selhurst Park"),
}

C = """
arsenal: Raya 7.5|Saliba 8.5|Gabriel Magalhães 8|Jurriën Timber 7.5|Riccardo Calafiori 7|Ben White 6.5|Piero Hincapié 7|Cristhian Mosquera 6.5|Myles Lewis-Skelly 7|Ezri Konsa 6.5|Martin Ødegaard 8.5|Declan Rice 9|Martín Zubimendi 8|Mikel Merino 7|Eberechi Eze 8|Bruno Guimarães 8|Bukayo Saka 9.5|Viktor Gyökeres 8|Kai Havertz 7.5|Noni Madueke 7|Christos Tzolis 6.5|Kepa Arrizabalaga 6|Illan Meslier 5.5|Max Dowman 7
manchester-city: Gianluigi Donnarumma 8|Rúben Dias 8|Marc Guéhi 8|Josko Gvardiol 8|Rayan Aït-Nouri 7|Nico O'Reilly 7.5|Abdukodir Khusanov 7|Vitor Reis 6.5|Rico Lewis 6.5|Elliot Anderson 8|Rayan Cherki 8.5|Enzo Fernández 8.5|Phil Foden 8|Matheus Nunes 7|Mateo Kovacic 6.5|Ayyoub Bouaddi 7|Erling Haaland 9.5|Jérémy Doku 7.5|Antoine Semenyo 7.5|Iliman Ndiaye 7|Gerónimo Rulli 5
liverpool: Alisson Becker 7.5|Giorgi Mamardashvili 7|Virgil van Dijk 8|Jérémy Jacquet 7.5|Milos Kerkez 7.5|Jeremie Frimpong 7|Ronald Araujo 7.5|Joe Gomez 6|Conor Bradley 6.5|Giovanni Leoni 7|Kostas Tsimikas 6|Florian Wirtz 9|Dominik Szoboszlai 8|Alexis Mac Allister 8.5|Ryan Gravenberch 8|Trey Nyoni 6.5|Wataru Endo 5.5|Alexander Isak 9|Cody Gakpo 7.5|Hugo Ekitike 8|Víctor Muñoz 7|Bradley Barcola 8|Federico Chiesa 6.5|Rio Ngumoha 7
chelsea: Emiliano Martínez 7|Wesley Fofana 7|Maxence Lacroix 7|Levi Colwill 7.5|Jorrel Hato 7.5|Reece James 7.5|Malo Gusto 7|Pep Chavarría 6|Marco Palestra 7|Josh Acheampong 6.5|Aaron Anselmino 6|Cole Palmer 9|Morgan Rogers 8|Moisés Caicedo 8.5|Romeo Lavia 7|Jordan Henderson 5.5|Geovany Quenda 7.5|Valentín Barco 6|Pedro Neto 7.5|João Pedro 8|Estêvão 8.5|Jamie Gittens 7|Danny Welbeck 5|Emmanuel Emegha 6
brighton: Bart Verbruggen 7|Lewis Dunk 5.5|Ferdi Kadioglu 6.5|Maxim De Cuyper 6.5|Olivier Boscagli 6|Luka Vuskovic 7.5|Pascal Struijk 6|Costinha 6|Pascal Gross 5.5|Yasin Ayari 6.5|Diego Gómez 6.5|Mats Wieffer 6.5|Jack Hinshelwood 6.5|Malick Yalcouyé 6|Kaoru Mitoma 7|Yankuba Minteh 7|Georginio Rutter 7|Charalambos Kostoulas 7|Evan Ferguson 6.5|Stefanos Tzimas 6.5|Matt O'Riley 6.5
bournemouth: Djordje Petrovic 6.5|Adrien Truffert 6.5|James Hill 6.5|António Silva 7|Adam Smith 4.5|Bafodé Diakité 6.5|Alex Scott 7|Tyler Adams 6.5|Marcus Tavernier 6.5|Lewis Cook 5.5|Ryan Christie 5.5|Evanilson 7|Justin Kluivert 6.5|Rayan 7|Amine Adli 6|Junior Kroupi 6.5|Ben Gannon-Doak 6|Álvaro Rodríguez 6|Michele Di Gregorio 6|Fraser Forster 4
brentford: Caoimhín Kelleher 6.5|Nathan Collins 6.5|Kristoffer Ajer 6|Michael Kayode 6.5|Sepp van den Berg 6.5|Aaron Hickey 6|Kevin Schade 6.5|Vitaly Janelt 6|Mathias Jensen 5.5|Mamadou Sangare 6|Mikkel Damsgaard 6.5|Yehor Yarmoliuk 6|Fábio Carvalho 6|Igor Thiago 7|Dango Ouattara 6.5|Keane Lewis-Potter 6.5|Jaidon Anthony 6|Callum Wilson 4.5|Antoni Milambo 6|Jannik Schuster 6
leeds-united: James Trafford 6.5|Jayden Bogle 6|Gabriel Gudmundsson 6|Tarik Muharemovic 6.5|James Justin 5.5|Jaka Bijol 6|Joe Rodon 5.5|Nico Elvedi 5.5|Ethan Ampadu 6|Anton Stach 6.5|Ao Tanaka 6.5|Brenden Aaronson 6|Sean Longstaff 5.5|Dominic Calvert-Lewin 6.5|Noah Okafor 6.5|Harry Wilson 6|Lukas Nmecha 5.5|Daniel James 5.5
everton: Jordan Pickford 7|Jarrad Branthwaite 7|James Tarkowski 5.5|Jake O'Brien 6|Vitaliy Mykolenko 6|Michael Keane 4.5|Kiernan Dewsbury-Hall 6.5|Jack Grealish 6.5|James Garner 6.5|Hayden Hackney 6|Merlin Röhl 6|Charly Alcaraz 6|Harrison Armstrong 6|Christian Nørgaard 5|Thierno Barry 7|Tyrique George 6.5|Tyler Dibling 6.5|Brennan Johnson 6.5|Ainsley Maitland-Niles 5
tottenham-hotspur: Antonín Kinsky 6.5|Martin Dúbravka 4.5|Andy Robertson 6|Marcos Senesi 6|Jan Paul van Hecke 7|Destiny Udogie 7|Pedro Porro 7|Micky van de Ven 8|Ben Davies 4.5|Xavi Simons 8|Conor Gallagher 7|James Maddison 7|Archie Gray 7.5|Lucas Bergvall 7.5|Sandro Tonali 8|Mateus Fernandes 7|Mohammed Kudus 7.5|Dejan Kulusevski 7|Mykhailo Mudryk 5.5|Rodrigo Bentancur 6.5|Richarlison 6|Mathys Tel 7|Sávio 7.5|Dominic Solanke 7|Omar Marmoush 7.5|Wilson Odobert 6.5
hull-city: Konstantinos Tzolakis 6|Jack Butland 5|Lewie Coyle 5|Ryan Giles 5.5|Semi Ajayi 5|John Egan 4.5|Brooke Norton-Cuffy 5.5|Nobel Mendy 5.5|Lucas Herrington 5.5|Hidemasa Morita 5.5|Regan Slater 5|Elliot Stroud 5.5|Matt Crooks 4.5|Lucas Gourna-Douath 5.5|Tim Iroegbunam 5.5|Abdülkadir Ömür 5.5|Sorba Thomas 5|Oliver McBurnie 5|Mohamed Belloumi 6|Joe Gelhardt 5|Mohamed-Ali Cho 5.5|Robinio Vaz 6|Christos Mouzakitis 6
aston-villa: Zion Suzuki 6.5|Marco Bizot 4.5|Matty Cash 6|Victor Lindelöf 5.5|Tyrone Mings 5|Pau Torres 6.5|Ian Maatsen 6.5|Aaron Wan-Bissaka 6|Matteo Ruggeri 6|Taylor Harwood-Bellis 6|John McGinn 6|Boubacar Kamara 7|Emiliano Buendía 5.5|Amadou Onana 7|Leon Goretzka 6|João Gomes 7|Johan Manzambi 7|Ross Barkley 5|Lamare Bogarde 6|Nicolas Jackson 7|Alejandro Garnacho 7|Tammy Abraham 6|Ibrahim Mbaye 6.5|Alysson 6.5
newcastle-united: Lukás Hornícek 6|Nick Pope 5|Lewis Hall 7|Sven Botman 7|Malick Thiaw 7|Tino Livramento 7|Amar Dedic 6.5|Fabian Schär 4.5|Dan Burn 4.5|Nico González 7|Joelinton 6.5|Aladji Bamba 6|Harvey Barnes 6.5|Sean Steur 6.5|Jacob Murphy 5.5|Joe Willock 6|Jacob Ramsey 6|Lewis Miley 7|Yoane Wissa 6.5|William Osula 6.5|Bazoumana Touré 6|Anthony Elanga 7|Matias Fernandez-Pardo 6
coventry-city: Carl Rushworth 5.5|Ethan Pinnock 4.5|Jay Da Silva 5|Bobby Thomas 5.5|Milan van Ewijk 5.5|Aurèle Amenda 5.5|Stephen Mfuni 5|Jack Rudoni 6|Matt Grimes 5|Tatsuhiro Sakamoto 5|Caleb Yirenkyi 5.5|Ephron Mason-Clark 5|Frank Onyeka 5.5|Victor Torp 5.5|Gustavo Hamer 5.5|Ellis Simms 5|Haji Wright 5.5|Taiwo Awoniyi 5.5|Loum Tchaouna 5.5|Brandon Thomas-Asante 5|Yann Gboho 5.5|Sidiki Cherif 6|Ben Wilson 4|Daniel Bentley 4.5
fulham: Bernd Leno 5.5|Calvin Bassey 6|Timothy Castagne 5.5|Antonee Robinson 6.5|David Affengruber 5.5|Joachim Andersen 5.5|Jorge Cuenca 5.5|Kenny Tete 5|Sander Berge 6|Oscar Bobb 6.5|Josh King 7|César Palacios 6|Shea Charles 6|Hugo Larsson 6.5|Emile Smith Rowe 6|Alex Iwobi 6|Tom Cairney 4.5|Gonzalo García 7|Rodrigo Muniz 6.5|Kevin 6.5|Ryan Sessegnon 5.5|Benjamin Lecomte 4
ipswich-town: Christian Walton 5|Kjell Scherpen 5|Leif Davis 6|Issa Diop 5.5|Dara O'Shea 5.5|Jacob Greaves 5.5|Abdoul Ouattara 6|Cedric Kipre 5|Julio Enciso 7|Florentino 6|Sasa Lukic 5.5|Exequiel Palacios 6|Marcelino Núñez 5.5|Jack Clarke 6|Fatawu Issahaku 6.5|Sindre Walle Egeli 6|Zian Flemming 5.5|Jaden Philogene 6|Emersonn 6|Chuba Akpom 5|Daizen Maeda 6.5|Anis Mehmeti 5.5|Azor Matusiwa 5.5|David Button 4
nottingham-forest: Matz Sels 6|Ousmane Diomande 6.5|Neco Williams 6|Murillo 7.5|Jair Cunha 6.5|Daniel Muñoz 6.5|Nikola Milenkovic 6.5|Ola Aina 6|Luca Netz 6|Nicolò Savona 6.5|Ibrahim Sangaré 6|Nicolás Domínguez 6|Morgan Gibbs-White 7.5|Xaver Schlager 6.5|James McAtee 6.5|Ryan Yates 5|Callum Hudson-Odoi 6|Chris Wood 5|Igor Jesus 6.5|Dan Ndoye 7|Arnaud Kalimuendo 6.5|Liam Delap 7
sunderland: Robin Roefs 6.5|Kevin Danso 6.5|Danny Ballard 5.5|Thomas Meunier 4.5|Omar Alderete 5.5|Reinildo Mandava 5|Nordi Mukiele 6|Trai Hume 6|Chris Rigg 6.5|Luke O'Nien 4.5|Habib Diarra 6.5|Noah Sadiki 6.5|Enzo Le Fée 6.5|Granit Xhaka 5.5|Chemsdine Talbi 6.5|Brian Brobbey 6.5|Nilson Angulo 6|Wilson Isidor 6|Simon Moore 4
manchester-united: Senne Lammens 6.5|Diogo Dalot 6.5|Noussair Mazraoui 6|Matthijs de Ligt 7|Harry Maguire 5|Lisandro Martínez 7|Patrick Dorgu 6.5|Leny Yoro 7.5|Luke Shaw 5.5|Ayden Heaven 6.5|Harry Amass 6|Mason Mount 6|Bruno Fernandes 7.5|Andrey Santos 7|Youri Tielemans 6.5|Carlos Baleba 7.5|Manuel Ugarte 6.5|Kobbie Mainoo 7|Marcus Rashford 7|Matheus Cunha 7.5|Joshua Zirkzee 6.5|Amad Diallo 7|Bryan Mbeumo 7.5|Benjamin Sesko 7.5|Shea Lacey 6|Tom Heaton 3.5|Karl Darlow 4
crystal-palace: Dean Henderson 6.5|Walter Benítez 5.5|Tyrick Mitchell 6|Chadi Riad 5.5|Axel Disasi 6|Jaydee Canvot 6.5|Takehiro Tomiyasu 5.5|Honest Ahanor 6.5|Anan Khalaili 6|Chris Richards 6.5|Óscar Mingueza 6|Ben Chilwell 5|Jefferson Lerma 5|Yéremy Pino 7|Daichi Kamada 6|Adam Wharton 7.5|Quinten Timber 6.5|Darío Osorio 6|Cheick Doucouré 6|Ismaïla Sarr 6.5|Eddie Nketiah 5.5|Dwight McNeil 6|Zavier Gozo 6|Jean-Philippe Mateta 6.5|Jørgen Strand Larsen 6.5|Evann Guessand 6.5
"""


def classes():
    out = {}
    for line in C.strip().splitlines():
        slug, rest = line.split(": ", 1)
        d = {}
        for item in rest.split("|"):
            n, c = item.rsplit(" ", 1)
            d[n.strip()] = float(c)
        out[slug] = d
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cl = classes()
    missing = []
    for slug, (name, city, stadium) in META.items():
        raw = os.path.join(RAW, f"{slug}.txt")
        cmap = cl.get(slug, {})
        names = {l.split("|")[0] for l in open(raw, encoding="utf-8") if l.strip()}
        # "Raya" ve "Saliba" gibi kısa adları tam adla eşleştir
        full = {}
        for k, v in cmap.items():
            hit = [n for n in names if n == k] or [n for n in names if n.split()[-1] == k or n.startswith(k + " ")]
            if hit:
                full[hit[0]] = v
            else:
                missing.append(f"{slug}: {k}")
        # Varsayılan: Premier Lig kadro oyuncusu 5.5, 19 yaş ve altı 4.5
        meta = {"slug": slug, "name": name, "city": city, "stadium": stadium,
                "source": "ESPN kadro istatistikleri (Premier Lig)"}
        club = convert(raw, meta, full)
        for p in club["players"]:
            if p["name"] not in full:
                p["class"] = 4.5 if p["age"] <= 19 else 5.5
        json.dump(club, open(os.path.join(OUT, f"{slug}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("eşleşmeyen:", missing or "yok")
