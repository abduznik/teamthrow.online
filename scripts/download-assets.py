#!/usr/bin/env python3
"""Download all Overwatch hero renders and icons to local assets"""
import urllib.request
import os

HEROES_RENDERS = {
    "Ana": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/5/5e/OW2_Ana.png/revision/latest?cb=20241102141052",
    "Ashe": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/8/89/OW2_Ashe.png/revision/latest?cb=20250329135344",
    "Baptiste": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/0/00/OW2_Baptiste.png/revision/latest?cb=20241108201237",
    "Bastion": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/5/51/OW2_Bastion.png/revision/latest?cb=20221005165909",
    "Brigitte": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/8/83/OW2_Brigitte.png/revision/latest?cb=20220930191642",
    "Cassidy": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/a/a0/OW2_Cassidy.png/revision/latest?cb=20241108201305",
    "D.Va": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/1a/OW2_Dva.png/revision/latest?cb=20241108201346",
    "Doomfist": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/1e/OW2_Doomfist_render.png/revision/latest?cb=20241102135923",
    "Genji": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/17/OW2_Genji.png/revision/latest?cb=20241102133634",
    "Hanzo": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/6/66/OW2_Hanzo.png/revision/latest?cb=20241220134913",
    "Junkrat": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/f/f2/OW2_Junkrat.png/revision/latest?cb=20260214122743",
    "Mei": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/7/7e/OW2_Mei.png/revision/latest?cb=20241102134134",
    "Mercy": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/11/OW2_Mercy.png/revision/latest?cb=20241102143122",
    "Orisa": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/3/34/OW2_Orisa.png/revision/latest?cb=20240404155812",
    "Reaper": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/8/8c/OW2_Reaper.png/revision/latest?cb=20241108201455",
    "Reinhardt": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/2/27/OW2_Reinhardt.png/revision/latest?cb=20220409014723",
    "Roadhog": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/3/34/OW2_Roadhog.png/revision/latest?cb=20260213114356",
    "Sigma": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/c/c9/OW2_Sigma.png/revision/latest?cb=20240404193956",
    "Sojourn": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/a/ae/OW2_Sojourn.png/revision/latest?cb=20240928162620",
    "Soldier: 76": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/b/bf/OW2_S76.png/revision/latest?cb=20260208153542",
    "Sombra": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/d/d7/OW2_Sombra.png/revision/latest?cb=20241108201559",
    "Symmetra": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/5/51/OW2_Symmetra.png/revision/latest?cb=20240130124019",
    "Tracer": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/6/63/OW2_Tracer.png/revision/latest?cb=20241102134907",
    "Widowmaker": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/a/ab/OW2_Widowmaker.png/revision/latest?cb=20241108201530",
    "Winston": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/3/39/OW2_Winston.png/revision/latest?cb=20241102142153",
    "Zarya": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/0/02/OW2_Zarya.png/revision/latest?cb=20241108201623",
    "Zenyatta": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/4/44/OW2_Zenyatta.png/revision/latest?cb=20260324055645",
}

ICONS = {
    "Ana": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/3/3d/Icon-Ana.png/revision/latest?cb=20221005160847",
    "Ashe": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/b/be/Icon-Ashe.png/revision/latest?cb=20221005165904",
    "Baptiste": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/f/fb/Icon-Baptiste.png/revision/latest?cb=20221005160910",
    "Bastion": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/5/51/Icon-Bastion.png/revision/latest?cb=20221005165909",
    "Brigitte": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/a/a6/Icon-Brigitte.png/revision/latest?cb=20221005160917",
    "Cassidy": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/0/05/Icon-Cassidy.png/revision/latest?cb=20221005165914",
    "D.Va": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/19/Icon-D.Va.png/revision/latest?cb=20221005161600",
    "Doomfist": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/a/a1/Icon-Doomfist.png/revision/latest?cb=20221005161638",
    "Genji": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/1c/Icon-Genji.png/revision/latest?cb=20221005165931",
    "Hanzo": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/7/71/Icon-Hanzo.png/revision/latest?cb=20221005165925",
    "Junkrat": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/9/99/Icon-Junkrat.png/revision/latest?cb=20221005170201",
    "Mei": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/9/99/Icon-Mei.png/revision/latest?cb=20221005170206",
    "Mercy": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/0/03/Icon-Mercy.png/revision/latest?cb=20221005160926",
    "Orisa": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/11/Icon-Orisa.png/revision/latest?cb=20221005161652",
    "Reaper": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/a/a9/Icon-Reaper.png/revision/latest?cb=20221005170219",
    "Reinhardt": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/8/83/Icon-Reinhardt.png/revision/latest?cb=20221005161659",
    "Roadhog": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/16/Icon-Roadhog.png/revision/latest?cb=20221005161706",
    "Sigma": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/e/e0/Icon-Sigma.png/revision/latest?cb=20221005161714",
    "Sojourn": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/e/e0/Icon-Sojourn.png/revision/latest?cb=20221005170226",
    "Soldier: 76": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/1/10/Icon-Soldier76.png/revision/latest?cb=20221005170231",
    "Sombra": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/7/70/Icon-Sombra.png/revision/latest?cb=20221005170556",
    "Symmetra": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/0/06/Icon-Symmetra.png/revision/latest?cb=20221005170604",
    "Tracer": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/2/29/Icon-Tracer.png/revision/latest?cb=20221005170620",
    "Widowmaker": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/5/54/Icon-Widowmaker.png/revision/latest?cb=20221005170629",
    "Winston": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/f/f8/Icon-Winston.png/revision/latest?cb=20221005161721",
    "Zarya": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/7/75/Icon-Zarya.png/revision/latest?cb=20221005161732",
    "Zenyatta": "https://static.wikia.nocookie.net/overwatch_gamepedia/images/f/f7/Icon-Zenyatta.png/revision/latest?cb=20221005160943",
}

RENDER_DIR = "F:/Coding/teamthrow.online/assets/heroes/render"
ICON_DIR = "F:/Coding/teamthrow.online/assets/heroes/icon"
os.makedirs(RENDER_DIR, exist_ok=True)
os.makedirs(ICON_DIR, exist_ok=True)

def download(url, dest_dir, name):
    safe_name = name.replace(":", "_").replace(" ", "_").replace("/", "_")
    existing = [f for f in os.listdir(dest_dir) if f.startswith(safe_name)]
    if existing:
        print(f"  SKIP {name} (exists)")
        return os.path.join(dest_dir, existing[0])
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            ct = r.headers.get("Content-Type", "")
            if "webp" in ct:
                ext = ".webp"
            elif "png" in ct:
                ext = ".png"
            elif "jpeg" in ct or "jpg" in ct:
                ext = ".jpg"
            else:
                ext = ".png"
            fname = safe_name + ext
            path = os.path.join(dest_dir, fname)
            with open(path, "wb") as f:
                f.write(data)
            print(f"  OK {fname} ({len(data)/1024:.0f}KB)")
            return path
    except Exception as e:
        print(f"  FAIL {name}: {e}")
        return None

print("=== Renders ===")
for name, url in sorted(HEROES_RENDERS.items()):
    download(url, RENDER_DIR, f"render_{name}")

print("\n=== Icons ===")
for name, url in sorted(ICONS.items()):
    download(url, ICON_DIR, f"icon_{name}")

print("\nDone!")
