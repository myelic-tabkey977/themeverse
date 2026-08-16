#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static preview site: site/themes.json + copy of index.html."""

import json
import os
import shutil

from palettes import PALETTES
from generate_hub import ansi_from, mix, lighten, darken

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

FORMATS = [
    ("hermes", "Hermes", "yaml"),
    ("claude-code", "Claude Code", "json"),
    ("opencode", "OpenCode", "json"),
    ("vscode", "VS Code", "json"),
    ("zed", "Zed", "json"),
    ("iterm2", "iTerm2", "itermcolors"),
    ("windows-terminal", "Windows Terminal", "json"),
    ("kitty", "kitty", "conf"),
    ("neovim", "Neovim", "lua"),
    ("oh-my-posh", "Oh My Posh", "omp.json"),
]

DATA = []
for slug, title, desc, cat, p_, s_, a_, bg_, tx_ in PALETTES:
    a = ansi_from(p_, s_, a_, bg_, tx_)
    DATA.append({
        "slug": slug,
        "title": title,
        "desc": desc,
        "cat": cat,
        "colors": {
            "primary": p_, "secondary": s_, "accent": a_, "background": bg_, "text": tx_,
        },
        "ansi": a,
        "files": {
            f[0]: {"label": f[1], "url": f"themes/{f[0]}/{slug}.{f[2]}"}
            for f in FORMATS
        },
    })

os.makedirs(SITE, exist_ok=True)
with open(os.path.join(SITE, "themes.json"), "w", encoding="utf-8") as fh:
    json.dump(DATA, fh, ensure_ascii=False, indent=1)

# keep docs/ (GitHub Pages source) in sync
DOCS = os.path.join(os.path.dirname(SITE), "docs")
os.makedirs(DOCS, exist_ok=True)
shutil.copy(os.path.join(SITE, "index.html"), os.path.join(DOCS, "index.html"))
shutil.copy(os.path.join(SITE, "themes.json"), os.path.join(DOCS, "themes.json"))

print(f"wrote site/themes.json ({len(DATA)} themes) + docs/ copy")
