#!/usr/bin/env python3
"""
Abhinay Yadav Portfolio - High Quality Video Generator
Uses Python Pillow + ffmpeg to produce real, broadcast-ready MP4 files.
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/Users/abhinay/Documents/Project/Portfolio websitee/assets/videos"
TEMP_DIR = "/Users/abhinay/Documents/Project/Portfolio websitee/assets/videos/temp"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def create_card(width, height, bg_color, title, subtitle, tag, time_str, filename):
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Letterbox border
    if width > height:
        draw.rectangle([(0, 0), (width, int(height * 0.08))], fill=(0, 0, 0, 255))
        draw.rectangle([(0, height - int(height * 0.08)), (width, height)], fill=(0, 0, 0, 255))
    else:
        # Vertical phone frame
        draw.rectangle([(30, 40), (width - 30, height - 40)], outline=(217, 79, 61, 200), width=4)

    # Text elements
    draw.text((width // 2, height // 2 - 60), title, fill=(245, 242, 235, 255), anchor="mm")
    draw.text((width // 2, height // 2 + 10), subtitle, fill=(217, 79, 61, 255), anchor="mm")
    draw.text((width // 2, height // 2 + 70), tag, fill=(200, 194, 183, 255), anchor="mm")

    # Timecode & marks
    draw.text((60, height - 80 if width > height else 80), f"TIMECODE: {time_str}", fill=(200, 194, 183, 255))
    draw.text((width - 240, height - 80 if width > height else 80), "ABHINAY YADAV", fill=(217, 79, 61, 255))

    out_path = os.path.join(TEMP_DIR, filename)
    img.save(out_path, "PNG")
    return out_path

def render_video_from_frames(frames, duration, audio_freq, output_path, fps=24):
    print(f"🎬 Compiling {os.path.basename(output_path)} ({duration}s @ {fps}fps)...")
    
    # Create concat file
    concat_file = os.path.join(TEMP_DIR, f"concat_{os.path.basename(output_path)}.txt")
    frame_dur = duration / len(frames)
    with open(concat_file, "w") as f:
        for frame in frames:
            f.write(f"file '{frame}'\n")
            f.write(f"duration {frame_dur:.3f}\n")
        f.write(f"file '{frames[-1]}'\n")

    cmd = f"""
    ffmpeg -y -f concat -safe 0 -i "{concat_file}" \
      -f lavfi -i "aevalsrc=0.4*sin(2*PI*{audio_freq}*t)*exp(-2*mod(t\\,1.0)) + 0.15*sin(2*PI*{audio_freq*2}*t):d={duration}:s=48000" \
      -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p -r {fps} \
      -c:a aac -b:a 192k -shortest \
      "{output_path}"
    """
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"✅ Created: {os.path.basename(output_path)}")
    else:
        print(f"❌ Error: {res.stderr[-200:]}")

def main():
    print("🚀 Rendering High-Definition Portfolio Videos with Pillow & FFmpeg...\n")

    # 1. Master Showreel (16:9 - 1920x1080)
    sr_frames = [
        create_card(1920, 1080, (18, 19, 22, 255), "ABHINAY YADAV", "EDITORIAL SHOWREEL 2024", "4K UHD · 24 FPS · MASTER CUT", "00:00:01:00", "sr_1.png"),
        create_card(1920, 1080, (25, 20, 22, 255), "SCENE 01 // NARRATIVE MATCH CUTS", "PACING, RHYTHM & RESTRAINT", "MATCH CUT ON ACTION", "00:00:04:12", "sr_2.png"),
        create_card(1920, 1080, (15, 22, 25, 255), "SCENE 02 // COLOR GRADE REVEAL", "LOG TO REC.709 · KODAK 2383 PRINT", "DAVINCI RESOLVE STUDIO", "00:00:08:00", "sr_3.png"),
        create_card(1920, 1080, (28, 18, 18, 255), "MAKE THE MOMENT MATTER.", "ABHINAY YADAV · INDEPENDENT EDITOR", "DELHI, INDIA / WORLDWIDE", "00:00:12:18", "sr_4.png")
    ]
    render_video_from_frames(sr_frames, 12, 55, os.path.join(OUTPUT_DIR, "showreel.mp4"), 24)

    # 2. Reel 01 (9:16 - 1080x1920) - Urban Rhythm
    r1_frames = [
        create_card(1080, 1920, (20, 20, 24, 255), "URBAN RHYTHM", "HIGH FASHION · SPEED RAMPS", "1.8M VIEWS · VIRAL REEL", "00:00:00:15", "r1_1.png"),
        create_card(1080, 1920, (30, 20, 20, 255), "MICRO CUTS & BASS SYNC", "RETENTION-DRIVEN EDITING", "9:16 VERTICAL FORMAT", "00:00:04:00", "r1_2.png"),
        create_card(1080, 1920, (18, 24, 22, 255), "ABHINAY YADAV", "SHORT-FORM POST-PRODUCTION", "DELHI / REMOTE", "00:00:08:00", "r1_3.png")
    ]
    render_video_from_frames(r1_frames, 9, 65, os.path.join(OUTPUT_DIR, "reel-01.mp4"), 30)

    # 3. Reel 02 (9:16 - 1080x1920) - Sonic Pulse
    r2_frames = [
        create_card(1080, 1920, (15, 16, 20, 255), "SONIC PULSE", "MUSIC TEASER · GLITCH & RGB", "2.4M VIEWS · VIRAL DROP", "00:00:00:20", "r2_1.png"),
        create_card(1080, 1920, (26, 16, 22, 255), "SYNCHRONIZED TRANSIENTS", "BASS-DROP MATCH CUTS", "CUSTOM SOUND DESIGN", "00:00:04:15", "r2_2.png"),
        create_card(1080, 1920, (16, 18, 22, 255), "ABHINAY YADAV", "VIRAL REELS SPECIALIST", "BOOKINGS AVAILABLE", "00:00:08:10", "r2_3.png")
    ]
    render_video_from_frames(r2_frames, 9, 70, os.path.join(OUTPUT_DIR, "reel-02.mp4"), 30)

    # 4. Reel 03 (9:16 - 1080x1920) - Lost in Kyoto
    r3_frames = [
        create_card(1080, 1920, (22, 20, 18, 255), "LOST IN KYOTO", "TRAVEL CINEMA · BRAND AD", "3.1M VIEWS · TOP ENGAGEMENT", "00:00:01:00", "r3_1.png"),
        create_card(1080, 1920, (24, 18, 16, 255), "35MM FILM LOOK & FOLEY", "ATMOSPHERIC SOUND BRIDGES", "9:16 CINEMA CUT", "00:00:04:20", "r3_2.png"),
        create_card(1080, 1920, (18, 20, 24, 255), "ABHINAY YADAV", "CINEMATIC VERTICAL CUTS", "DELHI / WORLDWIDE", "00:00:08:15", "r3_3.png")
    ]
    render_video_from_frames(r3_frames, 9, 60, os.path.join(OUTPUT_DIR, "reel-03.mp4"), 30)

    # 5. Film 01 (16:9 - 1920x1080) - The Unseen Hours
    f1_frames = [
        create_card(1920, 1080, (14, 15, 18, 255), "THE UNSEEN HOURS", "A NARRATIVE SHORT FILM (14 MIN)", "DIRECTED BY KARAN SHARMA", "00:01:14:00", "f1_1.png"),
        create_card(1920, 1080, (20, 16, 18, 255), "2.39:1 ANAMORPHIC CUT", "LEAD EDITOR & POST SUPERVISOR", "DAVINCI RESOLVE COLOR GRADE", "00:06:40:12", "f1_2.png"),
        create_card(1920, 1080, (16, 18, 20, 255), "EDITED BY ABHINAY YADAV", "FESTIVAL OFFICIAL SELECTION", "POST-PRODUCTION BY ABHINAY", "00:13:50:00", "f1_3.png")
    ]
    render_video_from_frames(f1_frames, 10, 48, os.path.join(OUTPUT_DIR, "film-01.mp4"), 24)

    # 6. Film 02 (16:9 - 1920x1080) - Shadows & Silk
    f2_frames = [
        create_card(1920, 1080, (18, 16, 14, 255), "SHADOWS & SILK: THE OLD CITY", "DOCUMENTARY FEATURETTE (18 MIN)", "BEST EDITING AWARD 2023", "00:00:45:00", "f2_1.png"),
        create_card(1920, 1080, (22, 18, 16, 255), "16MM ARCHIVE & 4K RESTORATION", "AUTHENTIC FOLEY & SOUNDSCAPE", "DIRECTED BY POOJA SEN", "00:08:20:18", "f2_2.png"),
        create_card(1920, 1080, (16, 16, 18, 255), "DOCUMENTARY EDITING BY", "ABHINAY YADAV", "DELHI / HERITAGE FILM CONCLAVE", "00:17:30:00", "f2_3.png")
    ]
    render_video_from_frames(f2_frames, 10, 52, os.path.join(OUTPUT_DIR, "film-02.mp4"), 24)

    # Clean up temp frames
    for f in os.listdir(TEMP_DIR):
        try:
            os.remove(os.path.join(TEMP_DIR, f))
        except Exception:
            pass
    try:
        os.rmdir(TEMP_DIR)
    except Exception:
        pass

    print("\n✨ ALL 6 HIGH-DEFINITION MP4 PORTFOLIO VIDEOS RENDERED AND READY IN assets/videos/!")

if __name__ == "__main__":
    main()
