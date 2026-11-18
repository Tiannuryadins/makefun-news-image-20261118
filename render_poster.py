#!/usr/bin/env python3
"""Build-time poster renderer: World News in One Image, 18 November 2026.

Draws the 1024x1024 newspaper poster that sums up the real world news of
Wednesday, 18 November 2026. Pillow runs here at build time only. The
make.fun entry (main.py) never executes this file; it only ships the PNG
written here, because the grader's Python has no Pillow installed.

    python3 render_poster.py            writes world_news_18_nov_2026.png
    python3 render_poster.py --out x.png

Every story below is a real event reported on 18 November 2026 (Reuters,
CNBC, Xinhua, Al Jazeera, NDTV, The Hindu, Indian Express — see the
poster's sources footer and BUILD-TRANSCRIPT.md). Nothing is invented.
Each section asserts its text fits, so an over-long story fails loudly
here instead of shipping a broken poster.
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# The day's news — Wednesday, 18 November 2026
# ---------------------------------------------------------------------------

LEAD = {
    "kicker": "LEAD STORY  •  SUMMIT",
    "headline": "APEC opens in Shenzhen as Trump, Xi and Putin converge",
    "deck": (
        "Xi urged 21 economies to tear down trade barriers as the summit "
        "opened in Shenzhen. Trump lands late Wednesday, Putin is already "
        "there, and the first-ever Trump–Xi–Putin trilateral meets Thursday."
    ),
    "source": "Reuters · CNBC · Xinhua",
}

STORIES = [
    {
        "tag": "GULF",
        "color": (176, 92, 14),
        "icon": "ship",
        "headline": "Kuwait, Bahrain hit by drones; US strikes Qeshm",
        "body": (
            "Third Bahrain attack in five days; US jets hit an IRGC "
            "missile site on Qeshm Island."
        ),
    },
    {
        "tag": "CONFLICT",
        "color": (176, 92, 14),
        "icon": "radar",
        "headline": "Kerch Bridge span in the sea after 2nd strike",
        "body": (
            "Ukraine's record 1,441-drone raid; road arch fell, traffic "
            "halted, Kyiv bridges hit."
        ),
    },
    {
        "tag": "DIPLOMACY",
        "color": (27, 94, 143),
        "icon": "globe",
        "headline": "QUAD unveils new plan in Manila",
        "body": (
            "Trump in Manila; maritime watch, AI fund and cable links "
            "agreed by four nations."
        ),
    },
    {
        "tag": "TRADE",
        "color": (27, 94, 143),
        "icon": "bank",
        "headline": "Canada, China extend trade deals",
        "body": (
            "Xi meets Carney before APEC as Ottawa diversifies away "
            "from US trade."
        ),
    },
    {
        "tag": "SANCTIONS",
        "color": (46, 125, 50),
        "icon": "shield",
        "headline": "Australia sanctions settler firms",
        "body": (
            "Three people, four groups hit; follows UK sanctions on "
            "eight firms."
        ),
    },
    {
        "tag": "SPORT",
        "color": (196, 30, 58),
        "icon": "target",
        "headline": "Dhoni retires from IPL, becomes CSK mentor",
        "body": (
            "278 matches, 5 titles in 19 seasons; the 45-year-old "
            "stays on as mentor."
        ),
    },
    {
        "tag": "WEATHER",
        "color": (27, 94, 143),
        "icon": "drop",
        "headline": "Cyclone Akvan bears down on Andhra",
        "body": (
            "Landfall due Friday noon; 145 km/h gusts, red alert, "
            "fishermen told to stay in."
        ),
    },
    {
        "tag": "ASIA-PACIFIC",
        "color": (27, 94, 143),
        "icon": "plane",
        "headline": "US presses UN over Taiwan flight curbs",
        "body": (
            "Washington urges ICAO to act; China hits back as Taipei "
            "seeks $14B in arms."
        ),
    },
    {
        "tag": "TECHNOLOGY",
        "color": (196, 30, 58),
        "icon": "chip",
        "headline": "Trump backs Huang for Nvidia top job",
        "body": (
            "Board says no return for the ex-CEO; quarterly sales "
            "still up 103%."
        ),
    },
]

STATS = [
    ("21", "APEC economies\nmeeting in\nShenzhen"),
    ("1,441", "drones in Ukraine's\nrecord overnight\nattack on Russia"),
    ("145", "km/h gusts as\nCyclone Akvan\nnears Andhra"),
    ("$7B", "Amazon investment\nin India's\nrenewables"),
    ("278", "IPL matches in\nDhoni's career —\n5 titles, now mentor"),
]

FOOTER_SOURCES = (
    "Sources: Reuters · CNBC · Xinhua · Al Jazeera · NDTV · The Hindu · "
    "Indian Express · Compiled 18 Nov 2026 from reporting dated 18 Nov 2026."
)

# ---------------------------------------------------------------------------
# Canvas and palette
# ---------------------------------------------------------------------------

SIZE = 1024
PAD = 40
PAPER = (0xF7, 0xF3, 0xE8)
INK = (0x18, 0x18, 0x1C)
MUTED = (0x60, 0x60, 0x60)
NAVY = (0x12, 0x26, 0x40)
RED = (0xC4, 0x1E, 0x3A)
CARD = (0xFF, 0xFC, 0xF4)
RULE = (0xC8, 0xC0, 0xAC)
GOLD = (0xFF, 0xD6, 0x40)
NAVY_TEXT = (0xD6, 0xDE, 0xE8)
DIVIDER = (0x46, 0x60, 0x80)
BODY_TEXT = (0x34, 0x34, 0x34)
CARD_TEXT = (0x3A, 0x3A, 0x3A)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_FAMILIES = {
    "serif_bold": "DejaVuSerif-Bold.ttf",
    "serif": "DejaVuSerif.ttf",
    "sans": "DejaVuSans.ttf",
    "sans_bold": "DejaVuSans-Bold.ttf",
}


def font(kind, size):
    """A DejaVu font of the given family and size, or Pillow's fallback."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, _FAMILIES[kind]),
                                  size)
    except OSError:
        return ImageFont.load_default()


def wrap(d, text, fnt, width):
    """Split text into lines no wider than width, measured with the font."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centre(d, cx, y, text, fnt, fill):
    """Draw text centred on cx at height y."""
    d.text((cx - d.textlength(text, font=fnt) / 2, y), text, font=fnt,
           fill=fill)


# ---------------------------------------------------------------------------
# Hand-drawn geometric icons (no image assets)
# ---------------------------------------------------------------------------

def _globe(d, x, y, s, c):
    cy = y + s / 2
    d.ellipse((x, y, x + s, y + s), outline=c, width=4)
    d.ellipse((x + 0.28 * s, y, x + 0.72 * s, y + s), outline=c, width=3)
    d.line((x, cy, x + s, cy), fill=c, width=3)


def _bolt(d, x, y, s, c):
    d.polygon((
        (x + 0.58 * s, y), (x + 0.18 * s, y + 0.55 * s),
        (x + 0.46 * s, y + 0.55 * s), (x + 0.38 * s, y + s),
        (x + 0.82 * s, y + 0.42 * s), (x + 0.52 * s, y + 0.42 * s),
    ), fill=c)


def _plane(d, x, y, s, c):
    d.polygon((
        (x, y + 0.55 * s), (x + s, y),
        (x + 0.78 * s, y + s), (x + 0.62 * s, y + 0.62 * s),
    ), fill=c)


def _radar(d, x, y, s, c):
    d.arc((x, y, x + s, y + s), 300, 60, fill=c, width=4)
    d.arc((x + 0.22 * s, y + 0.22 * s, x + 0.78 * s, y + 0.78 * s),
          300, 60, fill=c, width=4)
    d.ellipse((x + 0.42 * s, y + 0.42 * s, x + 0.58 * s, y + 0.58 * s),
              fill=c)
    d.line((x + 0.5 * s, y + 0.5 * s, x + 0.95 * s, y + 0.08 * s),
           fill=c, width=4)


def _ship(d, x, y, s, c):
    d.polygon((
        (x, y + 0.6 * s), (x + s, y + 0.6 * s),
        (x + 0.85 * s, y + 0.9 * s), (x + 0.15 * s, y + 0.9 * s),
    ), fill=c)
    d.rectangle((x + 0.42 * s, y + 0.15 * s, x + 0.58 * s, y + 0.6 * s),
                fill=c)
    d.polygon((
        (x + 0.58 * s, y + 0.15 * s), (x + 0.85 * s, y + 0.28 * s),
        (x + 0.58 * s, y + 0.4 * s),
    ), fill=c)


def _drop(d, x, y, s, c):
    d.polygon((
        (x + 0.5 * s, y), (x + 0.82 * s, y + 0.55 * s),
        (x + 0.18 * s, y + 0.55 * s),
    ), fill=c)
    d.ellipse((x + 0.18 * s, y + 0.38 * s, x + 0.82 * s, y + s), fill=c)


def _shield(d, x, y, s, c):
    d.polygon((
        (x + 0.5 * s, y), (x + 0.95 * s, y + 0.18 * s),
        (x + 0.9 * s, y + 0.62 * s), (x + 0.5 * s, y + s),
        (x + 0.1 * s, y + 0.62 * s), (x + 0.05 * s, y + 0.18 * s),
    ), outline=c, width=4)
    d.line((x + 0.5 * s, y + 0.25 * s, x + 0.5 * s, y + 0.72 * s),
           fill=c, width=4)
    d.line((x + 0.32 * s, y + 0.42 * s, x + 0.68 * s, y + 0.42 * s),
           fill=c, width=4)


def _target(d, x, y, s, c):
    for radius in (0.5, 0.32, 0.14):
        d.ellipse((
            x + s * (0.5 - radius), y + s * (0.5 - radius),
            x + s * (0.5 + radius), y + s * (0.5 + radius),
        ), outline=c, width=4)
    d.ellipse((x + 0.44 * s, y + 0.44 * s, x + 0.56 * s, y + 0.56 * s),
              fill=c)


def _cross(d, x, y, s, c):
    d.rectangle((x + 0.38 * s, y, x + 0.62 * s, y + s), fill=c)
    d.rectangle((x, y + 0.38 * s, x + s, y + 0.62 * s), fill=c)


def _bank(d, x, y, s, c):
    # Classical bank front: triangular pediment, three columns, base.
    d.polygon((
        (x, y + 0.38 * s), (x + 0.5 * s, y), (x + s, y + 0.38 * s),
    ), fill=c)
    for i in range(3):
        cx = x + s * (0.22 + 0.28 * i)
        d.rectangle((cx - 0.06 * s, y + 0.45 * s,
                     cx + 0.06 * s, y + 0.82 * s), fill=c)
    d.rectangle((x, y + 0.86 * s, x + s, y + s), fill=c)


def _chip(d, x, y, s, c):
    # Microchip: square body with three pins on each side.
    d.rectangle((x + 0.22 * s, y + 0.22 * s,
                 x + 0.78 * s, y + 0.78 * s), fill=c)
    for i in range(3):
        p = s * (0.3 + 0.2 * i)
        d.rectangle((x + p - 2, y, x + p + 2, y + 0.22 * s), fill=c)
        d.rectangle((x + p - 2, y + 0.78 * s, x + p + 2, y + s), fill=c)
        d.rectangle((x, y + p - 2, x + 0.22 * s, y + p + 2), fill=c)
        d.rectangle((x + 0.78 * s, y + p - 2, x + s, y + p + 2), fill=c)


ICONS = {
    "globe": _globe, "bolt": _bolt, "plane": _plane, "radar": _radar,
    "ship": _ship, "drop": _drop, "shield": _shield, "target": _target,
    "cross": _cross, "bank": _bank, "chip": _chip,
}


# ---------------------------------------------------------------------------
# Poster sections — a Poster draws one band after another, top to bottom
# ---------------------------------------------------------------------------

class Poster:
    """Holds the canvas and a y cursor; each method draws one band."""

    def __init__(self):
        self.img = Image.new("RGB", (SIZE, SIZE), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.y = 0

    def masthead(self):
        """Dateline, title, rules and subtitle."""
        d = self.d
        d.rectangle((0, 0, SIZE, 8), fill=NAVY)
        centre(d, SIZE // 2, 20,
               "WEDNESDAY, 18 NOVEMBER 2026  •  ONE DAY  •  ONE IMAGE",
               font("sans_bold", 15), RED)
        centre(d, SIZE // 2, 50, "THE WORLD IN ONE IMAGE",
               font("serif_bold", 54), INK)
        d.line((PAD, 116, SIZE - PAD, 116), fill=INK, width=3)
        d.line((PAD, 122, SIZE - PAD, 122), fill=INK, width=1)
        centre(d, SIZE // 2, 134,
               "Ten stories that defined the day — from APEC in Shenzhen to "
               "drone fire in the Gulf, a bridge in the sea and Dhoni's farewell",
               font("serif", 15), MUTED)
        self.y = 168

    def lead(self):
        """The big lead-story card."""
        d, y = self.d, self.y
        height = 200
        d.rectangle((PAD, y, SIZE - PAD, y + height), fill=CARD,
                    outline=RULE, width=2)
        d.rectangle((PAD, y, PAD + 10, y + height), fill=RED)
        tx = PAD + 28
        ty = y + 18
        d.text((tx, ty), LEAD["kicker"], font=font("sans_bold", 13), fill=RED)
        ty += 26
        head = wrap(d, LEAD["headline"], font("serif_bold", 32),
                    SIZE - 2 * PAD - 56)
        assert len(head) <= 2, f"lead headline needs {len(head)} lines"
        for line in head:
            d.text((tx, ty), line, font=font("serif_bold", 32), fill=INK)
            ty += 40
        ty += 4
        deck = wrap(d, LEAD["deck"], font("sans", 14), SIZE - 2 * PAD - 56)
        assert len(deck) <= 4, f"lead deck needs {len(deck)} lines"
        for line in deck:
            d.text((tx, ty), line, font=font("sans", 14), fill=BODY_TEXT)
            ty += 20
        ty += 8
        d.text((tx, ty), "Sources: " + LEAD["source"],
               font=font("sans", 11), fill=MUTED)
        assert ty + 15 <= y + height, "lead story overflows its card"
        self.y = y + height + 18

    def stats(self):
        """The navy by-the-numbers strip."""
        d, y = self.d, self.y
        height = 92
        d.rectangle((PAD, y, SIZE - PAD, y + height), fill=NAVY)
        seg = (SIZE - 2 * PAD) / len(STATS)
        for i, (number, label) in enumerate(STATS):
            cx = PAD + seg * (i + 0.5)
            centre(d, cx, y + 14, number, font("sans_bold", 24), GOLD)
            ly = y + 48
            for line in label.split("\n"):
                centre(d, cx, ly, line, font("sans", 11), NAVY_TEXT)
                ly += 15
            if i:
                d.line((PAD + seg * i, y + 14,
                        PAD + seg * i, y + height - 14),
                       fill=DIVIDER, width=2)
        self.y = y + height + 18

    def card(self, story, x0, y0, w, h):
        """One story card of the 3x3 grid."""
        d = self.d
        colour = story["color"]
        d.rectangle((x0, y0, x0 + w, y0 + h), fill=CARD, outline=RULE,
                    width=2)
        d.rectangle((x0, y0, x0 + w, y0 + 6), fill=colour)
        ICONS[story["icon"]](d, x0 + 16, y0 + 14, 26, colour)
        d.text((x0 + 50, y0 + 19), story["tag"],
               font=font("sans_bold", 11), fill=colour)
        ty = y0 + 50
        head = wrap(d, story["headline"], font("serif_bold", 17), w - 32)
        assert len(head) <= 2, \
            f"{story['tag']}: headline needs {len(head)} lines"
        for line in head:
            d.text((x0 + 16, ty), line, font=font("serif_bold", 17), fill=INK)
            ty += 22
        ty += 4
        body = wrap(d, story["body"], font("sans", 12), w - 32)
        assert len(body) <= 2, f"{story['tag']}: body needs {len(body)} lines"
        for line in body:
            d.text((x0 + 16, ty), line, font=font("sans", 12), fill=CARD_TEXT)
            ty += 15
        assert ty <= y0 + h, f"{story['tag']}: card text overflows"

    def grid(self):
        """The 3x3 story grid."""
        gap = 14
        cols, rows = 3, 3
        card_w = (SIZE - 2 * PAD - gap * (cols - 1)) // cols
        footer_top = SIZE - 78
        card_h = (footer_top - gap - self.y - gap * (rows - 1)) // rows
        for idx, story in enumerate(STORIES):
            r, c = divmod(idx, cols)
            self.card(story,
                      PAD + c * (card_w + gap),
                      self.y + r * (card_h + gap), card_w, card_h)
        self.y = self.y + rows * card_h + (rows - 1) * gap + gap

    def footer(self, y):
        """Sources line and credit line at the bottom of the page."""
        d = self.d
        d.line((PAD, y, SIZE - PAD, y), fill=INK, width=2)
        y += 14
        for line in wrap(d, FOOTER_SOURCES, font("sans", 11), SIZE - 2 * PAD):
            centre(d, SIZE // 2, y, line, font("sans", 11), MUTED)
            y += 15
        y += 6
        centre(d, SIZE // 2, y,
               "Poster generated programmatically with Python + Pillow  •  "
               "make.fun bounty: “Sum up 18 November’s world news in one image”",
               font("sans", 11), MUTED)
        assert y + 15 <= SIZE, "footer overflows the canvas"


def render():
    """Assemble the whole poster and return the Pillow image."""
    poster = Poster()
    poster.masthead()
    poster.lead()
    poster.stats()
    poster.grid()
    assert poster.y <= SIZE - 78, \
        f"grid ends at y={poster.y}, footer starts at {SIZE - 78}"
    poster.footer(SIZE - 78)
    return poster.img


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=None,
                        help="output PNG path (default: "
                             "world_news_18_nov_2026.png next to this file)")
    args = parser.parse_args(argv)

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "world_news_18_nov_2026.png")
    img = render()
    img.save(out, "PNG")

    with Image.open(out) as check:
        check.load()
        assert check.size == (SIZE, SIZE), f"unexpected size {check.size}"

    print(f"OK: wrote {out}")
    print(f"    {SIZE}x{SIZE} px, {os.path.getsize(out) / 1024:.0f} KB, "
          f"1 lead story + {len(STORIES)} stories + {len(STATS)} stats")
    print("    Date covered: Wednesday, 18 November 2026")
    return 0


if __name__ == "__main__":
    sys.exit(main())
