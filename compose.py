#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026 and save news.jpg.

A broadsheet: black masthead, a drawn night scene for the lead story
(Russian missiles landing in Poland during NATO drills), five
illustrated story rows, and a ticker. Everything is drawn with PIL;
no generated media, no network. Deterministic: fixed fonts, a seeded
star field, fixed JPEG settings — two runs write identical bytes.

Run:  python3 compose.py   (writes news.jpg next to this file)
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "news.jpg"

W, H = 1024, 1024

# --- palette: cream paper, ink, crimson, gold, navy -------------------------
PAPER = (246, 241, 229)
INK = (22, 34, 46)
BLACK = (14, 18, 24)
CRIMSON = (168, 30, 40)
GOLD = (185, 138, 47)
NAVY = (29, 58, 95)
NAVY_DARK = (14, 30, 51)
GREY = (92, 98, 104)
ROW_BG = (255, 253, 247)
DUSK = (198, 90, 46)
SKY_TOP = (13, 28, 50)
SKY_MID = (38, 62, 96)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w, min_size=10):
    """Largest font size at or under `size` that fits `text` in max_w."""
    s = size
    while s > min_size:
        f = font(path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return font(path, min_size)


def wrap(draw, text, f, max_w, max_lines=2):
    """Word-wrap to at most max_lines; ellipsis only if words are cut."""
    words = text.split()
    lines, cur, used = [], "", 0
    for i, w in enumerate(words):
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
            used = i + 1
        else:
            if cur:
                lines.append(cur)
            cur = w
            used = i + 1
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if used < len(words) and lines:
        # words were cut: ellipsize the last line
        last = lines[-1]
        while last and draw.textlength(last + " …", font=f) > max_w:
            last = last[:-1].rstrip()
        lines[-1] = last + " …"
    return lines


def vgrad(draw, box, top, bottom):
    """Vertical gradient fill inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / span
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def draw_lead_scene(draw):
    """Night over a Polish farm: missile streak, jets, farmhouse, map inset."""
    x0, y0, x1, y1 = 36, 138, 988, 384
    vgrad(draw, (x0, y0, x1, 300), SKY_TOP, SKY_MID)
    vgrad(draw, (x0, 300, x1, 330), SKY_MID, DUSK)
    draw.rectangle([x0, 330, x1, y1], fill=(16, 22, 18))

    rng = random.Random(20261121)
    for _ in range(70):
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, 296)
        r = rng.choice([1, 1, 1, 2])
        draw.ellipse([sx, sy, sx + r, sy + r], fill=(235, 238, 245))

    # moon
    draw.ellipse([880, 158, 916, 194], fill=(240, 236, 214))
    draw.ellipse([892, 166, 908, 182], fill=(214, 208, 182))

    # missile streak: bright core + glow + smoke trail
    mx, my = 700, 210  # warhead
    trail = [(mx, my), (640, 178), (560, 158), (470, 152), (390, 162)]
    draw.line(trail, fill=(120, 120, 118), width=9)
    draw.line(trail, fill=(205, 200, 190), width=4)
    draw.line([(mx, my), (mx + 46, my - 26)], fill=(255, 214, 120), width=5)
    draw.line([(mx, my), (mx + 46, my - 26)], fill=(255, 246, 210), width=2)
    draw.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(255, 236, 170))
    draw.ellipse([mx - 3, my - 3, mx + 3, my + 3], fill=(255, 255, 240))
    # explosion bloom where the first missile came down
    draw.ellipse([202, 276, 238, 304], fill=(255, 170, 60))
    draw.ellipse([210, 282, 230, 298], fill=(255, 220, 130))
    draw.ellipse([214, 286, 226, 296], fill=(200, 40, 30))

    # NATO jets, top left (dark silhouettes, light edge)
    for jx, jy, s in [(120, 168, 1.0), (168, 150, 0.7)]:
        w = int(34 * s)
        pts = [(jx, jy), (jx + w, jy + 5), (jx + w * 0.55, jy + 9),
               (jx + w * 0.35, jy + 16), (jx + w * 0.2, jy + 7)]
        draw.polygon(pts, fill=(52, 58, 66), outline=(205, 210, 216))

    # farmhouse silhouette with one lit window, bottom left
    draw.rectangle([70, 316, 170, 384], fill=(10, 14, 12))
    draw.polygon([(62, 316), (120, 288), (178, 316)], fill=(10, 14, 12))
    draw.rectangle([104, 336, 122, 358], fill=(255, 205, 90))
    draw.rectangle([140, 330, 152, 352], fill=(60, 66, 72))
    # fence posts
    for fx in range(190, 420, 26):
        draw.rectangle([fx, 352, fx + 4, 384], fill=(12, 16, 14))
    draw.line([(180, 360), (430, 360)], fill=(12, 16, 14), width=3)

    # map inset: Poland, three impact sites
    ix0, iy0, ix1, iy1 = 748, 252, 968, 372
    draw.rounded_rectangle([ix0, iy0, ix1, iy1], radius=8,
                           fill=(250, 247, 238), outline=GOLD, width=2)
    draw.text((ix0 + 10, iy0 + 6), "POLAND — 3 IMPACT SITES",
              font=font(MONO_B, 12), fill=INK)
    poly = [(790, 292), (830, 276), (880, 282), (920, 292), (940, 308),
            (930, 330), (890, 342), (840, 338), (800, 328), (778, 312)]
    draw.polygon(poly, fill=(206, 216, 226), outline=NAVY)
    sites = [(836, 302, "NOWY LIPOWIEC"), (884, 292, "RUDNIK"),
             (912, 312, "MOLODYCZ")]
    for sx, sy, _name in sites:
        draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=CRIMSON,
                     outline=(255, 255, 255), width=1)
    draw.text((ix0 + 10, iy1 - 22), "NATO DRILLS AT NOWA DEBA",
              font=font(MONO, 11), fill=GREY)
    # caption over the scene, bottom left
    draw.text((48, 356), "ALEKSANDROW, POLAND — FRIDAY",
              font=font(MONO_B, 13), fill=(240, 238, 230))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def pictogram(draw, kind, x, y, w, h):
    """White-on-navy pictogram for one story row, drawn in box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    white = (245, 247, 250)
    if kind == "markets":
        base = cy + 18
        bars = [(cx - 34, 26), (cx - 12, 40), (cx + 10, 18), (cx + 30, 8)]
        for bx, bh in bars:
            draw.rectangle([bx, base - bh, bx + 12, base], fill=GOLD)
        draw.line([(cx - 40, base), (cx + 44, base)], fill=white, width=3)
        draw.line([(cx - 36, cy - 26), (cx + 38, cy + 6)], fill=CRIMSON, width=4)
        draw.polygon([(cx + 38, cy + 6), (cx + 24, cy + 2), (cx + 36, cy + 16)],
                     fill=CRIMSON)
    elif kind == "denmark":
        draw.ellipse([cx - 26, cy - 30, cx + 26, cy + 22], outline=white, width=3)
        draw.line([(cx, cy - 30), (cx, cy - 12)], fill=white, width=3)
        draw.ellipse([cx - 9, cy - 26, cx + 9, cy - 8], fill=white)
        draw.rectangle([cx - 4, cy - 8, cx + 4, cy + 16], fill=white)
        draw.line([(cx - 16, cy + 30), (cx + 16, cy + 30)], fill=white, width=3)
        draw.line([(cx, cy + 16), (cx, cy + 30)], fill=white, width=3)
    elif kind == "hormuz":
        draw.polygon([(cx - 38, cy + 6), (cx + 38, cy + 6), (cx + 30, cy + 20),
                      (cx - 30, cy + 20)], fill=white)
        draw.rectangle([cx - 6, cy - 14, cx + 22, cy + 6], fill=white)
        draw.rectangle([cx + 8, cy - 24, cx + 14, cy - 14], fill=GOLD)
        draw.polygon([(cx - 30, cy - 18), (cx - 22, cy - 34), (cx - 14, cy - 18)],
                     fill=(255, 170, 60))
        draw.polygon([(cx - 14, cy - 14), (cx - 8, cy - 28), (cx - 2, cy - 14)],
                     fill=(255, 214, 120))
        draw.line([(cx - 44, cy + 28), (cx + 44, cy + 28)], fill=(150, 180, 210),
                  width=3)
    elif kind == "cop31":
        draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=white, width=3)
        draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=GOLD, width=1)
        draw.arc([cx - 26, cy - 26, cx + 26, cy + 26], 200, 340, fill=white,
                 width=2)
        draw.line([(cx - 26, cy), (cx + 26, cy)], fill=white, width=2)
        draw.line([(cx, cy - 26), (cx, cy + 26)], fill=white, width=2)
        draw.rectangle([cx + 30, cy - 6, cx + 36, cy + 26], outline=white, width=2)
        draw.ellipse([cx + 27, cy + 20, cx + 39, cy + 32], fill=CRIMSON)
    elif kind == "trump":
        draw.polygon([(cx - 32, cy + 28), (cx + 32, cy + 28), (cx + 20, cy - 4),
                      (cx - 20, cy - 4)], fill=white)
        draw.rectangle([cx - 24, cy - 12, cx + 24, cy - 4], fill=GOLD)
        draw.line([(cx + 6, cy - 12), (cx + 6, cy - 28)], fill=white, width=3)
        draw.ellipse([cx + 1, cy - 34, cx + 11, cy - 24], fill=white)
        draw.rectangle([cx - 32, cy + 28, cx + 32, cy + 32], fill=GOLD)


ROWS = [
    ("markets",
     "AI ROUT DRAGS WALL STREET INTO CORRECTION",
     "S&P 500 falls 3.7% on its seventh straight down day; Nasdaq sheds "
     "5.3% and wipes out its 2026 gains. Nvidia plunges 14%.",
     "WSJ · CNN"),
    ("denmark",
     "DENMARK FOILS \u2018RUSSIAN\u2019 MURDER PLOT",
     "PET says Moscow planned to kill US-Ukrainian rapper Kyivstoner at a "
     "September concert; the defence attach\u00e9 is expelled within seven days.",
     "REUTERS · CNN"),
    ("hormuz",
     "TANKER ABLAZE IN THE STRAIT OF HORMUZ",
     "An unknown projectile strikes a tanker off Oman \u2014 the fourth hit "
     "near Khasab in three days. No casualties reported.",
     "REUTERS · UKMTO"),
    ("cop31",
     "COP31 DRIFTS PAST DEADLINE, FOSSIL FUELS ERASED",
     "The draft deal drops every mention of coal, oil and gas; a third text "
     "is due Saturday as Panama threatens to object.",
     "REUTERS · UN NEWS"),
    ("trump",
     "TRUMP: SUMMIT WAS \u201812 OUT OF 10\u2019",
     "In a 90-minute White House briefing he touts the Shenzhen trilateral "
     "and threatens a tax on US tech building data centres abroad.",
     "AP · KNKX"),
]

TICKER = ("AKVAN DONE \u2014 370,000 EVACUATED  \u00b7  IRAN DECISION PAST 1 JAN  "
          "\u00b7  MYANMAR SANCTIONS PRESSED  \u00b7  BITCOIN $59K, 7TH WEEKLY DROP")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------------
    d.rectangle([0, 0, W, 104], fill=BLACK)
    d.rectangle([0, 104, W, 108], fill=CRIMSON)
    d.text((36, 22), "THE WORLD", font=font(SERIF_B, 62), fill=(250, 248, 242))
    d.text((36, 86), "ONE IMAGE  \u00b7  EVERY STORY THAT MATTERED",
           font=font(MONO, 12), fill=(190, 194, 200))
    d.text((988, 18), "SATURDAY", font=font(SERIF_B, 26), fill=GOLD,
           anchor="ra")
    d.text((988, 50), "21 NOVEMBER 2026", font=font(SERIF_B, 26), fill=GOLD,
           anchor="ra")
    d.text((988, 86), "No. 325  \u00b7  $100 USDC",
           font=font(MONO, 12), fill=(190, 194, 200), anchor="ra")

    # --- dateline ------------------------------------------------------------
    d.text((36, 116),
           "Compiled 21 November 2026, about 03:40 UTC \u2014 the day is still "
           "in progress",
           font=font(MONO, 13), fill=GREY)

    # --- lead scene + headline ----------------------------------------------
    draw_lead_scene(d)
    head_f = fit(d, "RUSSIAN MISSILES HIT POLAND", SERIF_B, 44, 760)
    d.text((36, 392), "RUSSIAN MISSILES HIT POLAND", font=head_f, fill=INK)
    d.text((988, 402), "BBC \u00b7 AL JAZEERA", font=font(MONO_B, 12),
           fill=CRIMSON, anchor="ra")
    sub_f = font(SANS, 18)
    sub = ("Two cruise missiles and a jet-powered drone cross into NATO "
           "territory during allied drills \u2014 no one is hurt, jets "
           "scramble, and PM Tusk says the timing was \u2018no coincidence\u2019.")
    for i, line in enumerate(wrap(d, sub, sub_f, 952, max_lines=2)):
        d.text((36, 440 + i * 22), line, font=sub_f, fill=(52, 60, 68))

    # --- story rows ----------------------------------------------------------
    y = 500
    for kind, head, summ, src in ROWS:
        d.rounded_rectangle([36, y, 988, y + 78], radius=6, fill=ROW_BG,
                            outline=(214, 206, 188), width=1)
        d.rounded_rectangle([36, y, 132, y + 78], radius=6, fill=NAVY)
        d.rectangle([96, y, 132, y + 78], fill=NAVY)  # square off right edge
        pictogram(d, kind, 36, y, 96, 78)
        hf = fit(d, head, SANS_B, 21, 800)
        d.text((148, y + 8), head, font=hf, fill=INK)
        sf = font(SANS, 16)
        for i, line in enumerate(wrap(d, summ, sf, 800, max_lines=2)):
            d.text((148, y + 36 + i * 20), line, font=sf, fill=(52, 60, 68))
        d.text((972, y + 10), src, font=font(MONO_B, 11), fill=CRIMSON,
               anchor="ra")
        y += 86

    # --- ticker --------------------------------------------------------------
    ty = y + 4
    d.rectangle([0, ty, W, ty + 44], fill=BLACK)
    d.text((36, ty + 12), "ALSO TODAY", font=font(MONO_B, 14), fill=GOLD)
    tf = fit(d, TICKER, MONO, 15, 830)
    d.text((180, ty + 13), TICKER, font=tf, fill=(235, 238, 242))

    # --- footer --------------------------------------------------------------
    d.text((36, ty + 56),
           "Every story checked against the reporting named above; nothing is "
           "shown as decided before it happens.",
           font=font(SANS, 13), fill=GREY)
    d.text((988, ty + 56), "news-image-20261121 \u00b7 make.fun",
           font=font(MONO, 12), fill=GREY, anchor="ra")

    img.save(OUT, format="JPEG", quality=92, optimize=False,
             progressive=False)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
