#!/usr/bin/env python3
"""Render the make.fun news-image-20261118 entry: a newspaper front page
summing up Wednesday 18 November 2026 world news. 51 stories (3 photo
leads + 48 numbered grid stories), every story illustrated.
Deterministic: fixed fonts, fixed layout, PNG saved with fixed parameters.

Every story below happened or was first reported on 18 November 2026,
verified against Reuters / AP / AFP / BBC / NYT / official sources.
Stories first reported on 17 Nov (Serbia MiG-29, Russian An-12, Phuket
fire, Spain wage approval, France troop denial) were checked and EXCLUDED.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (163, 18, 18)
GREY = (90, 86, 76)
RULE = (60, 58, 50)
TILE = (232, 224, 205)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_IT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_image(path, w, h):
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, (w, h), Image.LANCZOS)


def trunc(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    words = text.split(" ")
    out = ""
    for w in words:
        t = (out + " " + w).strip()
        if draw.textlength(t + " …", font=fnt) > max_w:
            break
        out = t
    return (out + " …") if out else "…"


# ---------------------------------------------------------------- stories
# (headline, summary, icon). Icons are flat pictograms drawn in code.
COL_A = [
    ("BOARD OF PEACE BLAMES BOTH SIDES",
     "Trump's board: Israel and Hamas both failing ceasefire pledges.", "gavel"),
    ("KAHANA ELECTED SPEAKER",
     "Knesset picks Eisenkot ally Matan Kahana, 66–52, in a blow to Netanyahu.", "vote"),
    ("IRAN REFUSES IAEA INSPECTION",
     "No access to damaged nuclear sites until the war ends, Tehran says.", "lock"),
    ("BAHRAIN ISSUES ALL-CLEAR",
     "Third Iranian attack this week; base hosts the US Navy's 5th Fleet.", "shield"),
    ("ETHIOPIA–ERITREA BUILD-UP",
     "Forces massed on the shared border, within striking distance.", "blast"),
    ("NIGERIA: US INTEL VS MILITANTS",
     "Real-time intel and near-daily missions back the 2027 vote.", "satellite"),
    ("ZAMFARA: 20 ABDUCTED FREED",
     "Police free women and children held 22 days in NW Nigeria.", "cross"),
    ("EGYPT–INDIA TRADE GROUP",
     "Working group on pharma, farm goods and tech barriers.", "chart"),
    ("AU PUSHES SUDAN, CONGO PEACE",
     "African Union urges regional solutions as wars drag on.", "globe"),
    ("RWANDA HUB TALKS IN VIENNA",
     "Delegation in Vienna as EU return-hub plan is debated.", "plane"),
    ("S. AFRICA SHOOTING PROBE GOES ON",
     "17 dead in weekend shootings; police inquiry continues.", "gavel"),
    ("S. SUDAN VOTE UNCERTAIN",
     "AU and UN press for a clear election timeline.", "vote"),
    ("CHINA BUYS W. AFRICAN CRUDE",
     "Gulf tensions push refiners to shift oil supply west.", "tanker"),
    ("US CALLS QESHM STRIKE 'SELF-DEFENCE'",
     "US official: it answered IRGC attacks, incl. a Bahrain radar site.", "jet"),
    ("KUWAIT REPELS DRONE ATTACK",
     "Air defences counter hostile drones at Ali Al Salem base.", "shield"),
]

COL_B = [
    ("APEC OPENS IN SHENZHEN",
     "21 leaders meet in China's tech hub; trade and AI top the agenda.", "globe"),
    ("XI, PUTIN MEET BEFORE TRILATERAL",
     "Talks a day before the first three-way summit with Trump.", "flag"),
    ("XI: STAND AGAINST PROTECTIONISM",
     "Putin calls the West 'former hegemons'; sanctions 'spent'.", "chart"),
    ("EU'S €45BN FOR UKRAINE",
     "Loan repaid only after Russia pays war reparations.", "money"),
    ("PUTIN 'NOT READY' FOR PEACE",
     "Western intel: he aims to fight on through the winter.", "blast"),
    ("PISTORIUS: COLBY COMMENT 'STUPID'",
     "Berlin defends Ukraine's strikes on Wildberries depots.", "shield"),
    ("QUAD'S NEW PLAN IN MANILA",
     "Maritime watch, $85M AI Accelerator and a cable pact.", "plane"),
    ("MODI: FREE E-VISAS FOR ASEAN",
     "Tourism pitch at the East Asia Summit in Manila.", "flag"),
    ("ASEAN CHAIR TO SINGAPORE",
     "Digital economy pact done; sea code 85–90% agreed.", "globe"),
    ("CANADA–CHINA EXTEND DEALS",
     "Carney meets Xi as Ottawa diversifies from the US.", "chart"),
    ("CYCLONE AKVAN RED ALERT",
     "Landfall 20 Nov; gusts to 145 km/h; Andhra on alert.", "storm"),
    ("TAIWAN SEEKS $14BN IN ARMS",
     "US presses UN over flight curbs; China pushes back.", "jet"),
    ("INDIA RE-ELECTED TO ITU COUNCIL",
     "Digital India wins the 2027–30 telecom term.", "phone"),
    ("AMAZON'S $7BN FOR INDIA",
     "Renewables push by 2030, focused on solar and data centres.", "money"),
    ("INDIA'S FIRST SAF PLANT READY",
     "Panipat unit turns used cooking oil into jet fuel.", "tanker"),
]

COL_C = [
    ("PELTOLA WINS ALASKA",
     "Democrats take a 56–44 Senate majority, flipping nine seats.", "vote"),
    ("US LOSES MEASLES STATUS",
     "PAHO: a year of spread ends elimination; RFK Jr vows to regain it.", "cross"),
    ("NVIDIA'S $115.8BN QUARTER",
     "Revenue up 103%; board will not bring Huang back.", "chip"),
    ("HUANG TO FACE SENATE PANEL",
     "Ex-CEO to testify over the spy scandal.", "gavel"),
    ("WAYMO OFF THE FREEWAYS",
     "Driverless rides halted US-wide after California's ban.", "car"),
    ("KALSHI HALTS 'MENTION' BETS",
     "CFTC order ends wagers on Trump's words.", "money"),
    ("AI GUN DETECTOR SUED",
     "System mistook a chips bag for a gun; students held at gunpoint.", "lock"),
    ("AI MODELS MISLABEL CIVILIANS",
     "Tests flag ambulances and schools as military targets.", "chip"),
    ("CRITICAL JAVA FLAW FOUND",
     "AI-hunted bug hits 'practically all major companies'.", "lock"),
    ("FAA HALTS ROUTER ROLLOUT",
     "Router blamed in the nationwide ground stop.", "plane"),
    ("IRS PROBES LEFT-WING GROUPS",
     "Four-plus criminal inquiries since the Charlie Kirk killing.", "gavel"),
    ("DHS: NO SHIPS FOR DEPORTATIONS",
     "Agency rules out deporting migrants by sea.", "ship"),
    ("TRUMP–MARCOS TRADE CLAIM",
     "'Very big deal', says Trump; Manila calls it an understanding.", "flag"),
    ("VULCAN FAULT FOUND",
     "ULA: fuel supply starved the BE-4 engines; 40 satellites lost.", "rocket"),
    ("DHONI'S FAREWELL, IN LIGHTS",
     "CSK drone show over Chepauk honours the IPL great's retirement.", "cricket"),
]

COLUMNS = [
    ("MIDDLE EAST & AFRICA", COL_A),
    ("EUROPE & ASIA-PACIFIC", COL_B),
    ("AMERICAS & GLOBAL", COL_C),
]

# (file, headline, summary) — hero first, then two smaller leads.
LEADS = [
    ("media-generation-lead-gulf-intercept-0-bc2708ff-e939-4779-8d4e-817e51f7b71c.webp",
     "IRAN FIRES ON US BASES IN THE GULF",
     "Missiles and drones hit Kuwait's Ali Al Salem base and Bahrain, home of the US 5th Fleet; both say the attacks were intercepted. First Iranian strike on Kuwait since September."),
    ("media-generation-lead-shenzhen-tarmac-0-724eb922-38c4-478d-98a2-4aa9f870b1ff.webp",
     "XI GREETS TRUMP AT SHENZHEN",
     "Xi meets Trump on the tarmac as APEC opens; Xi and Putin talk before Thursday's summit."),
    ("media-generation-lead-voyager-0-cb7eab58-6bf4-4d73-8412-0da4233bbbf1.webp",
     "VOYAGER 1: ONE LIGHT-DAY OUT",
     "At 10:16 UTC the probe passes 25.9bn km out — a first for any human-made object."),
]

NUMBERS = [
    ("$115.8bn", "Nvidia's Q3 revenue, up 103% on a year ago"),
    ("25.9bn km", "Voyager 1 from Earth — one light-day out"),
    ("56–44", "Democrats' Senate majority after Alaska win"),
    ("€45bn", "EU's new loan for Ukraine, proposed today"),
]

CLOCK = [
    ("00:16 UTC", "Iran fires at Kuwait & Bahrain"),
    ("10:16 UTC", "Voyager 1: one light-day"),
    ("MORNING", "Xi greets Trump in Shenzhen"),
    ("MIDDAY", "Trump meets Marcos in Manila"),
    ("EVENING", "Nvidia posts $115.8bn quarter"),
]

# Numbered map pins: (fraction x, fraction y of the fit-cropped map,
# label, label anchor: 'r' = label right of dot, 'l' = left of dot,
# 'b' = below-right, 'a' = above-left). Fractions are mapped through the
# centre crop ImageOps.fit applies to reach the 470x202 map area.
PINS = [
    (0.050, 0.197, "ALASKA", "r"),
    (0.477, 0.667, "NIGERIA", "l"),
    (0.575, 0.650, "ETHIOPIA", "r"),
    (0.592, 0.372, "ISRAEL", "l"),
    (0.620, 0.411, "KUWAIT", "b"),
    (0.855, 0.439, "SHENZHEN", "r"),
    (0.870, 0.600, "MANILA", "r"),
    (0.752, 0.559, "ANDHRA", "r"),
    (0.729, 0.452, "DELHI", "a"),
]

ICON_COLORS = {"chip": (26, 72, 140), "cross": (163, 18, 18), "globe": (18, 110, 88),
               "gavel": (94, 52, 140), "chart": (26, 72, 140), "plane": (18, 110, 88),
               "jet": (94, 52, 140), "lock": (163, 18, 18), "car": (26, 72, 140),
               "blast": (176, 106, 12), "phone": (60, 60, 60), "tanker": (163, 18, 18),
               "rocket": (94, 52, 140), "vote": (18, 110, 88), "money": (176, 106, 12),
               "storm": (26, 72, 140), "cricket": (18, 110, 88), "satellite": (26, 72, 140),
               "flag": (163, 18, 18), "shield": (26, 72, 140), "clock": (60, 60, 60),
               "ship": (18, 110, 88)}


def draw_icon(d, kind, x, y, s, color):
    """Simple flat geometric pictogram inside an s x s box at (x, y)."""
    if kind == "chip":
        d.rounded_rectangle([x + 4, y + 4, x + s - 4, y + s - 4], 3, fill=color)
        d.rectangle([x + 7, y + 7, x + s - 7, y + s - 7], outline=PAPER, width=2)
        for i in range(3):
            d.line([x + 6 + i * 5, y + 1, x + 6 + i * 5, y + 4], fill=color, width=2)
            d.line([x + 6 + i * 5, y + s - 4, x + 6 + i * 5, y + s - 1], fill=color, width=2)
    elif kind == "cross":
        d.rectangle([x + s // 2 - 2, y + 3, x + s // 2 + 2, y + s - 3], fill=color)
        d.rectangle([x + 3, y + s // 2 - 2, x + s - 3, y + s // 2 + 2], fill=color)
    elif kind == "globe":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=color, width=2)
        d.ellipse([x + s // 2 - 4, y + 2, x + s // 2 + 4, y + s - 2], outline=color, width=2)
        d.line([x + 2, y + s // 2, x + s - 2, y + s // 2], fill=color, width=2)
    elif kind == "gavel":
        d.rectangle([x + 3, y + 4, x + s - 7, y + 10], fill=color)
        d.line([x + s - 7, y + 10, x + s - 2, y + s - 3], fill=color, width=3)
    elif kind == "chart":
        for i, hgt in enumerate((6, 10, 14)):
            d.rectangle([x + 3 + i * 6, y + s - 3 - hgt, x + 7 + i * 6, y + s - 3], fill=color)
    elif kind in ("plane", "jet"):
        d.polygon([(x + 2, y + s // 2), (x + s - 3, y + s // 2 - 2), (x + s - 3, y + s // 2 + 2)],
                  fill=color)
        d.polygon([(x + s // 2 - 2, y + s // 2 - 2), (x + s // 2 + 5, y + 2),
                   (x + s // 2 + 7, y + 2), (x + s // 2 + 3, y + s // 2)], fill=color)
        d.polygon([(x + s // 2 - 2, y + s // 2 + 2), (x + s // 2 + 5, y + s - 2),
                   (x + s // 2 + 7, y + s - 2), (x + s // 2 + 3, y + s // 2)], fill=color)
    elif kind == "lock":
        d.arc([x + 6, y + 3, x + s - 6, y + 13], 180, 360, fill=color, width=2)
        d.rounded_rectangle([x + 4, y + 11, x + s - 4, y + s - 3], 2, fill=color)
    elif kind == "car":
        d.rounded_rectangle([x + 2, y + 10, x + s - 2, y + s - 6], 3, fill=color)
        d.polygon([(x + 6, y + 10), (x + 9, y + 5), (x + s - 9, y + 5), (x + s - 6, y + 10)],
                  fill=color)
        d.ellipse([x + 5, y + s - 8, x + 9, y + s - 4], fill=INK)
        d.ellipse([x + s - 9, y + s - 8, x + s - 5, y + s - 4], fill=INK)
    elif kind == "blast":
        cx, cy, r1, r2 = x + s // 2, y + s // 2, s // 2 - 2, s // 4
        pts = []
        for i in range(12):
            r = r1 if i % 2 == 0 else r2
            a = math.pi * i / 6
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=color)
    elif kind == "phone":
        d.rounded_rectangle([x + 6, y + 2, x + s - 6, y + s - 2], 3, outline=color, width=2)
        d.line([x + 9, y + 6, x + s - 9, y + 6], fill=color, width=2)
        d.line([x + 9, y + 10, x + s - 9, y + 10], fill=color, width=2)
    elif kind == "tanker":
        d.polygon([(x + 2, y + s - 7), (x + s - 2, y + s - 7), (x + s - 5, y + s - 2),
                   (x + 5, y + s - 2)], fill=color)
        d.rectangle([x + s - 10, y + 5, x + s - 4, y + s - 7], fill=color)
        d.rectangle([x + 5, y + 10, x + s - 11, y + s - 7], fill=color)
    elif kind == "rocket":
        d.polygon([(x + s // 2, y + 1), (x + s - 5, y + 11), (x + s // 2 + 2, y + s - 7),
                   (x + s // 2 - 2, y + s - 7), (x + 5, y + 11)], fill=color)
        d.polygon([(x + s // 2 - 2, y + s - 7), (x + s // 2 + 2, y + s - 7),
                   (x + s // 2, y + s - 1)], fill=(176, 106, 12))
    elif kind == "vote":
        d.rounded_rectangle([x + 3, y + 5, x + s - 3, y + s - 3], 2, outline=color, width=2)
        d.line([x + 5, y + s // 2 + 1, x + 8, y + s - 5, x + s - 4, y + 5],
               fill=color, width=2)
    elif kind == "money":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=color, width=2)
        d.text((x + s // 2, y + s // 2 - 1), "$", font=font(F_BOLD, 12),
               fill=color, anchor="mm")
    elif kind == "storm":
        d.ellipse([x + 2, y + 3, x + 11, y + 10], fill=color)
        d.ellipse([x + 8, y + 2, x + s - 2, y + 11], fill=color)
        d.polygon([(x + s // 2 + 1, y + 9), (x + s // 2 - 3, y + s - 2),
                   (x + s // 2 + 1, y + s - 2), (x + s // 2 - 1, y + s - 6),
                   (x + s // 2 + 3, y + s - 6)], fill=(176, 106, 12))
    elif kind == "cricket":
        d.line([x + 5, y + 3, x + s - 6, y + s - 6], fill=color, width=3)
        d.ellipse([x + s - 8, y + 2, x + s - 3, y + 7], fill=(163, 18, 18))
    elif kind == "satellite":
        d.rectangle([x + s // 2 - 3, y + s // 2 - 3, x + s // 2 + 3, y + s // 2 + 3],
                    fill=color)
        d.rectangle([x + 1, y + 4, x + s // 2 - 4, y + s - 5], outline=color, width=2)
        d.rectangle([x + s // 2 + 4, y + 4, x + s - 1, y + s - 5], outline=color, width=2)
        d.line([x + s // 2, y + 2, x + s // 2 + 4, y + s // 2 - 3], fill=color, width=2)
    elif kind == "flag":
        d.line([x + 4, y + 2, x + 4, y + s - 2], fill=color, width=2)
        d.polygon([(x + 4, y + 2), (x + s - 2, y + 5), (x + 4, y + 9)], fill=color)
    elif kind == "shield":
        d.polygon([(x + 3, y + 3), (x + s - 3, y + 3), (x + s - 3, y + 10),
                   (x + s // 2, y + s - 2), (x + 3, y + 10)], outline=color, width=2)
        d.line([x + 6, y + s // 2, x + 9, y + s - 5, x + s - 5, y + 5],
               fill=color, width=2)
    elif kind == "clock":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=color, width=2)
        d.line([x + s // 2, y + s // 2, x + s // 2, y + 5], fill=color, width=2)
        d.line([x + s // 2, y + s // 2, x + s - 5, y + s // 2 + 2], fill=color, width=2)
    elif kind == "ship":
        d.polygon([(x + 2, y + s - 7), (x + s - 2, y + s - 7), (x + s - 5, y + s - 2),
                   (x + 5, y + s - 2)], fill=color)
        d.rectangle([x + 5, y + 4, x + 10, y + s - 7], fill=color)
        d.rectangle([x + 11, y + 7, x + s - 6, y + s - 7], outline=color, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_mast = font(F_SERIF, 46)
    f_date = font(F_BOLD, 21)
    f_deck = font(F_BOLD, 13)
    f_hero_h = font(F_BOLD, 14)
    f_hero_s = font(F_SANS, 11)
    f_lead_h = font(F_BOLD, 12)
    f_lead_s = font(F_SANS, 10)
    f_quote = font(F_SERIF_IT, 11)
    f_col = font(F_BOLD, 12)
    f_head = font(F_BOLD, 11)
    f_sum = font(F_SANS, 10)
    f_num = font(F_BOLD, 10)
    f_map = font(F_BOLD, 9)
    f_foot = font(F_BOLD, 12)
    f_small = font(F_SANS, 10)

    # ---- masthead
    d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=f_mast, fill=INK, anchor="ma")
    d.text((W // 2, 62), "WEDNESDAY  ·  18 NOVEMBER 2026", font=f_date, fill=RED, anchor="ma")
    d.line([16, 94, W - 16, 94], fill=RULE, width=2)
    d.text((W // 2, 100),
           "48 STORIES  •  6 REGIONS  •  4 CONTINENTS  •  ONE DAY OF WORLD NEWS",
           font=f_deck, fill=INK, anchor="ma")

    # ---- leads: one hero (left) + two smaller (right, photo left / text right)
    lead_y = 118
    # hero
    hx, hw, hp_h = 16, 560, 148
    hero = fit_image(os.path.join(ASSETS, LEADS[0][0]), hw, hp_h)
    img.paste(hero, (hx, lead_y))
    d.rectangle([hx, lead_y, hx + hw - 1, lead_y + hp_h - 1], outline=RULE, width=1)
    cy = lead_y + hp_h + 6
    for line in wrap(d, LEADS[0][1], f_hero_h, hw):
        d.text((hx, cy), line, font=f_hero_h, fill=INK)
        cy += 17
    for line in wrap(d, LEADS[0][2], f_hero_s, hw):
        d.text((hx, cy), line, font=f_hero_s, fill=(40, 40, 40))
        cy += 13
    # two small leads, right column
    rx, rw = 592, 416
    for i in (1, 2):
        fname, head, summ = LEADS[i]
        by = lead_y + (i - 1) * 78
        pw, ph = 150, 66
        photo = fit_image(os.path.join(ASSETS, fname), pw, ph)
        img.paste(photo, (rx, by))
        d.rectangle([rx, by, rx + pw - 1, by + ph - 1], outline=RULE, width=1)
        tx = rx + pw + 8
        tw = rw - pw - 8
        ty = by - 1
        for line in wrap(d, head, f_lead_h, tw)[:2]:
            d.text((tx, ty), line, font=f_lead_h, fill=INK)
            ty += 14
        for line in wrap(d, summ, f_lead_s, tw)[:2]:
            d.text((tx, ty), line, font=f_lead_s, fill=(40, 40, 40))
            ty += 12
    # Xi quote under the small leads
    qy = lead_y + 156
    d.rectangle([rx, qy, rx + rw - 1, qy + 52], outline=RULE, width=1)
    d.rectangle([rx, qy, rx + rw - 1, qy + 52], fill=(232, 224, 205))
    d.text((rx + 8, qy + 5),
           "“China is a country of etiquette and has a", font=f_quote, fill=INK)
    d.text((rx + 8, qy + 20),
           "tradition of reciprocating courtesy.”", font=f_quote, fill=INK)
    d.text((rx + 8, qy + 37), "— XI JINPING, APEC CEO SUMMIT, SHENZHEN",
           font=f_small, fill=GREY)
    d.line([16, 322, W - 16, 322], fill=RULE, width=2)

    # ---- clock strip
    ck_y = 328
    d.rectangle([16, ck_y, 186, ck_y + 28], fill=INK)
    d.text((22, ck_y + 7), "THE DAY BY THE CLOCK", font=f_col, fill=(246, 241, 229))
    cx = 196
    cw = (W - 16 - cx) // len(CLOCK)
    for t, ev in CLOCK:
        d.text((cx + 4, ck_y + 2), t, font=f_num, fill=RED)
        for j, line in enumerate(wrap(d, ev, f_small, cw - 8)):
            d.text((cx + 4, ck_y + 14 + j * 11), line, font=f_small, fill=INK)
        cx += cw
    d.line([16, 364, W - 16, 364], fill=RULE, width=2)

    # ---- map + numbers row
    map_y, map_h = 370, 222
    map_w = 470
    d.rectangle([16, map_y, 16 + map_w - 1, map_y + 19], fill=INK)
    d.text((22, map_y + 3), "WHERE IT HAPPENED — 9 PLACES", font=f_col,
           fill=(246, 241, 229))
    world = Image.open(os.path.join(
        ASSETS, "media-generation-world-map-0-45ca06c3-66d7-4e0e-8184-7c126301f064.webp")
    ).convert("RGB")
    grey = world.convert("L")
    bbox = grey.point(lambda p: 255 if p < 200 else 0).getbbox()
    world = world.crop(bbox)
    # drop Antarctica: cut the bottom 12% of the cropped map
    world = world.crop((0, 0, world.width, int(world.height * 0.88)))
    # fill the map area exactly (centre crop to the area's aspect)
    world = ImageOps.fit(world, (map_w, map_h - 20), Image.LANCZOS)
    mx, my = 16, map_y + 20
    img.paste(world, (mx, my))
    d.rectangle([mx, my, mx + world.width - 1, my + world.height - 1],
                outline=RULE, width=1)
    for fx, fy, name, side in PINS:
        px, py = mx + int(fx * world.width), my + int(fy * world.height)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                  outline=(255, 255, 255), width=1)
        if side == "r":
            d.text((px + 5, py - 5), name, font=f_map, fill=INK,
                   stroke_width=2, stroke_fill=(246, 241, 229))
        elif side == "l":
            d.text((px - 5, py - 5), name, font=f_map, fill=INK, anchor="ra",
                   stroke_width=2, stroke_fill=(246, 241, 229))
        elif side == "b":
            d.text((px + 5, py + 4), name, font=f_map, fill=INK,
                   stroke_width=2, stroke_fill=(246, 241, 229))
        else:  # 'a' above-left
            d.text((px - 5, py - 13), name, font=f_map, fill=INK, anchor="ra",
                   stroke_width=2, stroke_fill=(246, 241, 229))

    # numbers band
    bx, bw = 500, 508
    d.rectangle([bx, map_y, bx + bw - 1, map_y + 19], fill=INK)
    d.text((bx + 8, map_y + 3), "THE DAY IN NUMBERS", font=f_col, fill=(246, 241, 229))
    d.rectangle([bx, map_y, bx + bw - 1, map_y + map_h - 1], outline=RULE, width=1)
    cell_w, cell_h = bw // 2, (map_h - 20) // 2
    f_big = font(F_BOLD, 28)
    for i, (num, txt) in enumerate(NUMBERS):
        cxx = bx + (i % 2) * cell_w
        cyy = map_y + 20 + (i // 2) * cell_h
        if i % 2 == 1:
            d.line([cxx, cyy + 6, cxx, cyy + cell_h - 6], fill=(200, 192, 170), width=1)
        if i // 2 == 1:
            d.line([cxx + 6, cyy, cxx + cell_w - 6, cyy], fill=(200, 192, 170), width=1)
        d.text((cxx + 10, cyy + 8), num, font=f_big, fill=RED)
        ty = cyy + 44
        for line in wrap(d, txt, f_small, cell_w - 20):
            d.text((cxx + 10, ty), line, font=f_small, fill=INK)
            ty += 12
    d.line([16, 596, W - 16, 596], fill=RULE, width=2)

    # ---- story grid: 3 columns x 15 numbered rows
    grid_y = 602
    col_w = (W - 32 - 2 * 12) // 3
    cell_h = 24
    n_illustrated = 3  # the three photo leads
    for ci, (title, items) in enumerate(COLUMNS):
        cx = 16 + ci * (col_w + 12)
        d.rectangle([cx, grid_y, cx + col_w - 1, grid_y + 17], fill=INK)
        d.text((cx + 6, grid_y + 2), title, font=f_col, fill=(246, 241, 229))
        y = grid_y + 22
        for n, (head, summ, icon) in enumerate(items, start=1):
            tx = cx
            if icon:
                d.rectangle([cx, y + 1, cx + 19, y + 20], fill=TILE, outline=RULE, width=1)
                draw_icon(d, icon, cx, y + 1, 20, ICON_COLORS[icon])
                n_illustrated += 1
                tx = cx + 24
            f_no = font(F_BOLD, 10)
            num = f"{n:02d}"
            d.text((tx, y), num, font=f_no, fill=RED)
            nw = d.textlength(num, font=f_no)
            d.text((tx + nw + 4, y),
                   trunc(d, head, f_head, col_w - (tx - cx) - nw - 4),
                   font=f_head, fill=INK)
            d.text((tx, y + 12),
                   trunc(d, summ, f_sum, col_w - (tx - cx)), font=f_sum,
                   fill=(50, 48, 42))
            y += cell_h
        if ci < 2:
            d.line([cx + col_w + 6, grid_y, cx + col_w + 6, 984],
                   fill=(200, 192, 170), width=1)

    # ---- footer
    d.line([16, 988, W - 16, 988], fill=RULE, width=2)
    d.text((W // 2, 994),
           f"48 STORIES  •  {n_illustrated} ILLUSTRATED  •  WEDNESDAY 18 NOVEMBER 2026",
           font=f_foot, fill=INK, anchor="ma")
    d.text((W // 2, 1010),
           "All 48 stories happened or were first reported on 18 Nov 2026 — date-checked "
           "against Reuters, AP, AFP, BBC, NYT and official sources.",
           font=f_small, fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes",
          "illustrated:", n_illustrated)


if __name__ == "__main__":
    main()
