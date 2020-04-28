import json

with open('public/json/mouvements.json', 'r') as mouvements_json, \
        open('public/json/sigles.json', 'w') as sigles_json, \
        open('public/json/circonscriptions.json', 'w') as circonscriptions_json:
    mouvements = json.load(mouvements_json)
    json.dump(list({m['SIGLE'] for m in mouvements}), sigles_json, indent=2)
    json.dump(list({m['CIRCONSCRIPTION'] for m in mouvements}), circonscriptions_json, indent=2)
