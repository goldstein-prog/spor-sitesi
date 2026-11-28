"""La Liga içe aktarma. Seviye puanları editör (Claude) değerlendirmesi; listede olmayan 5, 19 yaş ve altı 4.5."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from league_tool import run

META = {
    "barcelona": ("Barcelona", "Barselona", "Spotify Camp Nou"),
    "real-madrid": ("Real Madrid", "Madrid", "Santiago Bernabéu"),
    "atletico-madrid": ("Atlético Madrid", "Madrid", "Riyadh Air Metropolitano"),
    "real-sociedad": ("Real Sociedad", "San Sebastián", "Reale Arena"),
    "sevilla": ("Sevilla", "Sevilla", "Ramón Sánchez-Pizjuán"),
    "athletic-club": ("Athletic Club", "Bilbao", "San Mamés"),
    "villarreal": ("Villarreal", "Villarreal", "Estadio de la Cerámica"),
    "alaves": ("Alavés", "Vitoria-Gasteiz", "Mendizorrotza"),
    "espanyol": ("Espanyol", "Barselona", "RCDE Stadium"),
    "deportivo": ("Deportivo La Coruña", "A Coruña", "Riazor"),
    "osasuna": ("Osasuna", "Pamplona", "El Sadar"),
    "celta-vigo": ("Celta Vigo", "Vigo", "Balaídos"),
    "levante": ("Levante", "Valensiya", "Ciutat de València"),
    "rayo-vallecano": ("Rayo Vallecano", "Madrid", "Estadio de Vallecas"),
    "valencia": ("Valencia", "Valensiya", "Mestalla"),
    "getafe": ("Getafe", "Getafe", "Coliseum"),
    "elche": ("Elche", "Elche", "Martínez Valero"),
    "real-betis": ("Real Betis", "Sevilla", "Benito Villamarín"),
    "racing-santander": ("Racing Santander", "Santander", "El Sardinero"),
    "malaga": ("Málaga", "Málaga", "La Rosaleda"),
}

C = """
barcelona: Joan García 7.5|Wojciech Szczesny 4.5|João Cancelo 6.5|Alejandro Balde 7.5|Pau Cubarsí 8.5|Xavi Espart 6.5|Andreas Christensen 6.5|Gerard Martín 7|Jules Koundé 8|Eric García 7|Gavi 8|Fermín López 8|Pedri 10|Rodri 8.5|Dani Olmo 8|Frenkie de Jong 7.5|Marc Bernal 7.5|Gabriel Jesus 6.5|Lamine Yamal 9.75|Raphinha 8.5|Karim Adeyemi 7.5|Anthony Gordon 8|Roony Bardghji 6.5|Brian Fariñas 5.5
real-madrid: Thibaut Courtois 7.5|Andriy Lunin 6|Raúl Asencio 6.5|Éder Militão 7|Dean Huijsen 8.5|Trent Alexander-Arnold 8|Ibrahima Konaté 8|Marc Cucurella 7.5|Álvaro Carreras 7.5|Antonio Rüdiger 6|Ferland Mendy 5.5|Denzel Dumfries 6.5|Jude Bellingham 9.5|Eduardo Camavinga 8|Federico Valverde 9|Aurélien Tchouaméni 8.5|Arda Güler 8.75|Bernardo Silva 7|Brahim Díaz 7|Thiago Pitarch 6|Vinícius Júnior 9.5|Endrick 7.5|Kylian Mbappé 9.5|Rodrygo 8|Carlos Espí 6.5|Yan Diomande 8
atletico-madrid: Jan Oblak 7|Juan Musso 5|Dávid Hancko 7|Marc Pubill 7|Cristian Romero 7.5|Alejandro Grimaldo 7|Robin Le Normand 7|Rodrigo Mendoza 6.5|Johnny Cardoso 7|Koke 5.5|Lee Kang-In 7.5|Pablo Barrios 8|Álex Baena 8|Marcos Llorente 6.5|Morten Hjulmand 7.5|Alexander Sørloth 6.5|Ademola Lookman 7|Jonathan David 7.5|Julián Álvarez 8.5|Giuliano Simeone 7.5|Obed Vargas 6|Arnau Ortiz 6
real-sociedad: Álex Remiro 6.5|Unai Marrero 5.5|Jon Aramburu 6.5|Aihen Muñoz 5.5|Igor Zubeldia 6|Jon Martín 7|Jon Pacheco 6|Mamadou Sarr 6.5|Álvaro Odriozola 5|Héctor Fort 6.5|Jon Gorrotxategi 6|Beñat Turrientes 6.5|Carlos Soler 6.5|Yangel Herrera 6.5|Arsen Zakharyan 6.5|Luka Sucic 7|Ander Barrenetxea 6.5|Orri Óskarsson 7|Mikel Oyarzabal 7.5|Gonçalo Guedes 6|Job Ochieng 6|Takefusa Kubo 7.5|Sergio Gómez 6.5
sevilla: Odisseas Vlachodimos 5.5|Juan Iglesias 6|Julio Díaz 5.5|Enrique Salas 6|Andrés Castrín 6|Arouna Sangante 5.5|Gabriel Suazo 5.5|Lucien Agoumé 6.5|Giorgi Kochorashvili 6|Rubén Vargas 6|Manu Bueno 6|Jon Guridi 5.5|Youssouf Fofana 6.5|Alfonso González 5.5|Robbie Ure 6|Peque 6.5|Isaac Romero 6.5|Lucas Stassin 6.5|Felix Correia 6|Chidera Ejuke 6|Pepe Carmona 5|Miguel Sierra 6
athletic-club: Unai Simón 7|Álex Padilla 5.5|Dani Vivian 6.5|Aitor Paredes 6.5|Yeray 6|Jesús Areso 6|Aymeric Laporte 6|Hugo Rincón 6|Yuri Berchiche 4.5|Beñat Prados 6.5|Oihan Sancet 7.5|Iñigo Ruiz de Galarreta 5|Mikel Jauregizar 7|Alejandro Rego 6|Robert Navarro 6.5|Beñat Gerenabarrena 6|Peio Canales 6.5|Álex Berenguer 6|Iñaki Williams 6|Nico Williams 8|Gorka Guruzeta 6|Maroan Sannadi 6|Johaneko Louis Jean 5.5|Álvaro Djaló 5.5
villarreal: Luiz Júnior 6|Péter Gulácsi 4|Logan Costa 6.5|Alex Freeman 6.5|Pau Navarro 6.5|Juan Foyth 6.5|Renato Veiga 7|Santiago Mouriño 6.5|Carlos Romero 6|Sergi Cardona 6|Alberto Moleiro 7.5|Santi Comesaña 6.5|Carlos Macià 6|Pape Gueye 7|Nathan Saliba 6.5|Gerard Moreno 5.5|Georges Mikautadze 7|Ilias Akhomach 6.5|Tajon Buchanan 6.5|Nicolas Pépé 5.5|Tani Oluwaseyi 6|Ayoze Pérez 5.5|Alassane Diatta 5.5
alaves: Antonio Sivera 6|Nicolás Valentini 5.5|Youssef Lekhedim 5.5|Ángel Pérez 6|Nahuel Tenaglia 5.5|Ville Koski 6|Jonny 5|Denis Suárez 5|Ander Guevara 5.5|Antonio Blanco 6|Carles Aleñá 5.5|Pablo Ibáñez 5.5|Carlos Protesoni 5.5|Mariano Díaz 4.5|Toni Martínez 5.5|Lucas Boyé 6|Aitor Mañas 5.5|Abde Rebbach 5.5|Hugo Novoa 5.5
espanyol: Ángel Fortuño 5.5|Marko Dmitrovic 5|Quilindschy Hartman 6|Clemens Riedel 6|Leandro Cabrera 4.5|Unai Núñez 5.5|Vanja Drkusic 5.5|Roger Hinojo 6|Omar El Hilali 6|Urko Gonzalez 6|Edu Expósito 6|Pol Lozano 6|Pere Milla 4.5|Gabriel Moscardo 6|Cala 5.5|Rafael Bauza 5.5|Javi Hernandez 6.5|Javier Puado 6|Roberto Fernández 6.5|Bryan Zaragoza 6|Jofre Carreras 5.5|Marcos Fernández 5.5|Tyrhys Dolan 6
deportivo: Leo Román 5.5|Adrià Altimira 5.5|Lucas Noubi 6|Giacomo Quagliata 5.5|Miguel Loureiro 5|Angeliño 5.5|José María Giménez 6|Ximo Navarro 4|Marc Casadó 7|Diego Villares 5.5|Riki Rodríguez 5.5|Lorenzo Amatucci 6|Jonathan Asp Jensen 6|Mario Soriano Carreno 6.5|Pierre-Emerick Aubameyang 4.5|Zakaria Eddahchouri 6|Yeremay Hernández 7|David Mella 6.5|Luismi Cruz 6|Adama Traoré 5|Bil Nsongo 6|Arnau Comas 5.5|Dani Barcia 5.5
osasuna: Sergio Herrera 5|Aitor Fernández 4.5|Diego Rico 4.5|Enzo Boyomo 6|Iñigo Arguibide 6|Aimar Oroz 6.5|Romain Del Castillo 5|Raúl Moro 6|Jonathan Dubasin 6|Jorge Herrando 6|Lucas Torró 5|Rubén García 4.5|Moi Gómez 4.5|Iker Muñoz 6|Asier Osambela 6|Ante Budimir 5.5|Raúl García 6.5|Valentin Rosier 5.5|Alejandro Catena 5.5|Abel Bretones 6|Enrique Barja 5.5|Jon Moncayola 6
celta-vigo: Andrei Radu 6|Altay Bayindir 5.5|Williot Swedberg 6.5|Yoel Lago 6.5|Ferran Jutglà 5.5|Ilaix Moriba 6.5|Aleix Febas 5.5|Sergio Carreira 6|Javi Galán 5|Javi Rueda 6|Hugo Álvarez 6.5|Marcos Alonso 4.5|Pablo Durán 6.5|Javi Rodríguez 6.5|Hugo González 6|Iago Aspas 4.5|Hugo Burcio 5.5|Miguel Román 6|Sebastián Cáceres 5.5|Couhaib Driouech 6|Borja Iglesias 5|Álvaro Núñez 5.5|Carl Starfelt 5
levante: Mathew Ryan 4.5|Aïssa Mandi 4.5|Ifeanyi Ndukwe 5.5|Adrián de la Fuente 5.5|Víctor García 4.5|Jeremy Toljan 4.5|Manu Sánchez 5|Nacho Pérez 5.5|Hugo Sotelo 5.5|Dani Requena 5.5|Roger Brugué 5.5|Jon Ander Olasagasti 5.5|Enzo Bardeli 5.5|Orio Rey 5|Iván Romero 6|Petar Ratkov 6|Etta Eyong 6|Thiago Fernández 5.5|Paco Cortés 5
rayo-vallecano: Emil Audero 5.5|Daniel Cárdenas 5|Augusto Batalla 5|Andrei Ratiu 6|Marash Kumbulla 5.5|Luiz Felipe 5|Mujaid Sadick 5.5|Adrià Pedrosa 5.5|Iván Balliu 4.5|Florian Lejeune 4.5|Jozhua Vertrouwd 5.5|Pedro Díaz 5.5|Pathé Ciss 4.5|Isi Palazón 5|Unai López 5.5|Randy Nteka 5|Álvaro García 4.5|Óscar Valentín 4.5|Alexandre Alemão 5.5|Sergio Camello 6.5|Giorgi Tsitaishvili 5.5|Jorge de Frutos 6|Fran Pérez 5.5|Raúl de Tomás 4.5
valencia: Stole Dimitrievski 5|Mouctar Diakhaby 5.5|César Tárrega 6.5|Justin de Haas 5.5|José Gayà 5.5|Dimitri Foulquier 4|Jesús Vázquez 6|Arnau Martínez 5.5|Pablo Maffeo 5.5|Guido Rodríguez 5|Javi Guerra 7|Harvey Elliott 7|Aliou Dieng 5.5|Pepelu 6|Filip Ugrinic 6|Umar Sadiq 5.5|Arnaut Danjuma 6|Hugo Duro 6|Luis Rioja 4.5|Diego López 6.5|Dani Raba 5|David Otorbi 6|Ryunosuke Sato 5.5|Copete 5
getafe: David Soria 5.5|Jirí Letácek 5|Djené 4.5|Davinchi 6|Saba Sazonov 5.5|Abdel Abqar 5.5|Dani Carvajal 5.5|Sebastián Boselli 6|Kiko Femenía 4|Andrés García 6|Johan Mojica 4.5|Zaid Romero 5.5|Jean Ives Valou 5.5|Mario Martín 6|Nemanja Gudelj 4|Ramón Terrats 6|Francho Serrano 5.5|Christantus Uche 6|Orel Mangala 6|Alberto Risco 5|Martín Satriano 6|Borja Mayoral 5.5|Enes Ünal 6|Ivan Azón 6|Juanmi 4
elche: Matías Dituro 4|Buba Sangaré 6|Roy Revivo 6|Pedro Bigas 4|Rubén Sánchez 5|Víctor Chust 6|Matia Barzic 5.5|Federico Redondo 6.5|Marc Aguado 6|Facundo Buonanotte 6.5|Gonzalo Villar 5.5|Martim Neto 6|Thomas Lemar 5|Javier Morcillo 5.5|Ezequiel Ponce 5|Germán Valera 6|Fer Niño 6|Grady Diangana 5|José Antonio Morente 5.5|Lucas Cepeda 6|Abiel Osorio 5.5|Ali Houary 5.5|Kevin Lomónaco 5.5|Bambo Diaby 5
real-betis: Álvaro Valles 6.5|Héctor Bellerín 5.5|Diego Llorente 5|Natan 6.5|Marc Bartra 4.5|Fran García 6|Ángel Ortiz 6|Valentín Gómez 6.5|Junior Firpo 5|Facundo Bernal 6|Pablo Fornals 6.5|Álvaro Fidalgo 6.5|Rodrigo Riquelme 6.5|Nelson Deossa 6.5|Giovani Lo Celso 6.5|Marc Roca 6|Isco 6|Dani Ceballos 6|Antony 7|Cucho Hernández 6.5|Abde Ezzalzouli 7|Troy Parrott 6.5|Aitor Ruibal 5
racing-santander: Julen Agirrezabala 6.5|Alvaro Mantilla 5.5|Aarón Martín 5.5|Manu 5|Pablo Ramon 5.5|Facundo González 6|Jorge Salinas 6|Pedro Felipe 5.5|Jeanuël Belocian 6|Íñigo Sainz 5|André Almeida 5.5|Maguette Gueye 5.5|Matteo Prati 6|Sergio Canales 5.5|Iván Martín 6|Giorgi Guliashvili 5.5|Iñigo Vicente 6|Andrés Martín 6|Asier Villalibre 5|Pablo García 6|Iker Luque 5.5|Yassir Zabiri 7
malaga: Alfonso Herrero 5|Carlos Puga 5|Einar Galilea 4.5|Álex Pastor 5|José Salinas 5|Ángel Recio 5|Diego Murillo 5|Fernando Calero 5|Juan Berrocal 5|Rafa Garrido 5|Adam Aznou 5.5|Jens Cajuste 5.5|Ramón Enríquez 5|Carlos Dotor 5.5|Rafa Rodríguez 5|Pablo Martínez 5|Juan Cruz 5|Daniel Lorenzo 5|Izan Merino 5.5|Haitam Abaida 5|Chupete 5.5|David Larrubia 5.5|Joaquín Muñoz 5|Eneko Jauregui 4.5|Adrián Niño 5.5|Julen Lobete 5
"""

if __name__ == "__main__":
    run("la-liga", sys.argv[1] if len(sys.argv) > 1 else "/tmp/raw/la-liga", META, C,
        "ESPN kadro istatistikleri (La Liga)", "2026-11-27")
