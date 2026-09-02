#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Double-click this file to rebuild the upload zip after you've
# made edits. Then drag the new zip into Cloudflare Pages.
# ─────────────────────────────────────────────────────────────
cd "$(dirname "$0")"
rm -f ../raze-renders-site.zip
zip -r ../raze-renders-site.zip index.html styles.css script.js assets -x '*.DS_Store' >/dev/null
echo ""
echo "  ✅  Fresh site zip built:"
echo "      $(cd .. && pwd)/raze-renders-site.zip"
echo ""
echo "  Next: Cloudflare dashboard → your 'raze' project →"
echo "        Deployments → Create deployment → drag that zip → Deploy."
echo ""
read -n 1 -s -r -p "  Press any key to close this window."
echo ""
