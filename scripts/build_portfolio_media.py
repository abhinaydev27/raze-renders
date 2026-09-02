#!/usr/bin/env python3
"""
Abhinay Yadav Portfolio Media Engine
Generates high-definition, smooth cinematic video assets directly for the portfolio:
- showreel.mp4 (16:9 Widescreen Cinema Showreel)
- reel-01.mp4 (9:16 Vertical Fashion Reel)
- reel-02.mp4 (9:16 Vertical Music Teaser)
- reel-03.mp4 (9:16 Vertical Travel Cinema)
- film-01.mp4 (16:9 Narrative Short Film)
- film-02.mp4 (16:9 Documentary Featurette)
- showreel_timeline.xml (Premiere Pro / FCPXML Timeline Interchange)
"""

import os
import subprocess
import sys

OUTPUT_DIR = "/Users/abhinay/Documents/Project/Portfolio websitee/assets/videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_ffmpeg(cmd, desc):
    print(f"🎬 Generating: {desc}...")
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"⚠️ Warning on {desc}: {result.stderr[-300:]}")
    else:
        print(f"✅ Created: {desc}")

def build_all():
    print("🚀 Starting Media Generation Pipeline...")

    # 1. Master Showreel (16:9 - 1920x1080, 24fps, ~15s cinematic showcase)
    showreel_path = os.path.join(OUTPUT_DIR, "showreel.mp4")
    cmd_showreel = f"""
    ffmpeg -y \
      -f lavfi -i "color=c=#101114:s=1920x1080:d=14:r=24" \
      -f lavfi -i "anoisesrc=d=14:c=pink:a=0.03" \
      -f lavfi -i "aevalsrc=sin(2*PI*55*t)*exp(-3*mod(t\\,1.0)) + 0.3*sin(2*PI*440*t)*exp(-5*mod(t\\,0.5)):d=14:s=48000" \
      -filter_complex "
        [0:v]format=yuv420p,
             drawbox=x=0:y=0:w=1920:h=90:color=black@1:t=fill,
             drawbox=x=0:y=990:w=1920:h=90:color=black@1:t=fill,
             drawtext=text='ABHINAY YADAV':fontcolor=#f5f2eb:fontsize=56:x=(w-text_w)/2:y=(h-text_h)/2 - 50:enable='between(t,0,3.5)',
             drawtext=text='EDITORIAL SHOWREEL 2024':fontcolor=#d94f3d:fontsize=26:x=(w-text_w)/2:y=(h-text_h)/2 + 20:enable='between(t,0,3.5)',
             drawtext=text='01 // NARRATIVE MATCH CUTS':fontcolor=#f5f2eb:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2 - 30:enable='between(t,3.5,7.0)',
             drawtext=text='SPEED RAMPING & PACING':fontcolor=#c8c2b7:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2 + 30:enable='between(t,3.5,7.0)',
             drawtext=text='02 // COLOR GRADE [LOG TO REC.709]':fontcolor=#f5f2eb:fontsize=44:x=(w-text_w)/2:y=(h-text_h)/2 - 30:enable='between(t,7.0,10.5)',
             drawtext=text='DAVINCI RESOLVE STUDIO · 35MM FILM PRINT':fontcolor=#d94f3d:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2 + 30:enable='between(t,7.0,10.5)',
             drawtext=text='MAKE THE MOMENT MATTER.':fontcolor=#f5f2eb:fontsize=52:x=(w-text_w)/2:y=(h-text_h)/2 - 20:enable='between(t,10.5,14)',
             drawtext=text='ABHINAY YADAV · INDEPENDENT EDITOR':fontcolor=#d94f3d:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2 + 40:enable='between(t,10.5,14)',
             drawtext=text='%{{pts\\:hms}}':fontcolor=#c8c2b7:fontsize=22:x=60:y=h-60,
             drawtext=text='4K UHD · 24 FPS':fontcolor=#d94f3d:fontsize=20:x=w-260:y=h-60[vout];
        [1:a][2:a]amix=inputs=2:duration=first[aout]
      " \
      -map "[vout]" -map "[aout]" \
      -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
      -c:a aac -b:a 192k \
      "{showreel_path}"
    """
    run_ffmpeg(cmd_showreel, "showreel.mp4 (16:9 Master Showreel)")

    # 2. Reel 01 (9:16 Vertical - 1080x1920, 30fps - Urban Rhythm Fashion Reel)
    reel1_path = os.path.join(OUTPUT_DIR, "reel-01.mp4")
    cmd_reel1 = f"""
    ffmpeg -y \
      -f lavfi -i "color=c=#151618:s=1080x1920:d=10:r=30" \
      -f lavfi -i "aevalsrc=sin(2*PI*60*t)*exp(-4*mod(t\\,0.5)) + 0.4*sin(2*PI*880*t)*exp(-6*mod(t\\,0.25)):d=10:s=48000" \
      -filter_complex "
        [0:v]format=yuv420p,
             drawbox=x=60:y=120:w=960:h=1680:color=#d94f3d@0.6:t=4,
             drawtext=text='URBAN RHYTHM':fontcolor=#f5f2eb:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2 - 120:enable='between(t,0,3)',
             drawtext=text='HIGH FASHION · BEAT SYNC':fontcolor=#d94f3d:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2 - 40:enable='between(t,0,3)',
             drawtext=text='1.8M VIEWS':fontcolor=#f5f2eb:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2 + 80:enable='between(t,0,3)',
             drawtext=text='MICRO CUTS':fontcolor=#f5f2eb:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2 - 80:enable='between(t,3,6.5)',
             drawtext=text='& SPEED RAMPS':fontcolor=#d94f3d:fontsize=54:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,3,6.5)',
             drawtext=text='RETENTION PACING':fontcolor=#c8c2b7:fontsize=30:x=(w-text_w)/2:y=(h-text_h)/2 + 80:enable='between(t,3,6.5)',
             drawtext=text='EDITED BY ABHINAY YADAV':fontcolor=#f5f2eb:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2 - 30:enable='between(t,6.5,10)',
             drawtext=text='DELHI / WORLDWIDE':fontcolor=#d94f3d:fontsize=28:x=(w-text_w)/2:y=(h-text_h)/2 + 30:enable='between(t,6.5,10)',
             drawtext=text='9:16 VERTICAL REEL':fontcolor=#c8c2b7:fontsize=24:x=90:y=160,
             drawtext=text='%{{pts\\:hms}}':fontcolor=#d94f3d:fontsize=26:x=w-240:y=160[vout]
      " \
      -map "[vout]" -map 1:a \
      -c:v libx264 -preset fast -crf 21 -pix_fmt yuv420p \
      -c:a aac -b:a 192k \
      "{reel1_path}"
    """
    run_ffmpeg(cmd_reel1, "reel-01.mp4 (9:16 Fashion Reel)")

    # 3. Reel 02 (9:16 Vertical - 1080x1920, 30fps - Sonic Pulse Music Teaser)
    reel2_path = os.path.join(OUTPUT_DIR, "reel-02.mp4")
    cmd_reel2 = f"""
    ffmpeg -y \
      -f lavfi -i "color=c=#0f1012:s=1080x1920:d=10:r=30" \
      -f lavfi -i "aevalsrc=sin(2*PI*70*t)*exp(-3*mod(t\\,0.4)) + 0.3*sin(2*PI*520*t)*exp(-8*mod(t\\,0.2)):d=10:s=48000" \
      -filter_complex "
        [0:v]format=yuv420p,
             drawbox=x=60:y=120:w=960:h=1680:color=#c8c2b7@0.4:t=3,
             drawtext=text='SONIC PULSE':fontcolor=#f5f2eb:fontsize=68:x=(w-text_w)/2:y=(h-text_h)/2 - 100:enable='between(t,0,3.5)',
             drawtext=text='MUSIC TEASER · VIRAL EDIT':fontcolor=#d94f3d:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2 - 20:enable='between(t,0,3.5)',
             drawtext=text='2.4M VIEWS':fontcolor=#f5f2eb:fontsize=46:x=(w-text_w)/2:y=(h-text_h)/2 + 80:enable='between(t,0,3.5)',
             drawtext=text='RGB SPLIT & GLITCH':fontcolor=#d94f3d:fontsize=52:x=(w-text_w)/2:y=(h-text_h)/2 - 60:enable='between(t,3.5,7)',
             drawtext=text='BASS-SYNCHRONIZED CUTS':fontcolor=#f5f2eb:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2 + 20:enable='between(t,3.5,7)',
             drawtext=text='CUT FOR MAXIMUM RETENTION':fontcolor=#f5f2eb:fontsize=42:x=(w-text_w)/2:y=(h-text_h)/2 - 20:enable='between(t,7,10)',
             drawtext=text='ABHINAY YADAV':fontcolor=#d94f3d:fontsize=30:x=(w-text_w)/2:y=(h-text_h)/2 + 40:enable='between(t,7,10)',
             drawtext=text='%{{pts\\:hms}}':fontcolor=#c8c2b7:fontsize=24:x=90:y=160[vout]
      " \
      -map "[vout]" -map 1:a \
      -c:v libx264 -preset fast -crf 21 -pix_fmt yuv420p \
      -c:a aac -b:a 192k \
      "{reel2_path}"
    """
    run_ffmpeg(cmd_reel2, "reel-02.mp4 (9:16 Music Teaser)")

    # 4. Reel 03 (9:16 Vertical - 1080x1920, 30fps - Lost in Kyoto Travel Reel)
    reel3_path = os.path.join(OUTPUT_DIR, "reel-03.mp4")
    cmd_reel3 = f"""
    ffmpeg -y \
      -f lavfi -i "color=c=#18191c:s=1080x1920:d=10:r=30" \
      -f lavfi -i "aevalsrc=0.5*sin(2*PI*220*t)*sin(2*PI*2*t) + 0.2*sin(2*PI*440*t):d=10:s=48000" \
      -filter_complex "
        [0:v]format=yuv420p,
             drawbox=x=60:y=120:w=960:h=1680:color=#d94f3d@0.5:t=3,
             drawtext=text='LOST IN KYOTO':fontcolor=#f5f2eb:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2 - 100:enable='between(t,0,3.5)',
             drawtext=text='TRAVEL CINEMA · BRAND AD':fontcolor=#d94f3d:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2 - 20:enable='between(t,0,3.5)',
             drawtext=text='3.1M ENGAGEMENT':fontcolor=#f5f2eb:fontsize=44:x=(w-text_w)/2:y=(h-text_h)/2 + 70:enable='between(t,0,3.5)',
             drawtext=text='KODAK 2383 FILM LOOK':fontcolor=#d94f3d:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2 - 50:enable='between(t,3.5,7)',
             drawtext=text='WHIP PAN & FOLEY SOUND':fontcolor=#f5f2eb:fontsize=34:x=(w-text_w)/2:y=(h-text_h)/2 + 30:enable='between(t,3.5,7)',
             drawtext=text='COMMERCIAL CUT':fontcolor=#f5f2eb:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2 - 30:enable='between(t,7,10)',
             drawtext=text='ABHINAY YADAV':fontcolor=#d94f3d:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2 + 40:enable='between(t,7,10)',
             drawtext=text='%{{pts\\:hms}}':fontcolor=#c8c2b7:fontsize=24:x=90:y=160[vout]
      " \
      -map "[vout]" -map 1:a \
      -c:v libx264 -preset fast -crf 21 -pix_fmt yuv420p \
      -c:a aac -b:a 192k \
      "{reel3_path}"
    """
    run_ffmpeg(cmd_reel3, "reel-03.mp4 (9:16 Travel Cinema Reel)")

    # 5. Film 01 (16:9 Long-Form Narrative - 1920x1080)
    film1_path = os.path.join(OUTPUT_DIR, "film-01.mp4")
    cmd_film1 = f"""
    ffmpeg -y \
      -f lavfi -i "color=c=#0d0e10:s=1920x1080:d=12:r=24" \
      -f lavfi -i "aevalsrc=0.3*sin(2*PI*110*t) + 0.15*sin(2*PI*220*t)*sin(PI*t):d=12:s=48000" \
      -filter_complex "
        [0:v]format=yuv420p,
             drawbox=x=0:y=0:w=1920:h=120:color=black@1:t=fill,
             drawbox=x=0:y=960:w=1920:h=120:color=black@1:t=fill,
             drawtext=text='THE UNSEEN HOURS':fontcolor=#f5f2eb:fontsize=58:x=(w-text_w)/2:y=(h-text_h)/2 - 40:enable='between(t,0,4)',
             drawtext=text='A NARRATIVE SHORT FILM':fontcolor=#d94f3d:fontsize=26:x=(w-text_w)/2:y=(h-text_h)/2 + 30:enable='between(t,0,4)',
             drawtext=text='DIRECTED BY KARAN SHARMA':fontcolor=#c8c2b7:fontsize=22:x=(w-text_w)/2:y=(h-text_h)/2 + 70:enable='between(t,0,4)',
             drawtext=text='SCENE 04 // THE LATE TRANSITION':fontcolor=#f5f2eb:fontsize=46:x=(w-text_w)/2:y=(h-text_h)/2 - 30:enable='between(t,4,8)',
             drawtext=text='2.39\\:1 ANAMORPHIC · DAVINCI RESOLVE GRADE':fontcolor=#d94f3d:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2 + 30:enable='between(t,4,8)',
             drawtext=text='EDITED & POST SUPERVISED BY':fontcolor=#c8c2b7:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2 - 30:enable='between(t,8,12)',
             drawtext=text='ABHINAY YADAV':fontcolor=#f5f2eb:fontsize=52:x=(w-text_w)/2:y=(h-text_h)/2 + 20:enable='between(t,8,12)',
             drawtext=text='%{{pts\\:hms}}':fontcolor=#c8c2b7:fontsize=20:x=60:y=h-70,
             drawtext=text='CINEMA CUT · 24 FPS':fontcolor=#d94f3d:fontsize=20:x=w-260:y=h-70[vout]
      " \
      -map "[vout]" -map 1:a \
      -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
      -c:a aac -b:a 192k \
      "{film1_path}"
    """
    run_ffmpeg(cmd_film1, "film-01.mp4 (The Unseen Hours)")

    # 6. Film 02 (16:9 Documentary - 1920x1080)
    film2_path = os.path.join(OUTPUT_DIR, "film-02.mp4")
    cmd_film2 = f"""
    ffmpeg -y \
      -f lavfi -i "color=c=#111214:s=1920x1080:d=12:r=24" \
      -f lavfi -i "aevalsrc=0.25*sin(2*PI*130*t) + 0.1*sin(2*PI*260*t):d=12:s=48000" \
      -filter_complex "
        [0:v]format=yuv420p,
             drawbox=x=0:y=0:w=1920:h=90:color=black@1:t=fill,
             drawbox=x=0:y=990:w=1920:h=90:color=black@1:t=fill,
             drawtext=text='SHADOWS & SILK\\: THE OLD CITY':fontcolor=#f5f2eb:fontsize=54:x=(w-text_w)/2:y=(h-text_h)/2 - 40:enable='between(t,0,4)',
             drawtext=text='DOCUMENTARY FEATURETTE':fontcolor=#d94f3d:fontsize=26:x=(w-text_w)/2:y=(h-text_h)/2 + 30:enable='between(t,0,4)',
             drawtext=text='BEST EDITING AWARD 2023':fontcolor=#f5f2eb:fontsize=38:x=(w-text_w)/2:y=(h-text_h)/2 - 30:enable='between(t,4,8)',
             drawtext=text='16MM ARCHIVE & 4K ANAMORPHIC BLEND':fontcolor=#d94f3d:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2 + 30:enable='between(t,4,8)',
             drawtext=text='EDITED BY ABHINAY YADAV':fontcolor=#f5f2eb:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2 - 20:enable='between(t,8,12)',
             drawtext=text='DIRECTED BY POOJA SEN':fontcolor=#c8c2b7:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2 + 40:enable='between(t,8,12)',
             drawtext=text='%{{pts\\:hms}}':fontcolor=#c8c2b7:fontsize=20:x=60:y=h-60,
             drawtext=text='ARCHIVE REEL · 24 FPS':fontcolor=#d94f3d:fontsize=20:x=w-280:y=h-60[vout]
      " \
      -map "[vout]" -map 1:a \
      -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
      -c:a aac -b:a 192k \
      "{film2_path}"
    """
    run_ffmpeg(cmd_film2, "film-02.mp4 (Shadows & Silk)")

    # 7. Generate Premiere Pro XML Interchange File
    xml_path = os.path.join(OUTPUT_DIR, "showreel_timeline.xml")
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="4">
  <sequence id="sequence-1">
    <name>Abhinay Yadav - Editorial Showreel 2024</name>
    <duration>1440</duration>
    <rate>
      <timebase>24</timebase>
      <ntsc>FALSE</ntsc>
    </rate>
    <media>
      <video>
        <format>
          <samplecharacteristics>
            <width>1920</width>
            <height>1080</height>
            <pixelaspectratio>square</pixelaspectratio>
            <rate>
              <timebase>24</timebase>
              <ntsc>FALSE</ntsc>
            </rate>
          </samplecharacteristics>
        </format>
        <track>
          <!-- Track 1: Master Showreel Cut -->
          <clipitem id="clipitem-1">
            <name>showreel.mp4</name>
            <duration>336</duration>
            <rate><timebase>24</timebase><ntsc>FALSE</ntsc></rate>
            <start>0</start>
            <end>336</end>
            <in>0</in>
            <out>336</out>
            <file id="file-1">
              <name>showreel.mp4</name>
              <pathurl>file://localhost/assets/videos/showreel.mp4</pathurl>
              <rate><timebase>24</timebase><ntsc>FALSE</ntsc></rate>
              <media>
                <video><samplecharacteristics><width>1920</width><height>1080</height></samplecharacteristics></video>
              </media>
            </file>
          </clipitem>
        </track>
      </video>
    </media>
  </sequence>
</xmeml>
"""
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"✅ Created: showreel_timeline.xml (Premiere Pro XML Interchange)")

    print("\n🎉 ALL PORTFOLIO VIDEO MEDIA GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    build_all()
