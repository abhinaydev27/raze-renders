#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Double-click to PUBLISH website changes.
# Commits everything in this folder and pushes to GitHub, which
# auto-deploys to razerenders.live in ~30 seconds.
# ─────────────────────────────────────────────────────────────
cd "$(dirname "$0")"
echo ""
echo "  Publishing changes to razerenders.live ..."
echo ""
git add -A
# Commit only if there's anything uncommitted. This must NOT gate the push:
# a commit can already exist and still be unpushed, and skipping the push in
# that case leaves the work sitting on this Mac while the site looks up to date.
if ! git diff --cached --quiet; then
  git commit -m "Update site"
fi

if [ -z "$(git log @{u}.. 2>/dev/null)" ]; then
  echo "  ℹ️  Nothing new to publish (already live)."
else
  if git push; then
    echo ""
    echo "  ✅  Pushed. Cloudflare is redeploying — razerenders.live"
    echo "      updates in about 30 seconds. Refresh to see it."
  else
    echo ""
    echo "  ❌  Push failed — check your internet connection and try again."
  fi
fi
echo ""
read -n 1 -s -r -p "  Press any key to close this window."
echo ""
