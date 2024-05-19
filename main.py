import os
import cv2
import json
from collections import defaultdict

# funcția pentru analiza culorilor dintr-o imagine
def analizaculori(caleimagine):
    # incărcarea imaginii utilizând OpenCV
    imagine = cv2.imread(caleimagine)
    # verificarea dacă imaginea a fost încărcată corect
    if imagine is None:
        raise ValueError(f"Nu s-a putut accesa imaginea: {caleimagine}")

    # calcularea valorii medii pentru fiecare componentă de culoare
    mean_b, mean_g, mean_r = cv2.mean(imagine)[:3]

    # returnarea scorului pentru fiecare culoare
    return {'rosu': mean_r, 'verde': mean_g, 'albastru': mean_b}

# funcția pentru clasificarea imaginilor în funcție de culorile predominante
def clasificareimagini(imaginedirector):
    # inițializarea unui dicționar pentru a stoca imaginile clasificate pe culori
    cul = {'rosu': [], 'verde': [], 'albastru': []}
    # inițializarea unui dicționar pentru a stoca scorurile culorilor pentru fiecare imagine
    imaginescor = defaultdict(dict)

    # iterarea prin fiecare imagine din directorul dat
    for numeimagine in os.listdir(imaginedirector):
        caleimagine = os.path.join(imaginedirector, numeimagine)
        # verificarea dacă elementul iterat este un fișier
        if os.path.isfile(caleimagine):
            try:
                # analiza culorilor pentru imaginea curentă
                scor = analizaculori(caleimagine)
                # Adăugarea scorului la dicționarul imaginescor
                imaginescor[numeimagine] = scor

                # determinarea culorii predominante pentru imaginea curentă
                culpre = max(scor, key=scor.get)
                # adăugarea numelui imaginii la lista corespunzătoare culorii predominante
                cul[culpre].append(numeimagine)
            except ValueError as e:
                print(e)

    # returnarea dicționarelor cu imaginile clasificate și scorurile culorilor
    return cul, imaginescor

# funcția pentru salvarea rezultatelor într-un fișier JSON
def salvarejson(cul, imaginescor, outputfile):
    # crearea unui dicționar care va fi convertit în format JSON
    results = {
        'grupuri_culori': cul,
        'scorurile imaginilor': imaginescor
    }

    # salvarea dicționarului într-un fișier JSON
    with open(outputfile, 'w') as json_file:
        json.dump(results, json_file, indent=4)

# funcția principală a scriptului
def main(imaginedirector, outputfile):
    # apelarea funcției pentru clasificarea imaginilor și obținerea rezultatelor
    cul, imaginescor = clasificareimagini(imaginedirector)
    # salvarea rezultatelor într-un fișier JSON
    salvarejson(cul, imaginescor, outputfile)
    print(f"Rezultatul salvat în {outputfile}")

# verificarea dacă scriptul este rulat direct
if __name__ == "__main__":
    # input de la utilizator pentru directorul imaginilor
    imaginedirector = input("Introduceți directorul imaginilor: ")
    # numele fișierului în care se vor salva rezultatele
    outputfile = "culorimagine.json"
    # apelarea funcției principale cu directorul imaginilor și numele fișierului de ieșire
    main(imaginedirector, outputfile)

