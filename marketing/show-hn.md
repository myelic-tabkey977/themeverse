# Show HN draft

**Title (pick one — titles are the whole game on HN):**
1. `Show HN: 195 cartoon and anime themes for 10 dev tools (one install.sh)`
2. `Show HN: ThemeVerse — my terminal is now Ben 10, Naruto, and Sailor Moon`
3. `Show HN: I made 195 themes for Hermes, Claude Code, VS Code, Zed, Neovim… from cartoons and anime`

**Body:**

I got tired of my whole dev setup being different colors depending on the tool, so I built a theme pack that covers everything at once.

**195 themes** — Ben 10, Powerpuff Girls, Courage, Samurai Jack, Adventure Time, Dragon Ball Z, Naruto, One Piece, Demon Slayer, JJK, Cowboy Bebop, Evangelion… both Cartoon Network and anime.

**10 formats from one palette:**
- Hermes (full 28-color skin schema)
- Claude Code (official theme JSON — prompts, plan mode, diffs, subagent colors)
- OpenCode (dark + light)
- VS Code (~120 color keys + full token grammar)
- Zed (style + syntax + ANSI)
- iTerm2, Windows Terminal, kitty (16-color ANSI)
- Neovim (80+ highlight groups)
- Oh My Posh (full prompt config)

**The part I think is actually novel:** one `install.sh <theme>` that detects which of those tools you have installed and installs the theme into all of them. `./install.sh naruto` → Claude Code, VS Code, Neovim, kitty and the terminal emulators all flip to Naruto colors.

There's also a zero-dependency preview site where you can search all 195 and preview each one before installing: https://thanvish21.github.io/themeverse/

Every palette is derived from 5 base colors and expanded per format by `generate_hub.py` — adding a show is one line in `palettes.py`, so new themes and new formats are cheap. I'd love contributions: new shows, new tools.

Tech: Python (single generator, no runtime deps for users), shell installer, vanilla JS site.

**Tips for posting:**
- Post between 8–10am ET on a weekday (Mon–Wed best).
- The README + site are the landing page; the first ~10 comments set the tone — answer everything, don't argue.
- If it takes off, the "front page" itself is the distribution; your replies keep it there.
- HN users will poke holes (why 195? are these good colors? why not $TOOL?) — have the honest answers: yes some are template-derived, the star picks (Ben 10, Naruto, Batman, Goku) are hand-tuned, and new formats are easy to add.
