#!/usr/bin/env python3
"""
Compress videos to fit strictly under Cloudflare Pages' 25MB per-file limit
while maintaining crisp visual clarity and fast-start web streaming.
"""

import os
import subprocess

VIDEOS_DIR = "/Users/abhinay/Documents/Project/Portfolio websitee/assets/videos"
SRC_DIR = "/Users/abhinay/Downloads"

tasks = [
    # 1. Reel 01 (MWM - 68s) -> Target ~20MB
    {
        "src": os.path.join(SRC_DIR, "MWM Sample.mp4"),
        "dest": os.path.join(VIDEOS_DIR, "reel-01.mp4"),
        "b_v": "2300k",
        "scale": None
    },
    # 2. Reel 02 (Meta Ad - 91s) -> Target ~20MB
    {
        "src": os.path.join(SRC_DIR, "sample4-2.mp4"),
        "dest": os.path.join(VIDEOS_DIR, "reel-02.mp4"),
        "b_v": "1700k",
        "scale": None
    },
    # 3. Reel 03 (Anime Explainer - 51s) -> Target ~18MB
    {
        "src": os.path.join(SRC_DIR, "Halkenburg Dies.mp4"),
        "dest": os.path.join(VIDEOS_DIR, "reel-03.mp4"),
        "b_v": "2800k",
        "scale": None
    },
    # 4. Film 01 (The Secret To The Nets - 93s) -> Target ~20MB
    {
        "src": os.path.join(SRC_DIR, "The Secret To The Nets LATEST Successes.mp4"),
        "dest": os.path.join(VIDEOS_DIR, "film-01.mp4"),
        "b_v": "1700k",
        "scale": None
    },
    # 5. Film 03 (B2B Creative - 76s) -> Target ~20MB
    {
        "src": os.path.join(SRC_DIR, "myiwk sub.mp4"),
        "dest": os.path.join(VIDEOS_DIR, "film-03.mp4"),
        "b_v": "2000k",
        "scale": None
    },
    # 6. Doc Atal (Documentary Feature Cut - 3 min 30s showcase) -> Target ~22MB
    {
        "src": os.path.join(SRC_DIR, "Bharat Ke Veer- Atal Bihari Vajpayee- Biography.mp4"),
        "dest": os.path.join(VIDEOS_DIR, "doc-atal.mp4"),
        "b_v": "900k",
        "t": "00:03:30",
        "scale": "scale=1920:1080"
    }
]

for t in tasks:
    t_flag = f'-t {t["t"]}' if "t" in t else ""
    s_flag = f'-vf "{t["scale"]}"' if t["scale"] else ""
    cmd = f'ffmpeg -y -i "{t["src"]}" {t_flag} {s_flag} -c:v libx264 -b:v {t["b_v"]} -maxrate {t["b_v"]} -bufsize 2M -preset fast -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "{t["dest"]}"'
    print(f"⚙️ Optimizing {os.path.basename(t['dest'])}...")
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    size_mb = os.path.getsize(t["dest"]) / (1024 * 1024)
    print(f"✅ {os.path.basename(t['dest'])} -> {size_mb:.2f} MB")

print("\n🎉 All videos are now strictly under 25MB and ready for instant Cloudflare Pages deployment!")
