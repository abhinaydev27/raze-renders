# RaZe Renders — video portfolio

Dark, cinematic, single-page portfolio for **Abhinay / RaZe Renders**.
Videos play **directly on the page** — no YouTube, no Drive, no embeds.

```
raze-renders/
├─ index.html      ← structure & copy
├─ styles.css      ← all styling
├─ script.js       ← intro, autoplay, custom players
├─ make-posters.sh ← regenerate poster thumbnails from your videos
└─ assets/
   ├─ videos/      ← your .mp4 files go here
   └─ posters/     ← auto-generated thumbnail per video
```

## ▶ How it plays

- **Showreel** autoplays muted in the hero. Click it (or the button) for sound.
- **Work & reels** start playing muted when they scroll into view, and pause when they leave — so nothing hammers bandwidth.
- **Hover** a clip (desktop) to hear it · **tap** a clip (mobile) to play it.
- Only **one** clip plays sound at a time — unmuting one mutes the rest.
- Each clip has a minimal custom player: play/pause, scrubber, mute, fullscreen.

## 🎬 Swapping in your real videos (the only step you need)

1. Export your clips and **name them exactly** like the placeholders, then drop them into `assets/videos/`, replacing what's there:

   | File                     | Slot            | Best aspect |
   |--------------------------|-----------------|-------------|
   | `showreel.mp4`           | Hero showreel   | 16:9        |
   | `long-ad.mp4`            | Work · piece 1  | 16:9        |
   | `long-doc.mp4`           | Work · piece 2  | 16:9        |
   | `reel-anime.mp4`         | Reel 1          | 9:16        |
   | `reel-brand.mp4`         | Reel 2          | 9:16        |
   | `reel-gaming.mp4`        | Reel 3          | 9:16        |

   > Keep the same names and you never touch the code. Want different names/titles? Edit the `data-src`, `poster`, and titles in `index.html`.

2. **Regenerate the poster thumbnails** (first frame shown before a clip loads):

   ```bash
   ./make-posters.sh
   ```

   Needs `ffmpeg` (`brew install ffmpeg`). Skip this and it'll just use the old posters — no breakage.

3. Refresh the page. Done.

### Editing text
Names, titles, tags, bio, stats, email and social links are all plain text in `index.html`. Search for `hello@razerenders.live` and the `contact__socials` list to set your real links.

## 🌐 Publishing to razerenders.live
See **[DEPLOY.md](DEPLOY.md)** for the full free step-by-step (Cloudflare Pages + your name.com domain). A ready-to-upload `raze-renders-site.zip` is generated next to this folder.

## 🌐 Publishing (free options)
Any static host works — it's just files.

- **Netlify / Vercel:** drag the `raze-renders` folder onto their dashboard.
- **GitHub Pages:** push the folder to a repo, enable Pages.
- **Cloudflare Pages:** connect the repo or upload directly.

### ⚠️ Keep it fast (you said files stay under ~1 GB)
Big raw exports will load slowly. Before publishing, compress each clip — good balance of quality/size:

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow -vf "scale=-2:1080" -c:a aac -b:a 128k -movflags +faststart output.mp4
```

- `-crf 23` ≈ visually lossless-ish; raise to 26–28 for smaller files.
- `-movflags +faststart` lets playback start before the whole file downloads (important).
- Reels can be `scale=-2:1350` (vertical) and long-form `scale=-2:1080`.

## 🎨 Tweaking the look
Open `styles.css` → the `:root` block at the top. Change `--ember` (accent), `--bg` (background), or the fonts in one place.

---
Built for RaZe Renders. Swap the clips, ship it.
