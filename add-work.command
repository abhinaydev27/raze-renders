#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Double-click to ADD A VIDEO to the site.
#
#   1. Drop your finished exports into the  incoming  folder
#   2. Double-click this file
#   3. Type a title + tags for each one when asked
#   4. Double-click publish.command
#
# Landscape files land in Selected work, vertical ones in Reels.
# Everything is converted to a web-ready mp4 and hosted on your own
# domain — no YouTube embed, no third-party player.
# ─────────────────────────────────────────────────────────────
cd "$(dirname "$0")"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo ""
  echo "  ffmpeg is missing — it does the video conversion."
  echo "  Install it once with:"
  echo ""
  echo "      brew install ffmpeg"
  echo ""
  read -n 1 -s -r -p "  Press any key to close this window."
  echo ""
  exit 1
fi

python3 tools/add-work.py "$@"
echo ""
read -n 1 -s -r -p "  Press any key to close this window."
echo ""
