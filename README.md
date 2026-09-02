# Abhinay Yadav — Portfolio Website

A bespoke, dark-themed editorial portfolio website for **Abhinay Yadav**, Independent Video Editor & Filmmaker based in Delhi, India.

---

## 🌟 Features

- **Cinematic Aesthetic:** Obsidian background (`#17181a`), ivory typography (`#f2eee6`), terracotta red accents (`#c94a3a`), and subtle film grain overlay.
- **Typography:** Hand-picked Google Fonts pairing (*Cormorant Garamond*, *IBM Plex Mono*, and *IBM Plex Sans*).
- **Interactive Project & Showreel Modals:** Click any project card or the "Watch the showreel" button to launch a clean modal with embedded video playback and project breakdown.
- **Live Frame Timecode:** Dynamic 24fps real-time timecode clock (`00:00:00:00`).
- **Responsive Navigation:** Sticky blurred glass header with active scrollspy and animated mobile drawer menu.
- **Interactive Contact Form:** Input validation, animated state transitions, and automatic `mailto:` client invocation.
- **Ultra Lightweight & Fast:** 100% vanilla HTML5/CSS3/ES6 with zero bulky runtime dependencies.

---

## 🚀 Running Locally

You can run this site with any local static web server:

### Option 1: Using Python (Built-in)
```bash
python3 -m http.server 3000
```
Then open [http://localhost:3000](http://localhost:3000) in your browser.

### Option 2: Using Node / npx
```bash
npm start
# or
npx serve .
```

---

## 🌐 Making It Live on the Internet (Free Hosting Options)

### 1. Vercel (Recommended - 1 Click)
1. Install Vercel CLI: `npm i -g vercel` (or visit [vercel.com](https://vercel.com))
2. Run in the project directory:
   ```bash
   vercel
   ```
3. Your site will be live on a `*.vercel.app` domain with free SSL in under 30 seconds!

### 2. Netlify
1. Drag and drop this folder directly into [app.netlify.com/drop](https://app.netlify.com/drop)
2. Or use Netlify CLI: `npx netlify deploy --prod --dir=.`

### 3. GitHub Pages
1. Push this folder to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio release"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```
2. Go to **Repository Settings** > **Pages** > Select `main` branch / `root` directory > **Save**.
3. Your site is live at `https://<your-username>.github.io/<your-repo-name>/`
