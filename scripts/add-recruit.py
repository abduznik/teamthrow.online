#!/usr/bin/env python3
"""GitHub Action helper: add a new recruit to recruits.json"""
import json
import random
import os
import sys

tag = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('INPUT_TAG', 'Unknown')
role = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('INPUT_ROLE', 'DPS')

win_rate = int(sys.argv[3]) if len(sys.argv) > 3 else random.randint(1, 5)
deaths = int(sys.argv[4]) if len(sys.argv) > 4 else random.randint(12, 26)
kda = float(sys.argv[5]) if len(sys.argv) > 5 else round(random.random() * 0.3, 2)

heroes = [
    {"name":"Baptiste","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/f/fb/Icon-Baptiste.png/revision/latest?cb=20221005160910"},
    {"name":"Orisa","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/11/Icon-Orisa.png/revision/latest?cb=20221005161652"},
    {"name":"Mei","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/9/99/Icon-Mei.png/revision/latest?cb=20221005170206"},
    {"name":"Hanzo","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/7/71/Icon-Hanzo.png/revision/latest?cb=20221005165925"},
    {"name":"Mercy","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/0/03/Icon-Mercy.png/revision/latest?cb=20221005160926"},
    {"name":"Reinhardt","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/8/83/Icon-Reinhardt.png/revision/latest?cb=20221005161659"},
    {"name":"Sombra","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/7/70/Icon-Sombra.png/revision/latest?cb=20221005170556"},
    {"name":"Tracer","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/2/29/Icon-Tracer.png/revision/latest?cb=20221005170620"},
    {"name":"Zenyatta","img":"https://static.wikia.nocookie.net/overwatch_gamepedia/images/f/f7/Icon-Zenyatta.png/revision/latest?cb=20221005160943"},
]
pick = random.choice(heroes)

specialties = [
    'Fresh meat, still learning to feed',
    'Promising thrower, needs seasoning',
    'Natural talent for underperformance',
    'Consistently inconsistent',
    'Master of the accidental feed',
    'Ultimate economy: always wasted',
    'Positionally challenged',
    'Professional stagger artist',
    'Gold damage (to his own team)',
    'World record: most deaths per minute',
]

try:
    with open('recruits.json') as f:
        recruits = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    recruits = []

new_recruit = {
    'tag': tag,
    'role': role,
    'hero': pick['name'],
    'heroImg': pick['img'],
    'winRate': f'{win_rate}%',
    'deaths': str(deaths),
    'kda': f'{kda:.2f}',
    'bonusStat': '???',
    'bonusLabel': 'Seriously?',
    'specialty': random.choice(specialties)
}

recruits.append(new_recruit)

with open('recruits.json', 'w') as f:
    json.dump(recruits, f, indent=2)

print(f'Added {tag} as {pick["name"]} ({role})')
