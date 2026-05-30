#!/usr/bin/env python3
"""Process fanart submission: download from Imgur URL, compress to .jpg, save locally"""
import json
import os
import sys
import re
import uuid
from PIL import Image
from io import BytesIO
import urllib.request

def process_fanart(image_url, title, artist, description, artist_link=""):
    """Download an image from a URL, compress to JPEG, save to assets/fanart/"""
    
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dst_dir = os.path.join(script_dir, "assets", "fanart")
    os.makedirs(dst_dir, exist_ok=True)
    
    # Download image from URL
    try:
        req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0 (Team Throw Bot)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            image_bytes = r.read()
            print(f"Downloaded {len(image_bytes)/1024:.0f}KB from {image_url}")
    except Exception as e:
        print(f"ERROR: Failed to download image: {e}")
        return None
    
    # Open with Pillow
    try:
        img = Image.open(BytesIO(image_bytes))
    except Exception as e:
        print(f"ERROR: Failed to open image: {e}")
        return None
    
    # Convert to RGB (saving as JPEG)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (13, 13, 13))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[3])
        else:
            background.paste(img)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Generate unique filename
    file_id = uuid.uuid4().hex[:12]
    safe_title = re.sub(r'[^a-zA-Z0-9]+', '_', title)[:30]
    filename = f"{safe_title}_{file_id}.jpg"
    filepath = os.path.join(dst_dir, filename)
    
    # Compress and save as JPEG (quality 85, optimized)
    img.save(filepath, 'JPEG', quality=85, optimize=True)
    
    file_size_kb = os.path.getsize(filepath) / 1024
    print(f"Saved: {filename} ({file_size_kb:.1f}KB) - original size: {img.size}")
    
    # Build relative URL for the site
    relative_url = f"assets/fanart/{filename}"
    
    # Update fanarts.json
    json_path = os.path.join(script_dir, "fanarts.json")
    
    try:
        with open(json_path) as f:
            fanarts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        fanarts = []
    
    entry = {
        "id": file_id,
        "title": title,
        "artist": artist,
        "artistLink": artist_link,
        "description": description,
        "image": relative_url,
        "date": __import__('datetime').datetime.now().isoformat()
    }
    fanarts.append(entry)
    
    with open(json_path, 'w') as f:
        json.dump(fanarts, f, indent=2)
    
    print(f"fanarts.json updated: {len(fanarts)} total entries")
    return entry


if __name__ == "__main__":
    # CLI usage: python3 process-fanart.py <image_url> <title> <artist> [description] [artist_link]
    if len(sys.argv) < 4:
        print("Usage: python3 process-fanart.py <image_url> <title> <artist> [description] [artist_link]")
        print("  image_url: direct link to image (e.g. https://i.imgur.com/abcd123.jpg)")
        sys.exit(1)
    
    image_url = sys.argv[1]
    title = sys.argv[2]
    artist = sys.argv[3]
    description = sys.argv[4] if len(sys.argv) > 4 else ""
    artist_link = sys.argv[5] if len(sys.argv) > 5 else ""

    # Debug: dump all args
    print(f"DEBUG: received {len(sys.argv)} args:")
    for i, a in enumerate(sys.argv):
        print(f"  sys.argv[{i}] = {repr(a)}")

    if not image_url:
        print("ERROR: image URL is empty! Check that the Worker is forwarding the 'image' field in client_payload.")
        sys.exit(1)
    
    result = process_fanart(image_url, title, artist, description, artist_link)
    if result:
        print(f"\nDone! Artwork '{title}' by {artist} added.")
    else:
        sys.exit(1)
