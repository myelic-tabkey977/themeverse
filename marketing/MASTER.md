# 📣 ThemeVerse Marketing Master Plan

The plan for getting stars, users, and contributors. You (the repo owner) post everything — this kit makes each post a copy-paste job. Never spam, always add value first.

---

## 1. Positioning (the one-line pitch)

> **195 cartoon & anime themes for 10 dev tools — one `install.sh`, your whole stack matches.**

Alternates by audience:
- Developers: *"Every theme pack you've seen only covers one tool. This one covers ten — Hermes, Claude Code, OpenCode, VS Code, Zed, iTerm2, Windows Terminal, kitty, Neovim, Oh My Posh."*
- Anime fans: *"Your terminal, but it's Naruto. Or Goku. Or Sailor Moon."*
- r/unixporn: *"A theme pack where the terminal actually looks like the show."*

**Why this angle wins:** theme packs are inherently visual and shareable. The multi-tool angle is the differentiator nobody else has.

---

## 2. Target audiences & where they hang out

| Audience | Where | Hook |
|----------|-------|------|
| AI coding tool users | r/ClaudeAI, Claude Code Discord, OpenCode Discord, Hermes Discord | "Claude Code in Ben 10 green" |
| Neovim/terminal people | r/neovim, r/commandline, r/unixporn, kitty/zsh discords | 10 formats incl. Neovim + kitty |
| Anime fans | r/anime, r/animesuggest, anime discords | Naruto/Goku/Sailor Moon terminals |
| CN nostalgia | r/CartoonNetwork, r/90scartoons | Roll No 21, Powerpuff, Dexter's Lab |
| Trading crowd | r/algotrading, r/forex | separate gold-dominator play (see §6) |

---

## 3. The launch sequence (first 2 weeks)

| Day | Action | Where | Status |
|-----|--------|-------|--------|
| 0 | Create repo → live preview site | github.com | ✅ done |
| 0 | Set repo description + topics (see §4) | GitHub | ⬜ do first |
| 1 | **Show HN post** (draft in `show-hn.md`) | news.ycombinator.com | ⬜ |
| 1 | Tweet thread with 3–4 screenshots (draft in `twitter.md`) | X | ⬜ |
| 2 | Post to r/ClaudeAI (draft in `reddit.md`) | reddit.com/r/ClaudeAI | ⬜ |
| 2 | Post to r/unixporn (MUST include screenshots, tag `[OC]`) | reddit.com/r/unixporn | ⬜ |
| 3 | Post to r/anime (community-appropriate angle) | reddit.com/r/anime | ⬜ |
| 3–4 | Post to Hermes / Claude Code / OpenCode / Zed Discords (ask-first) | Discord | ⬜ |
| 5 | r/CartoonNetwork nostalgia post | reddit.com/r/CartoonNetwork | ⬜ |
| 7 | Follow-up: "added 30 more anime themes" (if expanded) | same channels | ⬜ |
| 10 | r/neovim + r/commandline | reddit | ⬜ |
| 14 | Review, iterate on what worked | — | ⬜ |

**Golden rule:** post where you have *some* presence or lurk first. A brand-new account posting promo gets flagged. Comment on other posts in each community for a few days before dropping yours.

---

## 4. GitHub metadata (do this first — it's free discovery)

```bash
gh repo edit thanvish21/themeverse \
  --description "195 cartoon & anime themes (Ben 10, Naruto, DBZ…) for 10 tools — Hermes, Claude Code, OpenCode, VS Code, Zed, iTerm2, Windows Terminal, kitty, Neovim, Oh My Posh" \
  --add-topic themes --add-topic color-schemes --add-topic claude-code \
  --add-topic neovim --add-topic vscode-theme --add-topic hermes \
  --add-topic anime --add-topic cartoon-network --add-topic oh-my-posh \
  --add-topic zed-editor --add-topic kitty --add-topic iterm2 \
  --add-topic windows-terminal --add-topic terminal-themes
```

Also do the same for `anime-skins` and `cartoon-network-skins` (each with its own description + topics). GitHub search + "explore" surfaces topic-tagged repos.

---

## 5. Repo-level improvements that help conversion (worth doing before posting)

1. **OG image** — the preview site has no social preview. Add `docs/og.png` (1200×630) so links on X/Reddit/Discord show a real image. Generate from screenshots.
2. **Star-able hook in README** — already has one (`./install.sh naruto`). Add a GIF of the install running.
3. **Pin the repos** — GitHub profile pins: themeverse, anime-skins, cartoon-network-skins.
4. **Contributing.md + good-first-issue labels** — "add a theme for X" is the easiest contributor on-ramp (see §7).

---

## 6. Secondary plays (don't skip — separate audiences)

### gold-dominator (trading)
- **Hook:** "Open-source Gold Dominator Pro (XAU/USD) + crypto arbitrage bot".
- **Where:** r/algotrading, r/forex, r/quant; X trading community.
- **CAREFUL:** financial software = huge scrutiny. Only share backtested results with full methodology + disclaimer. Never promise returns.
- Draft in `gold-dominator.md`.

### claude-config
- **Hook:** "My Claude Code setup — skills, agents, workflows, MCP config, open-sourced".
- **Where:** r/ClaudeAI, X, Claude Code Discord (the #configs channel loves this).
- This one is a *credibility* play: the more visible it is, the more trust your other repos get.
- Draft in `claude-config.md`.

### Portfolio / other repos
- The portfolio + backend repos (`azure-mlops-fraud`, `rag-grounding-eval`, etc.) belong on **LinkedIn + resume**, not Reddit. Mention the flagship repo in your profile README.

---

## 7. Contributors (the "no contributors" problem)

Stars come from users; contributors come from users who care. Sequence:
1. Add `CONTRIBUTING.md` (template in this repo's root) — "Adding a theme takes 5 minutes: copy a palette row into `palettes.py`, run `generate_hub.py`".
2. Add `good first issue` labels: "Add theme: [anime show]", "New format: [tool]".
3. Put a "Contributing" section in the README with the 5-minute recipe.
4. When someone opens a real PR, thank them publicly (mention in release notes / README contributors section). A contributor graph with 1–2 names attracts more.

---

## 8. Metrics to watch & iterate

- **Week 1:** stars (aim 30–100), traffic on preview site (check GitHub Insights)
- **Week 2:** which post drove the most — double down on that channel
- **Month 1:** first PR — celebrate it publicly
- **Honest targets:** 100–500 stars in month 1 is a *great* result for a theme pack; 1k+ is possible via Show HN + r/unixporn front page but rare. The goal is momentum, not a number.

**What NOT to do:** buy stars/forks, bot engagement, post the same link to 20 subs in one day (shadowban bait), make fake "rate my repo" accounts. One bad look kills the whole thing.
