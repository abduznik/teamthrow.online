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
bonus_stat = sys.argv[6] if len(sys.argv) > 6 else os.environ.get('INPUT_BONUS_STAT', '')
bonus_label = sys.argv[7] if len(sys.argv) > 7 else os.environ.get('INPUT_BONUS_LABEL', '')
specialty = sys.argv[8] if len(sys.argv) > 8 else os.environ.get('INPUT_SPECIALTY', '')

heroes = [
    {"name":"Baptiste","img":"assets/heroes/render/render_Baptiste.webp"},
    {"name":"Orisa","img":"assets/heroes/render/render_Orisa.webp"},
    {"name":"Mei","img":"assets/heroes/render/render_Mei.webp"},
    {"name":"Hanzo","img":"assets/heroes/render/render_Hanzo.webp"},
    {"name":"Mercy","img":"assets/heroes/render/render_Mercy.webp"},
    {"name":"Reinhardt","img":"assets/heroes/render/render_Reinhardt.webp"},
    {"name":"Sombra","img":"assets/heroes/render/render_Sombra.webp"},
    {"name":"Tracer","img":"assets/heroes/render/render_Tracer.webp"},
    {"name":"Zenyatta","img":"assets/heroes/render/render_Zenyatta.webp"},
]
pick = random.choice(heroes)

bonus_labels = [
    'Headshots (Career)',
    'Flashbang Hit Rate',
    'Riptire Suicide Rate',
    'I Need Healing Spam',
    'TP to Cliff/Game',
    'Seconds on Point',
    'Teammate Avoids',
    'Match Chat Bans',
    'Ultimates Wasted',
    'Times Blamed Supports',
    'Suicides per Game',
    'Walls Bumped Into',
    'Ults into Walls',
    'GG EZ After Loss',
]
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
    'bonusStat': bonus_stat or '???',
    'bonusLabel': bonus_label or random.choice(bonus_labels),
    'specialty': specialty or random.choice(specialties)
}

recruits.append(new_recruit)

with open('recruits.json', 'w') as f:
    json.dump(recruits, f, indent=2)

print(f'Added {tag} as {pick["name"]} ({role})')
