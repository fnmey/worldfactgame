# Einbinden der notwendigen Module
import json,re,os
import pandas as pd

# Definieren der Funktionen // bisher ist nur die einwohner-Funktion 
# auskommentiert und funktioniert für jedes Land
def flaeche(xx):
    # in Quadratkilometer
    
    aa = xx["Geography"]
    aa = aa["Area"]
    aa = aa["total"]
    aa = aa["text"]
    
    zahl = re.compile(r"""([0-9,])+""")
    zahlsuche = zahl.search(aa)
    zahlsuche = zahlsuche.group()
    
    aa = zahlsuche.replace(",","")
    aa = int(aa)
    
    return aa

def einwohner(xx):
    
    # Öffnen der jeweiligen Dictionaries, um Wert zu erhalten
    try:
        aa = xx["People and Society"]
        aa = aa["Population"]
        aa = aa["text"]
    except KeyError:
        aa = "0"
    
    # Suchen nach Zahl innerhalb des Dictionaries und Ausgabe der Zahl als str
    zahl = re.compile(r"""([0-9,])+""")
    zahlsuche = zahl.search(aa)
    if zahlsuche is None:
        zahlsuche = "0"
    else:
        zahlsuche = zahlsuche.group()
    
    # Entfernen der Dezimalzeichen(","), um in einheitliches Zahlenformat
    # umzuwandeln
    if type(zahlsuche) is str:
        aa = zahlsuche.replace(",","")
    try:    
        aa = int(aa)
    except ValueError:
        aa = 0
        
    return aa

def kuestenlinie(xx):
    # in Kilometer
    
    aa = xx["Geography"]
    aa = aa["Coastline"]
    aa = aa["text"]
    
    zahl = re.compile(r"""([0-9,.])+""")
    aa = zahl.search(aa)
    aa = aa.group()
    
    
    
    if len(aa)>1 and aa[-2] == ".":
        aa = aa[:-2]
    aa = aa.replace(",","")
    aa = int(aa)
    
    return aa

def landesgrenze(xx):
    # in Kilometer
    
    aa = xx["Geography"]
    aa = aa["Land boundaries"]
    aa = aa["total"]
    aa = aa["text"]
    
    aa = aa[:-3]
    aa = aa.replace(",","")
    aa = int(aa)

    return aa

def hoechsterpunkt(xx):
    # in Meter
    
    aa = xx["Geography"]
    aa = aa["Elevation"]
    aa = aa["highest point"]
    aa = aa["text"]
    
    hoehe = re.compile(r"""(\d)+(,)*(\d)*""")
    hoehensuche = hoehe.search(aa) 
    hoehe_text = hoehensuche.group()
    
    hoehe_text = hoehe_text.replace(",","")
    hoehe_text = int(hoehe_text)
    
    return hoehe_text

def hoechsterpunktname(xx):
    
    aa = xx["Geography"]
    aa = aa["Elevation"]
    aa = aa["highest point"]
    aa = aa["text"]
    
    name = re.compile(r"""(([a-zA-Z])+(0-9)*(,)*( )+([a-zA-Z])*)""")
    namesuche = name.search(aa)
    name_text = namesuche.group()

    if name_text[-1] == " ":
        name_text = name_text[:-1]
    
    return name_text

# Generieren einer Liste aus allen Dateien im Ordner "_Alle" um Liste mit Kürzeln zu erzeugen
liste = os.listdir(r"D:\Projekte\Python\Factbook\factbook.json-master\_Alle")
kuerzelliste = []

# for-Loop um nur die ersten beiden Buchstaben der jeweiligen Dateien zu extrahieren und
# in die Kürzelliste einzufügen
for i in liste:
    laenderkuerzel = re.compile("""([a-zA-Z]){2}""")
    test = laenderkuerzel.search(i)
    test = test.group()
    kuerzelliste.append(test)

# Definieren der Spalten für die Tabelle / Definieren der Kategorien
kuerzel = ["kürzel"]
kategorien = ["einwohner"]
spalten = kuerzel + kategorien

# Erstellen der Liste, in der im nächsten Schritt die Werte eingetragen werden
laenderliste = []

# for-Loop um oben definierte Funktionen für alle Länder auszuführen und in 
# die Tabelle einzutragen
for i in kuerzelliste:
    
    # Öffnen der Dateien
    with open(r'D:\Projekte\Python\Factbook\factbook.json-master\_Alle\{0}.json'.format(i), encoding='utf-8') as file:
        land = json.load(file)
    
    # Anwenden der Funktionen und Anhängen an Tabelle, wenn Wert != 0 
    for j in kategorien:
        if globals()[j](land) != 0:    
            laenderliste.append((i,(globals()[j](land))))
            
# Liste in Pandas-Tabelle einfügen und exportieren
laendertabelle = pd.DataFrame(laenderliste,columns=spalten)
laendertabelle.to_excel("D:\Projekte\Python\Factbook\Datentabelle.xlsx")

