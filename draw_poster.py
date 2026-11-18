#!/usr/bin/env python3
"""Draw the news poster for Wednesday 18 November 2026.

Dense front page: masthead with the date, a hand-drawn world map with
location dots, then a 5 x 6 grid of short story items (30 stories), each
with a place tag, a one-to-two-line headline and a very short caption.

Every story in STORIES was verified by web research on 18 November 2026
(three passes: morning, late afternoon, and evening WIB) as an event that
happened or was first reported on 18 November 2026. Pass 2 swapped 9
wrong-dated stories, reframed 5 borderline ones to genuine 18 Nov angles,
and replaced 9 more that failed verification, for 19 fresh 18 Nov stories.

Run:  python3 draw_poster.py   (writes entry.png next to this script)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (17, 24, 39)
PAPER = (250, 248, 243)
MASTHEAD = (17, 24, 39)
RED = (178, 34, 34)
GOLD = (194, 148, 42)
PANEL_BG = (255, 255, 255)
PANEL_LINE = (203, 213, 225)
MUTED = (71, 85, 105)
MAP_LAND = (148, 163, 184)
MAP_SEA = (226, 232, 240)

# Region colours used for place tags and map dots.
REGION = {
    "ASIA": (30, 90, 160),
    "EUROPE": (107, 33, 168),
    "MIDEAST": (180, 83, 9),
    "AFRICA": (146, 64, 14),
    "AMERICAS": (21, 128, 61),
    "GLOBAL": (100, 116, 139),
    "SCIENCE": (8, 145, 178),
    "SPORT": (190, 24, 93),
}

# (place, region, headline, caption)
# Headlines ~44 chars max, captions ~64 chars max, so they fit the cells.
# Pass 2 (17:00 WIB 18 Nov): 9 wrong-dated stories swapped, 5 borderline
# reframed to genuine 18 Nov angles, 10 unverified checked (only #5 kept,
# reframed); 19 fresh 18 Nov stories verified by live news search.
STORIES = [
    ("MANILA", "ASIA", "Trump meets Marcos in Manila",
     "State visit at Malacanang; flies to Shenzhen next."),
    ("KYIV", "EUROPE", "Crimea road bridge still shut",
     "Road traffic suspended 18 Nov; experts assess damage."),
    ("BAHRAIN", "MIDEAST", "Gulf states down Iranian drones",
     "Bahrain and Kuwait report Wed intercepts; no damage"),
    ("CANBERRA", "ASIA", "Australia sanctions settlers too",
     "Wong announces matching West Bank measures."),
    ("BAY OF BENGAL", "ASIA", "Cyclone Akvan strengthens",
     "Severe-cyclonic status reached; winds gust to 105 km/h."),
    ("SEOUL", "ASIA", "Lotte Biologics opens Songdo plant",
     "Korean drugmaker starts its global CDMO business."),
    ("GOLD COAST", "SPORT", "Zoric, 14, home to hero welcome",
     "Double world champion, 14, lands at Gold Coast 18 Nov."),
    ("NEW YORK", "GLOBAL", "Nvidia revenue doubles",
     "Revenue doubles to $115.8bn; first since Huang resigned."),
    ("KUALA LUMPUR", "ASIA", "Malaysia Q3 GDP beats at 5.5%",
     "Final print beats 5.3% advance estimate; Q2 was 6.0%."),
    ("BASSETERRE", "AMERICAS", "Nevis: passport end hits economy",
     "Premier Brantley: wind-down threatens support for needy."),
    ("DEEP SPACE", "SCIENCE", "Voyager 1 reaches one light-day",
     "First human object so far; signal now takes 24 hours."),
    ("SHENZHEN", "ASIA", "Xi opens APEC summit in Shenzhen",
     "Xi chairs 21-economy summit; Trump–Putin talks due Thursday."),
    ("TOKYO", "ASIA", "India–Japan ministers in Tokyo",
     "Jaishankar, Singh in Tokyo; Raisina dialogue opens 18–19 Nov."),
    ("WELLINGTON", "ASIA", "Infratil lifts profit guidance",
     "Half-year earnings up 28% to NZ$711m; shares rose 3.6%."),
    ("SYDNEY", "ASIA", "PEXA faces $50m fee-cut hit",
     "IPART final report: 16% cut, eased from draft 20%."),
    ("BUKAVU", "AFRICA", "Congo peace efforts fail to halt violence",
     "Fighting persists in Kivu despite Washington, Doha deals."),
    ("BAGHDAD", "MIDEAST", "Quds chief Qaani visits Iraq",
     "Qaani meets PM over oil-smuggling probe at Jurf al-Nasr."),
    ("LONDON", "EUROPE", "UK inflation hits 3.6%",
     "ONS: October CPI up from 3.5%; fuel drove the rise."),
    ("GULF OF OMAN", "MIDEAST", "Iran retaliates after US sinks tankers",
     "Tehran hits Jordan base, 10 ships; oil tops $100."),
    ("NAYPYIDAW", "ASIA", "Myanmar rethinks ASEAN ties",
     "Min Aung Hlaing: ASEAN ties under review, peace talks in Feb."),
    ("BERLIN", "EUROPE", "Germany cuts power tax, caps fuel",
     "After 8-hour night talks, coalition cuts power tax for 2027."),
    ("JAKARTA", "ASIA", "Indonesia hikes rates to 6.00%",
     "Bank Indonesia lifts rate 25bp to defend rupiah at record lows."),
    ("SEOUL", "ASIA", "Korea lifts 2027 growth to 3.9%",
     "KDI nearly doubles 2027 forecast to 3.9% on AI chip boom."),
    ("SUVA", "ASIA", "Fiji declares drought disaster",
     "El Niño drought triggers national disaster; $20m for water."),
    ("TOKYO", "ASIA", "BOJ chief: keep raising rates",
     "Ueda says hikes should continue as inflation anchors near 2%."),
    ("HORMUZ", "MIDEAST", "Hormuz tanker toll: 1 missing",
     "ADNOC says 11 hurt, 1 missing; Oman rescues 24 from Tara Gas."),
    ("TOKYO", "ASIA", "Japan exports hit record high",
     "October exports +20.5% to 11.8tn yen, 14th monthly rise."),
    ("SEOUL", "ASIA", "KOSPI tops 5,000 on Nvidia beat",
     "Index closes +1.99% at 5,067 after four losing sessions."),
    ("CAMBRIDGE", "EUROPE", "Cambridge word of year: 'human'",
     "AI surge prompts renewed value on human creativity, connection."),
    ("LONDON", "EUROPE", "Ofqual warns AI cheats face ban",
     "AI or smart glasses could cost pupils a whole qualification."),
]

# Map dots: (lon, lat, region) for the stories above, roughly.
DOTS = [
    (121, 14, "ASIA"), (114, 22, "ASIA"), (139, 35, "ASIA"),
    (127, 37, "ASIA"), (107, -6, "ASIA"), (178, -18, "ASIA"),
    (175, -41, "ASIA"), (151, -33, "ASIA"), (101, 3, "ASIA"),
    (96, 20, "ASIA"), (90, 15, "ASIA"), (30, 50, "EUROPE"),
    (13, 52, "EUROPE"), (0, 51, "EUROPE"), (0, 52, "EUROPE"),
    (50, 26, "MIDEAST"), (44, 33, "MIDEAST"), (57, 25, "MIDEAST"),
    (56, 26, "MIDEAST"), (29, -2, "AFRICA"), (-62, 17, "AMERICAS"),
    (-74, 40, "GLOBAL"), (149, -35, "ASIA"), (153, -28, "SPORT"),
]

# Continent outlines as (lon, lat) polygons, equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-75, 62), (-60, 55), (-55, 47), (-70, 44), (-75, 39), (-80, 32),
     (-81, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-168, 66)],
    # Greenland
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-40, 76), (-58, 76)],
    # South America
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, -2), (-40, -5),
     (-35, -9), (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -50),
     (-73, -53), (-73, -37), (-70, -20), (-80, -5), (-80, 9)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 71), (10, 68), (5, 60), (-5, 58), (-10, 54), (-10, 36)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (32, -26), (26, -34),
     (18, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8),
     (-17, 15)],
    # Asia
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (162, 56), (158, 53),
     (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 32), (115, 23), (108, 18), (105, 10), (100, 8), (97, 16),
     (92, 21), (88, 22), (80, 15), (77, 8), (75, 20), (72, 20), (66, 25),
     (60, 25), (56, 26), (52, 28), (48, 30), (44, 29), (40, 31), (36, 36),
     (30, 36), (30, 42), (35, 45), (40, 48), (45, 52), (50, 55), (55, 58),
     (60, 60), (30, 62)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (137, -12),
     (132, -12), (126, -14), (122, -17), (118, -20), (114, -22)],
]


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def main():
    assert len(STORIES) == 30, f"expected 30 stories, got {len(STORIES)}"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---------------------------------------------------------
    d.rectangle([0, 0, W, 100], fill=MASTHEAD)
    d.rectangle([0, 100, W, 105], fill=RED)
    d.text((24, 16), "WEDNESDAY 18 NOVEMBER 2026", font=font(34, bold=True),
           fill=(255, 255, 255))
    d.text((1000, 16), "THE WORLD IN ONE DAY", font=font(22, bold=True),
           fill=GOLD, anchor="ra")
    d.text((24, 60), "30 STORIES  ·  SIX CONTINENTS  ·  ONE DAY",
           font=font(20, bold=True), fill=(203, 213, 225))
    d.text((1000, 60), "18 NOV 2026", font=font(20, bold=True),
           fill=(203, 213, 225), anchor="ra")

    # --- world map --------------------------------------------------------
    map_x0, map_y0, map_x1, map_y1 = 16, 118, 1008, 262
    d.rounded_rectangle([map_x0, map_y0, map_x1, map_y1], radius=8,
                        fill=MAP_SEA, outline=PANEL_LINE, width=1)
    d.text((map_x0 + 10, map_y0 + 6), "WHERE THE NEWS HAPPENED",
           font=font(13, bold=True), fill=MUTED)

    def project(lon, lat):
        x = map_x0 + 8 + (lon + 170) / 360.0 * (map_x1 - map_x0 - 16)
        y = map_y0 + 22 + (75 - lat) / 130.0 * (map_y1 - map_y0 - 30)
        return (x, y)

    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly], fill=MAP_LAND)
    for lon, lat, region in DOTS:
        x, y = project(lon, lat)
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=RED,
                  outline=(255, 255, 255), width=1)

    # --- story grid: 5 columns x 6 rows -----------------------------------
    margin, gap = 16, 8
    cols, rows = 5, 6
    top0 = 274
    grid_h = H - top0 - 30  # leave room for the footer line
    cw = (W - 2 * margin - (cols - 1) * gap) // cols
    ch = (grid_h - (rows - 1) * gap) // rows
    for i, (place, region, headline, caption) in enumerate(STORIES):
        col, row = i % cols, i // cols
        x0 = margin + col * (cw + gap)
        y0 = top0 + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        colour = REGION[region]
        d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=PANEL_BG,
                            outline=PANEL_LINE, width=1)
        d.rectangle([x0, y0 + 4, x0 + 4, y1 - 4], fill=colour)
        tx = x0 + 10
        # place tag
        d.text((tx, y0 + 6), f"{i + 1:02d}  {place}", font=font(12, bold=True),
               fill=colour)
        # headline, up to 2 lines at 15px
        hl = wrap(d, headline, font(15, bold=True), cw - 20)
        y = y0 + 24
        for line in hl[:2]:
            d.text((tx, y), line, font=font(15, bold=True), fill=INK)
            y += 18
        # caption, up to 3 lines at 11px
        cap = wrap(d, caption, font(11), cw - 20)
        for line in cap[:3]:
            d.text((tx, y), line, font=font(11), fill=MUTED)
            y += 14

    # --- footer -----------------------------------------------------------
    d.text((512, H - 16),
           "All 30 stories happened or were first reported on Wednesday 18 November 2026.",
           font=font(14), fill=MUTED, anchor="mm")

    img.save(OUT, optimize=True)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
