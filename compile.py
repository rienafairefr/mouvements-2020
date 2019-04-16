import json

mouvements = json.load(open('src/assets/mouvements.json', 'r'))

sigles = list({m['SIGLE'] for m in mouvements})
circonscriptions = list({m['CIRCONSCRIPTION'] for m in mouvements})

json.dump(sigles, open('src/assets/sigles.json', 'w'))
json.dump(circonscriptions, open('src/assets/circonscriptions.json', 'w'))
