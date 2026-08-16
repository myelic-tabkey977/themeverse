# Contributing

Thanks for wanting to add to ThemeVerse! There are two easy ways in:

## Add a theme (5 minutes)

1. Add one row to `palettes.py` — a show is just 5 colors:

```python
("one-punch-man", "One Punch Man",
 "The hero who ends every fight with one punch.",
 "Action",
 "#DC2626",   # primary (borders, strong accents)
 "#FACC15",   # secondary (keywords, labels)
 "#FDE047",   # accent (highlights, active states)
 "#0F0505",   # background
 "#F7E9E9",   # text
),
```

2. Run the generator:

```bash
python3 generate_hub.py     # writes + validates all 10 formats
python3 generate_site.py    # updates the preview site data
```

3. Commit and open a PR. That's it — the theme now works in all 10 tools.

**Tips:**
- Pick colors that *feel* like the show (see the existing entries for reference).
- The `cn-` prefix is used when a show already exists from the other pack (e.g. `cn-dragon-ball-z`).
- Check `themes/` after running to make sure your slug appears in every format.

## Add a format (new tool)

1. Add an `export_<tool>(palette, outdir)` function in `generate_hub.py` (the others are good templates).
2. Register it in the `EXPORTERS` list at the bottom.
3. Add the tool to `install.sh` (a `install_<tool>()` function + a detection line in the main body).
4. Add a row to the README format table and the preview-site `FORMATS` list in `generate_site.py`.
5. Run `generate_hub.py` and `generate_site.py`, verify, PR.

## Report a bad color

Open an issue with the theme slug and what looks wrong. We try to keep every palette readable (the `--check` in `generate_hub.py` validates structure; luminance sanity is a manual review).

## Code of conduct

Be nice, keep it on-topic, and don't claim the fan art as your own. All shows/characters belong to their owners.
