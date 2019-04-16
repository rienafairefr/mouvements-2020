import json

regroupements = json.load(open('src/assets/regroupements.json', 'r'))

new_regroupements = {}
for regr in regroupements:
    for key, value in regr.items():
        new_regroupements.setdefault(key, {'name': key, 'cities': [], 'circonscriptions': None})
        if value == '':
            continue
        if value.startswith('Circonscription'):
            new_regroupements[key]['circonscriptions'] = list(m.strip() for m in value.split('\n')[1:])
        else:
            new_regroupements[key]['cities'].append(value)

json.dump(list(new_regroupements.values()), open('src/assets/regroupements.json', 'w'), indent=2)
