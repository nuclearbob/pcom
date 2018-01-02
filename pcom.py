#!/usr/bin/env python3

import cgi
import json
import os
import random

import cgitb; cgitb.enable() # Optional; for debugging only

FILE='/usr/lib/cgi-bin/pcom/data.json'

colors = {
    'white': 0xFFFFFF,
    'blue': 0x0000FF,
    'yellow': 0xFFFF00,
    'black': 0x000000,
}

cities = []
cities.append({
    'name': 'New York',
    'color': 'blue',
    'count': 3,
})
cities.append({
    'name': 'Washington',
    'color': 'blue',
    'count': 3,
})
cities.append({
    'name': 'London',
    'color': 'blue',
    'count': 3,
})
cities.append({
    'name': 'Lagos',
    'color': 'yellow',
    'count': 3,
})
cities.append({
    'name': 'Sao Paolo',
    'color': 'yellow',
    'count': 3,
})
cities.append({
    'name': 'Jacksonville',
    'color': 'yellow',
    'count': 3,
})
cities.append({
    'name': 'Istanbul',
    'color': 'black',
    'count': 3,
})
cities.append({
    'name': 'Cairo',
    'color': 'black',
    'count': 3,
})
cities.append({
    'name': 'Tripoli',
    'color': 'black',
    'count': 3,
})

pack = []
for city in cities:
    for _ in range(city['count']):
        pack.append(city['name'])
packs = [pack]

discard = []

game = {
    'colors': colors,
    'cities': cities,
    'packs': packs,
    'discard': discard,
}

print('Content-type: text/plain')
print()

if os.path.isfile(FILE):
    try:
        with open(FILE, 'r') as file_object:
            game.update(json.load(file_object))
    except:
        pass

arguments = cgi.FieldStorage()
print(arguments)
print()
if 'draw' in arguments.keys():
    city = arguments.getvalue('draw')
    if city is '':
        city = random.choice(packs[-1])
    print('Drawing city:' + city)
    print()
    game['discard'].append(city)
    game['packs'][-1].remove(city)

if len(game['packs'][-1]) == 0:
    game['packs'].pop()
print("Pack has: " + str(sum([len(pack) for pack in game['packs']])) +
      ' cards.')
print()
print(game['packs'])
print()
print(game['discard'])
print()

with open(FILE, 'w') as file_object:
    json.dump(game, file_object)
