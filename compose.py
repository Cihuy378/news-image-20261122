#!/usr/bin/env python3
"""Draw the front page for news-image-20261122.

One 1024x1024 newspaper front page summing up the world news of
Sunday 22 November 2026. Every word is rendered here with Pillow, so
no AI-generated text can come out garbled. The four editorial pictures
in assets/ carry no text of their own.

Layout, top to bottom: kicker, masthead, standfirst, a strip of key
numbers, a region bar, three large lead stories with pictures, five
shorter leads (one with a picture), a world map beside the numbered
list of the remaining briefs, a date-check box, and a footer.

30 stories in all, across 7 regions. The count on the date strip is
checked by hand against the stories drawn: 9 leads + 21 briefs = 30.

Deterministic: no network, no clock, no randomness. Running this
script twice writes the same entry.png byte for byte.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (22, 22, 22)
RED = (178, 32, 32)
NAVY = (28, 52, 88)
TEAL = (14, 96, 96)
GREY = (98, 94, 84)
RULE = (180, 172, 158)
SKY = (198, 220, 228)
LAND = (222, 206, 178)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_crop(img, tw, th):
    """Centre-crop to the target aspect, then resize to it."""
    iw, ih = img.size
    want = tw / th
    have = iw / ih
    if have > want:
        nw = int(ih * want)
        x0 = (iw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / want)
        y0 = (ih - nh) // 2
        img = img.crop((0, y0, iw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, gap=3, max_lines=None):
    """Draw a wrapped paragraph; return the y just below it."""
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def headline(draw, x, y, text, size, width, max_lines=3):
    fnt = font(SERIF_B, size)
    return para(draw, x, y, text, fnt, width, gap=1, max_lines=max_lines)


def kicker(draw, x, y, text, fill=RED, size=11):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + size + 4


def load_pic(name, tw, th):
    path = os.path.join(ASSETS, name)
    img = Image.open(path).convert("RGB")
    return fit_crop(img, tw, th)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    mx = 24
    right = W - mx

    # ---- kicker line -------------------------------------------------
    d.text((mx, 12), "THE WORLD IN ONE DAY", font=font(SANS_B, 12), fill=RED)
    tail = "AS REPORTED ON SUNDAY 22 NOVEMBER 2026"
    d.text((right - d.textlength(tail, font=font(SANS_B, 12)), 12),
           tail, font=font(SANS_B, 12), fill=GREY)
    d.line([(mx, 30), (right, 30)], fill=RULE, width=1)

    # ---- masthead ----------------------------------------------------
    d.text((mx, 34), "Sunday 22 November 2026",
           font=font(SERIF_B, 56), fill=INK)
    d.text((mx, 100),
           "COP31 nears a deal in Antalya  ·  Iran strikes US bases in Bahrain  ·  Tankers hit in Hormuz",
           font=font(SERIF, 15), fill=(60, 60, 60))

    # ---- key-numbers strip -------------------------------------------
    stats = [
        ("06:00 GMT", "COP31 approval vote"),
        ("M 6.7", "Peru quake toll: 1 dead"),
        ("16", "crew off the Sparta II"),
        ("2", "tankers hit in Hormuz"),
        ("37–12", "England beat All Blacks"),
    ]
    y0, y1 = 124, 160
    d.rectangle([mx, y0, right, y1], outline=RULE, width=1)
    cell = (right - mx) // 5
    for i, (big, small) in enumerate(stats):
        x = mx + i * cell + 10
        if i:
            d.line([(mx + i * cell, y0 + 4), (mx + i * cell, y1 - 4)],
                   fill=RULE, width=1)
        d.text((x, y0 + 3), big, font=font(SERIF_B, 18), fill=RED)
        d.text((x, y0 + 24), small, font=font(SANS, 8), fill=GREY)

    # ---- region bar ----------------------------------------------------
    regions = [("EUROPE", 11, NAVY), ("ASIA", 2, (176, 128, 32)),
               ("MIDDLE EAST", 7, RED), ("AFRICA", 1, (46, 120, 70)),
               ("AMERICAS", 7, (110, 60, 140)), ("OCEANIA", 1, TEAL),
               ("GLOBAL", 1, GREY)]
    y = 166
    x = mx
    total_w = right - mx
    for name, n, col in regions:
        label = "%s %d" % (name, n)
        w = int(total_w * n / 30)
        d.rectangle([x, y, x + w - 2, y + 16], fill=col)
        if w >= 70:
            tw = d.textlength(label, font=font(SANS_B, 9))
            d.text((x + (w - tw) / 2, y + 3), label,
                   font=font(SANS_B, 9), fill=(255, 255, 255))
        x += w
    d.text((mx, 186),
           "30 STORIES  ·  7 REGIONS — EUROPE 11 · ASIA 2 · MIDDLE EAST 7 · AFRICA 1 · AMERICAS 7 · OCEANIA 1 · GLOBAL 1",
           font=font(SANS_B, 10), fill=INK)

    # ---- lead row: three large stories --------------------------------
    top = 206
    colw = 318
    gap = 10
    lead_h = 208
    leads = [
        ("media-generation-cop31-antalya-0-8a62d543-e311-43f0-a40c-ef60983632b7.webp",
         "1  ·  ANTALYA, TURKIYE — CLIMATE",
         "COP31 nears a deal as a new text is tabled",
         "After two days of overtime, the presidents put forward a package "
         "they say all sides can accept. Objections by 03:00 GMT; vote at "
         "06:00 GMT. (Reuters)"),
        ("media-generation-gulf-tanker-0-d2eaad41-35fa-4b94-a846-358d3a9b70de.webp",
         "2–3  ·  BAHRAIN & HORMUZ — WAR",
         "Iran strikes US bases as tankers are hit",
         "Tehran says it hit US bases at al-Riffa and Awali; Bahrain says a "
         "plant caught fire, no injuries. Two tankers were hit leaving the "
         "Strait of Hormuz. (Al Jazeera, UKMTO)"),
        ("media-generation-sparta-ship-0-7b76bfa6-9460-424f-baa9-e88a4089b059.webp",
         "4  ·  GULF OF FINLAND — WAR AT SEA",
         "Russian cargo ship ablaze after drone strike",
         "The Sparta II, bound for Kaliningrad, caught fire and drifted into "
         "Finnish waters; all 16 crew were taken off. Kyiv has not confirmed "
         "the drone claim. (Reuters, Finland)"),
    ]
    for i, (pic, kick, head, deck) in enumerate(leads):
        x = mx + i * (colw + gap)
        d.rectangle([x, top, x + colw, top + lead_h], outline=INK, width=1)
        img = load_pic(pic, colw - 2, 96)
        page.paste(img, (x + 1, top + 1))
        yy = top + 102
        yy = kicker(d, x + 8, yy, kick, size=10)
        yy = headline(d, x + 8, yy, head, 17, colw - 16, max_lines=2)
        para(d, x + 8, yy + 2, deck, font(SANS, 10), colw - 16,
             fill=(50, 50, 50), gap=1, max_lines=3)

    # ---- second lead row: five shorter stories -----------------------
    top2 = 424
    colw2 = 188
    gap2 = 12
    row2 = [
        ("media-generation-peru-andes-0-14e6bd68-2605-45c8-be52-872659d9f938.webp",
         "5  ·  PERU — EARTHQUAKE",
         "M6.7 quake: Peru counts the cost",
         "Sunday's toll from Friday's Junin quake: 1 dead, 16 hurt, 152 homes "
         "uninhabitable. Shaking was felt in Lima. (USGS, Peru govt)"),
        (None, "6  ·  KRYVYI RIH — WAR",
         "Missiles kill two in Zelensky's home city",
         "A Russian double-tap strike hit Kryvyi Rih on Friday night: a "
         "7-year-old boy and a 20-year-old paramedic died; 52 were hurt. "
         "(Local officials)"),
        (None, "7  ·  SINALOA, MEXICO — CRIME",
         "Mexico confirms capture of 'El Chapo Isidro'",
         "FBI Top Ten fugitive Fausto Isidro Meza-Flores was seized in "
         "Guasave on Friday; 11 died in the clashes that followed. "
         "(Mexico Defence Ministry)"),
        (None, "8  ·  LAS VEGAS — FORMULA 1",
         "Verstappen on pole for Sunday's race",
         "Antonelli was fastest in qualifying but drops five places for an "
         "engine change, so Verstappen starts first, with Russell beside "
         "him. (F1)"),
        (None, "9  ·  LONDON — RUGBY",
         "England thrash the All Blacks 37–12",
         "A record margin at Twickenham keeps England in the Nations "
         "Championship title hunt; New Zealand lost two in a row. (BBC)"),
    ]
    for i, (pic, kick, head, deck) in enumerate(row2):
        x = mx + i * (colw2 + gap2)
        d.rectangle([x, top2, x + colw2, top2 + 182], outline=INK, width=1)
        yy = top2 + 6
        if pic:
            img = load_pic(pic, colw2 - 2, 62)
            page.paste(img, (x + 1, top2 + 1))
            yy = top2 + 68
        yy = kicker(d, x + 7, yy, kick, size=9)
        yy = headline(d, x + 7, yy, head, 13, colw2 - 14, max_lines=3)
        para(d, x + 7, yy + 2, deck, font(SANS, 9), colw2 - 14,
             fill=(50, 50, 50), gap=1, max_lines=4)

    # ---- map + also-today --------------------------------------------
    top3 = 620
    d.text((mx, top3), "WHERE IT HAPPENED — numbered as the stories",
           font=font(SANS_B, 11), fill=RED)
    map_x, map_y, map_w, map_h = mx, top3 + 20, 372, 168
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                fill=SKY, outline=INK, width=1)
    # rough continents, drawn as simple polygons
    d.polygon([(map_x + 18, map_y + 28), (map_x + 118, map_y + 18),
               (map_x + 128, map_y + 62), (map_x + 96, map_y + 96),
               (map_x + 52, map_y + 88), (map_x + 16, map_y + 58)], fill=LAND)
    d.polygon([(map_x + 78, map_y + 108), (map_x + 128, map_y + 104),
               (map_x + 138, map_y + 138), (map_x + 104, map_y + 162),
               (map_x + 76, map_y + 140)], fill=LAND)
    d.polygon([(map_x + 168, map_y + 22), (map_x + 216, map_y + 16),
               (map_x + 228, map_y + 52), (map_x + 196, map_y + 66),
               (map_x + 168, map_y + 48)], fill=LAND)
    d.polygon([(map_x + 196, map_y + 72), (map_x + 232, map_y + 70),
               (map_x + 240, map_y + 112), (map_x + 212, map_y + 128),
               (map_x + 192, map_y + 100)], fill=LAND)
    d.polygon([(map_x + 238, map_y + 26), (map_x + 340, map_y + 18),
               (map_x + 352, map_y + 66), (map_x + 312, map_y + 96),
               (map_x + 258, map_y + 74)], fill=LAND)
    d.polygon([(map_x + 318, map_y + 118), (map_x + 352, map_y + 116),
               (map_x + 356, map_y + 142), (map_x + 326, map_y + 146)],
              fill=LAND)
    pins = [(292, 52), (318, 78), (332, 84), (268, 34), (96, 128),
            (262, 44), (62, 92), (56, 72), (240, 28)]
    for i, (px, py) in enumerate(pins, start=1):
        cx, cy = map_x + px, map_y + py
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((cx - 3, cy - 6), str(i), font=font(SANS_B, 9),
               fill=(255, 255, 255))
    d.text((mx, top3 + 196),
           "Red dots: stories 1–9 above.  ·  Map drawn for this page.",
           font=font(SANS, 9), fill=GREY)

    # also-today list, stories 10–30, two columns of briefs
    bx = 416
    d.text((bx, top3), "ALSO ON SUNDAY 22 NOVEMBER — 21 MORE STORIES",
           font=font(SANS_B, 11), fill=RED)
    d.line([(bx, top3 + 16), (right, top3 + 16)], fill=RED, width=2)
    briefs = [
        (10, "Poland: Russian missiles land; NATO protests."),
        (11, "Denmark expels Russia's defence attache."),
        (12, "Finland: Russian helicopter flew 4.1 km in."),
        (13, "Houthi missiles at Riyadh intercepted."),
        (14, "Zelensky: no written guarantee seen yet."),
        (15, "Russia rejects NATO-like guarantees."),
        (16, "Ukraine downed 117 of 148 drones."),
        (17, "US denies Iran hit an F-16 jet."),
        (18, "Iran says it downed two US drones."),
        (19, "Kuwait intercepted drones overnight."),
        (20, "Basra power fire kills 4, hurts 35."),
        (21, "Nigeria: 24 bodies after boat capsizes."),
        (22, "EU and Indonesia sign a trade deal."),
        (23, "EU proposes a 1.78tn budget, 2028-34."),
        (24, "Nasdaq dives 5.3%; S&P in correction."),
        (25, "Oil climbs on Gulf supply fears."),
        (26, "FBI probes hack of its NCIC database."),
        (27, "M6.8 quake off Timor-Leste. (USGS)"),
        (28, "Paolo Bulgari, jeweller, has died."),
        (29, "Trump warns firms on AI centres abroad."),
        (30, "Nvidia slides 14% as Huang steps down."),
    ]
    # briefs 10-20 in the left column, 21-30 in the right column
    cols = [(bx, briefs[:11]), (bx + 292, briefs[11:])]
    bf = font(SANS, 10)
    for cx, items in cols:
        yy = top3 + 24
        for n, text in items:
            d.text((cx, yy), "%d." % n, font=font(SANS_B, 10), fill=RED)
            yy = para(d, cx + 22, yy, text, bf, 262, gap=0, max_lines=2)
            yy += 5

    # ---- date check ----------------------------------------------------
    dy = 906
    d.rectangle([mx, dy, right, dy + 62], outline=RED, width=1)
    d.text((mx + 8, dy + 5), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
    para(d, mx + 8, dy + 22,
         "Shown only where Sunday brought something new — a toll, a "
         "confirmation or a vote. The Peru quake struck on Friday, the "
         "Sinaloa capture on Friday, the Kryvyi Rih strike on Friday night. "
         "Not confirmed when drawn: the final COP31 text; the Gulf casualty toll.",
         font(SANS, 10), right - mx - 16, gap=1, max_lines=2)

    # ---- footer ----------------------------------------------------------
    d.line([(mx, 980), (right, 980)], fill=INK, width=2)
    d.text((mx, 988),
           "Every story here happened, or was first reported, on Sunday 22 November 2026.",
           font=font(SANS, 9), fill=GREY)
    src = "Sources named beside each story. Original drawings."
    d.text((right - d.textlength(src, font=font(SANS, 9)), 988),
           src, font=font(SANS, 9), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote", out, page.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
