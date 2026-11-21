#!/usr/bin/env python3
"""Build the Friday 20 November 2026 front page (1024x1024) with PIL.

Fresh code written for the v5 entry. Structure follows the winning template:
giant serif date masthead, region bar, THE DAY IN NUMBERS strip, UTC timeline,
3 illustrated hero cards, 10 illustrated medium cards, world map with numbered
pins, numbered briefs, DATE CHECK, sources per story. Every illustration is an
original flat-vector drawing made in code. The market chart comes from
make_chart.py (matplotlib, verified closing figures only).
"""
import json
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 24
CW = W - 2 * MX
BG = (247, 243, 232)
INK = (26, 26, 26)
MUT = (96, 89, 74)
RED = (166, 30, 34)
NAVY = (14, 42, 71)
LINE = (178, 170, 148)
PANEL = (239, 232, 211)
BADGE = {"OFFICIAL": (46, 107, 52), "CONFIRMED": (46, 90, 136), "REPORTED": (107, 107, 107)}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def F(path, size):
    if (path, size) not in _cache:
        _cache[(path, size)] = ImageFont.truetype(path, size)
    return _cache[(path, size)]


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def pill(d, x, y, text, font, bg, fg=(255, 255, 255)):
    w = int(d.textlength(text, font=font)) + 10
    h = font.size + 6
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    d.text((x + 5, y + 3), text, font=font, fill=fg)
    return w


def dashed_line(d, p0, p1, fill, width=2, dash=7, gap=5):
    import math
    x0, y0 = p0
    x1, y1 = p1
    dist = math.hypot(x1 - x0, y1 - y0)
    n = max(1, int(dist / (dash + gap)))
    for i in range(n):
        t0 = i / n
        t1 = (i + dash / (dash + gap)) / n
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=fill, width=width)


# ---------------------------------------------------------------- illustrations
def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    rng = random.Random(42)
    for _ in range(26):
        sx, sy = x + rng.randint(4, w - 4), y + rng.randint(3, h // 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 210, 225))
    # skyline
    base = y + h - 26
    bx, bw = x, w // 7
    heights = [26, 40, 22, 52, 34, 46, 28]
    for i, hh in enumerate(heights):
        d.rectangle([bx + i * bw + 2, base - hh, bx + (i + 1) * bw - 2, base + 26],
                    fill=(10, 26, 48))
        for wy in range(base - hh + 5, base - 2, 9):
            if rng.random() < 0.5:
                d.rectangle([bx + i * bw + 5, wy, bx + i * bw + 8, wy + 4], fill=(255, 200, 90))
    # river
    d.rectangle([x, base, x + w, y + h], fill=(28, 78, 138))
    d.line([x, base + 8, x + w, base + 8], fill=(120, 170, 220), width=2)
    d.line([x, base + 16, x + w, base + 16], fill=(90, 140, 200), width=1)
    # bridges: three arcs over the river
    for cx in (0.22, 0.5, 0.78):
        ccx = x + int(w * cx)
        d.arc([ccx - 34, base - 16, ccx + 34, base + 22], start=180, end=360,
              fill=(230, 230, 225), width=3)
        d.line([ccx - 34, base + 2, ccx + 34, base + 2], fill=(230, 230, 225), width=2)
    # missile trails
    dashed_line(d, (x + 12, y + 6), (x + int(w * 0.30), base - 6), (255, 170, 60), 2)
    dashed_line(d, (x + w - 14, y + 10), (x + int(w * 0.62), base - 8), (255, 170, 60), 2)
    # fires on the bridges
    for fx in (0.22, 0.5, 0.78):
        fxx, fyy = x + int(w * fx), base - 4
        d.ellipse([fxx - 8, fyy - 8, fxx + 8, fyy + 8], fill=(255, 120, 30))
        d.ellipse([fxx - 4, fyy - 4, fxx + 4, fyy + 4], fill=(255, 210, 90))
    # smoke
    d.ellipse([x + int(w * 0.52), y + 8, x + int(w * 0.52) + 12, y + 20], fill=(120, 120, 120))


def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 110, 166))
    # land: east coast of India, left side
    land = [(x, y + int(h * 0.10)), (x + int(w * 0.30), y), (x + int(w * 0.48), y + int(h * 0.22)),
            (x + int(w * 0.42), y + int(h * 0.52)), (x + int(w * 0.34), y + int(h * 0.78)),
            (x + int(w * 0.18), y + h), (x, y + h)]
    d.polygon(land, fill=(227, 213, 179))
    d.line(land + [land[0]], fill=(180, 164, 126), width=1)
    # cyclone spiral
    cx, cy = x + int(w * 0.64), y + int(h * 0.44)
    for r in range(10, 46, 8):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=470,
              fill=(255, 255, 255), width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    # landfall dot at Gopalpur
    gx, gy = x + int(w * 0.47), y + int(h * 0.52)
    d.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=(200, 30, 30))
    d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(255, 255, 255))
    dashed_line(d, (x + w - 6, y + int(h * 0.20)), (gx + 4, gy - 4), (255, 120, 90), 2)
    # rain streaks
    for rx in range(0, 5):
        sx = x + 10 + rx * 14
        d.line([sx, y + h - 34, sx - 5, y + h - 22], fill=(200, 220, 240), width=2)


def art_markets(d, x, y, w, h):
    chart = Image.open("chart.png").convert("RGB")
    chart = chart.resize((w, h), Image.LANCZOS)
    img.paste(chart, (x, y))


def art_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 239, 230))
    # Union Jack, simplified
    jx, jy, jw, jh = x + 6, y + 6, w // 2 - 10, h - 12
    d.rectangle([jx, jy, jx + jw, jy + jh], fill=(18, 44, 92))
    d.line([jx, jy, jx + jw, jy + jh], fill=(255, 255, 255), width=4)
    d.line([jx + jw, jy, jx, jy + jh], fill=(255, 255, 255), width=4)
    d.line([jx + jw // 2, jy, jx + jw // 2, jy + jh], fill=(200, 30, 40), width=5)
    d.line([jx, jy + jh // 2, jx + jw, jy + jh // 2], fill=(200, 30, 40), width=5)
    # EU flag
    ex, ey, ew, eh = x + w // 2 + 4, y + 6, w // 2 - 10, h - 12
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153))
    import math
    for k in range(8):
        a = 2 * math.pi * k / 8
        sx = ex + ew // 2 + int(0.32 * ew * math.cos(a))
        sy = ey + eh // 2 + int(0.32 * eh * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 0))


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 233, 242))
    cx, cy, r = x + w // 3, y + h // 2, h // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 110, 180))
    d.ellipse([cx - r + 6, cy - r + 4, cx - r + 16, cy - r + 12], fill=(90, 170, 90))
    d.ellipse([cx + 2, cy + 2, cx + 14, cy + 12], fill=(90, 170, 90))
    # thermometer
    tx = x + w - 26
    d.rounded_rectangle([tx, y + 6, tx + 10, y + h - 12], radius=5, fill=(255, 255, 255),
                        outline=(120, 120, 120))
    d.rectangle([tx + 3, y + h - 20, tx + 7, y + h - 12], fill=(200, 30, 30))
    d.ellipse([tx - 3, y + h - 16, tx + 13, y + h - 2], fill=(200, 30, 30))


def art_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(207, 227, 192))
    for tx in (0.18, 0.34, 0.52):
        txx, tyy = x + int(w * tx), y + h - 8
        d.polygon([(txx, tyy - 22), (txx - 9, tyy), (txx + 9, tyy)], fill=(30, 90, 50))
    # missile, diagonal
    mx, my = x + int(w * 0.62), y + 12
    d.polygon([(mx, my), (mx + 26, my + 12), (mx + 20, my + 18), (mx - 4, my + 8)],
              fill=(120, 120, 125))
    d.polygon([(mx + 26, my + 12), (mx + 34, my + 16), (mx + 26, my + 20)], fill=(90, 90, 95))
    dashed_line(d, (x + 6, y + h - 6), (x + w - 6, y + h - 6), (200, 30, 30), 2)


def art_iraq(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 217, 176))
    d.ellipse([x + w - 30, y + 4, x + w - 10, y + 24], fill=(255, 220, 130))
    for i, tx in enumerate((0.10, 0.38, 0.66)):
        txx = x + int(w * tx)
        d.rectangle([txx, y + h - 22, txx + 26, y + h - 12], fill=(60, 90, 50))
        d.rectangle([txx + 26, y + h - 19, txx + 34, y + h - 12], fill=(60, 90, 50))
        d.ellipse([txx + 4, y + h - 12, txx + 10, y + h - 6], fill=(30, 30, 30))
        d.ellipse([txx + 22, y + h - 12, txx + 28, y + h - 6], fill=(30, 30, 30))
    d.line([x + 8, y + h - 6, x + w - 8, y + h - 6], fill=(150, 120, 80), width=2)


def art_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 239, 230))
    cols = [(255, 205, 170), (200, 150, 110), (240, 190, 150), (180, 130, 95), (255, 215, 180)]
    for i, c in enumerate(cols):
        hx = x + 14 + i * 32
        d.ellipse([hx, y + 14, hx + 18, y + 32], fill=c)
        d.rectangle([hx - 2, y + 32, hx + 20, y + h - 4], fill=(90, 90, 110) if i % 2 else (140, 60, 60))
    d.rectangle([x + 20, y + 2, x + 58, y + 12], fill=(255, 255, 255), outline=(120, 120, 120))
    d.rectangle([x + w - 62, y + 4, x + w - 24, y + 14], fill=(255, 255, 255), outline=(120, 120, 120))


def art_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.ellipse([x + w - 32, y + 18, x + w - 14, y + 36], fill=(200, 30, 40))
    bars = [10, 16, 22, 30]
    for i, bh in enumerate(bars):
        bx = x + 12 + i * 20
        d.rectangle([bx, y + h - 6 - bh, bx + 12, y + h - 6], fill=(120, 120, 125))
    d.line([x + 10, y + h - 40, x + w - 20, y + 14], fill=(200, 30, 40), width=3)
    d.polygon([(x + w - 20, y + 14), (x + w - 30, y + 16), (x + w - 22, y + 24)], fill=(200, 30, 40))


def art_seoul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    bx, by = x + 14, y + 8
    d.polygon([(bx, by + 10), (bx + 52, by + 10), (bx + 26, by)], fill=(90, 90, 100))
    d.rectangle([bx, by + 10, bx + 52, by + 36], fill=(150, 145, 135))
    for cx in range(4):
        d.rectangle([bx + 6 + cx * 12, by + 12, bx + 10 + cx * 12, by + 34], fill=(240, 240, 235))
    d.rectangle([bx - 4, by + 36, bx + 56, by + 40], fill=(90, 90, 100))
    # gavel
    gx, gy = x + w - 52, y + h - 20
    d.rectangle([gx, gy, gx + 26, gy + 8], fill=(120, 80, 40))
    d.line([gx + 26, gy + 4, gx + 44, gy - 6], fill=(120, 80, 40), width=4)


def art_kenya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 178, 92))
    d.ellipse([x + w - 40, y + 4, x + w - 16, y + 28], fill=(255, 230, 140))
    dx, dy = x + w // 2, y + 8
    d.line([dx - 16, y + h - 6, dx, dy], fill=(60, 45, 30), width=3)
    d.line([dx + 16, y + h - 6, dx, dy], fill=(60, 45, 30), width=3)
    d.line([dx - 10, y + h - 16, dx + 10, y + h - 16], fill=(60, 45, 30), width=2)
    d.line([dx - 6, y + h - 26, dx + 6, y + h - 26], fill=(60, 45, 30), width=2)
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(120, 90, 50))


def art_bukele(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 234, 242))
    bx, by = x + w // 2 - 26, y + 12
    d.rectangle([bx, by, bx + 52, by + 26], fill=(38, 90, 160))
    d.rectangle([bx + 16, by - 2, bx + 36, by + 2], fill=(255, 255, 255))
    d.line([bx + 8, by + 6, bx + 18, by + 20], fill=(46, 160, 80), width=4)
    d.line([bx + 18, by + 20, bx + 44, by - 2], fill=(46, 160, 80), width=4)
    d.rectangle([x + 8, y + h - 8, x + w - 8, y + h - 4], fill=(120, 120, 130))


def art_phillips(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(127, 176, 105))
    d.rectangle([x + w // 2 - 14, y, x + w // 2 + 14, y + h], fill=(210, 190, 140))
    for sx in (-8, 0, 8):
        d.line([x + w // 2 + sx, y + 6, x + w // 2 + sx, y + 18], fill=(255, 220, 60), width=2)
    d.polygon([(x + 24, y + h - 8), (x + 34, y + h - 8), (x + 52, y + 12), (x + 44, y + 8)],
              fill=(150, 105, 60))
    d.ellipse([x + w - 30, y + 8, x + w - 20, y + 18], fill=(255, 255, 255))
    d.arc([x + w - 30, y + 8, x + w - 20, y + 18], start=90, end=270, fill=(200, 30, 30), width=1)


ARTS = {"kyiv": art_kyiv, "cyclone": art_cyclone, "markets": art_markets,
        "ukeu": art_ukeu, "cop31": art_cop31, "poland": art_poland, "iraq": art_iraq,
        "italy": art_italy, "japan": art_japan, "seoul": art_seoul, "kenya": art_kenya,
        "bukele": art_bukele, "phillips": art_phillips}

CONTINENTS = {
    "N America": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62),
                  (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-95, 16),
                  (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60)],
    "S America": [(-80, 10), (-70, 12), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
                  (-40, -20), (-50, -30), (-60, -40), (-70, -50), (-75, -35), (-80, -20)],
    "Africa": [(-10, 35), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
               (48, 11), (40, 0), (40, -10), (35, -20), (30, -30), (20, -35),
               (15, -30), (12, -18), (8, 4), (-8, 5), (-15, 12)],
    "Europe": [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (12, 55),
               (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (20, 70),
               (10, 64), (5, 60), (-5, 50)],
    "Asia": [(30, 62), (40, 68), (60, 70), (80, 73), (110, 76), (140, 72), (160, 66),
             (178, 65), (170, 60), (160, 55), (140, 45), (130, 42), (127, 40), (122, 38),
             (120, 30), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
             (80, 15), (75, 8), (72, 20), (65, 25), (60, 25), (55, 26), (50, 29),
             (45, 30), (40, 32), (35, 36)],
    "Australia": [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
                  (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (122, -14)],
}


def draw_map(d, bx, by, bw, bh, pins, regions):
    d.rectangle([bx, by, bx + bw, by + bh], fill=(239, 232, 211), outline=LINE, width=1)

    def proj(lon, lat):
        return (bx + (lon + 168) / 360.0 * bw, by + (84 - lat) / 142.0 * bh)

    for name, pts in CONTINENTS.items():
        poly = [proj(lon, lat) for lon, lat in pts]
        d.polygon(poly, fill=(220, 207, 178), outline=(179, 163, 126))
    color_of = {r["name"]: r["color"] for r in regions}
    # numbered badges are offset from their true point where stories cluster
    OFFSETS = {1: (-14, -18), 2: (10, 14), 3: (14, 10), 4: (-30, -18), 5: (14, -6),
               6: (22, -14), 7: (24, 14), 8: (-22, -6), 9: (16, -12), 10: (-14, 10),
               13: (0, -14)}
    for p in pins:
        px, py = proj(p["pin"][0], p["pin"][1])
        col = color_of.get(p["region"], "#6B6B6B")
        dx, dy = OFFSETS.get(p["n"], (0, 0))
        nx, ny = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
            d.line([px, py, nx, ny], fill=col, width=1)
        d.ellipse([nx - 10, ny - 10, nx + 10, ny + 10], fill=col, outline=(255, 255, 255), width=1)
        f = F(SANSB, 10)
        t = str(p["n"])
        d.text((nx - d.textlength(t, font=f) / 2, ny - 7), t, font=f, fill=(255, 255, 255))


def card_image_frame(d, x, y, w, h, item):
    ARTS[item["art"]](d, x, y, w, h)
    # red label banner, top-left
    f = F(SANSB, 10 if w > 200 else 9)
    tw = d.textlength(item["label"], font=f)
    d.rectangle([x, y, x + tw + 10, y + 16], fill=RED)
    d.text((x + 5, y + 3), item["label"], font=f, fill=(255, 255, 255))
    # verification badge, top-right
    bf = F(SANSB, 8)
    pill(d, x + w - (d.textlength(item["badge"], font=bf) + 10) - 4, y + 3,
         item["badge"], bf, BADGE[item["badge"]])
    # tag, bottom-left
    tf = F(SANSB, 8)
    tw2 = d.textlength(item["tag"], font=tf)
    d.rectangle([x, y + h - 14, x + tw2 + 10, y + h], fill=(20, 20, 20))
    d.text((x + 5, y + h - 12), item["tag"], font=tf, fill=(255, 255, 255))


def hero_card(d, x, y, w, h, item):
    card_image_frame(d, x, y, w, 96, item)
    yy = y + 102
    # kicker: number + place
    d.ellipse([x, yy, x + 15, yy + 15], fill=RED)
    nf = F(SANSB, 10)
    t = str(item["n"])
    d.text((x + 7.5 - d.textlength(t, font=nf) / 2, yy + 2), t, font=nf, fill=(255, 255, 255))
    kf = F(SANSB, 11)
    d.text((x + 20, yy + 2), f"{item['place']} · {item['field']}", font=kf, fill=RED)
    yy += 20
    hf = F(SANSB, 19)
    yy = text_lines(d, x, yy, wrap(d, item["headline"], hf, w), hf, INK, 22)
    yy += 2
    sf = F(SANS, 12)
    text_lines(d, x, yy, wrap(d, item["summary"], sf, w)[:2], sf, (50, 50, 50), 15)
    srcf = F(SANSB, 9)
    d.text((x, y + h - 12), item["source"].upper(), font=srcf, fill=RED)


def medium_card(d, x, y, w, h, item):
    card_image_frame(d, x, y, w, 46, item)
    yy = y + 50
    kf = F(SANSB, 9)
    d.text((x, yy), f"{item['n']} {item['place']} · {item['field']}", font=kf, fill=RED)
    yy += 13
    hf = F(SANSB, 12)
    yy = text_lines(d, x, yy, wrap(d, item["headline"], hf, w), hf, INK, 14)
    yy += 1
    sf = F(SANS, 10)
    text_lines(d, x, yy, wrap(d, item["summary"], sf, w)[:2], sf, (50, 50, 50), 12)
    srcf = F(SANSB, 8)
    d.text((x, y + h - 10), item["source"].upper(), font=srcf, fill=RED)


def main():
    global img
    data = json.load(open("stories.json"))
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    y = 8
    # eyebrow
    ef = F(SANSB, 12)
    d.text((MX, y), data["eyebrow_left"], font=ef, fill=RED)
    rf = F(SANS, 11)
    rt = data["eyebrow_right"]
    d.text((W - MX - d.textlength(rt, font=rf), y + 1), rt, font=rf, fill=INK)
    y += 20
    d.line([MX, y, W - MX, y], fill=INK, width=2)
    y += 6
    # masthead
    mf = F(SERIFB, 62)
    d.text((MX, y), data["masthead"], font=mf, fill=INK)
    y += 72
    # subhead
    sf = F(SERIFI, 17)
    d.text((MX, y), data["subhead"], font=sf, fill=(60, 55, 45))
    y += 24
    # numbers strip
    cells = data["numbers"]
    cw = CW // len(cells)
    nf = F(SANSB, 28)
    lf = F(SANS, 10)
    for i, c in enumerate(cells):
        cx = MX + i * cw
        if i:
            d.line([cx - 4, y + 2, cx - 4, y + 40], fill=LINE, width=1)
        neg = c["value"].startswith("−")
        d.text((cx, y), c["value"], font=nf, fill=RED if neg else INK)
        text_lines(d, cx, y + 32, wrap(d, c["label"], lf, cw - 10), lf, MUT, 12)
    y += 46
    # region bar
    total = sum(r["count"] for r in data["regions"])
    rx = MX
    rf2 = F(SANSB, 11)
    for i, r in enumerate(data["regions"]):
        rw = int(CW * r["count"] / total) if i < len(data["regions"]) - 1 else W - MX - rx
        d.rectangle([rx, y, rx + rw, y + 18], fill=r["color"])
        t = f"{r['name']} {r['count']}"
        d.text((rx + rw / 2 - d.textlength(t, font=rf2) / 2, y + 3), t, font=rf2,
               fill=(255, 255, 255))
        rx += rw
    y += 22
    # UTC timeline
    tf = F(SANSB, 10)
    d.text((MX, y), "THE DAY IN UTC", font=tf, fill=RED)
    tx = MX + d.textlength("THE DAY IN UTC", font=tf) + 14
    lab = F(SANS, 10)
    for it in data["timeline"]:
        d.text((tx, y), it["time"], font=tf, fill=RED)
        tx += d.textlength(it["time"] + " ", font=tf)
        d.text((tx, y), it["label"], font=lab, fill=INK)
        tx += d.textlength(it["label"] + "    ", font=lab)
    y += 18
    # heroes
    hw = (CW - 22) // 3
    for i, item in enumerate(data["heroes"]):
        hero_card(d, MX + i * (hw + 11), y, hw, 212, item)
    y += 212
    # medium cards, 2 rows x 5
    mw = (CW - 4 * 9) // 5
    for row in range(2):
        for col in range(5):
            item = data["medium"][row * 5 + col]
            medium_card(d, MX + col * (mw + 9), y, mw, 128, item)
        y += 132
    y += 2
    # map + briefs
    map_w, map_h = 300, 256
    hf2 = F(SANSB, 12)
    d.text((MX, y), "WHERE IT HAPPENED", font=hf2, fill=RED)
    d.text((MX + 340, y), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES", font=hf2, fill=RED)
    y += 18
    draw_map(d, MX, y, map_w, map_h - 40, data["heroes"] + data["medium"], data["regions"])
    cf = F(SANS, 9)
    text_lines(d, MX, y + map_h - 36,
               wrap(d, "Each number is the story with that number on this page.",
                    cf, map_w), cf, MUT, 11)
    # briefs, two columns
    bx = MX + 340
    col_w = (W - MX - bx - 10) // 2
    bf = F(SANS, 10)
    bfb = F(SANSB, 10)
    for ci in range(2):
        for ri in range(11):
            b = data["briefs"][ci * 11 + ri]
            yy = y + ri * 22
            # auto-fit: shrink to 9px if the line is too wide
            f = bf
            while f.size > 9 and (bfb.getlength(f"{b['n']} {b['lead']} ") +
                                 f.getlength(b["text"] + f" ({b['source']})")) > col_w:
                f = F(SANS, f.size - 1)
            xx = bx + ci * (col_w + 10)
            d.text((xx, yy), f"{b['n']} ", font=bfb, fill=RED)
            nx = xx + bfb.getlength(f"{b['n']} ")
            d.text((nx, yy), f"{b['lead']} ", font=bfb, fill=INK)
            nx += bfb.getlength(f"{b['lead']} ")
            d.text((nx, yy), b["text"] + f" ({b['source']})", font=f, fill=(50, 50, 50))
    y += map_h + 8
    # DATE CHECK
    d.rectangle([MX, y, W - MX, y + 36], outline=RED, width=1)
    d.rectangle([MX, y, MX + 108, y + 36], fill=RED)
    d.text((MX + 8, y + 11), "DATE CHECK", font=F(SANSB, 12), fill=(255, 255, 255))
    df = F(SANS, 10)
    text_lines(d, MX + 118, y + 4, wrap(d, data["date_check"], df, W - MX - 128), df, INK, 13)
    y += 34
    # footer
    ff = F(SANS, 9)
    d.text((MX, y), data["footer_left"], font=ff, fill=MUT)
    d.text((W - MX - d.textlength(data["footer_right"], font=ff), y),
           data["footer_right"], font=ff, fill=MUT)

    img.save("entry.png", optimize=True)
    import os
    print("saved entry.png", os.path.getsize("entry.png"), "bytes", img.size)


if __name__ == "__main__":
    main()
