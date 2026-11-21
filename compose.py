#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026 and save news.jpg.

A broadsheet: black masthead, a drawn night scene for the lead story
(Russian missiles landing in Poland; NATO chief Rutte flies to Warsaw
on Saturday), six illustrated story rows, and a ticker. Everything is
drawn with PIL; no generated media, no network. Deterministic: fixed
fonts, a seeded star field, fixed JPEG settings — two runs write
identical bytes.

Stories (all checked against the reporting named on the page, compiled
about 06:00 UTC on 21 Nov 2026):
  LEAD  Russian missiles hit Poland; Rutte flies to Warsaw today,
        Warsaw seeks F-35s and AWACS under Operation Eastern Sentry.
  1     ICJ: Myanmar committed genocide against the Rohingya — the
        first time the court has held a state responsible.
  2     AI rout drags Wall Street into correction (S&P -3.7%, Nasdaq
        -5.3%, Nvidia -14%).
  3     Saudi-led coalition intercepts Houthi missiles aimed at Riyadh.
  4     Denmark foils a 'Russian' murder plot against rapper Kyivstoner.
  5     Tanker ablaze in the Strait of Hormuz, fourth hit near Khasab.
  6     COP31 drifts past its deadline into Saturday; fossil fuels
        erased from the draft.
  TICKER Trump joins allies' Ukraine call; EU EUR1bn more aid for Kyiv;
        pancreatic-cancer pill clears tumours in 1 of 12; Bitcoin $59K;
        Akvan evacuations done, 370,000 out.

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
        last = lines[-1]
        while last and draw.textlength(last + " \u2026", font=f) > max_w:
            last = last[:-1].rstrip()
        lines[-1] = last + " \u2026"
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
    """Night over south-eastern Poland: missile streak, jets, farmhouse,
    impact flash with smoke, and a map inset of the three impact sites."""
    x0, y0, x1, y1 = 36, 134, 988, 308
    vgrad(draw, (x0, y0, x1, 252), SKY_TOP, SKY_MID)
    vgrad(draw, (x0, 252, x1, 276), SKY_MID, DUSK)
    draw.rectangle([x0, 276, x1, y1], fill=(16, 22, 18))

    rng = random.Random(20261121)
    for _ in range(80):
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, 248)
        r = rng.choice([1, 1, 1, 2])
        draw.ellipse([sx, sy, sx + r, sy + r], fill=(235, 238, 245))

    # moon
    draw.ellipse([884, 148, 920, 184], fill=(240, 236, 214))
    draw.ellipse([896, 156, 912, 172], fill=(214, 208, 182))

    # missile streak: wide smoke trail, bright core, flaming warhead
    mx, my = 706, 196  # warhead
    trail = [(mx, my), (640, 168), (556, 150), (468, 146), (384, 156)]
    draw.line(trail, fill=(110, 110, 108), width=11)
    draw.line(trail, fill=(205, 200, 190), width=5)
    draw.line(trail, fill=(255, 246, 210), width=2)
    # flame behind the warhead
    draw.line([(mx, my), (mx + 52, my - 30)], fill=(255, 170, 60), width=8)
    draw.line([(mx, my), (mx + 52, my - 30)], fill=(255, 236, 170), width=4)
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(255, 236, 170))
    draw.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(255, 255, 240))

    # impact flash + smoke column where the first missile came down
    draw.ellipse([196, 252, 244, 292], fill=(255, 170, 60))
    draw.ellipse([206, 260, 234, 286], fill=(255, 220, 130))
    draw.ellipse([212, 266, 228, 282], fill=(200, 40, 30))
    smoke = [(220, 252), (214, 232), (224, 214), (216, 198)]
    draw.line(smoke, fill=(150, 148, 142), width=7)
    draw.line(smoke, fill=(200, 198, 192), width=3)

    # NATO jets, top left (dark silhouettes, light edge, afterburner dots)
    for jx, jy, s in [(118, 162, 1.0), (172, 144, 0.7)]:
        w = int(38 * s)
        pts = [(jx, jy), (jx + w, jy + 5), (jx + w * 0.55, jy + 10),
               (jx + w * 0.35, jy + 18), (jx + w * 0.2, jy + 7)]
        draw.polygon(pts, fill=(52, 58, 66), outline=(205, 210, 216))
        draw.ellipse([jx - 4, jy + 2, jx, jy + 6], fill=(255, 200, 90))

    # farmhouse silhouette with one lit window, bottom centre-left
    draw.rectangle([330, 272, 428, 308], fill=(10, 14, 12))
    draw.polygon([(322, 272), (379, 246), (436, 272)], fill=(10, 14, 12))
    draw.rectangle([362, 284, 380, 304], fill=(255, 205, 90))
    draw.rectangle([398, 280, 410, 300], fill=(60, 66, 72))
    # fence posts
    for fx in range(450, 660, 26):
        draw.rectangle([fx, 290, fx + 4, 308], fill=(12, 16, 14))
    draw.line([(440, 296), (670, 296)], fill=(12, 16, 14), width=3)

    # map inset: Poland, three impact sites
    ix0, iy0, ix1, iy1 = 748, 206, 968, 300
    draw.rounded_rectangle([ix0, iy0, ix1, iy1], radius=8,
                           fill=(250, 247, 238), outline=GOLD, width=2)
    draw.text((ix0 + 10, iy0 + 6), "POLAND \u2014 3 IMPACT SITES",
              font=font(MONO_B, 12), fill=INK)
    poly = [(790, 244), (830, 228), (880, 234), (920, 244), (940, 258),
            (930, 268), (890, 276), (840, 274), (800, 264), (778, 254)]
    draw.polygon(poly, fill=(206, 216, 226), outline=NAVY)
    sites = [(836, 252), (884, 242), (912, 262)]
    for sx, sy in sites:
        draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=CRIMSON,
                     outline=(255, 255, 255), width=1)
    draw.text((ix0 + 10, iy1 - 20), "RUTTE DUE IN WARSAW TODAY",
              font=font(MONO, 11), fill=GREY)
    # caption over the scene, bottom left (drawn last, over the dark ground)
    draw.text((48, 284), "SOUTH-EASTERN POLAND \u2014 FRIDAY, 06:30",
              font=font(MONO_B, 13), fill=(240, 238, 230))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def pictogram(draw, kind, x, y, w, h):
    """White-on-navy pictogram for one story row, drawn in box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    white = (245, 247, 250)
    if kind == "nato":
        # four-point compass star (NATO emblem)
        pts = [(cx, cy - 30), (cx + 7, cy - 7), (cx + 30, cy),
               (cx + 7, cy + 7), (cx, cy + 30), (cx - 7, cy + 7),
               (cx - 30, cy), (cx - 7, cy - 7)]
        draw.polygon(pts, fill=white)
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=NAVY,
                     outline=white, width=2)
    elif kind == "scales":
        # scales of justice (ICJ)
        draw.line([(cx, cy - 28), (cx, cy + 28)], fill=white, width=3)
        draw.line([(cx - 26, cy - 20), (cx + 26, cy - 20)], fill=white, width=3)
        draw.line([(cx - 26, cy - 20), (cx - 26, cy - 6)], fill=white, width=2)
        draw.line([(cx + 26, cy - 20), (cx + 26, cy - 6)], fill=white, width=2)
        draw.polygon([(cx - 34, cy - 6), (cx - 18, cy - 6), (cx - 26, cy + 6)],
                     fill=white)
        draw.polygon([(cx + 18, cy - 6), (cx + 34, cy - 6), (cx + 26, cy + 6)],
                     fill=white)
        draw.line([(cx - 16, cy + 28), (cx + 16, cy + 28)], fill=white, width=3)
        draw.ellipse([cx - 5, cy - 33, cx + 5, cy - 23], fill=GOLD)
    elif kind == "markets":
        base = cy + 18
        bars = [(cx - 34, 26), (cx - 12, 40), (cx + 10, 18), (cx + 30, 8)]
        for bx, bh in bars:
            draw.rectangle([bx, base - bh, bx + 12, base], fill=GOLD)
        draw.line([(cx - 40, base), (cx + 44, base)], fill=white, width=3)
        draw.line([(cx - 36, cy - 26), (cx + 38, cy + 6)], fill=CRIMSON, width=4)
        draw.polygon([(cx + 38, cy + 6), (cx + 24, cy + 2), (cx + 36, cy + 16)],
                     fill=CRIMSON)
    elif kind == "shield":
        # shield stopping a missile (Riyadh intercept)
        draw.polygon([(cx - 26, cy - 26), (cx + 26, cy - 26),
                      (cx + 26, cy + 2), (cx, cy + 30),
                      (cx - 26, cy + 2)], outline=white, width=3)
        draw.line([(cx - 12, cy + 2), (cx - 2, cy + 12), (cx + 14, cy - 10)],
                  fill=GOLD, width=4)
        draw.line([(cx - 34, cy - 28), (cx + 34, cy - 28)], fill=CRIMSON,
                  width=3)
    elif kind == "target":
        # crosshair (Denmark plot foiled)
        draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=white,
                     width=3)
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=white,
                     width=2)
        draw.line([(cx - 34, cy), (cx - 26, cy)], fill=white, width=3)
        draw.line([(cx + 26, cy), (cx + 34, cy)], fill=white, width=3)
        draw.line([(cx, cy - 34), (cx, cy - 26)], fill=white, width=3)
        draw.line([(cx, cy + 26), (cx, cy + 34)], fill=white, width=3)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=CRIMSON)
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
        draw.line([(cx - 26, cy), (cx + 26, cy)], fill=white, width=2)
        draw.line([(cx, cy - 26), (cx, cy + 26)], fill=white, width=2)
        draw.arc([cx - 26, cy - 26, cx + 26, cy + 26], 200, 340, fill=white,
                 width=2)
        draw.rectangle([cx + 30, cy - 6, cx + 36, cy + 26], outline=white, width=2)
        draw.ellipse([cx + 27, cy + 20, cx + 39, cy + 32], fill=CRIMSON)


ROWS = [
    ("scales",
     "UN COURT: MYANMAR COMMITTED GENOCIDE",
     "The Hague rules Myanmar responsible for genocide against the "
     "Rohingya \u2014 the first time the court has ever held a state "
     "responsible.",
     "REUTERS \u00b7 AP"),
    ("markets",
     "AI ROUT DRAGS WALL STREET INTO CORRECTION",
     "S&P 500 falls 3.7% on its seventh straight down day; Nasdaq sheds "
     "5.3% and wipes out its 2026 gains. Nvidia plunges 14%.",
     "WSJ \u00b7 CNN"),
    ("shield",
     "SAUDI DEFENCES STOP HOUTHI MISSILES AIMED AT RIYADH",
     "The Saudi-led coalition says it intercepted Houthi missiles aimed "
     "at the capital; no casualties are reported as the US\u2013Iran war "
     "grinds on.",
     "REUTERS"),
    ("target",
     "DENMARK FOILS \u2018RUSSIAN\u2019 MURDER PLOT",
     "PET says Moscow planned to kill US-Ukrainian rapper Kyivstoner at a "
     "September concert; the defence attach\u00e9 is expelled within seven days.",
     "REUTERS \u00b7 CNN"),
    ("hormuz",
     "TANKER ABLAZE IN THE STRAIT OF HORMUZ",
     "An unknown projectile strikes a tanker off Oman \u2014 the fourth hit "
     "near Khasab in three days. No casualties reported.",
     "REUTERS \u00b7 UKMTO"),
    ("cop31",
     "COP31 DRIFTS PAST DEADLINE INTO SATURDAY",
     "The draft deal drops every mention of coal, oil and gas; a third "
     "text is due today as Panama threatens to object.",
     "REUTERS \u00b7 UN NEWS"),
]

TICKER = ("TRUMP JOINS ALLIES\u2019 UKRAINE CALL  \u00b7  EU \u20ac1BN FOR KYIV  "
          "\u00b7  CANCER PILL: 1 IN 12 CLEAR  \u00b7  BITCOIN $59K  \u00b7  "
          "AKVAN DONE \u2014 370,000 EVACUATED")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------------
    d.rectangle([0, 0, W, 100], fill=BLACK)
    d.rectangle([0, 100, W, 104], fill=CRIMSON)
    d.text((36, 20), "THE WORLD", font=font(SERIF_B, 62), fill=(250, 248, 242))
    d.text((36, 84), "ONE IMAGE  \u00b7  EVERY STORY THAT MATTERED",
           font=font(MONO, 12), fill=(190, 194, 200))
    d.text((988, 16), "SATURDAY", font=font(SERIF_B, 26), fill=GOLD,
           anchor="ra")
    d.text((988, 48), "21 NOVEMBER 2026", font=font(SERIF_B, 26), fill=GOLD,
           anchor="ra")
    d.text((988, 84), "No. 325  \u00b7  $100 USDC",
           font=font(MONO, 12), fill=(190, 194, 200), anchor="ra")

    # --- dateline ------------------------------------------------------------
    d.text((36, 112),
           "Compiled 21 November 2026, about 06:00 UTC \u2014 from the "
           "morning\u2019s reporting",
           font=font(MONO, 13), fill=GREY)

    # --- lead scene + headline ----------------------------------------------
    draw_lead_scene(d)
    head_f = fit(d, "RUSSIAN MISSILES HIT POLAND", SERIF_B, 44, 760)
    d.text((36, 314), "RUSSIAN MISSILES HIT POLAND", font=head_f, fill=INK)
    d.text((988, 324), "AP \u00b7 REUTERS \u00b7 BBC", font=font(MONO_B, 12),
           fill=CRIMSON, anchor="ra")
    sub_f = font(SANS, 17)
    sub = ("Two cruise missiles and a jet-powered drone cross into NATO "
           "territory during allied drills \u2014 no one is hurt. Warsaw "
           "seeks F-35s and AWACS, and NATO chief Rutte flies in today.")
    for i, line in enumerate(wrap(d, sub, sub_f, 952, max_lines=2)):
        d.text((36, 360 + i * 21), line, font=sub_f, fill=(52, 60, 68))

    # --- story rows ----------------------------------------------------------
    y = 404
    for kind, head, summ, src in ROWS:
        d.rounded_rectangle([36, y, 988, y + 78], radius=6, fill=ROW_BG,
                            outline=(214, 206, 188), width=1)
        d.rounded_rectangle([36, y, 128, y + 78], radius=6, fill=NAVY)
        d.rectangle([92, y, 128, y + 78], fill=NAVY)  # square off right edge
        pictogram(d, kind, 36, y, 92, 78)
        hf = fit(d, head, SANS_B, 20, 800)
        d.text((144, y + 7), head, font=hf, fill=INK)
        sf = font(SANS, 16)
        for i, line in enumerate(wrap(d, summ, sf, 824, max_lines=2)):
            d.text((144, y + 34 + i * 20), line, font=sf, fill=(52, 60, 68))
        d.text((972, y + 9), src, font=font(MONO_B, 11), fill=CRIMSON,
               anchor="ra")
        y += 86

    # --- ticker --------------------------------------------------------------
    ty = y + 10
    d.rectangle([0, ty, W, ty + 40], fill=BLACK)
    d.text((36, ty + 11), "ALSO TODAY", font=font(MONO_B, 14), fill=GOLD)
    tf = fit(d, TICKER, MONO, 15, 808)
    d.text((180, ty + 12), TICKER, font=tf, fill=(235, 238, 242))

    # --- footer --------------------------------------------------------------
    d.text((36, ty + 52),
           "Every story checked against the reporting named above; nothing is "
           "shown as decided before it happens.",
           font=font(SANS, 13), fill=GREY)
    d.text((988, ty + 52), "news-image-20261121 \u00b7 make.fun",
           font=font(MONO, 12), fill=GREY, anchor="ra")

    img.save(OUT, format="JPEG", quality=92, optimize=False,
             progressive=False)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
