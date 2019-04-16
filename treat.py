import json

import googlemaps


gmaps = googlemaps.Client(key='AIzaSyB_1xuZiTbpyOs9-8r14spgzCm8P-Cj_XM')


data = json.load(open('src/assets/mouvements.json', 'r'))

for d in data:
    if 'geo' not in d:
        geocode_result = gmaps.geocode(d['ADRESSE'] + ' ' + d['COMMUNE'] + ' FRANCE')
        print(geocode_result)
        if len(geocode_result) >= 1:
            d['geo'] = geocode_result[0]['geometry']['location']
    else:
        if d['geo']['lat'] is None or d['geo']['lng'] is None:
            pass


# json.dump(data, open('src/assets/mouvements.json', 'w'), indent=4)


