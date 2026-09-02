#!/usr/bin/env python3
"""
Builds assets/videos/showreel.mp4 — the hero background reel.

Every frame is composed in Pillow and handed to ffmpeg to encode, because this
build of ffmpeg has no drawtext/freetype. That turns out to be the better route:
the transitions, the grade wipe and the graphics are all real pixel work with
proper easing rather than a stack of filter approximations.

Shots, and the transition that gets you into each one — no intro, straight
into the work:

    talking head  ·  (cut)
    night city    ·  whip pan
    stage         ·  cross dissolve
    product       ·  flash cut       + live LOG→GRADED wipe
    sunset        ·  bar wipe        + motion-graphics title-card build
    neon          ·  whip pan        + beat cuts and pop-on captions

Nothing names the technique on screen: .hero__hud in index.html does that in
crisp HTML text, driven off currentTime. Keep CHAPTERS in script.js in step
with TIMELINE below.

    python3 tools/make-reel.py

Requires the plates:  python3 tools/make-plates.py
"""
import os, math, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance, ImageFilter

OW, OH = 1600, 900          # output frame — matches the plates 1:1
FPS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PLATE_DIR = os.path.join(ROOT, "assets", "plates")
OUT_VIDEO = os.path.join(ROOT, "assets", "videos", "showreel.mp4")
OUT_POSTER = os.path.join(ROOT, "assets", "posters", "showreel.jpg")
TMP = os.path.join(os.environ.get("TMPDIR", "/tmp"), "reelframes")

BONE = (236, 229, 216)
BONE2 = (184, 177, 164)
MUTED = (140, 133, 121)
RED = (255, 43, 43)


# ── fonts ──────────────────────────────────────────────────────────────────
def font(paths, size):
    for p in paths:
        p = os.path.expanduser(p)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


MONO = ["/System/Library/Fonts/Supplemental/Courier New Bold.ttf"]
BOLD = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf"]
DISP = ["/System/Library/Fonts/Supplemental/Impact.ttf",
        "~/Library/Fonts/BebasNeue-Regular.ttf"]

F_SMALL = font(MONO, 19)
F_TITLE = font(DISP, 50)
F_CAP = font(DISP, 58)


# ── easing / math ──────────────────────────────────────────────────────────
def clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else hi if v > hi else v


def ease(t):                      # smooth in-out, for camera moves
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_out(t):                  # decelerate, for graphics settling
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in(t):
    t = clamp(t)
    return t ** 3


def lerp(a, b, t):
    return a + (b - a) * t


# ── plates ─────────────────────────────────────────────────────────────────
def load_plates():
    files = sorted(f for f in os.listdir(PLATE_DIR) if f.endswith(".jpg"))
    if len(files) < 6:
        sys.exit("run tools/make-plates.py first")
    out = {}
    for f in files:
        key = f.split("-", 1)[1].rsplit(".", 1)[0]
        out[key] = Image.open(os.path.join(PLATE_DIR, f)).convert("RGB")
    return out


PLATES = load_plates()


SHUTTER = 0.62      # fraction of each frame's duration the shutter is open
MB_SAMPLES = 3      # sub-frame samples averaged into the motion blur


def kenburns(name, p, dur, z0, z1, x0, y0, x1, y1):
    """Crop a moving window out of the plate. z is the crop size as a fraction
    of the plate, so z going down is a push in.

    Two things here are about not looking rendered. The window is sampled three
    times across the open shutter and averaged, which is real motion blur rather
    than a directional smear — a razor-sharp moving still is the single loudest
    tell that a frame was drawn and not photographed at 24fps. And the whole
    crop drifts by a pixel or two on incommensurate sines, because a strip of
    film never sits perfectly still in the gate and a render always does.
    """
    src = PLATES[name]
    sw, sh = src.size
    dq = (1.0 / FPS) * SHUTTER / dur
    wx = 1.7 * math.sin(p * 7.3) + 0.9 * math.sin(p * 19.1)
    wy = 1.4 * math.sin(p * 5.9 + 1.7)
    acc = None
    for j in range(MB_SAMPLES):
        e = ease(clamp(p / dur + dq * j / MB_SAMPLES, -0.4, 1.4))
        z = lerp(z0, z1, e)
        cw, ch = sw * z, sh * z
        cx = clamp(lerp(x0, x1, e) * (sw - cw) + wx, 0, sw - cw)
        cy = clamp(lerp(y0, y1, e) * (sh - ch) + wy, 0, sh - ch)
        f = src.crop((int(cx), int(cy), int(cx + cw), int(cy + ch))) \
               .resize((OW, OH), Image.LANCZOS)
        acc = f if acc is None else Image.blend(acc, f, 1.0 / (j + 1))
    return acc


# ── grading ────────────────────────────────────────────────────────────────
def to_log(im):
    """Flat, desaturated, lifted blacks — what it looks like out of camera."""
    im = ImageEnhance.Color(im).enhance(0.26)
    im = ImageEnhance.Contrast(im).enhance(0.70)
    im = ImageEnhance.Brightness(im).enhance(1.20)
    return Image.blend(im, Image.new("RGB", im.size, (62, 64, 58)), 0.18)


_WARM = [min(255, int(v + 22 * math.sin(math.pi * v / 255))) for v in range(256)]
_COOL = [max(0, min(255, int(v * 0.93 + 20 * (1 - v / 255)))) for v in range(256)]


def to_graded(im):
    """Teal shadows, warm highlights, more bite — the finished look."""
    im = ImageEnhance.Color(im).enhance(1.30)
    im = ImageEnhance.Contrast(im).enhance(1.18)
    r, g, b = im.split()
    return Image.merge("RGB", (r.point(_WARM), g, b.point(_COOL)))


# ── transition primitives ──────────────────────────────────────────────────
def hsmear(im, px, samples=13):
    """Horizontal smear — the motion blur that sells a whip pan."""
    if px < 2:
        return im
    out = im
    for i in range(1, samples):
        off = int(-px / 2 + px * i / (samples - 1))
        out = Image.blend(out, ImageChops.offset(im, off, 0), 1.0 / (i + 1))
    return out


def whip(a, b, t):
    """a slides out left, b slides in from right, both smeared."""
    e = ease(t)
    shift = int(OW * 1.05)
    sm = int(OW * 0.074 * math.sin(math.pi * clamp(t)) + 7)
    fa = hsmear(ImageChops.offset(a, -int(shift * e), 0), sm)
    fb = hsmear(ImageChops.offset(b, shift - int(shift * e), 0), sm)
    return Image.blend(fa, fb, e)


def dissolve(a, b, t):
    return Image.blend(a, b, ease(t))


def flash(a, b, t):
    """Cut on the peak of a light leak."""
    base = a if t < 0.5 else b
    k = math.sin(math.pi * clamp(t)) ** 0.7
    warm = Image.new("RGB", (OW, OH), (255, 238, 224))
    return Image.blend(base, warm, 0.58 * k)


def barwipe(a, b, t):
    """Hard-edged wipe with a hot leading edge."""
    e = ease(t)
    x = int(OW * e)
    out = a.copy()
    if x > 0:
        out.paste(b.crop((0, 0, x, OH)), (0, 0))
    if 0 < x < OW:
        ImageDraw.Draw(out).rectangle([x - 4, 0, x + 3, OH], fill=(255, 236, 220))
        ImageDraw.Draw(out, "RGBA").rectangle([x + 4, 0, x + 50, OH], fill=(255, 43, 43, 60))
    return out


# ── film look ──────────────────────────────────────────────────────────────
# Applied to the finished frame, where a grade and a film-emulation pass sit in
# a real timeline. Each of these is a cue the eye reads as "camera" rather than
# "computer", because a rendered image is clean, uniformly sharp, perfectly
# registered and reaches pure black — and a photographed one does none of that.

def _shift(im, dx):
    """Horizontal shift that doesn't wrap. ImageChops.offset wraps, which sends
    a flare streak out one side of the frame and straight back in the other."""
    out = Image.new(im.mode, im.size, 0)
    out.paste(im, (dx, 0))
    return out


def _tone_lut(lift, gamma, shoulder):
    lut = []
    for v in range(256):
        x = (v / 255.0) ** gamma
        x = x / (x + shoulder) * (1 + shoulder)      # highlight roll-off
        x = lift + (1 - lift) * x                    # film never hits pure black
        lut.append(max(0, min(255, int(round(x * 255)))))
    return lut


# Blue is lifted most and rolls off soonest. That single asymmetry is what gives
# film its teal shadows and warm highlights, without touching saturation at all.
_LUT_R = _tone_lut(0.040, 1.30, 0.94)
_LUT_G = _tone_lut(0.048, 1.34, 0.90)
_LUT_B = _tone_lut(0.072, 1.42, 0.84)


def film_curve(img):
    r, g, b = img.split()
    return Image.merge("RGB", (r.point(_LUT_R), g.point(_LUT_G), b.point(_LUT_B)))


def _highlights(img, thresh):
    return img.convert("L").point(
        lambda v: 0 if v < thresh else min(255, (v - thresh) * 255 // (255 - thresh)))


def halation(img, amt=0.50):
    """The warm bloom film gets around a blown highlight. The red-sensitive
    layer of the emulsion scatters furthest, so the glow is orange-red rather
    than white — sensors don't do it, which is why faking it reads as film."""
    wide = _highlights(img, 186).filter(ImageFilter.GaussianBlur(26))
    glow = Image.merge("RGB", (wide,
                               wide.point(lambda v: int(v * .38)),
                               wide.point(lambda v: int(v * .13))))
    img = ImageChops.add(img, glow.point(lambda v: int(v * amt)))
    tight = _highlights(img, 214).filter(ImageFilter.GaussianBlur(5))
    return ImageChops.add(img, Image.merge("RGB", (tight, tight, tight))
                          .point(lambda v: int(v * .22)))


def anamorphic(img, amt=0.34):
    """The horizontal blue streak off a hard specular. Pure lens signature:
    nothing in a rendered frame produces it by accident."""
    hot = _highlights(img, 236).filter(ImageFilter.GaussianBlur(2))
    s = hot
    for px, w in ((6, .78), (16, .58), (40, .40), (96, .24), (200, .11)):
        f = hot.point(lambda v, w=w: int(v * w))
        s = ImageChops.lighter(s, _shift(f, px))
        s = ImageChops.lighter(s, _shift(f, -px))
    s = s.filter(ImageFilter.GaussianBlur(3))
    tint = Image.merge("RGB", (s.point(lambda v: int(v * .46)),
                               s.point(lambda v: int(v * .68)), s))
    return ImageChops.add(img, tint.point(lambda v: int(v * amt)))


def chroma(img, px=2.6):
    """Lateral chromatic aberration — away from the optical centre the channels
    don't quite land on top of each other. Only the red and green are scaled, so
    every value stays >= 1 and the crop never runs off the edge of the frame."""
    w, h = img.size
    def scaled(ch, k):
        nw, nh = int(w * k), int(h * k)
        big = ch.resize((nw, nh), Image.BILINEAR)
        return big.crop(((nw - w) // 2, (nh - h) // 2,
                         (nw - w) // 2 + w, (nh - h) // 2 + h))
    r, g, b = img.split()
    return Image.merge("RGB", (scaled(r, 1 + px * 2 / w), scaled(g, 1 + px / w), b))


def soft_corners(img, amt=0.60):
    """Lens falloff costs corners resolution as well as light. It's just a
    blurred copy masked to the corners, but it stops the frame reading as though
    it were drawn edge to edge at one uniform sharpness."""
    m = Image.new("L", img.size, 255)
    ImageDraw.Draw(m).ellipse([-int(OW * .16), -int(OH * .28),
                               int(OW * 1.16), int(OH * 1.28)], fill=0)
    m = m.filter(ImageFilter.GaussianBlur(120)).point(lambda v: int(v * amt))
    return Image.composite(img.filter(ImageFilter.GaussianBlur(2.4)), img, m)


def grain(img, amt=0.075):
    """Fresh noise every frame, generated at output resolution so the grain
    stays a constant size on screen instead of zooming with the camera move."""
    n = Image.effect_noise(img.size, 22).convert("L")
    d = ImageChops.subtract(Image.merge("RGB", (n, n, n)),
                            Image.new("RGB", img.size, (128, 128, 128)), scale=1)
    return Image.blend(img, ImageChops.add(img, d), amt * 4)


def film(img):
    """The finishing chain, in capture order: lens, then emulsion, then grade,
    then the grain that sits on top of all of it."""
    img = chroma(img)
    img = soft_corners(img)
    img = halation(img)
    img = anamorphic(img)
    img = film_curve(img)
    return grain(img)


# ── text helpers ───────────────────────────────────────────────────────────
def tracked(d, xy, text, fnt, fill, track=0.0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + track
    return x - xy[0]


def tracked_w(d, text, fnt, track=0.0):
    return sum(d.textlength(c, font=fnt) + track for c in text)


# ── segment renderers ──────────────────────────────────────────────────────
# Each takes (p, dur): p is seconds into the shot, dur its full length. They
# are called with p > dur while the next shot transitions over them, so the
# camera keeps moving through the cut instead of freezing on it.

def seg_talkinghead(p, dur):
    return kenburns("talkinghead", p, dur, 1.00, 0.80, 0.10, 0.30, 0.24, 0.36)


def seg_nightcity(p, dur):
    return kenburns("nightcity", p, dur, 0.82, 0.82, 0.02, 0.30, 0.62, 0.22)


def seg_stage(p, dur):
    return kenburns("stage", p, dur, 0.72, 0.98, 0.42, 0.40, 0.30, 0.30)


def hold_mid(u, hold=0.34):
    """Wipe in, pause dead-centre, then finish.

    A linear sweep looks like a transition; pausing at the halfway line is what
    you actually do when you're checking a grade against the plate. It also
    earns the labels their screen time: on a phone, object-fit:cover throws away
    everything outside the middle 416px, so LOG and GRADED are only both legible
    while the wipe is near centre. The hold turns that from 14% of the travel
    into most of the shot.
    """
    a = (1 - hold) / 2
    if u < a:
        return ease(u / a) * 0.5
    if u < a + hold:
        return 0.5
    return 0.5 + ease((u - a - hold) / a) * 0.5


def seg_product(p, dur):
    """The grade demo: one shot, log on the right, graded on the left, with
    the wipe travelling across it so you watch the correction happen."""
    base = kenburns("product", p, dur, 0.96, 0.80, 0.50, 0.40, 0.46, 0.44)
    graded, logged = to_graded(base), to_log(base)

    x = int(OW * hold_mid(clamp((p - 0.45) / (dur - 1.1))))
    img = graded.copy()
    if x < OW:
        img.paste(logged.crop((x, 0, OW, OH)), (x, 0))
    d = ImageDraw.Draw(img, "RGBA")
    if 0 < x < OW:
        d.rectangle([x - 2, 0, x + 1, OH], fill=(255, 244, 232, 230))
        d.rectangle([x + 2, 0, x + 32, OH], fill=(255, 43, 43, 44))

    a = int(255 * clamp(min(ease_out(p / 0.3), 1 - ease_in((p - (dur - 0.4)) / 0.3))))
    if a > 4:
        # labels ride either side of the wipe so the difference is legible
        lw = tracked_w(d, "GRADED", F_SMALL, 3.2)
        tracked(d, (max(18, x - lw - 28), int(OH * .34)), "GRADED", F_SMALL, BONE + (a,), 3.2)
        tracked(d, (min(OW - 116, x + 28), int(OH * .34)), "LOG", F_SMALL, BONE2 + (a,), 3.2)
    return img


TITLE_CARD = "GOLDEN HOUR"
TITLE_SUB = "DOC SERIES  ·  CH 02"


def seg_sunset(p, dur):
    """The motion-graphics beat — a title card that builds itself, then leaves.

    It says GOLDEN HOUR, not a name: the page already says who I am twice over
    right underneath, and a name card is the intro this reel deliberately
    doesn't have. A chapter card demos the same three moves — rule, mask
    reveal, self-drawing underline — and reads as actual client work.
    """
    img = kenburns("sunset", p, dur, 0.94, 0.78, 0.44, 0.34, 0.34, 0.40)
    d = ImageDraw.Draw(img, "RGBA")
    out = clamp(1 - ease_in((p - (dur - 0.65)) / 0.45))
    mid, y0 = OW // 2, int(OH * .21)

    # the rule opens outward from the centre
    bar = int(96 * ease_out((p - 0.15) / 0.5))
    if bar > 1:
        d.rectangle([mid - bar, y0, mid + bar, y0 + 5], fill=RED + (int(255 * out),))

    # the title rises out from under the rule — a mask reveal, not a fade
    nq = ease_out((p - 0.32) / 0.55)
    if nq > 0.01:
        LW, LH = 620, 74
        lay = Image.new("RGBA", (LW, LH), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        tw = tracked_w(ld, TITLE_CARD, F_TITLE, 5.0)
        tracked(ld, ((LW - tw) / 2, -3), TITLE_CARD, F_TITLE,
                BONE + (int(255 * out),), 5.0)
        vis = max(1, int(LH * nq))
        part = lay.crop((0, 0, LW, vis))
        img.paste(part, (mid - LW // 2, y0 + 24 + (LH - vis)), part)

    sq = clamp((p - 0.62) / 0.5)
    if sq > 0.01:
        w = tracked_w(d, TITLE_SUB, F_SMALL, 3.4)
        tracked(d, (mid - w / 2, y0 + 108), TITLE_SUB, F_SMALL,
                BONE2 + (int(255 * ease_out(sq) * out),), 3.4)

    # an underline that draws itself, left to right — the classic build
    uq = ease_out((p - 0.88) / 0.6)
    if uq > 0.01:
        half = int(150 * uq)
        d.rectangle([mid - 150, y0 + 146, mid - 150 + half * 2, y0 + 147],
                    fill=BONE2 + (int(150 * out),))
    return img


# ── icon set ───────────────────────────────────────────────────────────────
# Drawn as shapes rather than glyphs so they scale and animate cleanly. Each
# takes (draw, cx, cy, s, colour, phase) and fits inside an s-by-s box.

def ic_play(d, cx, cy, s, col, phase):
    w = max(2, int(s * .075))
    d.rounded_rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                        radius=s * .26, outline=col, width=w)
    t = s * .21
    d.polygon([(cx - t * .62, cy - t), (cx - t * .62, cy + t), (cx + t, cy)], fill=col)


def ic_heart(d, cx, cy, s, col, phase):
    r = s * .25
    d.ellipse([cx - r * 1.88, cy - r * 1.5, cx - r * .08, cy + r * .3], fill=col)
    d.ellipse([cx + r * .08, cy - r * 1.5, cx + r * 1.88, cy + r * .3], fill=col)
    d.polygon([(cx - r * 1.84, cy - r * .38), (cx + r * 1.84, cy - r * .38),
               (cx, cy + r * 1.72)], fill=col)


def ic_wave(d, cx, cy, s, col, phase):
    """Live audio levels — the one icon that keeps moving after it lands."""
    n, bw, gap = 5, s * .11, s * .08
    total = n * bw + (n - 1) * gap
    x = cx - total / 2
    for i in range(n):
        h = s * .52 * (0.26 + 0.74 * abs(math.sin(phase * 6.2 + i * 0.85)))
        d.rounded_rectangle([x, cy - h / 2, x + bw, cy + h / 2], radius=bw / 2, fill=col)
        x += bw + gap


def ic_bell(d, cx, cy, s, col, phase):
    w = s * .32
    d.pieslice([cx - w, cy - w * 1.5, cx + w, cy + w * .9], 180, 360, fill=col)
    d.rectangle([cx - w, cy - w * .4, cx + w, cy + w * .3], fill=col)
    d.rounded_rectangle([cx - w * 1.3, cy + w * .3, cx + w * 1.3, cy + w * .58],
                        radius=w * .14, fill=col)
    d.ellipse([cx - w * .26, cy + w * .66, cx + w * .26, cy + w * 1.18], fill=col)


def ic_ring(d, cx, cy, s, col, phase):
    """A progress ring that fills as it sits there."""
    r = s * .42
    w = max(2, int(s * .085))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col[:3] + (int(col[3] * .28),), width=w)
    d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 300 * ease_out(phase * 1.6),
          fill=col, width=w)


ICONS = [ic_play, ic_heart, ic_wave, ic_bell, ic_ring]
ICON_HOT = 1                        # the heart takes the accent colour

CAPTION = ["SHORT", "FORM", "CAPTIONS"]
CAPTION_HOT = "CAPTIONS"            # the one word that takes the accent


def ease_back(t, s=1.9):
    """Overshoot, then settle — how a graphic 'lands' instead of just fading."""
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def seg_neon(p, dur):
    """Fast cuts, an icon row that pops in on the beat, and word-by-word
    captions. Everything is centred: the hero video is object-fit:cover, so on
    a phone only the middle quarter of the frame survives the crop."""
    img = kenburns("neon", p, dur, 0.98, 0.68, 0.50, 0.50, 0.50, 0.48)

    # beat cuts — a jolt of scale every 0.28s, the way a fast edit lands
    if int(p / 0.28) % 2 == 1:
        k = 1.045
        cw, ch = int(OW / k), int(OH / k)
        img = img.crop(((OW - cw) // 2, (OH - ch) // 2,
                        (OW - cw) // 2 + cw, (OH - ch) // 2 + ch)) \
                 .resize((OW, OH), Image.BILINEAR)
    if p % 0.28 < 0.05 and p < dur - 0.5:
        img = Image.blend(img, Image.new("RGB", (OW, OH), (255, 60, 48)), 0.16)

    d = ImageDraw.Draw(img, "RGBA")
    out = clamp(1 - ease_in((p - (dur - 0.85)) / 0.45))
    mid = OW // 2

    # Icon row — each one punches in a beat after the last. The row has to fit
    # inside the middle ~26% of the frame: that is all a 375px phone sees once
    # object-fit:cover has cropped a 16:9 video into a tall hero. That band is
    # ~416px wide here, and ease_back overshoots past k=1, so the row is sized
    # to leave real margin rather than to just barely clear the edge.
    size, gap = 54, 18
    span = len(ICONS) * size + (len(ICONS) - 1) * gap
    for i, fn in enumerate(ICONS):
        age = p - 0.10 - i * 0.11
        if age <= 0:
            break
        k = ease_back(age / 0.30)
        a = int(235 * clamp(age / 0.12) * out)
        if a < 4:
            continue
        col = (RED if i == ICON_HOT else BONE) + (a,)
        cx = mid - span / 2 + size / 2 + i * (size + gap)
        # age passes through unclamped so the live icons keep animating after
        # they've landed
        fn(d, cx, int(OH * .19), size * k, col, age)

    # captions swap word by word on the beat, one at a time, centred — which
    # is what short-form captions actually look like
    raw = (p - 0.34) / 0.38
    if raw > 0:
        i = int(raw)
        # hold the last word instead of letting it re-pop every beat
        word = CAPTION[min(i, len(CAPTION) - 1)]
        wq = 1.0 if i >= len(CAPTION) else clamp((raw - i) / 0.34)
        a = int(255 * ease_out(wq) * out)
        if a > 4:
            w = d.textlength(word, font=F_CAP)
            # .27 rather than mid-frame: on a phone the hero's own slate line
            # sits at roughly 41% of the video's height, and a caption plate
            # down there lands right on top of it
            y = int(OH * .27) - int(14 * (1 - ease_out(wq)))
            col = (RED if word == CAPTION_HOT else BONE) + (a,)
            # a soft plate behind the word so it holds up over busy footage
            d.rounded_rectangle([mid - w / 2 - 22, y - 6, mid + w / 2 + 22, y + 68],
                                radius=4, fill=(11, 11, 12, int(104 * out * ease_out(wq))))
            d.text((mid - w / 2, y), word, font=F_CAP, fill=col)
    return img


# ── timeline ───────────────────────────────────────────────────────────────
# (renderer, duration, transition-in, transition-length)
TIMELINE = [
    (seg_talkinghead, 2.40, None,     0.00),
    (seg_nightcity,   2.20, whip,     0.34),
    (seg_stage,       2.20, dissolve, 0.46),
    (seg_product,     3.20, flash,    0.30),
    (seg_sunset,      3.20, barwipe,  0.36),
    (seg_neon,        2.40, whip,     0.28),
]
LOOP_BLEND = 0.40          # dissolve the tail back into frame one so it loops
TOTAL = sum(s[1] for s in TIMELINE)


def frame_at(t):
    """Composite the frame for time t, resolving any transition in flight, then
    run the film chain over the result.

    The finish goes last on purpose — same as a real timeline, where the grade
    and the film emulation sit on the master and not on individual clips. It
    means the burned-in titles bloom and fringe along with everything else,
    which is what stops them reading as a separate layer pasted on top.
    """
    start = 0.0
    for i, (fn, dur, trans, tlen) in enumerate(TIMELINE):
        if t < start + dur or i == len(TIMELINE) - 1:
            local = t - start
            img = fn(local, dur)
            if trans and local < tlen:
                pfn, pdur = TIMELINE[i - 1][0], TIMELINE[i - 1][1]
                prev = pfn(pdur + local, pdur)      # previous shot keeps rolling
                img = trans(prev, img, local / tlen)
            return film(img)
        start += dur
    return film(TIMELINE[-1][0](t - start, TIMELINE[-1][1]))


def render():
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP)
    n = int(TOTAL * FPS)
    first = frame_at(0.0)
    for k in range(n):
        t = k / FPS
        img = frame_at(t)
        # seamless loop: cross back into the opening frame over the last beat
        tail = t - (TOTAL - LOOP_BLEND)
        if tail > 0:
            img = Image.blend(img, first, ease(tail / LOOP_BLEND) * 0.92)
        img.save(os.path.join(TMP, f"f{k:04d}.jpg"), "JPEG", quality=95)
        if k % 24 == 0:
            print(f"  {t:5.2f}s / {TOTAL:.2f}s", flush=True)
    return n


def encode():
    os.makedirs(os.path.dirname(OUT_VIDEO), exist_ok=True)
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-framerate", str(FPS), "-i", os.path.join(TMP, "f%04d.jpg"),
        "-an",
        "-c:v", "libx264", "-preset", "slow", "-crf", "30",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.0",
        "-g", str(FPS * 2), "-movflags", "+faststart",
        OUT_VIDEO,
    ], check=True)
    # poster = the graded side of the colour-grade beat, the best single frame
    frame_at(7.9).save(OUT_POSTER, "JPEG", quality=84, optimize=True, progressive=False)


if __name__ == "__main__":
    print(f"rendering {TOTAL:.2f}s @ {FPS}fps → {int(TOTAL * FPS)} frames")
    render()
    encode()
    print("video  ", OUT_VIDEO, f"{os.path.getsize(OUT_VIDEO) // 1024} KB")
    print("poster ", OUT_POSTER, f"{os.path.getsize(OUT_POSTER) // 1024} KB")
