#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# make-posters.sh — regenerate poster thumbnails for every clip
# in assets/videos/. Grabs a frame a couple seconds in so the
# poster isn't a black opening frame.
#
# Usage:  ./make-posters.sh
# Needs:  ffmpeg  (brew install ffmpeg)
# ─────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

VID_DIR="assets/videos"
POS_DIR="assets/posters"
GRAB_AT="00:00:02"   # timestamp to grab; falls back to frame 0 for very short clips

command -v ffmpeg >/dev/null 2>&1 || { echo "✗ ffmpeg not found — run: brew install ffmpeg"; exit 1; }
mkdir -p "$POS_DIR"

shopt -s nullglob
found=0
for f in "$VID_DIR"/*.mp4 "$VID_DIR"/*.mov "$VID_DIR"/*.webm; do
  found=1
  name="$(basename "${f%.*}")"
  out="$POS_DIR/$name.jpg"
  # try grabbing at GRAB_AT; if the clip is shorter, grab the first frame
  if ! ffmpeg -y -loglevel error -ss "$GRAB_AT" -i "$f" -frames:v 1 -q:v 3 "$out" 2>/dev/null; then
    ffmpeg -y -loglevel error -i "$f" -frames:v 1 -q:v 3 "$out"
  fi
  echo "✓ $name.jpg"
done

[ "$found" -eq 0 ] && echo "No videos found in $VID_DIR — add your .mp4 files first." || echo "Done. Posters written to $POS_DIR/"
