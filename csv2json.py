import csv
import json
import os

with open('Liste.csv') as liste:
    reader = csv.DictReader(liste)

    data = []
    for datum in reader:
        new_datum = {}
        for k, v in datum.items():
            new_datum[k] = v.strip()

        new_datum['Nb Postes Vacants'] = int(float(new_datum['Nb Postes Vacants'])) if new_datum['Nb Postes Vacants'] else 0
        new_datum['Quotité'] = int(float(new_datum['Quotité'])) if new_datum['Quotité'] else 0
        new_datum['N°POSTE'] = int(new_datum['N°POSTE'])
        new_datum['N°POSTE'] = int(new_datum['N°POSTE'])
        data.append(new_datum)

with open('public/mouvements.json"', 'w') as mouvements_json_file:
    json.dump(data, mouvements_json_file, indent=2)
