#!/usr/bin/env python3
"""Process fanart submission: compress image to .jpg and save to assets/fanart/"""
import json
import os
import sys
from PIL import Image
from io import BytesIO
import base64
import re
import uuid

def process_fanart(image_data_url, title, artist, description, artist_link=""):
    """Compress a base64 image to .jpg and save metadata to fanarts.json"""
    
    dst_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fanart")
    os.makedirs(dst_dir, exist_ok=True)
    
    # Decode base64 image
    match = re.match(r'data:image/(\w+);base64,(.+)', image_data_url)
    if not match:
        print("ERROR: Invalid image data URL")
        return None
    
    ext = match.group(1)
    base64_data = match.group(2)
    image_bytes = base64.b64decode(base64_data)
    
    # Open with Pillow
    img = Image.open(BytesIO(image_bytes))
    
    # Convert to RGB (saving as JPEG)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create white background for transparency
        background = Image.new('RGB', img.size, (13, 13, 13))  # near-black to match site
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
    print(f"Saved: {filename} ({filepath}) - {file_size_kb:.1f}KB")
    print(f"  Original size: {img.size}")
    print(f"  Mode: {img.mode}")
    
    # Build relative URL for the site
    relative_url = f"assets/fanart/{filename}"
    
    # Update fanarts.json
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fanarts.json")
    
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
    # CLI usage: python3 process-fanart.py <image_base64_file> <title> <artist> [description] [artist_link]
    if len(sys.argv) < 4:
        print("Usage: python3 process-fanart.py <image_base64_file> <title> <artist> [description] [artist_link]")
        print("  image_base64_file: path to file containing the base64 data URL")
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        image_data = f.read().strip()
    
    title = sys.argv[2]
    artist = sys.argv[3]
    description = sys.argv[4] if len(sys.argv) > 4 else ""
    artist_link = sys.argv[5] if len(sys.argv) > 5 else ""
    
    result = process_fanart(image_data, title, artist, description, artist_link)
    if result:
        print(f"\nDone! Artwork '{title}' by {artist} added.")
    else:
        sys.exit(1)
