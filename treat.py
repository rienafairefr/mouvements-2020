import json
import os

import googlemaps
from dotenv import load_dotenv
from googlemaps.geocoding import geocode

load_dotenv()

gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))


with open('public/mouvements.json', 'r') as mouvements_json:
    mouvements = json.load(mouvements_json)

    for mouvement in mouvements:
        if 'geocode' not in mouvement:
            mouvement['geocode'] = geocode(gmaps, mouvement['ADRESSE'] + ' ' + mouvement['COMMUNE'], region='fr')
        geocode_result = mouvement['geocode']
        print(geocode_result)
        if 'geo' not in mouvement:
            if len(geocode_result) >= 1:
                mouvement['geo'] = geocode_result[0]['geometry']['location']
        else:
            if mouvement['geo']['lat'] is None or mouvement['geo']['lng'] is None:
                pass

with open('public/mouvements.json', 'w') as mouvements_json:
    json.dump(mouvements, mouvements_json, indent=4)
