#!/usr/bin/env python3
"""Fetch YouTube channel RSS feed and save to youtube-videos.json"""
import json
import os
import xml.etree.ElementTree as ET
import urllib.request

CHANNEL_ID = "UCyZesfM1i6yY5lSDG9v7UVg"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(script_dir, "youtube-videos.json")

req = urllib.request.Request(FEED_URL, headers={"User-Agent": "TeamThrow-Bot"})
with urllib.request.urlopen(req, timeout=30) as r:
    xml_data = r.read()

root = ET.fromstring(xml_data)
ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}

videos = []
for entry in root.findall("atom:entry", ns):
    title = entry.find("atom:title", ns).text
    video_id = entry.find("yt:videoId", ns).text
    published = entry.find("atom:published", ns).text
    author = entry.find("atom:author/atom:name", ns).text
    link_el = entry.find("atom:link", ns)
    url = link_el.attrib.get("href", "") if link_el is not None else ""
    videos.append({
        "videoId": video_id,
        "title": title,
        "author": author,
        "url": url,
        "published": published
    })

with open(json_path, "w") as f:
    json.dump(videos, f, indent=2)

print(f"Saved {len(videos)} videos to youtube-videos.json")
