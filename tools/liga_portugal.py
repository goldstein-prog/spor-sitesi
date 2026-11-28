"""Liga Portugal içe aktarma. Seviye puanları editör (Claude) değerlendirmesi; listede olmayan 5, 19 yaş ve altı 4.5."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from league_tool import run

META = {
    "porto": ("FC Porto", "Porto", "Estádio do Dragão"),
    "benfica": ("Benfica", "Lizbon", "Estádio da Luz"),
    "sporting-cp": ("Sporting CP", "Lizbon", "Estádio José Alvalade"),
    "braga": ("Braga", "Braga", "Estádio Municipal de Braga"),
    "vitoria-guimaraes": ("Vitória de Guimarães", "Guimarães", "Estádio D. Afonso Henriques"),
    "santa-clara": ("Santa Clara", "Ponta Delgada", "Estádio de São Miguel"),
    "arouca": ("Arouca", "Arouca", "Estádio Municipal de Arouca"),
    "academico-de-viseu": ("Académico de Viseu", "Viseu", "Estádio do Fontelo"),
    "gil-vicente": ("Gil Vicente", "Barcelos", "Estádio Cidade de Barcelos"),
    "moreirense": ("Moreirense", "Moreira de Cónegos", "Parque de Jogos Comendador Joaquim de Almeida Freitas"),
    "famalicao": ("Famalicão", "Vila Nova de Famalicão", "Estádio Municipal 22 de Junho"),
    "nacional": ("Nacional", "Funchal", "Estádio da Madeira"),
    "alverca": ("Alverca", "Alverca do Ribatejo", "Complexo Desportivo do FC Alverca"),
    "estrela": ("Estrela Amadora", "Amadora", "Estádio José Gomes"),
    "maritimo": ("Marítimo", "Funchal", "Estádio do Marítimo"),
    "casa-pia": ("Casa Pia", "Lizbon", "Estádio Municipal de Rio Maior"),
    "rio-ave": ("Rio Ave", "Vila do Conde", "Estádio dos Arcos"),
    "estoril": ("Estoril", "Estoril", "Estádio António Coimbra da Mota"),
}

C = """
porto: Diogo Costa 8|Jakub Kiwior 7|Jan Bednarek 6.5|Zaidu Sanusi 6|Nehuén Pérez 6.5|Alberto Costa 6.5|Martim Fernandes 7|Victor Froholdt 7.5|Gabri Veiga 7.5|Pablo Rosario 6.5|Hwang In-Beom 6.5|Alan Varela 7|Seko Fofana 6|William Gomes 7|Samu Aghehowa 7.5|Pepê 7|Borja Sainz 7|André Silva 6|Santiago Gimenez 7|Oskar Pietuszewski 6
benfica: Samuel Soares 6|Clément Lenglet 6|Alessandro Circati 6.5|Alexander Bah 6|Samuel Dahl 6.5|Tomás Araújo 7|Enzo Barrenechea 6.5|Fredrik Aursnes 6.5|Georgiy Sudakov 7.5|Leandro Barreiro 6.5|Rafa Silva 6|Claudio Echeverri 6.5|João Palhinha 6.5|Dodi Lukébakio 7|Jakub Kaminski 6.5|Vangelis Pavlidis 7.5|Andreas Schjelderup 7|Jhon Durán 7|Gianluca Prestianni 7.5
sporting-cp: Rui Silva 6.5|Zeno Debast 7|Georgios Vagiannidis 6.5|Iván Fresneda 6.5|Gonçalo Inácio 7.5|Eduardo Quaresma 6.5|Silas Andersen 6.5|Sergi Altimira 6.5|Geny Catamo 7|Rodrigo Zalazar 7|Maxi Araújo 7|Issa Doumbia 6.5|Fotis Ioannidis 7|Nestory Irankunda 6|Luis Guilherme 6.5|Flávio Gonçalves 6.5|Luis Suárez 7.5
braga: Bernardo 6|Víctor Gómez 6|Gustaf Lagerbielke 6|Sergio Barcia 6|Vítor Carvalho 6|João Moutinho 4.5|Mario Dorgeles 6.5|Gorby 6|Demir Ege Tiknaz 6.5|Fran Navarro 6|Pau Víctor 6.5|Jovan Milosevic 6|Jonas Wind 6|Ricardo Horta 6|Gabri Martínez 6
"""

if __name__ == "__main__":
    run("liga-portugal", sys.argv[1] if len(sys.argv) > 1 else "tools/raw/liga-portugal", META, C,
        "ESPN kadro istatistikleri (Liga Portugal)", "2026-11-28")
