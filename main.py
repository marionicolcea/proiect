import os
import cv2
import json
from collections import defaultdict
def analizaculori(caleimagine):
# incărcarea imaginii utilizând OpenCV
    imagine = cv2.imread(caleimagine)
    # verigicarea dacă imaginea a fost încărcată corect
    if imagine is None:
        raise ValueError(f"nu s-a putut acesa imaginea: {caleimagine}")
# clcularea valorii medii pentru fiecare componentă de culoare
    mean_b, mean_g, mean_r = cv2.mean(imagine)[:3]
    return {'rosu': mean_r, 'verde': mean_g, 'albastru': mean_b}
# vlasificarea imaginilor în funcție de culorile predominante
def clasificareimagini(imaginedirector):
    # ceraerea unui dicționar pentru a stoca imaginile clasificate pe culori
    cul = {'rosu': [], 'verde': [], 'albastru': []}
    # crearea unui dicționar pentru aa stoca scorurole culorilor pentru fiecare imagine
    imaginescor = defaultdict(dict)
    for numeimagine in os.listdir(imaginedirector):
        caleimagine = os.path.join(imaginedirector, numeimagine)
        if os.path.isfile(caleimagine):
            try:
                # anAliza culorilor pentru imaginea curentă
                scor = analizaculori(caleimagine)
                # Adăugarea scorului la diionarul imaginescor
                imaginescor[numeimagine] = scor
                # determinarea culroii predominante pentru imagine
                culpre = max(scor, key=scor.get)
                #adăugarea numelui imaginii la lista culorii predominante
                cul[culpre].append(numeimagine)
            except ValueError as e:
                print(e)
    return cul, imaginescor

#salvarea rezultatelor într-un fișier JSON
def salvarejson(cul, imaginescor, outputfile):
    results = {
        'grupuri_culri': cul,
        'scorurile imaginilor': imaginescor
    }
    # salvarea dicționarului într-un fișier JSON
    with open(outputfile, 'w') as json_file:
        json.dump(results, json_file, indent=4)
def main(imaginedirector, outputfile):
    #clasificsrea imaginilor și obținerea rezultatelor
    cul, imaginescor = clasificareimagini(imaginedirector)
    salvarejson(cul, imaginescor, outputfile)
    print(f"Rezultatul salvat în {outputfile}")
if __name__ == "__main__":
    # input de la utilizator pentru directprul imaginilor
    imaginedirector = input("Introduceți drectorul imaginilor: ")
    # numele fișierului în care se vor salva rezultatele
    outputfile = "culorimagine.json"
    main(imaginedirector, outputfile)

