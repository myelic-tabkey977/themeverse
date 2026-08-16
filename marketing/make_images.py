#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate shareable marketing images for the theme pack.

Outputs (into marketing/images/):
  collage.png    6-theme grid with a title bar (for Reddit/X)
  og.png         1200x630 social preview (README/OG tag)
  promo-wide.png 16:9 hero (Discord embed, X)
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")
CN_SHOTS = os.path.join(HERE, "..", "..", "cartoon-network-skins", "screenshots")
AN_SHOTS = os.path.join(HERE, "..", "..", "anime-skins", "screenshots")


def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def pick(slug):
    for base in (CN_SHOTS, AN_SHOTS):
        f = os.path.join(base, slug + ".png")
        if os.path.exists(f):
            return f
    return None


def load_fit(slug, w, h):
    f = pick(slug)
    if not f:
        return None
    im = Image.open(f).convert("RGB")
    return im.resize((w, h), Image.LANCZOS)


def tile_bg(slug, w, h):
    """Fill a region with the theme's background color, sampled from its card."""
    f = pick(slug)
    if not f:
        return (10, 12, 16)
    im = Image.open(f).convert("RGB").resize((1, 1))
    return im.getpixel((0, 0))


def collage():
    slots = [
        ("ben-10", "BEN 10"), ("naruto", "NARUTO"), ("dragon-ball-z", "DRAGON BALL Z"),
        ("batman-the-animated-series", "BATMAN"), ("sailor-moon", "SAILOR MOON"),
        ("one-piece", "ONE PIECE"),
    ]
    cols, rows = 3, 2
    tw, th = 520, 330
    pad = 14
    W = cols * tw + (cols + 1) * pad
    H = 92 + rows * th + (rows + 1) * pad
    im = Image.new("RGB", (W, H), (13, 15, 20))
    d = ImageDraw.Draw(im)
    d.text((pad, 22), "ThemeVerse — 195 cartoon & anime themes for 10 dev tools",
           font=font(34), fill=(255, 255, 255))
    d.text((pad, 62), "Hermes · Claude Code · OpenCode · VS Code · Zed · iTerm2 · Windows Terminal · kitty · Neovim · Oh My Posh",
           font=font(19), fill=(160, 168, 180))
    for i, (slug, label) in enumerate(slots):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = 92 + pad + r * (th + pad)
        shot = load_fit(slug, tw, th)
        if shot:
            im.paste(shot, (x, y))
        d.rectangle([x, y, x + tw, y + th], outline=(40, 45, 55), width=2)
        d.rectangle([x, y, x + tw, y + 34], fill=(20, 24, 30))
        d.text((x + 10, y + 6), label, font=font(20), fill=(255, 255, 255))
    im.save(os.path.join(IMG, "collage.png"))
    print("collage.png", im.size)


def og():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), (10, 12, 16))
    d = ImageDraw.Draw(im)
    # left text column
    d.text((60, 150), "ThemeVerse", font=font(84), fill=(255, 255, 255))
    d.text((62, 260), "195 cartoon & anime themes", font=font(44), fill=(200, 205, 215))
    d.text((62, 320), "for 10 developer tools", font=font(44), fill=(200, 205, 215))
    d.text((62, 420), "github.com/thanvish21/themeverse", font=font(28), fill=(120, 180, 255))
    # right: 2x3 mini grid of screenshot crops
    slots = ["ben-10", "naruto", "dragon-ball-z", "batman-the-animated-series",
             "sailor-moon", "one-piece"]
    x0, y0, cw, ch, g = 660, 60, 250, 240, 12
    for i, slug in enumerate(slots):
        r, c = divmod(i, 3)
        x = x0 + c * (cw + g)
        y = y0 + r * (ch + g)
        shot = load_fit(slug, cw, ch)
        if shot:
            im.paste(shot, (x, y))
        else:
            d.rectangle([x, y, x + cw, y + ch], fill=(25, 30, 40))
    im.save(os.path.join(IMG, "og.png"))
    print("og.png", im.size)


def promo_wide():
    W, H = 1600, 900
    im = Image.new("RGB", (W, H), (13, 15, 20))
    d = ImageDraw.Draw(im)
    d.text((60, 60), "One show. Ten tools.", font=font(66), fill=(255, 255, 255))
    d.text((62, 150), "195 themes · Ben 10 · Naruto · DBZ · Batman · Sailor Moon · Roll No 21…",
           font=font(34), fill=(200, 205, 215))
    d.text((62, 210), "./install.sh naruto → your whole stack matches",
           font=font(28), fill=(140, 200, 150))
    # 5 wide screenshot strips
    slots = ["ben-10", "naruto", "dragon-ball-z", "sailor-moon", "one-piece"]
    n = len(slots)
    sw, sh = 280, 480
    gap = 20
    total = n * sw + (n - 1) * gap
    x0 = (W - total) // 2
    y0 = 320
    for i, slug in enumerate(slots):
        x = x0 + i * (sw + gap)
        shot = load_fit(slug, sw, sh)
        if shot:
            im.paste(shot, (x, y0))
        d.rectangle([x, y0, x + sw, y0 + sh], outline=(45, 52, 64), width=2)
    im.save(os.path.join(IMG, "promo-wide.png"))
    print("promo-wide.png", im.size)


def main():
    os.makedirs(IMG, exist_ok=True)
    collage()
    og()
    promo_wide()
    print("done ->", IMG)


if __name__ == "__main__":
    sys.exit(main())
