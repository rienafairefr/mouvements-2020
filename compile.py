import json

with open('src/assets/mouvements.json', 'r') as mouvements_json, \
        open('src/assets/sigles.json', 'w') as sigles_json, \
        open('src/assets/circonscriptions.json', 'w') as circonscriptions_json:
    mouvements = json.load(mouvements_json)
    json.dump(list({m['SIGLE'] for m in mouvements}), sigles_json, indent=2)
    json.dump(list({m['CIRCONSCRIPTION'] for m in mouvements}), circonscriptions_json, indent=2)
