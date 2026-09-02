#!/usr/bin/env python3
"""
Generates assets/plates/*.jpg — composed cinematic frames used as the source
footage for the hero showreel (see make-reel.py, which animates them).

These are built, not photographed: silhouettes, lit windows, haze beams,
speculars. The point is subject/ground separation and hard highlights, which
is what makes a frame read as footage rather than as a gradient.

    python3 tools/make-plates.py
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

W, H = 1600, 900
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "plates"))
os.makedirs(OUT, exist_ok=True)


# ── helpers ────────────────────────────────────────────────────────────────
def radial(size, cx, cy, rx, ry, power=2.0, blur=None):
    """Soft elliptical falloff mask."""
    w, h = size
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    steps = 64
    for i in range(steps, 0, -1):
        fx, fy = rx * i / steps, ry * i / steps
        d.ellipse([cx - fx, cy - fy, cx + fx, cy + fy],
                  fill=int(255 * (1 - i / steps) ** power))
    return m.filter(ImageFilter.GaussianBlur(blur if blur is not None else max(rx, ry) * 0.12))


def light(img, colour, mask, strength=1.0):
    """Screen-ish light pool: push colour in through a mask."""
    if strength != 1.0:
        mask = mask.point(lambda v: int(v * strength))
    return Image.composite(Image.new("RGB", img.size, colour), img, mask)


def add_layer(img, colour, mask, strength=1.0):
    """Additive light — for beams and speculars that should blow out."""
    lay = Image.new("RGB", img.size, (0, 0, 0))
    Image.composite(Image.new("RGB", img.size, colour), lay, mask)
    lay = Image.composite(Image.new("RGB", img.size, colour), lay,
                          mask.point(lambda v: int(v * strength)))
    return ImageChops.add(img, lay)


def rim(mask, dx, dy, softness=3):
    """The crescent of light along one edge of a silhouette."""
    shifted = mask.transform(mask.size, Image.AFFINE, (1, 0, dx, 0, 1, dy))
    return ImageChops.subtract(mask, shifted).filter(ImageFilter.GaussianBlur(softness))


def grain(img, amount=0.055, seed=1):
    random.seed(seed)
    n = Image.effect_noise(img.size, 26).convert("L")
    n = ImageChops.offset(n, seed * 37, seed * 19)
    noise_rgb = Image.merge("RGB", (n, n, n))
    grey = Image.new("RGB", img.size, (128, 128, 128))
    delta = ImageChops.subtract(noise_rgb, grey, scale=1)
    return Image.blend(img, ImageChops.add(img, delta), amount * 4)


def vignette(img, strength=1.0, edge=(3, 3, 4)):
    v = Image.new("L", img.size, 0)
    ImageDraw.Draw(v).ellipse(
        [-int(W * 0.26), -int(H * 0.40), int(W * 1.26), int(H * 1.40)], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(150))
    if strength != 1.0:
        v = v.point(lambda x: int(255 - (255 - x) * strength))
    return Image.composite(img, Image.new("RGB", img.size, edge), v)


def bokeh(size, n, seed, rmin=18, rmax=70, ymax=1.0):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    random.seed(seed)
    for _ in range(n):
        r = random.randint(rmin, rmax)
        x = random.randint(-40, size[0] + 40)
        y = random.randint(-40, int(size[1] * ymax))
        a = random.randint(60, 190)
        d.ellipse([x - r, y - r, x + r, y + r], fill=a)          # soft body
        d.ellipse([x - r * .74, y - r * .74, x + r * .74, y + r * .74], fill=int(a * .5))
    return m.filter(ImageFilter.GaussianBlur(6))


def turbulence(size, seed, scale=44, floor=96):
    """A soft cloudy field, normalised so it modulates without darkening.

    Haze is never smooth. Beams cutting through a smooth field is the exact
    reason a stage plate reads as a gradient with stripes on it rather than as
    air with light in it.
    """
    random.seed(seed)
    n = Image.effect_noise(size, 110).convert("L")
    n = ImageChops.offset(n, seed * 53, seed * 31)
    n = n.filter(ImageFilter.GaussianBlur(scale))
    lo, hi = n.getextrema()
    if hi > lo:
        n = n.point(lambda v: floor + (v - lo) * (255 - floor) // (hi - lo))
    return n


def head_and_shoulders(size, cx, scale=1.0):
    """Interview framing silhouette, returned alongside a separate hair mask.

    Nothing here is symmetrical, because nothing about a person sitting in a
    chair is: the head leans off the body axis and the right shoulder runs wider
    and lower. The hair comes back on its own so it can be textured and rimmed
    separately — a head whose outline is one clean unbroken curve reads as an
    avatar icon no matter how well the rest of it is lit.
    """
    w, h = size
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    hr = 132 * scale                      # head radius
    hy = h * 0.35                         # head centre
    lean = hr * .07                       # head off the body axis
    hx = cx + lean
    d.ellipse([hx - hr * .74, hy - hr * .92, hx + hr * .78, hy + hr * .98], fill=255)
    # The jaw is a second, narrower ellipse set lower and slightly forward. That
    # one overlap is most of the difference between a head and a circle.
    d.ellipse([hx - hr * .56, hy - hr * .10, hx + hr * .66, hy + hr * 1.06], fill=255)
    d.rounded_rectangle([cx + lean * .5 - hr * .40, hy + hr * .62,
                         cx + lean * .5 + hr * .40, hy + hr * 1.52],
                        radius=int(hr * .26), fill=255)                 # neck
    # Shoulders are a wide, shallow arc — horizontal radius ~2.6x the vertical.
    # Get that ratio wrong and the figure turns into a chess pawn. Right side
    # runs wider and lower so the line across the body isn't level.
    d.pieslice([cx - hr * 2.82, hy + hr * 1.30, cx + hr * 3.06, hy + hr * 2.96],
               180, 360, fill=255)
    # Below the shoulders the torso runs almost straight down, leaning out by a
    # few degrees. A plain rectangle leaves an edge exactly parallel to the
    # frame and reads as a pasted-on cutout; flare it hard and you get a
    # trapezoid instead of a body. The lean wants to be barely perceptible.
    top = hy + hr * 2.04
    d.polygon([(cx - hr * 2.82, top), (cx + hr * 3.06, top),
               (cx + hr * 3.22, h), (cx - hr * 2.96, h)], fill=255)

    # Hair: a shell over the crown with blobs breaking the edge, so the outline
    # is ragged where hair catches the rim and smooth where skin does.
    hairm = Image.new("L", size, 0)
    hd = ImageDraw.Draw(hairm)
    hd.ellipse([hx - hr * .82, hy - hr * 1.00, hx + hr * .86, hy + hr * .44], fill=255)
    random.seed(97)
    for _ in range(24):
        a = random.uniform(math.pi * 1.02, math.pi * 1.98)
        rr = hr * random.uniform(.74, .94)
        px, py = hx + math.cos(a) * rr * .80, hy + math.sin(a) * rr
        s = random.randint(11, 30)
        hd.ellipse([px - s, py - s, px + s, py + s], fill=255)
    hairm = hairm.filter(ImageFilter.GaussianBlur(2.4))
    m = ImageChops.lighter(m, hairm)
    return m.filter(ImageFilter.GaussianBlur(1.5)), hairm


def finish(img, seed, grain_amt=.05, vig=1.0, bright=1.0, contrast=1.0):
    """Grain, vignette and the exposure lift.

    The lift matters more than it looks like it should: these plates sit under
    a scrim with body copy over them, so a plate that reads fine on its own
    disappears into the page. Expose for the hero, not for the file.

    Grain is scaled right down here because the reel adds its own at output
    resolution. Grain baked into a plate gets zoomed by the camera move, so it
    breathes — real grain sits on the print and never changes size.
    """
    if bright != 1.0:
        img = ImageEnhance.Brightness(img).enhance(bright)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    return vignette(grain(img, grain_amt * 0.35, seed), vig)


# ══ 01 · TALKING HEAD ══════════════════════════════════════════════════════
def plate_talkinghead():
    img = Image.new("RGB", (W, H), (20, 15, 13))
    img = light(img, (118, 62, 38), radial((W, H), W * .70, H * .34, W * .58, H * .74), .95)
    img = light(img, (226, 124, 58), radial((W, H), W * .78, H * .26, W * .32, H * .42, 2.2), .82)
    img = light(img, (40, 56, 88), radial((W, H), W * .08, H * .78, W * .42, H * .52), .60)

    # blurred practical lights behind the subject
    img = light(img, (255, 206, 148), bokeh((W, H), 18, 3, 22, 64, .72), .60)
    img = img.filter(ImageFilter.GaussianBlur(9))          # background is out of focus

    cx, hy, hr = W * .29, H * .35, 132.0
    sil, hairm = head_and_shoulders((W, H), cx, 1.0)

    # The subject gets lit, not filled. A flat fill is precisely what makes a
    # silhouette read as a logo: the eye expects a key to fall off across a
    # body, so the near shoulder carries a warm mid-tone and the far side dies
    # to almost nothing. Everything after this is modelling on that falloff.
    subj = Image.new("RGB", (W, H), (8, 7, 9))
    subj = light(subj, (88, 58, 42),
                 radial((W, H), cx + hr * 1.5, hy + hr * .2, W * .26, H * .42, 1.5), .95)
    subj = light(subj, (142, 94, 64),
                 radial((W, H), cx + hr * .64, hy + hr * .16, hr * 1.1, hr * 1.2, 2.0), .62)
    sd = ImageDraw.Draw(subj, "RGBA")
    sd.ellipse([cx - hr * .70, hy + hr * .30, cx + hr * .45, hy + hr * 1.15],
               fill=(10, 8, 10, 150))                       # cheek into jaw
    sd.ellipse([cx - hr * .55, hy + hr * .86, cx + hr * .62, hy + hr * 1.62],
               fill=(9, 7, 9, 195))                         # chin shadow down the neck
    # Collar, then folds running down from it. Cloth is the cheapest interior
    # detail there is, and a torso with none reads as a paper cutout.
    sd.line([(cx - hr * .62, hy + hr * 1.44), (cx + hr * .06, hy + hr * 1.88),
             (cx + hr * .70, hy + hr * 1.38)],
            fill=(158, 106, 74, 62), width=7, joint="curve")
    for fx, fa in ((-1.44, 42), (-0.60, 28), (0.94, 52), (1.88, 34)):
        sd.line([(cx + hr * fx, hy + hr * 2.06), (cx + hr * (fx * 1.07 + .12), H)],
                fill=(196, 134, 94, fa), width=5)
    subj = subj.filter(ImageFilter.GaussianBlur(6))
    img = Image.composite(subj, img, sil)

    # rim() with a positive dx lights the right-hand edge, which is the side the
    # key is actually on. It's then multiplied down by a falloff of its own: an
    # even crescent all the way round the body is the loudest "this is an icon"
    # signal there is, so the light is hot at the shoulder and gone by the
    # bottom of frame.
    key = ImageChops.multiply(rim(sil, 17, 5, 4),
                              radial((W, H), cx + hr * 1.2, hy + hr * .4, W * .30, H * .52, 1.2))
    img = light(img, (255, 186, 116), key, 1.0)
    hairlit = ImageChops.multiply(rim(hairm, 13, 4, 3),
                                  radial((W, H), cx + hr * .8, hy - hr * .4,
                                         hr * 2.2, hr * 2.0, 1.3))
    img = light(img, (255, 216, 162), hairlit, .95)
    # the kicker stays weak on purpose: light both edges evenly and the
    # silhouette stops reading as lit and starts reading as an outlined icon
    img = light(img, (92, 132, 196), rim(sil, -10, -3, 7), .30)       # cool kicker, left

    # A foreground layer, badly out of focus, crossing the near edges. Real
    # interview footage almost always has one — a stand, a doorframe, a plant —
    # and it's the cheapest depth cue going, because it makes the eye read three
    # distances instead of two.
    fg = Image.new("L", (W, H), 0)
    fd = ImageDraw.Draw(fg)
    fd.polygon([(-40, H), (-40, H * .28), (W * .05, H * .20),
                (W * .11, H * .64), (W * .07, H)], fill=255)
    fd.ellipse([W * .92, H * .50, W * 1.24, H * 1.26], fill=255)
    fg = fg.filter(ImageFilter.GaussianBlur(28))
    img = Image.composite(Image.new("RGB", (W, H), (13, 9, 10)), img, fg)

    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([W * .855, H * .175, W * .875, H * .205], fill=(255, 238, 204, 225))  # hard specular
    return finish(img, 1, .05, .92, bright=1.16, contrast=1.10)


# ══ 02 · NIGHT CITY ════════════════════════════════════════════════════════
def plate_nightcity():
    img = Image.new("RGB", (W, H), (6, 8, 14))
    img = light(img, (18, 40, 74), radial((W, H), W * .30, H * .30, W * .70, H * .80), .9)
    img = light(img, (120, 190, 220), radial((W, H), W * .62, H * .12, W * .26, H * .30, 2.4), .35)

    # building blocks with lit windows, drawn sharp then softened by distance
    city = Image.new("RGB", (W, H), (0, 0, 0))
    cm = Image.new("L", (W, H), 0)
    cd, md = ImageDraw.Draw(city), ImageDraw.Draw(cm)
    random.seed(11)
    x = -60
    while x < W + 60:
        bw = random.randint(90, 210)
        top = random.randint(int(H * .18), int(H * .62))
        cd.rectangle([x, top, x + bw, H], fill=(9, 12, 20))
        md.rectangle([x, top, x + bw, H], fill=255)
        for wy in range(top + 22, int(H * .92), 34):
            for wx in range(x + 14, x + bw - 14, 26):
                if random.random() < .34:
                    col = (255, 198, 128) if random.random() < .82 else (168, 206, 240)
                    f = random.uniform(.45, 1.0)     # one factor for all channels,
                    cd.rectangle([wx, wy, wx + 11, wy + 17],  # or the block goes rainbow
                                 fill=(int(col[0] * f), int(col[1] * f), int(col[2] * f)))
        x += bw + random.randint(6, 26)
    city = city.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.composite(city, img, cm.filter(ImageFilter.GaussianBlur(1)))

    img = add_layer(img, (90, 170, 230), bokeh((W, H), 22, 7, 16, 58, .78), .30)
    img = img.filter(ImageFilter.GaussianBlur(2.4))

    # wet-street bounce along the bottom
    img = light(img, (46, 84, 130), radial((W, H), W * .5, H * 1.06, W * .8, H * .30), .5)
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(5):
        yy = random.randint(int(H * .84), H)
        d.line([(0, yy), (W, yy + random.randint(-6, 6))], fill=(150, 210, 255, 26), width=2)
    return finish(img, 2, .06, 1.0, bright=1.22, contrast=1.08)


# ══ 03 · STAGE / CONCERT ═══════════════════════════════════════════════════
def plate_stage():
    img = Image.new("RGB", (W, H), (8, 5, 12))
    img = light(img, (58, 22, 78), radial((W, H), W * .5, H * .34, W * .8, H * .8), .8)

    # Haze beams. They converge from a truss above frame rather than running
    # straight down: parallel bars of even width and even spacing is a curtain
    # pattern, and a lighting rig is a row of heads at different angles.
    beams = Image.new("L", (W, H), 0)
    bd = ImageDraw.Draw(beams)
    random.seed(23)
    rig_y = -H * 0.34
    for i in range(7):
        ox = W * (0.10 + i * 0.135) + random.randint(-44, 44)
        aim = ox + random.randint(-430, 430)
        wtop, wbot = random.randint(15, 38), random.randint(90, 250)
        bd.polygon([(ox - wtop, rig_y), (ox + wtop, rig_y),
                    (aim + wbot, H * 1.04), (aim - wbot, H * 1.04)],
                   fill=random.randint(55, 195))
    beams = beams.filter(ImageFilter.GaussianBlur(22))
    # the beams are only visible because of what's in the air, so they inherit
    # its structure — this is the step that turns stripes into atmosphere
    beams = ImageChops.multiply(beams, turbulence((W, H), 5, 46, 104))
    img = add_layer(img, (196, 96, 230), beams, .58)
    img = add_layer(img, (90, 170, 255),
                    beams.transform((W, H), Image.AFFINE, (1, 0, 180, 0, 1, 0)), .30)
    # loose haze filling the room, heaviest low where the smoke sits
    img = add_layer(img, (128, 86, 168),
                    ImageChops.multiply(turbulence((W, H), 9, 74, 0),
                                        radial((W, H), W * .5, H * .82, W * .9, H * .58)), .34)

    img = img.filter(ImageFilter.GaussianBlur(3))
    img = add_layer(img, (255, 214, 255), bokeh((W, H), 14, 31, 10, 30, .5), .40)

    # A performer, backlit. The rig needs something to be pointing at — beams
    # crossing an empty stage read as an abstract, not as coverage.
    fig = Image.new("L", (W, H), 0)
    fd = ImageDraw.Draw(fig)
    px, py = W * .46, H * .56
    fd.ellipse([px - 33, py - 39, px + 33, py + 41], fill=255)
    fd.polygon([(px - 80, H * .99), (px - 52, py + 32), (px + 50, py + 28),
                (px + 94, H * .99)], fill=255)
    fd.polygon([(px - 148, py + 158), (px - 58, py + 46), (px - 30, py + 70),
                (px - 120, py + 184)], fill=255)          # arm out, mid-gesture
    fig = fig.filter(ImageFilter.GaussianBlur(3))
    img = Image.composite(Image.new("RGB", (W, H), (6, 4, 9)), img, fig)
    img = light(img, (238, 174, 255), rim(fig, -9, -3, 3), .85)
    img = light(img, (140, 200, 255), rim(fig, 8, 2, 4), .55)

    # crowd — sharp heads along the bottom edge
    crowd = Image.new("L", (W, H), 0)
    cd = ImageDraw.Draw(crowd)
    random.seed(41)
    for _ in range(46):
        r = random.randint(26, 54)
        cx = random.randint(-40, W + 40)
        cy = random.randint(int(H * .84), int(H * 1.02))
        cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        cd.rectangle([cx - r * 1.5, min(cy + r * .6, H - 1), cx + r * 1.5, H], fill=255)
    img = Image.composite(Image.new("RGB", (W, H), (5, 4, 8)), img,
                          crowd.filter(ImageFilter.GaussianBlur(2)))
    return finish(img, 3, .06, 1.0, bright=1.18, contrast=1.06)


# ══ 04 · PRODUCT / AD ══════════════════════════════════════════════════════
def plate_product():
    img = Image.new("RGB", (W, H), (10, 10, 12))
    img = light(img, (54, 58, 70), radial((W, H), W * .5, H * .30, W * .62, H * .66), .85)
    img = light(img, (190, 66, 40), radial((W, H), W * .90, H * .70, W * .34, H * .44), .55)
    img = img.filter(ImageFilter.GaussianBlur(7))          # soft sweep behind

    # the hero object — a hard-edged block, lit from one side
    obj = Image.new("L", (W, H), 0)
    od = ImageDraw.Draw(obj)
    ox, oy, ow, oh = W * .40, H * .26, W * .20, H * .54
    od.rounded_rectangle([ox, oy, ox + ow, oy + oh], radius=26, fill=255)
    img = Image.composite(Image.new("RGB", (W, H), (17, 17, 21)), img, obj)
    img = light(img, (236, 240, 255), rim(obj, 9, 0, 2), 1.0)        # sharp edge highlight
    img = light(img, (255, 120, 70), rim(obj, -13, -2, 5), .70)      # warm kick opposite

    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([ox + ow * .16, oy + oh * .10, ox + ow * .23, oy + oh * .82],
                fill=(255, 255, 255, 40))                            # specular strip
    # tabletop reflection
    refl = img.crop((0, int(oy + oh - 40), W, int(oy + oh))).transpose(Image.FLIP_TOP_BOTTOM)
    refl = refl.resize((W, int(H * .22))).filter(ImageFilter.GaussianBlur(11))
    fade = Image.linear_gradient("L").resize((W, int(H * .22)))
    img.paste(refl, (0, int(oy + oh)), fade.point(lambda v: int((255 - v) * .38)))
    return finish(img, 4, .045, .90, bright=1.20, contrast=1.12)


# ══ 05 · SUNSET / DOC ══════════════════════════════════════════════════════
def plate_sunset():
    img = Image.new("RGB", (W, H), (16, 12, 16))
    d = ImageDraw.Draw(img)
    horizon = int(H * .68)
    for y in range(horizon):                                # sky ramp
        t = y / horizon
        d.line([(0, y), (W, y)],
               fill=(int(22 + 224 * t ** 2.1), int(20 + 128 * t ** 2.4), int(48 + 62 * t ** 3)))
    for y in range(horizon, H):                             # ground ramp
        t = (y - horizon) / (H - horizon)
        d.line([(0, y), (W, y)], fill=(int(52 - 34 * t), int(28 - 18 * t), int(22 - 14 * t)))

    sx, sy = W * .64, horizon - H * .04
    img = add_layer(img, (255, 176, 96), radial((W, H), sx, sy, W * .34, H * .40, 2.6), .55)

    d = ImageDraw.Draw(img, "RGBA")
    random.seed(59)
    # Cloud bars, warm-dark. Each one is a run of overlapping ellipses rather
    # than a rounded rectangle: a cloud with a constant thickness and two
    # matching ends is a shape, and clouds don't have ends.
    for _ in range(11):
        cy = random.randint(int(H * .12), horizon - 30)
        cx = random.randint(-100, W)
        cw = random.randint(300, 900)
        th = random.randint(10, 34)
        a = random.randint(58, 116)
        step = max(24, cw // 14)
        for bx in range(cx, cx + cw, step):
            f = 1 - abs((bx - cx) / cw - .5) * 1.7          # thin out at the tails
            bh = max(4, th * f * random.uniform(.6, 1.25))
            d.ellipse([bx - step, cy - bh / 2, bx + step * 1.5, cy + bh / 2],
                      fill=(64, 30, 30, int(a * max(.25, f))))
    img = img.filter(ImageFilter.GaussianBlur(7))           # clouds belong in the haze

    # sun goes on after the haze blur, so the disc keeps a hard edge
    img = add_layer(img, (255, 196, 130), radial((W, H), sx, sy, 260, 210, 2.4), .34)
    ImageDraw.Draw(img, "RGBA").ellipse([sx - 58, sy - 58, sx + 58, sy + 58],
                                        fill=(255, 240, 206, 255))
    img = add_layer(img, (255, 226, 182), radial((W, H), sx, sy, 150, 150, 3.0), .55)

    # sharp foreground ridge — the only in-focus element
    ridge = Image.new("L", (W, H), 0)
    rd = ImageDraw.Draw(ridge)
    pts = [(0, H)]
    random.seed(67)
    yy = horizon + 34
    for xx in range(0, W + 70, 70):
        yy += random.randint(-34, 30)
        pts.append((xx, max(horizon + 8, min(H - 40, yy))))
    pts.append((W, H))
    rd.polygon(pts, fill=255)
    img = Image.composite(Image.new("RGB", (W, H), (10, 8, 10)), img, ridge)
    img = light(img, (255, 170, 110), rim(ridge, 0, 6, 2), .60)
    return finish(img, 5, .05, .85, bright=1.10, contrast=1.06)


# ══ 06 · NEON CORRIDOR (gaming / anime) ════════════════════════════════════
def plate_neon():
    img = Image.new("RGB", (W, H), (6, 6, 12))
    vx, vy = W * .52, H * .48
    img = light(img, (18, 26, 60), radial((W, H), vx, vy, W * .7, H * .8), .9)

    lines = Image.new("L", (W, H), 0)
    ld = ImageDraw.Draw(lines)
    random.seed(83)
    # Rails at uneven spacing and uneven weight. Perfect symmetry about the
    # vanishing point is the tell here: it's the one thing a camera can't do,
    # because it would have to be exactly on the corridor's axis.
    for i in range(-7, 8):
        j = i + 0.30 * math.sin(i * 2.1)
        ld.line([(vx + j * 240, H + 200), (vx + j * 26, vy)],
                fill=random.randint(150, 210), width=random.randint(4, 6))
        ld.line([(vx + j * 240, -200), (vx + j * 26, vy)],
                fill=random.randint(90, 140), width=random.randint(3, 5))
    for k in range(1, 8):                                   # depth rungs
        f = k / 8
        ld.line([(0, vy + (H - vy) * f ** 2.2), (W, vy + (H - vy) * f ** 2.2)],
                fill=int(70 + 120 * f), width=3)
    img = add_layer(img, (255, 46, 120), lines.filter(ImageFilter.GaussianBlur(9)), .50)
    img = add_layer(img, (255, 255, 255), lines.filter(ImageFilter.GaussianBlur(1.2)), .34)

    strips = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(strips)
    sd.polygon([(0, H * .10), (vx * .92, vy * .96), (vx * .92, vy * 1.04), (0, H * .22)], fill=230)
    sd.polygon([(W, H * .17), (vx * 1.06, vy * .97), (vx * 1.06, vy * 1.05), (W, H * .27)], fill=196)
    img = add_layer(img, (60, 230, 255), strips.filter(ImageFilter.GaussianBlur(14)), .55)
    img = add_layer(img, (220, 255, 255), strips.filter(ImageFilter.GaussianBlur(2)), .40)

    # Depth fog, thickest at the vanishing point. Without it every rail stays
    # equally crisp all the way down the corridor and there is no distance in
    # the frame at all — just a flat pattern converging on a dot.
    img = add_layer(img, (96, 60, 170),
                    ImageChops.multiply(turbulence((W, H), 17, 60, 0),
                                        radial((W, H), vx, vy, W * .46, H * .52, 1.4)), .46)

    img = add_layer(img, (255, 120, 200), bokeh((W, H), 12, 71, 8, 26, .7), .34)
    img = light(img, (10, 8, 18), radial((W, H), W * .5, H * 1.14, W * .9, H * .34), .5)
    return finish(img, 6, .055, 1.0, bright=1.16, contrast=1.08)


PLATES = [
    ("talkinghead", plate_talkinghead),
    ("nightcity",   plate_nightcity),
    ("stage",       plate_stage),
    ("product",     plate_product),
    ("sunset",      plate_sunset),
    ("neon",        plate_neon),
]

if __name__ == "__main__":
    for i, (name, fn) in enumerate(PLATES, 1):
        path = os.path.join(OUT, f"{i:02d}-{name}.jpg")
        fn().save(path, "JPEG", quality=82, optimize=True, progressive=False)
        print(f"{os.path.basename(path):22} {os.path.getsize(path)//1024:>4} KB")
