import json


with open('public/json/mouvements.json', 'r') as mouvements_json:
    mouvements = json.load(mouvements_json)

    for mouvement in mouvements:
        try:
            jumelage = int(mouvement['OBSERVATIONS'].strip())
            mouvement['OBSERVATIONS'] = 'jumelé'
        except ValueError:
            pass

with open('public/json/mouvements.json', 'w') as mouvements_json:
    json.dump(mouvements, mouvements_json, indent=4)
