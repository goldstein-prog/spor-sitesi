"""Ligue 1 içe aktarma. Seviye puanları editör (Claude) değerlendirmesi; listede olmayan 5, 19 yaş ve altı 4.5."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from league_tool import run

META = {
    "psg": ("Paris Saint-Germain", "Paris", "Parc des Princes"),
    "marseille": ("Marseille", "Marsilya", "Orange Vélodrome"),
    "lyon": ("Lyon", "Lyon", "Groupama Stadium"),
    "lille": ("Lille", "Lille", "Decathlon Arena Pierre-Mauroy"),
    "monaco": ("Monaco", "Monako", "Stade Louis II"),
    "paris-fc": ("Paris FC", "Paris", "Stade Jean-Bouin"),
    "lens": ("Lens", "Lens", "Stade Bollaert-Delelis"),
    "rennes": ("Rennes", "Rennes", "Roazhon Park"),
    "nice": ("Nice", "Nice", "Allianz Riviera"),
    "strasbourg": ("Strasbourg", "Strazburg", "Stade de la Meinau"),
    "toulouse": ("Toulouse", "Toulouse", "Stadium de Toulouse"),
    "brest": ("Brest", "Brest", "Stade Francis-Le Blé"),
    "lorient": ("Lorient", "Lorient", "Stade du Moustoir"),
    "auxerre": ("Auxerre", "Auxerre", "Stade de l'Abbé-Deschamps"),
    "angers": ("Angers", "Angers", "Stade Raymond-Kopa"),
    "le-havre": ("Le Havre", "Le Havre", "Stade Océane"),
    "le-mans": ("Le Mans", "Le Mans", "MMArena"),
    "troyes": ("Troyes", "Troyes", "Stade de l'Aube"),
}

C = """
psg: Matvei Safonov 7|Lucas Chevalier 7|Achraf Hakimi 8.5|Marquinhos 7.5|Willian Pacho 8|Nuno Mendes 8.5|Illia Zabarnyi 7.5|Lucas Beraldo 7|Lucas Hernández 7|Lucas Digne 5.5|Vitinha 9|João Neves 8.5|Warren Zaïre-Emery 8|Fabián Ruiz 7.5|Khvicha Kvaratskhelia 9|Ousmane Dembélé 8.5|Désiré Doué 8|Ferran Torres 7|Maghnes Akliouche 7.5|Senny Mayulu 7|Mika Godts 7|Dro Fernández 7|Quentin Ndjantou 6
marseille: Jeffrey de Lange 6|CJ Egan-Riley 6.5|Nayef Aguerd 6.5|Emerson 5.5|Derek Cornelius 5.5|Ulisses Garcia 5.5|Angel Gomes 7|Himad Abdelli 6.5|Geoffrey Kondogbia 5.5|Pierre-Emile Højbjerg 6.5|Amine Harit 6.5|Amine Gouiri 7.5|Igor Paixão 7|Timothy Weah 6.5|Neal Maupay 5.5|Faris Moumbagna 5.5|Tochukwu Nnadi 6|Keyliane Abdallah 6|Nouhoum Kamissoko 6
lyon: Dominik Greif 6|Rémy Descamps 5|Zachary Athekame 6.5|Noah Nartey 6|Ernest Nuamah 6.5|Tyler Morton 6.5|Ruben Kluivert 6|Mads Bidstrup 6|Tanner Tessmann 6.5|Pavel Sulc 6.5|Abner 6|Felix Bacher 6|Keito Nakamura 6.5|Loïs Openda 7|Moussa Niakhaté 6.5|Corentin Tolisso 6|Nicolás Tagliafico 5|Clinton Mata 5|Khalis Merah 6|Julien Duranville 6|Kail Boudache 6
lille: Berke Özer 6.5|Orlando Gill 5|Nathan Ngoy 6.5|Alexsandro 7|Romain Perraud 6|Tiago Santos 6.5|Tanguy Nianzou 6|Calvin Verdonk 6|Nabil Bentaleb 5.5|Ethan Mbappé 6|Hákon Haraldsson 7|Maurits Kjaergaard 6|Ngal'ayel Mukau 6.5|Benjamin André 5.5|Dilane Bakwa 6.5|Olivier Giroud 5|Osame Sahraoui 6|Ayase Ueda 6|Gaetan Perrin 5.5
monaco: Lukas Hradecky 6|Philipp Köhn 6|Vanderson 7|Jordan Teze 6.5|Christian Mawissa 6.5|Eric Dier 6|Názinho 6|Mohammed Salisu 6.5|Sadibou Sané 6|Denis Zakaria 7|Lamine Camara 7|Aleksandr Golovin 6.5|Takumi Minamino 6|Mamadou Coulibaly 6|Edan Diop 6|Folarin Balogun 7|Matthis Abline 7|Mika Biereth 6.5|Paris Brunner 6.5|Ansu Fati 6|Stanis Idumbo 6
paris-fc: Kevin Trapp 6|Obed Nkambadio 5.5|Hamari Traoré 5|Thibault De Smet 5.5|Moustapha Mbow 6|Samir Chergui 5.5|Otavio 6|Diego Coppola 6.5|Vincent Marchetti 5.5|Pierre Lees-Melou 5.5|Maxime López 6|Ilan Kebbal 6.5|Adama Camara 5.5|Rudy Matondo 6|Moses Simon 6|Jonathan Ikoné 6|Jean-Phillipe Krasso 5.5|Lassine Sinayoko 6.5|Pablo Pagis 6|Luca Koleosho 6.5
lens: Robin Risser 6.5|Ruben Aguilar 5.5|Matthieu Udol 5.5|Jean-Clair Todibo 6.5|Saud Abdulhamid 6|Jonathan Gradit 5|Samson Baidoo 6|Maik Nawrocki 6|Pierre Ganiou 6|Andrija Bulatovic 5.5|Yassine Titraoui 6|Thorgan Hazard 5.5|Amadou Haidara 6|Michaël Cuisance 6|Florian Sotoca 5|Florian Thauvin 6.5|Odsonne Édouard 6|Abdallah Sima 6.5|Michal Skoras 6|Franjo Ivanovic 6.5
rennes: Brice Samba 6.5|Charlie Cresswell 6|Bryan Reynolds 6|Mahamadou Nagida 6|Anthony Rouault 6|Quentin Merlin 6|Abdelhamid Aït Boudlal 6|Djaoui Cissé 6|Sebastian Szymanski 6.5|Valentin Rongier 6|Adrien Thomasson 6|Mahdi Camara 6|Przemyslaw Frankowski 5.5|Esteban Lepaul 6.5|Ludovic Blas 6|Mousa Al-Tamari 6|Eliezer Mayenda 6|Boulaye Dia 6|Issa Soumaré 5.5|Arnaud Nordin 5.5
nice: Yehvann Diouf 6|Mohamed Abdelmoneim 6|Niels Nkounkou 5.5|Moïse Bombito 6.5|Jonathan Clauss 5.5|Hicham Boudaoui 6|Morgan Sanson 5.5|Sofiane Diop 6.5|Axel Witsel 4.5|Youssouf Ndayishimiye 6.5|Mohamed Amoura 6.5|Elye Wahi 6.5|Isak Jansson 6|Nathan N'Goumou 5.5|Alidu Seidu 5.5|Ali Abdi 5|Gauthier Hein 5.5|Salis Abdul Samed 6
strasbourg: Filip Jørgensen 6|Jeyland Mitchell 6|Ismael Doukoure 6.5|Mateo Del Blanco 6|Oso 6|Maximillian Oyedele 6|Giovanni Reyna 6.5|Sebastian Nanasi 6.5|Dário Essugo 6.5|Pape Diop 6|Diogo Sousa 6|Omari Kellyman 6|Samuel Amo-Ameyaw 6|Joaquín Panichelli 6.5|Sékou Mara 5.5|Martial Godo 6|Conrad Harder 6.5|Gessime Yassine 6
toulouse: Guillaume Restes 6.5|Rasmus Nicolaisen 5.5|Mark McKenzie 6|Christ Tapé 5.5|Thomas Jørgensen 6|Niko Sigur 6|Aron Donnum 5.5|Cristian Cásseres Jr. 6|Niklas Schmidt 5.5|Jacen Russell-Rowe 6|Casper Tengstedt 6|Santiago Hidalgo 5.5
brest: Egil Selvik 5.5|Bradley Locko 6|Gautier Lloris 5|Kenny Lala 4.5|Kamory Doumbia 6.5|Lucas Tousart 5.5|Hugo Magnetti 5.5|Joris Chotard 5.5|Ludovic Ajorque 5.5|Mama Baldé 5|Pathé Mboup 5.5
lorient: Yvon Mvogo 5.5|Montassar Talbi 5.5|Arthur Avom 6|Jean-Victor Makengo 5.5|Noah Cadiou 5|Tosin Aiyegun 5|Panos Katseris 5
auxerre: Paul Nardi 5|Axel Tuanzebe 5.5|Fredrik Oppegard 5.5|Lamine Sy 5.5|Romain Faivre 5.5|Cameron Archer 6|Danny Namaso 5.5|Pierre Ekwah 5.5|Naouirou Ahamada 5.5
angers: Anthony Lopes 5|Jordan Lefort 4.5|Haris Belkebla 4.5|Jim Allevinah 4.5|Yassin Belkhdim 5.5|Amine Sbaï 5.5
le-havre: Gauthier Gallon 5|Vincent Sasso 4|Mbwana Samatta 4.5|Josh Maja 5.5|Amir Richardson 5.5|Sota Nakamura 5.5
le-mans: Samuel Yohou 4|Djibril Sidibé 4|Adil Bourabaa 5.5
troyes: Adrien Monfray 4|Antoine Mille 5.5|Hugo Picard 5.5|Dermane Karim 5.5|Jeremy Le Douaron 5.5
"""

if __name__ == "__main__":
    run("ligue-1", sys.argv[1] if len(sys.argv) > 1 else "tools/raw/ligue-1", META, C,
        "ESPN kadro istatistikleri (Ligue 1)", "2026-11-27")
