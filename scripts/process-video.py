#!/usr/bin/env python3
"""Process video submission: append metadata to videos.json"""
import json
import os
import sys
import uuid
from datetime import datetime


def detect_platform(url):
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    if "instagram.com" in url_lower:
        return "instagram"
    if "tiktok.com" in url_lower:
        return "tiktok"
    if "twitch.tv" in url_lower:
        return "twitch"
    if "twitter.com" in url_lower or "x.com" in url_lower:
        return "twitter"
    if "vimeo.com" in url_lower:
        return "vimeo"
    if "facebook.com" in url_lower or "fb.watch" in url_lower:
        return "facebook"
    return "other"


def process_video(title, uploader, url):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(script_dir, "videos.json")

    try:
        with open(json_path) as f:
            videos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        videos = []

    entry = {
        "id": uuid.uuid4().hex[:12],
        "title": title,
        "uploader": uploader,
        "url": url,
        "platform": detect_platform(url),
        "date": datetime.now().isoformat()
    }
    videos.append(entry)

    with open(json_path, 'w') as f:
        json.dump(videos, f, indent=2)

    print(f"videos.json updated: {len(videos)} total entries")
    print(f"Added: {title} by {uploader} ({entry['platform']})")
    return entry


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 process-video.py <title> <uploader> <url>")
        sys.exit(1)

    title = sys.argv[1]
    uploader = sys.argv[2]
    url = sys.argv[3]

    print(f"DEBUG: title={repr(title)}, uploader={repr(uploader)}, url={repr(url)}")

    result = process_video(title, uploader, url)
    if result:
        print(f"\nDone! Video '{title}' by {uploader} added.")
    else:
        sys.exit(1)
