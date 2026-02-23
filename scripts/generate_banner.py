"""
Generate the ibge-geodata site banner aligned with the GitHub-style theme.

Colors:
  #24292f  — header/dark text
  #0969da  — GitHub blue (accent)
  #f6f8fa  — code background (light gray)
  #d0d7de  — border gray
  #57606a  — secondary text
  #ffffff  — white
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
W, H = 1536, 640
BG_TOP = (246, 248, 250)  # #f6f8fa
BG_BOTTOM = (255, 255, 255)  # #ffffff
DARK = (36, 41, 47)  # #24292f
BLUE = (9, 105, 218)  # #0969da
BLUE_LIGHT = (84, 174, 255)  # lighter accent
BORDER = (208, 215, 222)  # #d0d7de
SECONDARY = (87, 96, 106)  # #57606a
WHITE = (255, 255, 255)

FONT_BOLD = "/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

OUT = Path(__file__).parent.parent / "docs/wiki/assets/banner/readme_banner.png"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def vertical_gradient(
    draw: ImageDraw.ImageDraw, w: int, h: int, top: tuple, bottom: tuple
) -> None:
    for y in range(h):
        t = y / (h - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def dot_grid(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    gap: int = 28,
    r: int = 2,
) -> None:
    """Draw a subtle dot grid in the right portion of the banner."""
    for gx in range(x0, x1, gap):
        for gy in range(y0, y1, gap):
            alpha = 80
            draw.ellipse(
                [(gx - r, gy - r), (gx + r, gy + r)],
                fill=(*BORDER, alpha),
            )


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    xy: tuple,
    radius: int,
    fill: tuple,
    outline: tuple | None = None,
    outline_width: int = 1,
) -> None:
    draw.rounded_rectangle(
        xy, radius=radius, fill=fill, outline=outline, width=outline_width
    )


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------------------
# Draw badge  (e.g.  "pip install ibge-geodata")
# ---------------------------------------------------------------------------
def draw_badge(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    value: str,
    font_sm: ImageFont.FreeTypeFont,
) -> int:
    PAD = 10
    GAP = 4
    lw = draw.textlength(label, font=font_sm)
    vw = draw.textlength(value, font=font_sm)
    lbox = (x, y, x + lw + PAD * 2, y + 28)
    vbox = (lbox[2], y, lbox[2] + vw + PAD * 2, y + 28)
    rounded_rect(draw, lbox, 5, DARK)
    rounded_rect(draw, vbox, 5, BLUE)
    draw.text((x + PAD, y + 5), label, font=font_sm, fill=WHITE)
    draw.text((lbox[2] + PAD, y + 5), value, font=font_sm, fill=WHITE)
    return vbox[2]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    # --- gradient background ------------------------------------------------
    vertical_gradient(draw, W, H, BG_TOP, BG_BOTTOM)

    # --- subtle dot grid (right side) ---------------------------------------
    dot_grid(draw, W // 2, 0, W + 40, H, gap=30, r=2)

    # --- left accent bar  ---------------------------------------------------
    draw.rectangle([(0, 0), (6, H)], fill=BLUE)

    # --- top border line  ---------------------------------------------------
    draw.line([(0, 0), (W, 0)], fill=BORDER, width=1)
    draw.line([(0, H - 1), (W, H - 1)], fill=BORDER, width=1)

    # --- fonts  -------------------------------------------------------------
    try:
        font_title = load_font(FONT_BOLD, 88)
        font_sub = load_font(FONT_BOLD, 32)
        font_tag = load_font(FONT_REGULAR, 26)
        font_badge = load_font(FONT_MONO, 18)
    except OSError as exc:
        raise SystemExit(f"Font not found: {exc}") from exc

    # --- package name -------------------------------------------------------
    title = "ibge-geodata"
    MARGIN_L = 72

    # shadow
    draw.text((MARGIN_L + 2, 122), title, font=font_title, fill=(*BORDER, 180))
    # main text: "ibge-" in dark, "geodata" in blue
    dash_pos = title.index("-") + 1
    part1 = title[:dash_pos]  # "ibge-"
    part2 = title[dash_pos:]  # "geodata"
    w1 = draw.textlength(part1, font=font_title)
    draw.text((MARGIN_L, 120), part1, font=font_title, fill=DARK)
    draw.text((MARGIN_L + w1, 120), part2, font=font_title, fill=BLUE)

    # --- subtitle  ----------------------------------------------------------
    sub = "Brazilian IBGE Territorial Geospatial Data"
    draw.text((MARGIN_L, 228), sub, font=font_sub, fill=SECONDARY)

    # --- divider  -----------------------------------------------------------
    draw.line([(MARGIN_L, 285), (MARGIN_L + 580, 285)], fill=BORDER, width=1)

    # --- feature tags  ------------------------------------------------------
    tags = [
        "GeoDataFrame",
        "GeoLocator",
        "GeoCoords",
        "6 levels",
        "WGS-84 ↔ UTM",
    ]
    tx = MARGIN_L
    ty = 308
    for tag in tags:
        tw = draw.textlength(tag, font=font_tag)
        box = (tx - 10, ty - 6, tx + tw + 10, ty + 32)
        rounded_rect(draw, box, 6, fill=(*DARK, 8), outline=BORDER, outline_width=1)
        draw.text((tx, ty), tag, font=font_tag, fill=SECONDARY)
        tx += int(tw) + 28

    # --- pip install badge  -------------------------------------------------
    draw_badge(draw, MARGIN_L, 390, "pip install", "ibge-geodata", font_badge)

    # --- python badge  ------------------------------------------------------
    tx2 = MARGIN_L
    py_label = "python"
    py_value = "3.11+"
    pw = int(draw.textlength(py_label, font=font_badge)) + 20
    vw = int(draw.textlength(py_value, font=font_badge)) + 20
    badge_y = 428
    rounded_rect(draw, (tx2, badge_y, tx2 + pw, badge_y + 28), 5, DARK)
    rounded_rect(
        draw, (tx2 + pw, badge_y, tx2 + pw + vw, badge_y + 28), 5, (31, 136, 61)
    )  # green
    draw.text((tx2 + 10, badge_y + 5), py_label, font=font_badge, fill=WHITE)
    draw.text((tx2 + pw + 10, badge_y + 5), py_value, font=font_badge, fill=WHITE)

    # --- decorative hexagon grid (right area) --------------------------------
    # light hex outlines
    def hex_points(cx: int, cy: int, size: int):
        return [
            (
                cx + size * math.cos(math.radians(60 * i - 30)),
                cy + size * math.sin(math.radians(60 * i - 30)),
            )
            for i in range(6)
        ]

    hex_draw = ImageDraw.Draw(img, "RGBA")
    cols, rows = 7, 5
    hex_size = 68
    hx_off = int(hex_size * math.sqrt(3))
    hy_off = int(hex_size * 1.5)
    sx = W - (cols * hx_off) - 40
    sy = H // 2 - (rows * hy_off) // 2 - 30

    hex_labels = {
        (1, 1): "STATE",
        (3, 0): "REGION",
        (2, 2): "MUNI",
        (4, 2): "IBGE",
        (0, 3): "GEO",
        (5, 1): "UTM",
    }

    for col in range(cols):
        for row in range(rows):
            cx = sx + col * hx_off + (hx_off // 2 if row % 2 else 0)
            cy = sy + row * hy_off
            pts = hex_points(cx, cy, hex_size - 4)

            key = (col, row)
            if key in hex_labels:
                hex_draw.polygon(pts, fill=(*BLUE, 18), outline=(*BLUE, 60))
                lbl = hex_labels[key]
                fw = draw.textlength(lbl, font=font_badge)
                draw.text(
                    (cx - fw / 2, cy - 9), lbl, font=font_badge, fill=(*BLUE, 160)
                )
            else:
                hex_draw.polygon(pts, fill=(*DARK, 5), outline=(*BORDER, 80))

    # --- save  --------------------------------------------------------------
    OUT.parent.mkdir(parents=True, exist_ok=True)
    final = Image.new("RGB", (W, H), WHITE)
    final.paste(img, mask=img.split()[3])
    final.save(OUT, "PNG", optimize=True)
    print(f"Banner saved → {OUT}  ({W}×{H})")


if __name__ == "__main__":
    main()
