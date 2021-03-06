#!/usr/bin/env python3

import cgi
import copy
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
if 'draw' in arguments.keys():
    city = arguments.getvalue('draw')
    if city=='random':
        city = random.choice(game['packs'][-1])
    print('Drawing city: ' + city)
    game['discard'].append(city)
    game['packs'][-1].remove(city)

if 'infect' in arguments.keys():
    city = arguments.getvalue('infect')
    if city=='random':
        city = random.choice(game['packs'][0])
    print('Drawing city: ' + city)
    game['discard'].append(city)
    game['packs'][0].remove(city)

if 'intensify' in arguments.keys():
    game['packs'].append(copy.deepcopy(game['discard']))
    game['discard'] = []

if len(game['packs'][-1]) == 0:
    game['packs'].pop()
print("Pack has: " + str(sum([len(pack) for pack in game['packs']])) +
      ' cards.')
print()
print('Discards:')
print()
print(game['discard'])
print()

def percent(number):
    return str(100.0*number) + '%'

for city in game['cities']:
    name = city['name']
    top = percent(game['packs'][-1].count(name)/len(game['packs'][-1]))
    bottom = (game['packs'][-1].count(name)/len(game['packs'][-1]))
    print('{} {} {}'.format(name, top, bottom))

with open(FILE, 'w') as file_object:
    json.dump(game, file_object)
