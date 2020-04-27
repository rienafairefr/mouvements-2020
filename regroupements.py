import json
from csv import DictReader


regroupements = []
circonscriptions_map = {}

with open('src/assets/mouvements.json') as mouvements_json:
    mouvements = json.load(mouvements_json)
    for mouvement in mouvements:
        circonscription = mouvement['CIRCONSCRIPTION']
        circonscriptions_map.setdefault(circonscription, set()).add(mouvement['COMMUNE'])

with open('Liste_geo.csv') as liste_geo_csv:
    reader = DictReader(liste_geo_csv)
    list_geo = list(reader)
    for geo in list_geo:
        geo['N°POSTE'] = int(geo['N°POSTE'].strip())
        if geo.get('CIRCONSCRIPTIONS CORRESPONDANTES'):
            circonscriptions = [c.strip() for c in geo.get('CIRCONSCRIPTIONS CORRESPONDANTES').split('/')]

            cities = [el for c in circonscriptions for el in circonscriptions_map[c]]

            regroupements.append(
                {'name': geo['REGROUPEMENTS'], 'circonscriptions': circonscriptions, 'cities': cities}
            )

    with open('src/assets/mouvements_geo.json', 'w') as mouvements_geo_json:
        json.dump(list_geo, mouvements_geo_json, indent=2)


with open('src/assets/regroupements.json', 'w') as regroupements_json:
    json.dump(regroupements, regroupements_json, indent=2)
