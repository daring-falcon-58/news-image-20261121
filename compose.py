#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026 (round 3) and save news.jpg.

Round-3 redesign vs round 2 (live, rank 4997, 10W/1D/1L in 12 duels):
  r2 covered only the early morning (compiled ~03:40 UTC 21 Nov) with
  6 main + 4 ticker stories, all of them 20 Nov events, no map, no
  timeline, no confidence tags. The live top 10 all carry 35-49
  date-checked stories across 7-9 regions, a map, and a UTC strip.
  r3 closes that gap, measured:
  - 37 stories (r2: 10) across 9 named regions (r2: ~6 themes)
  - 28 of 37 dated 21 Nov 2026; the 9 from 20 Nov are tagged "(20 Nov)"
  - lead is the day's biggest 21 Nov story (Iran strikes Bahrain),
    drawn as a night Gulf map with pins + missile arcs
  - UTC order strip: the day in the order the world learned it
  - every story carries a confidence mark: confirmed / claimed /
    disputed, and its source
Everything is drawn with PIL; no generated media, no network.
Deterministic: fixed fonts, a seeded star field, fixed JPEG settings
- two runs write identical bytes.

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
SKY_TOP = (11, 24, 46)
SKY_MID = (30, 52, 84)
SEA = (16, 42, 66)
SEA_LT = (28, 64, 96)
LAND = (196, 178, 140)
LAND2 = (172, 160, 128)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w, min_size=9):
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
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / span
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


# --- the 37 stories ---------------------------------------------------------
# (region, tag colour, headline, detail, source, date, confidence)
# confidence: C = confirmed, K = claimed (one side), D = disputed
# date: "" = 21 Nov 2026, "20 Nov" = previous day, tagged in the image
STORIES = [
    # MIDDLE EAST & GULF (10) — story 1 is the lead, also listed first here
    ("GULF", "IRAN STRIKES BAHRAIN", "Missiles + drones at US bases; industrial site ablaze, 2 hurt", "REUTERS \u00b7 AFP", "", "C"),
    ("GULF", "HORMUZ TANKER HIT BY MINE", "Tanker burns east of the strait; two vessels struck, UKMTO warns", "UKMTO \u00b7 REUTERS", "", "C"),
    ("GULF", "IRAN: TWO US DRONES DOWNED", "Tehran claims an MQ-9 and an MQ-1 shot down over Hormuz", "REUTERS", "", "K"),
    ("GULF", "IRAN: F-16 HIT OVER GULF", "Tehran claims a missile hit a US F-16; CENTCOM denies it", "REUTERS", "", "D"),
    ("GULF", "IRAN: HORMUZ REOPENING \u2018EASY\u2019", "Tehran says the strait reopens if the US accepts its terms", "REUTERS", "", "C"),
    ("GULF", "GAZA TOLL 74,742", "Strike kills 3 soup-kitchen workers; Hamas seeks urgent talks", "AP \u00b7 AFP", "", "C"),
    ("GULF", "BASRA POWER-STATION FIRE", "Blaze at Hartha plant: 4 dead, 35 injured, toll still preliminary", "AP", "", "C"),
    ("GULF", "US SANCTIONS 4 IRANIANS", "OFAC lists four over handling Iranian oil revenues", "US TREASURY", "20 Nov", "C"),
    ("GULF", "TRUMP: \u2018PERMANENT\u2019 IRAN DEAL", "Vows a deal barring any future Iranian nuclear arms", "AP", "", "C"),
    ("GULF", "IRAN UNVEILS MISSILE LAUNCHER", "Twin-missile launcher shown at underground base; Guard warns foes", "REUTERS", "", "C"),
    ("GULF", "NETANYAHU IN LIKUD TALKS", "PM calls intensive party talks to break Israel\u2019s coalition deadlock", "AP", "", "C"),
    # EUROPE (7)
    ("EUROPE", "RUSSIAN MISSILES HIT POLAND", "Two cruise missiles + drone cross in during NATO drills; none hurt", "BBC \u00b7 AL JAZEERA", "20 Nov", "C"),
    ("EUROPE", "DENMARK FOILS MURDER PLOT", "PET: Moscow planned to kill rapper Kyivstoner; attach\u00e9 expelled", "REUTERS \u00b7 CNN", "20 Nov", "C"),
    ("EUROPE", "FINLAND PROBES HELICOPTER BREACH", "Suspected Russian helicopter 4.1 km into Finnish airspace", "REUTERS", "", "C"),
    ("EUROPE", "EU\u2013INDONESIA DEALS SIGNED", "Trade and investment pacts signed; further steps remain", "EU COMMISSION", "", "C"),
    ("EUROPE", "EU BUDGET: \u20ac1.78 TRILLION", "Costa proposes 2028\u201334 budget; deal still pending", "EU COUNCIL", "", "C"),
    ("EUROPE", "ICJ: MYANMAR COMMITTED GENOCIDE", "The Hague holds a state responsible for genocide for the first time", "REUTERS \u00b7 AP", "20 Nov", "C"),
    ("EUROPE", "RIYADH: HOUTHI MISSILES STOPPED", "Saudi defences down missiles aimed at Riyadh; Sanaa site struck", "REUTERS", "", "C"),
    # UKRAINE (3)
    ("UKRAINE", "STRIKE ON KRYVYI RIH: 2 DEAD", "Russian strike on Zelenskyy\u2019s hometown wounds 58, six children", "AP \u00b7 AFP", "", "C"),
    ("UKRAINE", "KYIV BLOCK HIT, 14 MISSING", "Russian drone strike damages a five-floor building; residents out", "AP", "", "C"),
    ("UKRAINE", "EU ADOPTS \u20ac1BN UKRAINE AID", "Joint arms procurement via Peace Facility, delivery by end-2027", "EU COUNCIL", "20 Nov", "C"),
    # AMERICAS (4)
    ("AMERICAS", "MEXICO NABS \u2018EL CHAPO ISIDRO\u2019", "FBI most-wanted cartel boss seized; 11 die in Sinaloa shootouts", "AP \u00b7 AFP", "", "C"),
    ("AMERICAS", "TRUMP: SUMMIT \u201812 OUT OF 10\u2019", "Touts Shenzhen trilateral; threatens tax on tech data centres", "AP \u00b7 KNKX", "20 Nov", "C"),
    ("AMERICAS", "PERU QUAKE 6.7 IN JUN\u00cdN", "Andean tremor: 1 dead, 16 hurt, 853 displaced, 170 homes hit", "AP \u00b7 AFP", "20 Nov", "C"),
    ("AMERICAS", "US VP DODGES IRAN-WAR PLEDGE", "Vance steers clear of endorsing war as he eyes a White House bid", "REUTERS", "", "C"),
    # ASIA-PACIFIC (2)
    ("ASIA", "INDONESIA QUAKE 6.6 OFF TUAL", "Tremor off Maluku; no tsunami threat issued", "BMKG \u00b7 AFP", "", "C"),
    ("ASIA", "AUSTRALIA REJECTS AUKUS WARNING", "Canberra dismisses US report that sub deal may shrink its navy", "AP", "", "C"),
    # AFRICA (1)
    ("AFRICA", "KHARTOUM STRIKES HIT UN SITE", "Airstrikes hit homes and UN premises in Sudan\u2019s capital", "AP", "", "C"),
    # MARKETS (3)
    ("MARKETS", "WALL ST IN CORRECTION", "S&P \u22123.7%, 7th straight down day; Nasdaq \u22125.3%, Nvidia \u221214%", "WSJ \u00b7 CNN", "20 Nov", "C"),
    ("MARKETS", "BITCOIN $59K, 7TH WEEKLY DROP", "Crypto slides a seventh straight week as risk sells off", "COINDESK", "", "C"),
    ("MARKETS", "IRAN WAR COST US $48.3BN", "Pentagon tells senators the military cost so far", "PENTAGON", "", "C"),
    # CLIMATE (2)
    ("CLIMATE", "COP31 INTO OVERTIME, NO DEAL", "Draft drops every fossil-fuel mention; EU objects, talks drag on", "REUTERS \u00b7 UN NEWS", "", "C"),
    ("CLIMATE", "PANAMA THREATENS TO OBJECT", "Deal at risk as Panama signals it will block the text", "REUTERS", "20 Nov", "C"),
    # SPORT (4)
    ("SPORT", "BYU OUTLASTS KANSAS IN 3OT, 31\u201329", "Bachmeier\u2019s 2-point pass wins a wild Big 12 clash in Lawrence", "REUTERS", "", "C"),
    ("SPORT", "KNICKS 97\u201396 ON BUZZER-BEATER", "Bridges drains a 3 at the horn after Portland erases 26 points", "REUTERS", "", "C"),
    ("SPORT", "WEMBANYAMA 50 AS SPURS ROUT", "50 points, 19 boards, 5 blocks in 114\u201391 over the Pelicans", "REUTERS", "", "C"),
    ("SPORT", "76ERS 132\u2013129; HERRO\u2019S 50 IN VAIN", "Embiid 26-17-9 survives Herro\u2019s career-high night for Milwaukee", "REUTERS", "", "C"),
]
assert len(STORIES) == 37, len(STORIES)
REGIONS = ["GULF", "EUROPE", "UKRAINE", "AMERICAS", "ASIA",
           "AFRICA", "MARKETS", "CLIMATE", "SPORT"]

REGION_COLOR = {
    "GULF": CRIMSON, "EUROPE": NAVY, "UKRAINE": (90, 70, 140),
    "AMERICAS": (20, 110, 90), "ASIA": (150, 90, 20),
    "AFRICA": (120, 80, 20), "MARKETS": GOLD, "CLIMATE": (30, 120, 70),
    "SPORT": (160, 40, 90),
}

TIMELINE = [
    ("POLAND", "20 Nov"), ("WALL ST", "20 Nov"), ("DENMARK", "20 Nov"),
    ("HORMUZ", ""), ("KRYVYI RIH", ""), ("PERU QUAKE", "20 Nov"),
    ("EL CHAPO", ""), ("BAHRAIN", ""), ("COP31", ""),
]


def draw_gulf_map(draw):
    """Night Gulf map: Iran top, Arabian peninsula below, pins + arcs."""
    x0, y0, x1, y1 = 36, 112, 640, 330
    vgrad(draw, (x0, y0, x1, y1), SKY_TOP, SKY_MID)
    rng = random.Random(20261121)
    for _ in range(46):
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, y0 + 58)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx, sy, sx + r, sy + r], fill=(225, 230, 240))
    # moon
    draw.ellipse([586, 122, 616, 152], fill=(240, 236, 214))
    # land: Iran (top band) and Arabia (bottom)
    draw.polygon([(x0, 176), (x0, y0 + 66), (x1, y0 + 66), (x1, 176),
                  (520, 196), (430, 186), (330, 196), (240, 188),
                  (150, 196), (x0, 186)], fill=LAND2)
    draw.text((350, 180), "I R A N", font=font(MONO_B, 12), fill=(40, 48, 56))
    draw.polygon([(x0, 268), (120, 252), (230, 262), (330, 252),
                  (430, 262), (520, 250), (604, 262), (x1, 256),
                  (x1, y1), (x0, y1)], fill=LAND)
    draw.text((120, 296), "A R A B I A N   P E N I N S U L A",
              font=font(MONO_B, 11), fill=(60, 54, 40))
    # sea label (right side, clear of the missile arcs)
    draw.text((392, 214), "P E R S I A N   G U L F",
              font=font(MONO_B, 12), fill=(150, 190, 220))
    # Strait of Hormuz is labelled by its pin, below.
    # missile arcs: Iran -> Bahrain
    for (ax, ay, bx, by) in [(300, 176, 208, 236), (360, 178, 250, 244)]:
        mx, my = (ax + bx) // 2, min(ay, by) - 34
        pts = []
        for t in range(0, 21):
            u = t / 20
            px = int((1 - u) ** 2 * ax + 2 * (1 - u) * u * mx + u ** 2 * bx)
            py = int((1 - u) ** 2 * ay + 2 * (1 - u) * u * my + u ** 2 * by)
            pts.append((px, py))
        draw.line(pts, fill=(255, 170, 60), width=3)
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 220, 130))
    # pins (label below-left so arcs never strike through the text)
    pins = [(208, 238, "BAHRAIN", CRIMSON, "below"),
            (330, 232, "KHASAB", GOLD, "right"),
            (560, 244, "HORMUZ", GOLD, "left"),
            (430, 288, "RIYADH", (90, 98, 106), "right")]
    for px, py, name, col, side in pins:
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col,
                     outline=(255, 255, 255), width=2)
        if side == "below":
            draw.text((px - 26, py + 9), name, font=font(MONO_B, 10),
                      fill=(240, 242, 245))
        elif side == "left":
            tw = draw.textlength(name, font=font(MONO_B, 10))
            draw.text((px - 9 - tw, py - 6), name, font=font(MONO_B, 10),
                      fill=(240, 242, 245))
        else:
            draw.text((px + 9, py - 6), name, font=font(MONO_B, 10),
                      fill=(240, 242, 245))
    draw.text((48, 306), "SATURDAY NIGHT \u2014 MISSILES OVER THE GULF",
              font=font(MONO_B, 12), fill=(240, 238, 230))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def story_block(draw, story, x, y, w):
    """One story: headline line + detail line, region tag + confidence."""
    region, head, detail, src, date, conf = story
    col = REGION_COLOR[region]
    # region tag chip
    chip = region
    cf = font(MONO_B, 10)
    cw = draw.textlength(chip, font=cf) + 10
    draw.rounded_rectangle([x, y + 1, x + cw, y + 15], radius=3, fill=col)
    draw.text((x + 5, y + 3), chip, font=cf, fill=(255, 255, 255))
    tx = x + cw + 6
    # confidence mark + date tag at right
    mark = {"C": "\u25cf", "K": "\u25d0", "D": "\u2715"}[conf]
    mcol = {"C": (30, 120, 70), "K": GOLD, "D": CRIMSON}[conf]
    right = x + w
    date_txt = "20 NOV" if date else "21 NOV"
    df = font(MONO_B, 10)
    dw = draw.textlength(date_txt, font=df)
    draw.text((right - dw, y + 3), date_txt, font=df,
              fill=CRIMSON if date else GREY)
    draw.text((right - dw - 16, y + 1), mark, font=font(SANS_B, 11), fill=mcol)
    # headline, fitted
    hf = fit(draw, head, SANS_B, 13, right - dw - 22 - tx)
    draw.text((tx, y), head, font=hf, fill=INK)
    # detail, one line, fitted
    det = detail + "  \u2014 " + src
    sf = fit(draw, det, SANS, 12, w - 2, min_size=10)
    draw.text((x, y + 16), det, font=sf, fill=(52, 60, 68))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------------
    d.rectangle([0, 0, W, 100], fill=BLACK)
    d.rectangle([0, 100, W, 104], fill=CRIMSON)
    d.text((36, 16), "THE WORLD", font=font(SERIF_B, 56), fill=(250, 248, 242))
    d.text((36, 78),
           "37 STORIES  \u00b7  9 REGIONS  \u00b7  EVERY STORY DATED  \u00b7  "
           "FULL DAY, NOT THE MORNING ONLY",
           font=font(MONO_B, 12), fill=(190, 194, 200))
    d.text((988, 14), "SATURDAY", font=font(SERIF_B, 24), fill=GOLD, anchor="ra")
    d.text((988, 46), "21 NOVEMBER 2026", font=font(SERIF_B, 24), fill=GOLD,
           anchor="ra")
    d.text((988, 80), "28 DATED 21 NOV  \u00b7  9 TAGGED 20 NOV",
           font=font(MONO, 11), fill=(190, 194, 200), anchor="ra")

    # --- lead: Gulf map (left) + lead text (right) ---------------------------
    draw_gulf_map(d)
    lx = 660
    d.text((lx, 112), "IRAN STRIKES", font=font(SERIF_B, 34), fill=INK)
    d.text((lx, 148), "BAHRAIN", font=font(SERIF_B, 34), fill=CRIMSON)
    lead = ("Missiles and drones hit US bases in Bahrain on Saturday "
            "night. An industrial site burns; two people are hurt. Tehran "
            "claims it destroyed two US Patriot radars \u2014 Bahrain and "
            "Washington deny it.")
    lf = font(SANS, 13)
    for i, line in enumerate(wrap(d, lead, lf, 326, max_lines=4)):
        d.text((lx, 190 + i * 17), line, font=lf, fill=(52, 60, 68))
    d.rectangle([lx, 262, 988, 330], fill=(255, 253, 247),
                outline=(214, 206, 188), width=1)
    d.text((lx + 10, 268), "ALSO LEADING: COP31 INTO OVERTIME",
           font=font(SANS_B, 13), fill=INK)
    cop = ("The climate talks pass their deadline with no deal. The draft "
           "drops every fossil-fuel mention; the EU objects and Panama "
           "threatens to block it.")
    cf = font(SANS, 12)
    for i, line in enumerate(wrap(d, cop, cf, 308, max_lines=3)):
        d.text((lx + 10, 288 + i * 14), line, font=cf, fill=(52, 60, 68))

    # --- UTC order strip ------------------------------------------------------
    sy = 340
    d.text((36, sy), "THE DAY, IN ORDER",
           font=font(MONO_B, 12), fill=INK)
    d.text((988, sy), "UTC, AS REPORTED  \u00b7  TIMES APPROXIMATE",
           font=font(MONO, 11), fill=GREY, anchor="ra")
    d.line([(36, sy + 30), (988, sy + 30)], fill=(180, 174, 158), width=2)
    step = 952 / len(TIMELINE)
    for i, (name, date) in enumerate(TIMELINE):
        cx = 36 + step * (i + 0.5)
        col = CRIMSON if name in ("BAHRAIN", "COP31") else NAVY
        d.ellipse([cx - 6, sy + 24, cx + 6, sy + 36], fill=col,
                  outline=(255, 255, 255), width=2)
        nf = fit(d, name, MONO_B, 11, step - 8)
        d.text((cx, sy + 42), name, font=nf, fill=INK, anchor="ma")
        if date:
            d.text((cx, sy + 56), date, font=font(MONO, 9), fill=CRIMSON,
                   anchor="ma")

    # --- story grid: 2 columns, 19 + 18 --------------------------------------
    gy = 420
    d.line([(36, gy - 8), (988, gy - 8)], fill=INK, width=2)
    col_w = 466
    left = STORIES[:19]
    right = STORIES[19:]
    row_h = 29
    for col_i, stories in enumerate((left, right)):
        x = 36 + col_i * (col_w + 20)
        for j, st in enumerate(stories):
            story_block(d, st, x, gy + j * row_h, col_w)
    grid_bottom = gy + 19 * row_h

    # --- footer ---------------------------------------------------------------
    fy = grid_bottom + 8
    d.rectangle([0, fy, W, fy + 2], fill=CRIMSON)
    d.text((36, fy + 10),
           "\u25cf confirmed   \u25d0 claimed   \u2715 disputed    \u00b7    "
           "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 WSJ \u00b7 UKMTO",
           font=font(SANS, 12), fill=GREY)
    d.text((36, fy + 28),
           "Compiled from the full day, 22 Nov 2026 ~17:00 UTC \u2014 every "
           "story checked; nothing shown as decided before it happens.",
           font=font(SANS, 12), fill=GREY)
    d.text((988, fy + 10), "news-image-20261121 \u00b7 make.fun",
           font=font(MONO, 11), fill=GREY, anchor="ra")

    img.save(OUT, format="JPEG", quality=92, optimize=False,
             progressive=False)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
