# Deploying RaZe Renders to razerenders.live (free)

Your site is just a folder of files, so any free static host works.
**Recommended: Cloudflare Pages** — free forever, fast global CDN, free SSL, and once your
domain's DNS is on Cloudflare, attaching `razerenders.live` is basically one click.

> A ready-to-upload **`raze-renders-site.zip`** sits next to this folder — that's what you drag in.

---

# ▶ Cloudflare Pages (recommended)

## Step 1 — Free Cloudflare account
Go to **[dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up)** and sign up. No card needed.

## Step 2 — Add your domain to Cloudflare (moves DNS to Cloudflare)
1. In the dashboard: **Add a site / Add a domain** → enter **`razerenders.live`** → pick the **Free** plan.
2. Cloudflare scans existing records, then shows you **2 nameservers** that look like
   `xxx.ns.cloudflare.com` and `yyy.ns.cloudflare.com`. **Keep this tab open.**

## Step 3 — Point name.com at Cloudflare (one-time)
1. Log in to **[name.com](https://www.name.com)** → **My Domains** → click **razerenders.live**.
2. Find **Nameservers** (left menu).
3. **Remove** the existing name.com nameservers and **enter Cloudflare's two** from Step 2.
4. Save. Back in Cloudflare, click **Done / Check nameservers**. Activation can take minutes to a few hours — Cloudflare emails you when it's active.

> This moves your DNS to Cloudflare. Totally fine for a portfolio (you have nothing else on this domain). Any future records (e.g. email) you'd just add inside Cloudflare.

## Step 4 — Upload the site
1. In Cloudflare: **Workers & Pages → Create → Pages → Upload assets** (a.k.a. "Direct Upload").
2. Name the project (e.g. `raze`).
3. Drag **`raze-renders-site.zip`** (or the `raze-renders` folder) onto the box → **Deploy**.
4. ~20 seconds later it's live at **`raze.pages.dev`**. Open it — it works.

## Step 5 — Attach razerenders.live
1. Open your Pages project → **Custom domains** → **Set up a domain**.
2. Enter **`razerenders.live`** → **Continue → Activate domain**.
3. Because Cloudflare now runs your DNS, it **creates the records automatically**. Repeat for **`www.razerenders.live`** if you want the www version too.
4. SSL is issued automatically. Visit **https://razerenders.live** — live. 🎬

---

## Updating later (adding your real videos)
1. Drop real clips into `assets/videos/` (same filenames — see [README.md](README.md)).
2. Run `./make-posters.sh` to refresh thumbnails.
3. Re-zip (command below), open your Pages project → **Create deployment / Upload assets** → drag the new zip. Same URL, no DNS changes.

```bash
cd "/Users/abhinay/Documents/Project/Job finding/raze-renders" && zip -r ../raze-renders-site.zip . -x '.claude/*' -x '*.DS_Store'
```

*(Optional, nicer long-term: connect a GitHub repo to the Pages project so every `git push` auto-deploys — but drag-and-drop is perfectly fine.)*

---

## Alternative: Netlify (no nameserver change)
If you'd rather **not** move nameservers, Netlify keeps name.com as your DNS and you add 2 records by hand:
1. [netlify.com](https://www.netlify.com) → sign up → **Add new site → Deploy manually** → drag the zip → live on `*.netlify.app`.
2. **Domain management → Add domain →** `razerenders.live` → choose **external DNS**. Netlify shows the exact records.
3. At name.com → **DNS Records → Add Record**:
   - **A** · Host blank (`@`) · Answer `75.2.60.5`
   - **CNAME** · Host `www` · Answer `your-site.netlify.app`
4. Wait for DNS + auto SSL. Done.

Both are 100% free. Cloudflare = simpler domain step + faster CDN; Netlify = no nameserver change.
