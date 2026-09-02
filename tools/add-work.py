#!/usr/bin/env python3
"""
add-work.py — drop finished exports in ./incoming, get real cards on the site.

Everything is self-hosted: each video is transcoded to a web-safe H.264 mp4 with
a poster frame and wired straight into index.html's own player. No YouTube
iframe, no Vimeo, no third-party script — the file plays off razerenders.live.

Usage
  python3 tools/add-work.py                     # interactive: asks title + tags
  python3 tools/add-work.py --auto              # no prompts, titles from filenames
  python3 tools/add-work.py --add FILE --title T --tags "A · B" [--slot wide|tall]
  python3 tools/add-work.py --rebuild           # re-emit cards from work.json only
  python3 tools/add-work.py --list              # show the current manifest
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / "incoming"
DONE = INCOMING / "done"
VIDEOS = ROOT / "assets" / "videos"
POSTERS = ROOT / "assets" / "posters"
INDEX = ROOT / "index.html"
MANIFEST = Path(__file__).resolve().parent / "work.json"

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".mpg", ".mpeg"}

# Cloudflare static assets refuse anything over 25 MiB; stay well clear so a
# single long piece can never quietly break the deploy.
MAX_BYTES = 18 * 1024 * 1024

# Wide cards render at most ~1000px across in the layout; 1280 gives retina
# headroom without paying for 4K nobody sees. Tall cards are narrower still.
WIDE_MAX_W, TALL_MAX_W = 1280, 720


def die(msg: str) -> None:
    print(f"\n  ✗  {msg}\n")
    sys.exit(1)


def need(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        die(f"{binary} is not installed. Install it with:  brew install ffmpeg")
    return path


def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", s) or "clip"


def title_from_filename(path: Path) -> str:
    stem = path.stem
    # strip export cruft: "final", "v3", "_1", "1080p", render dates, hashes
    stem = re.sub(r"[_\-. ]+(final|master|export|render|copy|v\d+|\d+p|h?264)\b",
                  " ", stem, flags=re.I)
    stem = re.sub(r"\s*\(\d+\)\s*$", "", stem)
    stem = re.sub(r"[_\-.]+", " ", stem)
    stem = re.sub(r"\s{2,}", " ", stem).strip()
    return stem.title() if stem.islower() or stem.isupper() else stem or path.stem


def probe(path: Path) -> dict:
    out = subprocess.run(
        [need("ffprobe"), "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        die(f"ffprobe could not read {path.name}:\n{out.stderr.strip()}")
    data = json.loads(out.stdout or "{}")
    streams = data.get("streams") or []
    if not streams:
        die(f"{path.name} has no video stream.")
    st = streams[0]
    has_audio = subprocess.run(
        [need("ffprobe"), "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    ).stdout.strip() != ""
    return {
        "w": int(st["width"]),
        "h": int(st["height"]),
        "duration": float((data.get("format") or {}).get("duration") or 0.0),
        "has_audio": has_audio,
    }


def target_scale(info: dict, slot: str) -> str:
    """Even-numbered scale filter, capped by slot, never upscaling."""
    cap = TALL_MAX_W if slot == "tall" else WIDE_MAX_W
    w = min(info["w"], cap)
    return f"scale={w if w % 2 == 0 else w - 1}:-2:flags=lanczos"


def transcode(src: Path, dst: Path, info: dict, slot: str, crf: int) -> None:
    args = [
        need("ffmpeg"), "-y", "-v", "error", "-stats", "-i", str(src),
        "-vf", target_scale(info, slot),
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.0",
        "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p",
        "-g", "48", "-keyint_min", "48", "-sc_threshold", "0",
        # faststart moves the moov atom to the front so the browser can begin
        # playing before the whole file lands — this is what makes it feel instant.
        "-movflags", "+faststart",
    ]
    if info["has_audio"]:
        args += ["-c:a", "aac", "-b:a", "128k", "-ac", "2", "-ar", "48000"]
    else:
        args += ["-an"]
    args.append(str(dst))
    if subprocess.run(args).returncode != 0:
        die(f"ffmpeg failed on {src.name}")


def make_poster(src: Path, dst: Path, info: dict, slot: str) -> None:
    # 30% in usually lands on real content rather than a fade-up from black
    at = max(0.0, info["duration"] * 0.30)
    args = [
        need("ffmpeg"), "-y", "-v", "error", "-ss", f"{at:.3f}", "-i", str(src),
        "-vf", target_scale(info, slot), "-frames:v", "1", "-q:v", "3", str(dst),
    ]
    if subprocess.run(args).returncode != 0:
        die(f"ffmpeg could not grab a poster from {src.name}")


def encode_to_budget(src: Path, dst: Path, info: dict, slot: str) -> None:
    """Encode once at good quality; only step the CRF up if the file is too big."""
    for crf in (22, 25, 28, 31):
        transcode(src, dst, info, slot, crf)
        size = dst.stat().st_size
        print(f"      crf {crf} → {size / 1_048_576:.1f} MB")
        if size <= MAX_BYTES:
            return
    print(f"      ⚠  still {dst.stat().st_size / 1_048_576:.1f} MB — trim the edit "
          f"or split it before publishing.")


# ── card markup ───────────────────────────────────────────────────────────────
# Kept byte-identical to the cards that were already hand-written in index.html
# so a rebuild never quietly restyles the page.

def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def frame_attrs(entry: dict) -> str:
    w, h = entry.get("w", 16), entry.get("h", 9)
    ar = w / h if h else 16 / 9
    if abs(ar - 16 / 9) < 0.02:
        return ' data-ratio="16:9"'
    if abs(ar - 9 / 16) < 0.02:
        return ' data-ratio="9:16"'
    # anything else keeps its own shape rather than being cropped by object-fit
    return f' data-ratio="{w}:{h}" style="aspect-ratio:{w}/{h}"'


def wide_card(entry: dict, n: int) -> str:
    return f"""      <figure class="vcard vcard--wide reveal" data-video>
        <div class="vcard__frame"{frame_attrs(entry)}>
          <video data-src="assets/videos/{entry['slug']}.mp4" poster="assets/posters/{entry['slug']}.jpg" muted loop playsinline preload="none"></video>
          <div class="vcard__grain" aria-hidden="true"></div>
          <div class="vcard__hover"><span>◼ Play · sound</span></div>
          <div class="vplayer" data-controls>
            <button class="vplayer__play" data-play aria-label="Play / pause">
              <svg class="i-play" viewBox="0 0 24 24" width="20" height="20"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>
              <svg class="i-pause" viewBox="0 0 24 24" width="20" height="20"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>
            </button>
            <div class="vplayer__scrub" data-scrub><i data-progress></i></div>
            <span class="vplayer__time" data-time>00:00</span>
            <button class="vplayer__mute" data-mute aria-label="Mute / unmute">
              <svg class="i-muted" viewBox="0 0 24 24" width="18" height="18"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 9l5 5m0-5l-5 5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
              <svg class="i-sound" viewBox="0 0 24 24" width="18" height="18"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a4 4 0 0 1 0 7" stroke="currentColor" stroke-width="1.7" fill="none" stroke-linecap="round"/></svg>
            </button>
            <button class="vplayer__full" data-full aria-label="Fullscreen">
              <svg viewBox="0 0 24 24" width="18" height="18"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" stroke="currentColor" stroke-width="1.7" fill="none" stroke-linecap="round"/></svg>
            </button>
          </div>
        </div>
        <figcaption class="vcard__meta">
          <div class="vcard__title"><span class="num">{n:02d}</span> {esc(entry['title'])}</div>
          <div class="vcard__tags">{esc(entry['tags'])}</div>
        </figcaption>
      </figure>"""


def tall_card(entry: dict, n: int) -> str:
    return f"""      <figure class="vcard vcard--tall reveal" data-video>
        <div class="vcard__frame"{frame_attrs(entry)}>
          <video data-src="assets/videos/{entry['slug']}.mp4" poster="assets/posters/{entry['slug']}.jpg" muted loop playsinline preload="none"></video>
          <div class="vcard__grain" aria-hidden="true"></div>
          <div class="vcard__hover"><span>◼ Tap</span></div>
          <div class="vplayer vplayer--mini" data-controls>
            <button class="vplayer__play" data-play aria-label="Play / pause">
              <svg class="i-play" viewBox="0 0 24 24" width="18" height="18"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>
              <svg class="i-pause" viewBox="0 0 24 24" width="18" height="18"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>
            </button>
            <div class="vplayer__scrub" data-scrub><i data-progress></i></div>
            <button class="vplayer__mute" data-mute aria-label="Mute / unmute">
              <svg class="i-muted" viewBox="0 0 24 24" width="16" height="16"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 9l5 5m0-5l-5 5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
              <svg class="i-sound" viewBox="0 0 24 24" width="16" height="16"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a4 4 0 0 1 0 7" stroke="currentColor" stroke-width="1.7" fill="none" stroke-linecap="round"/></svg>
            </button>
          </div>
        </div>
        <figcaption class="vcard__meta">
          <div class="vcard__title"><span class="num">/{n:02d}</span> {esc(entry['title'])}</div>
          <div class="vcard__tags">{esc(entry['tags'])}</div>
        </figcaption>
      </figure>"""


WIDE_OPEN, WIDE_CLOSE = "<!-- AUTO:WIDE -->", "<!-- /AUTO:WIDE -->"
TALL_OPEN, TALL_CLOSE = "<!-- AUTO:TALL -->", "<!-- /AUTO:TALL -->"


def splice(html: str, open_tag: str, close_tag: str, body: str) -> str:
    i, j = html.find(open_tag), html.find(close_tag)
    if i == -1 or j == -1:
        die(f"index.html is missing the {open_tag} … {close_tag} markers.")
    inner = f"\n{body}\n      " if body else "\n      "
    return html[: i + len(open_tag)] + inner + html[j:]


def toggle_section(html: str, cls: str, show: bool) -> str:
    """`hidden` the whole section when it has no cards — an empty heading with a
    bare rule under it reads as a broken page, not as 'coming soon'."""
    pattern = re.compile(rf'<section class="{cls}"(?: hidden)? id="{cls}">')
    if not pattern.search(html):
        die(f'index.html: could not find <section class="{cls}" id="{cls}">')
    return pattern.sub(
        f'<section class="{cls}"{"" if show else " hidden"} id="{cls}">',
        html, count=1)


def toggle_nav_link(html: str, href: str, show: bool) -> str:
    """A nav link that jumps to a hidden section is a dead link, so it goes with
    the section it points at."""
    pattern = re.compile(rf'<a href="#{href}"(?: hidden)?>')
    return pattern.sub(
        f'<a href="#{href}"{"" if show else " hidden"}>', html, count=1)


def toggle_hero_cta(html: str, show: bool) -> str:
    """Same reasoning for the hero's "See the work" button — with nothing in the
    Work section it would scroll into a void. "Get in touch" carries the hero on
    its own until there are cards again."""
    pattern = re.compile(
        r'<a href="#work" class="btn btn--primary"(?: hidden)?>')
    return pattern.sub(
        f'<a href="#work" class="btn btn--primary"{"" if show else " hidden"}>',
        html, count=1)


def renumber_marks(html: str) -> str:
    """The little 01/02/03 marks are a visible count, so hiding Reels must not
    leave a 02 → 04 gap. Hidden sections keep their old number; nobody sees it,
    and the next rebuild renumbers everything once they have cards again."""
    n = 0

    def bump(m: "re.Match[str]") -> str:
        nonlocal n
        head = html.rfind("<section ", 0, m.start())
        if head != -1 and " hidden " in html[head:html.find(">", head) + 1]:
            return m.group(0)
        n += 1
        return f'<span class="mark">{n:02d}</span>'

    return re.sub(r'<span class="mark">\d+</span>', bump, html)


def rebuild_index(entries: list[dict]) -> None:
    wide = [e for e in entries if e["slot"] == "wide"]
    tall = [e for e in entries if e["slot"] == "tall"]
    html = INDEX.read_text(encoding="utf-8")
    html = splice(html, WIDE_OPEN, WIDE_CLOSE,
                  "\n\n".join(wide_card(e, i) for i, e in enumerate(wide, 1)))
    html = splice(html, TALL_OPEN, TALL_CLOSE,
                  "\n\n".join(tall_card(e, i) for i, e in enumerate(tall, 1)))
    html = toggle_section(html, "work", bool(wide))
    html = toggle_section(html, "reels", bool(tall))
    html = toggle_nav_link(html, "work", bool(wide))
    html = toggle_hero_cta(html, bool(wide))
    html = renumber_marks(html)
    INDEX.write_text(html, encoding="utf-8")
    print(f"  ✓  index.html rebuilt — {len(wide)} long-form, {len(tall)} short-form")


# ── manifest ──────────────────────────────────────────────────────────────────

def load() -> list[dict]:
    if not MANIFEST.exists():
        return []
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"tools/work.json is not valid JSON ({exc}). Fix or delete it.")


def save(entries: list[dict]) -> None:
    MANIFEST.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")


def ingest(src: Path, title: str, tags: str, slot: str | None,
           entries: list[dict]) -> dict:
    info = probe(src)
    if slot is None:
        slot = "tall" if info["h"] > info["w"] else "wide"

    slug = slugify(title)
    taken = {e["slug"] for e in entries}
    base, n = slug, 2
    while slug in taken:
        slug, n = f"{base}-{n}", n + 1

    VIDEOS.mkdir(parents=True, exist_ok=True)
    POSTERS.mkdir(parents=True, exist_ok=True)
    mp4, jpg = VIDEOS / f"{slug}.mp4", POSTERS / f"{slug}.jpg"

    print(f"\n  ▸ {title}")
    print(f"      {info['w']}×{info['h']}  {info['duration']:.1f}s  "
          f"{'sound' if info['has_audio'] else 'silent'}  → {slot} card")
    encode_to_budget(src, mp4, info, slot)
    make_poster(src, jpg, info, slot)

    entry = {
        "slug": slug, "title": title, "tags": tags, "slot": slot,
        "w": info["w"] if slot == "wide" else min(info["w"], TALL_MAX_W),
        "h": info["h"], "duration": round(info["duration"], 2),
        "source": src.name,
    }
    # keep the emitted aspect ratio honest after the scale cap
    cap = TALL_MAX_W if slot == "tall" else WIDE_MAX_W
    if info["w"] > cap:
        entry["w"] = cap
        entry["h"] = max(2, round(info["h"] * cap / info["w"] / 2) * 2)
    entries.append(entry)
    print(f"  ✓  assets/videos/{slug}.mp4  +  assets/posters/{slug}.jpg")
    return entry


def default_tags(slot: str) -> str:
    return "Edit · Color · Sound" if slot == "wide" else "Short Form"


def main() -> None:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--auto", action="store_true",
                    help="no prompts — titles guessed from filenames")
    ap.add_argument("--add", metavar="FILE", help="add one specific file")
    ap.add_argument("--title")
    ap.add_argument("--tags")
    ap.add_argument("--slot", choices=("wide", "tall"))
    ap.add_argument("--rebuild", action="store_true",
                    help="re-emit cards from work.json without touching media")
    ap.add_argument("--list", action="store_true", help="print the manifest")
    args = ap.parse_args()

    entries = load()

    if args.list:
        if not entries:
            print("\n  (nothing on the site yet)\n")
        for e in entries:
            print(f"  {e['slot']:4}  {e['slug']:28}  {e['title']}  —  {e['tags']}")
        return

    if args.rebuild:
        rebuild_index(entries)
        return

    if args.add:
        src = Path(args.add).expanduser()
        if not src.is_file():
            die(f"no such file: {src}")
        info = probe(src)
        slot = args.slot or ("tall" if info["h"] > info["w"] else "wide")
        ingest(src, args.title or title_from_filename(src),
               args.tags or default_tags(slot), slot, entries)
        save(entries)
        rebuild_index(entries)
        return

    INCOMING.mkdir(parents=True, exist_ok=True)
    queue = sorted(p for p in INCOMING.iterdir()
                   if p.is_file() and p.suffix.lower() in VIDEO_EXT)
    if not queue:
        print(f"\n  Drop your finished exports into:\n    {INCOMING}\n"
              f"  then run this again. Vertical files become Reels, "
              f"landscape ones become Selected Work.\n")
        return

    print(f"\n  Found {len(queue)} file(s) in incoming/\n")
    for src in queue:
        info = probe(src)
        slot = "tall" if info["h"] > info["w"] else "wide"
        guess = title_from_filename(src)
        if args.auto:
            title, tags = guess, default_tags(slot)
        else:
            print(f"\n  ── {src.name}  ({info['w']}×{info['h']}, "
                  f"{info['duration']:.0f}s, {slot})")
            title = input(f"     Title [{guess}]: ").strip() or guess
            tags = (input(f"     Tags  [{default_tags(slot)}]: ").strip()
                    or default_tags(slot))
        ingest(src, title, tags, slot, entries)
        save(entries)
        DONE.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(DONE / src.name))

    rebuild_index(entries)
    print("\n  Now double-click publish.command to put it live.\n")


if __name__ == "__main__":
    main()
