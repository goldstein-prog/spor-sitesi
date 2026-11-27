"""Bundesliga içe aktarma. Seviye puanları editör (Claude) değerlendirmesi; listede olmayan 5, 19 yaş ve altı 4.5."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from league_tool import run

META = {
    "bayern-munich": ("Bayern Münih", "Münih", "Allianz Arena"),
    "borussia-dortmund": ("Borussia Dortmund", "Dortmund", "Signal Iduna Park"),
    "rb-leipzig": ("RB Leipzig", "Leipzig", "Red Bull Arena"),
    "bayer-leverkusen": ("Bayer Leverkusen", "Leverkusen", "BayArena"),
    "eintracht-frankfurt": ("Eintracht Frankfurt", "Frankfurt", "Deutsche Bank Park"),
    "werder-bremen": ("Werder Bremen", "Bremen", "Weserstadion"),
    "vfb-stuttgart": ("VfB Stuttgart", "Stuttgart", "MHPArena"),
    "tsg-hoffenheim": ("Hoffenheim", "Sinsheim", "PreZero Arena"),
    "mainz": ("Mainz 05", "Mainz", "Mewa Arena"),
    "fc-koln": ("1. FC Köln", "Köln", "RheinEnergieStadion"),
    "borussia-monchengladbach": ("Borussia Mönchengladbach", "Mönchengladbach", "Borussia-Park"),
    "hamburger-sv": ("Hamburger SV", "Hamburg", "Volksparkstadion"),
    "union-berlin": ("Union Berlin", "Berlin", "Stadion An der Alten Försterei"),
    "sc-freiburg": ("SC Freiburg", "Freiburg", "Europa-Park Stadion"),
    "fc-augsburg": ("FC Augsburg", "Augsburg", "WWK Arena"),
    "sv-elversberg": ("SV Elversberg", "Spiesen-Elversberg", "Ursapharm-Arena an der Kaiserlinde"),
    "sc-paderborn": ("SC Paderborn", "Paderborn", "Home Deluxe Arena"),
    "schalke-04": ("Schalke 04", "Gelsenkirchen", "Veltins-Arena"),
}

C = """
bayern-munich: Manuel Neuer 4|Jonas Urbig 6.5|Sven Ulreich 3|Dayot Upamecano 8|Kim Min-Jae 7|Jonathan Tah 7|Nathaniel Brown 7|Alphonso Davies 7.5|Hiroki Ito 6.5|Sacha Boey 6.5|Josip Stanisic 7|Joshua Kimmich 8.5|Tom Bischof 7.5|Jamal Musiala 9.5|Michael Olise 8.75|Konrad Laimer 7|Ismael Saibari 7.5|Lennart Karl 8|Aleksandar Pavlovic 8.5|Serge Gnabry 6.5|Harry Kane 9.5|Luis Díaz 8.5
borussia-dortmund: Gregor Kobel 7.5|Waldemar Anton 6.5|Nico Schlotterbeck 7.5|Ramy Bensebaini 5.5|Kouakou Gadou 7|Daniel Svensson 7|Julian Ryerson 6.5|Kauã Prates 5.5|Filippo Mané 6|Jobe Bellingham 8|Felix Nmecha 7.5|Carney Chukwuemeka 6.5|Ethan Nwaneri 7.5|Konstantinos Karetsas 7.5|Marcel Sabitzer 5.5|Emre Can 5|Joey Veerman 6.5|Serhou Guirassy 7.5|Maximilian Beier 7.5|Fábio Silva 7|Giannis Konstantelias 6
rb-leipzig: Maarten Vandevoordt 6.5|Ørjan Nyland 4|Tidiam Gomis 7|Ezechiel Banzuzi 7|Antonio Nusa 8|Willi Orbán 5|Neil El Aynaoui 7|David Raum 6.5|Brajan Gruda 7.5|Rômulo 7|Christopher Nkunku 7|Nicolas Seiwald 7|Ridle Baku 6.5|Benjamin Henrichs 5.5|Castello Lukeba 7.5|Andrija Maksimovic 6.5|Rocco Reitz 6.5|Maxime Estève 6.5|Christoph Baumgartner 6.5|Johan Bakayoko 7|Max Finkgrafe 5.5|Abdoul Koné 6|Marc Guiu 6.5|Assan Ouédraogo 7|Lukas Klostermann 5
bayer-leverkusen: Mark Flekken 5.5|Ibrahim Maza 8|Facundo Medina 6.5|Afonso Moreira 6.5|Jarell Quansah 7.5|Miguel Gutiérrez 7.5|Christian Kofane 7|Patrik Schick 7|Moussa Diaby 6.5|Ezequiel Fernández 7.5|Robert Andrich 5.5|Malik Tillman 7|Aleix García 6.5|Jonas Hofmann 5.5|Guela Doué 6.5|Loïc Badé 7|Edmond Tapsoba 7|Lucas Vázquez 4|Martin Terrier 5.5|Victor Boniface 6|Nathan Tella 6|Eliesse Ben Seghir 7|Tim Oermann 5.5
eintracht-frankfurt: Noah Atubolu 6.5|Kauã Santos 6|Elias Baum 6.5|Lilian Brassier 6|Robin Koch 6|Keita Kosugi 6.5|Nnamdi Collins 6.5|Oscar Højlund 6.5|Farès Chaïbi 6.5|Noël Aséko 6.5|Ritsu Doan 7|Raphael Onyedika 6.5|Mario Götze 4.5|Can Uzun 7.5|Ansgar Knauff 6|Jonathan Burkardt 7|Younes Ebnoutalib 6.5|Ayoube Amaimouni 6|Timothy Chandler 3
werder-bremen: Karl Hein 5.5|Olivier Deman 5.5|Amos Pieper 5.5|Mitchell Weiser 4.5|Arthur 5.5|Marco Friedl 5.5|Niklas Stark 4.5|Senne Lynen 6|Ludovit Reis 6|Chuki 6|Dariusz Stalmach 6|Youri Regeer 5.5|Jens Stage 6|Niclas Füllkrug 5|Marco Grüll 5.5|Eren Dinkci 6|Cedric Itten 5|Justin Njinmah 5.5|Keke Topp 5.5|Oskar Wójcik 5.5|Mick Schmetgens 5.5
vfb-stuttgart: Fabian Bredlow 4.5|Dennis Seimen 5.5|Ameen Al Dakhil 5.5|Ramon Hendriks 6|Josha Vagnoman 6|Maximilian Mittelstädt 6.5|Luca Jaquez 6|Leonidas Stergiou 5.5|Lorenz Assignon 5.5|Dan-Axel Zagadou 5.5|Jeff Chabot 6|Finn Jeltsch 6.5|Angelo Stiller 7|Chris Führich 6|Bilal El Khannouss 7|Atakan Karazor 5.5|Grischa Prömel 5|Nikolas Nartey 5.5|Tiago Tomás 6|Ermedin Demirovic 6.5|Dzenan Pejcinovic 6|Jamie Leweling 6.5|Deniz Undav 6|Leo Sauer 6
tsg-hoffenheim: Oliver Baumann 4.5|Robin Hranác 6|Ozan Kabak 6|Bernardo 5|Valentin Gendrey 5.5|Albian Hajdari 6|Alexander Prass 6|Koki Machida 6|Vladimír Coufal 4|Mats Rots 6|Leon Avdullahu 6.5|Patrick Wimmer 6|Wouter Burger 6|Bambasé Conté 6|Max Moerstedt 6|Adam Hlozek 6.5|Fisnik Asllani 6.5|Adam Daghim 6|Tim Lemperle 6|Andrej Kramaric 4.5|Nathan De Cat 6
mainz: Alexander Schwolow 4.5|Robin Zentner 4.5|Phillipp Mwene 4.5|Fabio Gruber 5.5|Stefan Posch 5.5|Anthony Caci 5.5|Danny da Costa 4|Silvan Widmer 4|Kacper Potulski 6|Eric Martel 5.5|Kaishu Sano 6.5|Lee Jae-Sung 4|Paul Nebel 6|Nadiem Amiri 5.5|Lennard Maloney 5|Phillip Tietz 5.5|Ransford-Yeboah Königsdörffer 5.5|Benedict Hollerbach 5.5|Sheraldo Becker 5
fc-koln: Marvin Schwäbe 5|Ron-Robert Zieler 3|Joel Schmied 5|Borna Sosa 5|Timo Hübers 5|Gideon Mensah 5|Jahmai Simpson-Pusey 6|Luka Lochoshvili 5|Sebastian Sebulonsen 5.5|Tom Krauss 5.5|Ellyes Skhiri 5.5|Ísak Jóhannesson 6|Said El Mala 7.5|Alessio Castro-Montes 5|Paul Okon-Engstler 5.5|Jan Thielmann 5.5|Linton Maina 5.5|Luca Waldschmidt 4.5|Ragnar Ache 5|Thijs Dallinga 5.5|Marius Bulter 4|Mikey Moore 6.5
borussia-monchengladbach: Moritz Nicolas 5.5|Daniel Batz 4|Fabio Chiarodia 6|Kevin Diks 5|Jan Leszczynski 5.5|Kou Itakura 5.5|Daiki Hashioka 5|David Herold 5|Lukas Ullrich 6|Joe Scally 6.5|Kevin Stöger 4.5|Franck Honorat 5.5|Florian Neuhaus 5.5|Philipp Sander 5.5|Jens Castrop 6|Robin Hack 5.5|Mathieu Nguefack 5|Wael Mohya 7|Hugo Bolin 5.5|Zento Uno 5.5|Isac Lidberg 5|Tim Kleindienst 5|Shuto Machino 5.5|Nicolas Kühn 6
hamburger-sv: Daniel Heuer Fernandes 4.5|Terem Moffi 6|Martin Adeline 6|Albert Grønbaek 6|David Møller Wolfe 5.5|Otto Stange 5.5|Zakaria El Ouahdi 6|Warmed Omari 5.5|Patson Daka 5.5|Yussuf Poulsen 4.5|Nicolás Capaldo 5.5|Albert Sambi Lokonga 5.5|Fabio Vieira 6|Sebastiaan Bornauw 5.5|Louis Lemke 5|Miro Muheim 5.5|Kofi Amoako 5.5|Nicolai Remberg 5|Shafiq Nandja 5|Jordan Torunarigha 5|Bilal Nadir 5.5|Bakery Jatta 4.5|Mario Vuskovic 5.5
union-berlin: Frederik Ronnow 5|Matheo Raab 4.5|Felix Uduokhai 5|Livan Burcu 6|Andrej Ilić 5|Marin Ljubicic 5|Oliver Burke 4.5|Aljoscha Kemlein 6|Kastriot Imeri 5|András Schäfer 5.5|Jeong Woo-Yeong 5.5|Michel Aebischer 5.5|Tim Skarke 5|Janik Haberer 4.5|Rani Khedira 4.5|Leopold Querfeld 6|Tom Rothe 6|Zeno Van Den Bosch 5.5|Derrick Köhn 5|Josip Juranovic 5|Marvin Friedrich 4.5|Christopher Trimmel 2.5
sc-freiburg: Mio Backhaus 6|Philipp Lienhart 6|Matthias Ginter 6|Lukas Kübler 5|Philipp Treu 6|Jordy Makengo 6|Maximilian Eggestein 6.5|Yuito Suzuki 6.5|Yannick Engelhardt 6|Niklas Beste 6|Vincenzo Grifo 5.5|Derry Scherhant 6|Lucas Höler 5|Cyriaque Irié 6|Igor Matanovic 6.5|Keisuke Goto 6|Patrick Osterhage 5.5|Christian Günter 4.5|Anthony Jung 4
fc-augsburg: Finn Dahmen 6|Calvin Brackelmann 5.5|Chrislain Matsima 6|Jeffrey Gouweleeuw 4.5|Seol Young-Woo 6|Hennes Behrens 5.5|Marius Wolf 5|Juma Bah 6|Noahkai Banks 5.5|Han-Noah Massengo 6|Mert Kömür 6.5|Yannik Keitel 5.5|Robin Fellhauer 5.5|Alexis Claude-Maurice 6|Arijon Ibrahimovic 6|Anton Kade 6|Fabian Rieder 6.5|Rodrigo Ribeiro 6|Michael Gregoritsch 5.5
sv-elversberg: Nicolas Kristof 5.5|Lukas Finn Pinckert 5|Lasse Günther 5.5|Luca Sirch 5|Jan Gyamerah 5|Maximilian Rohr 5|Felix Keidel 5.5|Maurice Krattenmacher 6|Lukasz Poreba 5.5|Lukas Petkov 5.5|Cole Campbell 6|David Mokwa 5.5|Noel Futkeu 5.5|Noah Darvich 5.5
sc-paderborn: Nahuel Nicolas Noll 5|Laurin Curda 5|Jano Horst 5|Mattes Hansen 5|Tjark Scheller 5|Santiago Castaneda 5.5|Raphael Obermair 5|Laurin Ulrich 5|Marvin Pieringer 5|Steffen Tigges 5|Stefano Marino 5|Gabriel Vidovic 5.5|Rayan Philippe 5|Sven Michel 4
schalke-04: Loris Karius 5|Hasan Kurucay 5|Timo Becker 5|Robin Gosens 5|Nikola Katic 5|Vitalie Becker 5.5|Maximilian Wöber 5.5|Satoshi Tanaka 5.5|Soufian El-Faouzi 5.5|Adil Aouchiche 5.5|Junior Dina Ebimbe 5.5|Hwang Hee-Chan 5.5|Moussa Sylla 5.5|Edin Dzeko 3.5|Kenan Karaman 4.5|Junior Adamu 5.5|Dejan Ljubicic 5
"""

if __name__ == "__main__":
    run("bundesliga", sys.argv[1] if len(sys.argv) > 1 else "/tmp/raw/bundesliga", META, C,
        "ESPN kadro istatistikleri (Bundesliga)", "2026-11-27")
