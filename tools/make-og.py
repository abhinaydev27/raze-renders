#!/usr/bin/env python3
"""
Generates assets/og.jpg — the branded 1200x630 card that WhatsApp, X,
LinkedIn and iMessage show when razerenders.live is shared.

Re-run after changing the headline:  python3 tools/make-og.py
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
INK = (11, 11, 12)
BONE = (236, 229, 216)
BONE2 = (184, 177, 164)
MUTED = (131, 124, 112)
RED = (255, 43, 43)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "og.jpg")

def font(paths, size):
    for p in paths:
        p = os.path.expanduser(p)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

DISPLAY = ["/System/Library/Fonts/Supplemental/Impact.ttf",
           "~/Library/Fonts/BebasNeue-Regular.ttf"]
SANS_B = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
          "/System/Library/Fonts/Supplemental/Arial.ttf"]
SANS = ["/System/Library/Fonts/Supplemental/Arial.ttf"]
MONO = ["/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf"]

f_head = font(DISPLAY, 150)
f_eyebrow = font(MONO, 20)
f_body = font(SANS, 25)
f_url = font(MONO, 22)
f_tag = font(MONO, 18)

img = Image.new("RGB", (W, H), INK)

# ── warm red glow, top-right (mirrors the site's hero lighting) ──────────
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
cx, cy, rad = int(W * 0.86), int(H * 0.14), 640
for i in range(rad, 0, -6):
    a = int(255 * (1 - i / rad) ** 2.0)
    gd.ellipse([cx - i, cy - i * 0.9, cx + i, cy + i * 0.9], fill=a)
glow = glow.filter(ImageFilter.GaussianBlur(80))
img = Image.composite(Image.new("RGB", (W, H), (150, 28, 26)), img, glow.point(lambda v: int(v * 0.68)))

# second, tighter ember
glow2 = Image.new("L", (W, H), 0)
gd2 = ImageDraw.Draw(glow2)
for i in range(280, 0, -4):
    gd2.ellipse([cx - i, cy - i * 0.8, cx + i, cy + i * 0.8], fill=int(255 * (1 - i / 280) ** 2.2))
glow2 = glow2.filter(ImageFilter.GaussianBlur(60))
img = Image.composite(Image.new("RGB", (W, H), (255, 82, 60)), img, glow2.point(lambda v: int(v * 0.55)))

# cool counter-light, bottom-left — stops the dark half going dead flat
glow3 = Image.new("L", (W, H), 0)
gd3 = ImageDraw.Draw(glow3)
for i in range(460, 0, -5):
    gd3.ellipse([-120 - i, H + 60 - i, -120 + i, H + 60 + i], fill=int(255 * (1 - i / 460) ** 1.9))
glow3 = glow3.filter(ImageFilter.GaussianBlur(70))
img = Image.composite(Image.new("RGB", (W, H), (46, 55, 78)), img, glow3.point(lambda v: int(v * 0.6)))

d = ImageDraw.Draw(img, "RGBA")

# ── faint technical grid ────────────────────────────────────────────────
for x in range(0, W, 60):
    d.line([(x, 0), (x, H)], fill=(236, 229, 216, 8), width=1)
for y in range(0, H, 60):
    d.line([(0, y), (W, y)], fill=(236, 229, 216, 8), width=1)

# ── timeline ruler along the bottom ─────────────────────────────────────
base = H - 74
for x in range(0, W, 14):
    d.line([(x, base), (x, base + 7)], fill=(236, 229, 216, 34), width=1)
for x in range(0, W, 70):
    d.line([(x, base - 6), (x, base + 7)], fill=(184, 177, 164, 80), width=2)

# ── corner registration marks ───────────────────────────────────────────
M, L, T = 44, 30, 2
for (px, py, sx, sy) in ((M, M, 1, 1), (W - M, M, -1, 1), (M, H - M, 1, -1), (W - M, H - M, -1, -1)):
    d.line([(px, py), (px + L * sx, py)], fill=(236, 229, 216, 120), width=T)
    d.line([(px, py), (px, py + L * sy)], fill=(236, 229, 216, 120), width=T)

def tracked(draw, xy, text, fnt, fill, track=0):
    """Draw text with letter-spacing; returns total width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + track
    return x - xy[0]

X = 84

# ── eyebrow ─────────────────────────────────────────────────────────────
d.rectangle([X, 176, X + 34, 179], fill=RED)
tracked(d, (X + 50, 166), "RAZE RENDERS", f_eyebrow, BONE2, 5)

# ── headline ────────────────────────────────────────────────────────────
d.text((X - 4, 212), "VIDEO EDITOR", font=f_head, fill=BONE)

# ── name + range ────────────────────────────────────────────────────────
d.text((X, 392), "Abhinay", font=font(SANS_B, 30), fill=BONE)
tracked(d, (X, 444), "SHORT FORM  ·  ADS  ·  DOCUMENTARY  ·  TALKING HEAD", f_tag, MUTED, 1.6)

# ── url, bottom left ────────────────────────────────────────────────────
tracked(d, (X, H - 52), "razerenders.live", f_url, BONE, 2)

# ── available pill, bottom right ────────────────────────────────────────
pill = "AVAILABLE FOR WORK"
pw = sum(d.textlength(c, font=f_tag) + 1.8 for c in pill)
px = W - 84 - pw - 26
d.ellipse([px, H - 47, px + 9, H - 38], fill=(74, 222, 128))
tracked(d, (px + 22, H - 51), pill, f_tag, BONE2, 1.8)

# ── film grain ──────────────────────────────────────────────────────────
random.seed(7)
noise = Image.effect_noise((W, H), 26).convert("L")
img = Image.blend(img, Image.composite(Image.new("RGB", (W, H), (255, 255, 255)), img, noise.point(lambda v: 0)), 0)
px_img = img.load()
npx = noise.load()
for y in range(0, H):
    for x in range(0, W):
        n = (npx[x, y] - 128) * 0.055
        r, g, b = px_img[x, y]
        px_img[x, y] = (max(0, min(255, int(r + n))),
                        max(0, min(255, int(g + n))),
                        max(0, min(255, int(b + n))))

# ── vignette ────────────────────────────────────────────────────────────
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-int(W * 0.34), -int(H * 0.5), int(W * 1.34), int(H * 1.5)], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(150))
img = Image.composite(img, Image.new("RGB", (W, H), (4, 4, 5)), vig)

# baseline (not progressive) — some link crawlers won't decode progressive JPEGs
img.save(os.path.normpath(OUT), "JPEG", quality=88, optimize=True, progressive=False)
print("wrote", os.path.normpath(OUT), os.path.getsize(os.path.normpath(OUT)), "bytes")
