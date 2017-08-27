import csv
import json
import roman

res = []

system_names = {}
system_sec = {}

special_planets = {
    'New Caldari Prime': 4,
    'Eon Prime': 3,
    'Ancient Gliese': 4,
    'Amarr Prime': 3,
    'Eyjafjallajokull II': 2
}

special_moons = {
    'Griklaeum': 1,
    'Black Viperia': 2,
    'Kileakum': 3,
}

planet_ids = {}

f = open('mapDenormalize.csv')
r = csv.DictReader(f)

for l in r:
    if l['groupID'] == '3':
        res.append({
            'pk': int(l['itemID']),
            'model': 'eve_sde.Region',
            'fields': {
                'name': l['itemName']
            }
        })
    elif l['groupID'] == '4':
        res.append({
            'pk': int(l['itemID']),
            'model': 'eve_sde.Constellation',
            'fields': {
                'name': l['itemName'],
                'region': int(l['regionID'])
            }
        })
    elif l['groupID'] == '5':
        res.append({
            'pk': int(l['itemID']),
            'model': 'eve_sde.SolarSystem',
            'fields': {
                'name': l['itemName'],
                'constellation': int(l['constellationID']),
                'security': float(l['security'])
            }
        })

        system_names[int(l['itemID'])] = l['itemName']
        system_sec[int(l['itemID'])] = float(l['security'])
    elif l['groupID'] == '7':
        if l['itemName'] in special_planets:
            s = special_planets[l['itemName']]
        else:
            trimmed = l['itemName'][len(system_names[int(l['solarSystemID'])]):].strip()
            s = roman.fromRoman(trimmed.split(' ')[0])

        res.append({
            'pk': int(l['itemID']),
            'model': 'eve_sde.Planet',
            'fields': {
                'system': int(l['solarSystemID']),
                'number': s
            }
        })

        planet_ids[l['itemName']] = int(l['itemID'])
    elif l['groupID'] == '8':
        s = l['itemName'].split(' - ')[0].strip()
        m = ' '.join(l['itemName'].split(' - ')[1].strip().split(' ')[1:])
        m = int(special_moons.get(m, m))

        res.append({
            'pk': int(l['itemID']),
            'model': 'eve_sde.Moon',
            'fields': {
                'planet': planet_ids[s],
                'number': m
            }
        })

print(json.dumps(res, indent=4))
