# 🌈 ThemeVerse

**195 hand-tuned themes — Cartoon Network classics, Ben 10, Toonami, and anime — for every tool you code in.**

One palette per show, exported to **10 formats**: Hermes, Claude Code, OpenCode, VS Code, Zed, iTerm2, Windows Terminal, kitty, Neovim, and Oh My Posh. Pick `naruto` and your whole stack matches.

**[🎨 Live preview site](https://thanvish21.github.io/themeverse/)** — search, filter, and preview every theme in your browser.

![Themes](https://img.shields.io/badge/themes-195-7873f5) ![Formats](https://img.shields.io/badge/formats-10-4ade80)

---

## Quick start

```bash
git clone https://github.com/thanvish21/themeverse
cd themeverse
./install.sh naruto          # installs into every tool it finds on your machine
./install.sh                 # interactive picker
./install.sh --list          # all 195 themes
```

The installer auto-detects **Hermes, Claude Code, OpenCode, VS Code, Zed, kitty, Neovim, Oh My Posh** (plus iTerm2 on macOS and Windows Terminal via `WT_SETTINGS`) and drops the theme into each one. Restart your tools and pick it from the theme picker.

### Manual install per tool

| Tool | Where it goes | Activate |
|------|--------------|----------|
| **Hermes** | `~/.hermes/skins/naruto.yaml` | `/skin naruto` |
| **Claude Code** | `~/.claude/themes/naruto.json` | `/theme` → *Naruto* |
| **OpenCode** | `~/.config/opencode/themes/naruto.json` | `/theme` → *Naruto* |
| **VS Code** | install as extension (see below) | *Naruto* in Color Theme |
| **Zed** | `~/.config/zed/themes/naruto.json` | theme picker → *Naruto* |
| **iTerm2** | double-click `naruto.itermcolors` | Profiles → Colors → Presets |
| **Windows Terminal** | add scheme to `settings.json` | Settings → Color scheme |
| **kitty** | `~/.config/kitty/themes/naruto.conf` | `include themes/naruto.conf` |
| **Neovim** | `~/.config/nvim/colors/naruto.lua` | `colorscheme naruto` |
| **Oh My Posh** | `~/.poshthemes/naruto.omp.json` | `--config ~/.poshthemes/naruto.omp.json` |

**VS Code as a real extension** (persists across machines, one command):

```bash
./install.sh naruto          # writes ~/.vscode/extensions/themeverse-naruto/
code --list-extensions       # or just reload the window
```

---

## What's inside

### The shows

| Category | Examples |
|----------|----------|
| **Ben 10 Universe** | Ben 10, Alien Force, Ultimate Alien, Omniverse, 2016, Generator Rex |
| **Cartoon Cartoons & Classics** | Powerpuff Girls, Dexter's Lab, Courage, Ed Edd n Eddy, KND, Samurai Jack, Chowder, Total Drama |
| **Modern CN** | Adventure Time, Regular Show, Gumball, Steven Universe, We Bare Bears, Craig of the Creek |
| **DC Super Heroes** | Batman TAS, Batman Beyond, Justice League, Young Justice, Static Shock |
| **Star Wars & LEGO** | Clone Wars, Ninjago, Monkie Kid |
| **Toonami & Action** | Dragon Ball Z, Naruto, One Piece, Cowboy Bebop, AoT, MHA, Sailor Moon |
| **Adult Swim** | Rick & Morty, Robot Chicken, ATHF, Venture Bros |
| **Acquired & International** | Tom & Jerry, Scooby-Doo, Mr. Bean, Transformers Animated |
| **Cartoon Network India** | Roll No 21, Pakdam Pakdai, Gattu Battu, Supa Strikas, Lamput |
| **Anime** | Demon Slayer, Jujutsu Kaisen, Chainsaw Man, Evangelion, Berserk, FMA, HxH, JoJo… |

17 shows exist in both packs (Dragon Ball Z, Naruto, One Piece, …) — the Cartoon Network palette ships as `cn-dragon-ball-z` and the anime palette as `dragon-ball-z`, so both versions are available.

### The formats

Every palette is derived from 5 base colors (primary / secondary / accent / background / text) and expanded to a full theme per format:

- **Hermes** — complete 28-color skin schema (banner, status bar, completion menus, spinner, branding)
- **Claude Code** — official theme JSON (50+ tokens: prompt, plan mode, diffs, subagent colors, ultrathink rainbow)
- **OpenCode** — official `theme.json` schema with dark + light pairs
- **VS Code** — full color theme (~120 color keys + tokenColors grammar scopes)
- **Zed** — theme family with style, syntax, terminal ANSI, and UI surfaces
- **iTerm2** — `.itermcolors` preset with all 16 ANSI colors
- **Windows Terminal** — color scheme with full ANSI palette
- **kitty** — `.conf` with 16-color ANSI + tab/selection/marks
- **Neovim** — Lua colorscheme with 80+ highlight groups (treesitter-ready naming)
- **Oh My Posh** — full prompt config (path, git, runtime segments) in theme colors

---

## Preview site

The GitHub Pages site at [`site/`](site/) is a zero-dependency interactive browser: search 195 themes, filter by category, preview the terminal look, and download any format.

```bash
python3 generate_site.py      # rebuild site/themes.json
```

## Regenerate everything

```bash
python3 palettes.py           # verify the 195-palette database
python3 generate_hub.py       # rebuild themes/* (all 10 formats, validates)
python3 generate_site.py      # rebuild site data
bash install.sh --list        # sanity check
```

Requires `python3` + `pyyaml` + `Pillow` (Pillow is only needed if you also build the source skin packs' screenshots).

## Repos

- [cartoon-network-skins](https://github.com/thanvish21/cartoon-network-skins) — the original 167 CN skins with character art
- [anime-skins](https://github.com/thanvish21/anime-skins) — 28 anime skins with truecolor half-block character heroes

## Contributing

Adding a theme is a 5-minute job — one palette row + one command. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Promotion kit

Ready-to-post drafts (Show HN, Reddit, X, Discord) + shareable images live in [`marketing/`](marketing/) — see [`marketing/MASTER.md`](marketing/MASTER.md).

## License

[MIT](LICENSE). Fan project — all show titles, characters and images belong to their respective owners; only derivative color themes are distributed. Not affiliated with or endorsed by Cartoon Network, any anime studio, or any publisher.
