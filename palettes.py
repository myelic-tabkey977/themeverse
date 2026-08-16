# -*- coding: utf-8 -*-
"""Canonical palette database for the theme hub.

Unifies both skin packs (Cartoon Network + Anime) into a single list of
palette records used by every exporter:

  (slug, title, desc, cat, p, s, a, bg, tx)

p/s/a/bg/tx = primary, secondary, accent, background, text hex colors.

17 shows exist in both packs (dragon-ball-z, naruto, one-piece, ...) with
different palettes. The Cartoon Network copy gets a `cn-` slug prefix; the
anime copy keeps the bare slug, matching the anime-skins repo.
"""

from shows_data1 import SHOWS_A
from shows_data2 import SHOWS_B
from anime_data import ANIME

_C = [s for s in (SHOWS_A + SHOWS_B) if len(s) >= 15]
_A = [s for s in ANIME if len(s) >= 17]

_ANIME_SLUGS = {s[0] for s in _A}


def _cn(s):
    slug = s[0]
    if slug in _ANIME_SLUGS:
        slug = "cn-" + slug
    return (slug, s[1], s[2], s[13], s[8], s[9], s[10], s[11], s[12])


def _an(s):
    return (s[0], s[1], s[4], s[3], s[10], s[11], s[12], s[13], s[14])


PALETTES = [_cn(s) for s in _C] + [_an(s) for s in _A]

CATEGORY_ORDER = [
    "Ben 10 Universe", "Cartoon Cartoons & Classics", "Modern Cartoon Network",
    "DC Super Heroes", "Star Wars & LEGO", "Toonami & Action",
    "Adult Swim", "Acquired & International", "Cartoon Network India",
    "Action", "Dark & Gritty", "Sci-Fi & Mecha", "Wholesome & Comedy",
]

if __name__ == "__main__":
    from collections import Counter
    slugs = [p[0] for p in PALETTES]
    dup = {k: v for k, v in Counter(slugs).items() if v > 1}
    assert not dup, f"duplicate slugs: {dup}"
    cats = Counter(p[3] for p in PALETTES)
    print(f"{len(PALETTES)} unique palettes across {len(cats)} categories")
    for c, n in cats.most_common():
        print(f"  {n:4d}  {c}")
