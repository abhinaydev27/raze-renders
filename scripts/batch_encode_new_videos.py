#!/usr/bin/env python3
"""
Batch encode user's new video portfolio assets with high visual quality and fast-start streaming headers.
"""

import os
import subprocess

SRC_DIR = "/Users/abhinay/Downloads"
DEST_VIDEOS = "/Users/abhinay/Documents/Project/Portfolio websitee/assets/videos"
DEST_IMAGES = "/Users/abhinay/Documents/Project/Portfolio websitee/assets/images"

os.makedirs(DEST_VIDEOS, exist_ok=True)
os.makedirs(DEST_IMAGES, exist_ok=True)

tasks = [
    {
        "src": os.path.join(SRC_DIR, "sample4-2.mp4"),
        "dest_vid": os.path.join(DEST_VIDEOS, "reel-02.mp4"),
        "dest_img": os.path.join(DEST_IMAGES, "reel-02-poster.jpg"),
        "time_poster": "00:00:04",
        "scale": None,
        "name": "Meta Ad Creative (Reel 02)"
    },
    {
        "src": os.path.join(SRC_DIR, "Halkenburg Dies.mp4"),
        "dest_vid": os.path.join(DEST_VIDEOS, "reel-03.mp4"),
        "dest_img": os.path.join(DEST_IMAGES, "reel-03-poster.jpg"),
        "time_poster": "00:00:03",
        "scale": None,
        "name": "Anime Explainer Short (Reel 03)"
    },
    {
        "src": os.path.join(SRC_DIR, "myiwk sub.mp4"),
        "dest_vid": os.path.join(DEST_VIDEOS, "film-03.mp4"),
        "dest_img": os.path.join(DEST_IMAGES, "film-03-poster.jpg"),
        "time_poster": "00:00:05",
        "scale": None,
        "name": "B2B Ad Creative (Film 03)"
    },
    {
        "src": os.path.join(SRC_DIR, "Bharat Ke Veer- Atal Bihari Vajpayee- Biography.mp4"),
        "dest_vid": os.path.join(DEST_VIDEOS, "doc-atal.mp4"),
        "dest_img": os.path.join(DEST_IMAGES, "doc-atal-poster.jpg"),
        "time_poster": "00:00:08",
        "scale": "scale=1920:1080",
        "name": "Bharat Ke Veer Documentary"
    }
]

for t in tasks:
    print(f"\n==========================================")
    print(f"🎬 Processing: {t['name']}")
    
    # 1. Extract poster thumbnail
    cmd_img = f'ffmpeg -y -ss {t["time_poster"]} -i "{t["src"]}" -vframes 1 -q:v 2 "{t["dest_img"]}"'
    subprocess.run(cmd_img, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"📸 Poster extracted: {os.path.basename(t['dest_img'])}")

    # 2. Encode video with faststart
    vf = f'-vf "{t["scale"]}"' if t["scale"] else ""
    cmd_vid = f'ffmpeg -y -i "{t["src"]}" {vf} -c:v libx264 -crf 21 -preset fast -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "{t["dest_vid"]}"'
    print(f"⚙️ Encoding: {os.path.basename(t['dest_vid'])}...")
    res = subprocess.run(cmd_vid, shell=True)
    if res.returncode == 0:
        print(f"✅ Finished: {os.path.basename(t['dest_vid'])}")
    else:
        print(f"❌ Error encoding {t['name']}")

print("\n🎉 Batch processing complete!")
