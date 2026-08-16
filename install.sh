#!/usr/bin/env bash
# themeverse — universal theme installer
#
# Install one theme into every tool it detects on your machine:
#   ./install.sh naruto              # install naruto everywhere possible
#   ./install.sh                     # interactive picker
#   ./install.sh --list              # list all available themes
#   ./install.sh --list-tools        # list what this machine has
#
# Works for: Hermes, Claude Code, OpenCode, VS Code, Zed, iTerm2,
# Windows Terminal, kitty, Neovim, Oh My Posh.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THEMES="$HERE/themes"

# ---------------------------------------------------------------- helpers

say() { printf '\033[1;32m%s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m%s\033[0m\n' "$*" >&2; }
die() { printf '\033[1;31m%s\033[0m\n' "$*" >&2; exit 1; }

has() { command -v "$1" >/dev/null 2>&1; }

themes_list() {
  ls "$THEMES/hermes" 2>/dev/null | sed 's/\.yaml$//' | sort
}

check_slug() {
  [ -f "$THEMES/hermes/$1.yaml" ] || die "Unknown theme '$1'. Run ./install.sh --list"
}

# ---------------------------------------------------------------- installers

install_claude_code() {
  local slug="$1" dest="$HOME/.claude/themes"
  mkdir -p "$dest"
  cp "$THEMES/claude-code/$slug.json" "$dest/"
  say "  Claude Code  -> $dest/$slug.json   (run /theme inside claude)"
}

install_opencode() {
  local slug="$1" dest="$HOME/.config/opencode/themes"
  mkdir -p "$dest"
  cp "$THEMES/opencode/$slug.json" "$dest/"
  say "  OpenCode     -> $dest/$slug.json   (run /theme inside opencode)"
}

install_hermes() {
  local slug="$1" dest="$HOME/.hermes/skins"
  mkdir -p "$dest"
  cp "$THEMES/hermes/$slug.yaml" "$dest/"
  say "  Hermes       -> $dest/$slug.yaml   (run /skin $slug inside hermes)"
}

install_vscode() {
  local slug="$1" title dest
  title="$(python3 -c "import json,sys; print(json.load(open('$THEMES/vscode/$slug.json'))['name'])")"
  dest="$HOME/.vscode/extensions/themeverse-$slug/themes"
  if [ "$(uname -s)" = "Darwin" ]; then dest="$HOME/.vscode/extensions/themeverse-$slug/themes"; fi
  mkdir -p "$dest"
  cat > "$HOME/.vscode/extensions/themeverse-$slug/package.json" <<PKG
{
  "name": "themeverse-$slug",
  "displayName": "$title (themeverse)",
  "version": "1.0.0",
  "engines": { "vscode": "^1.60.0" },
  "categories": ["Themes"],
  "contributes": { "themes": [ { "label": "$title", "uiTheme": "vs-dark", "path": "./themes/$slug.json" } ] }
}
PKG
  cp "$THEMES/vscode/$slug.json" "$dest/"
  say "  VS Code      -> ~/.vscode/extensions/themeverse-$slug   (reload window, pick '$title' in Color Theme)"
}

install_zed() {
  local slug="$1" title dest
  title="$(python3 -c "import json,sys; print(json.load(open('$THEMES/zed/$slug.json'))['name'])")"
  dest="$HOME/.config/zed/themes"
  mkdir -p "$dest"
  cp "$THEMES/zed/$slug.json" "$dest/"
  say "  Zed          -> $dest/$slug.json   (pick '$title' in theme picker)"
}

install_iterm2() {
  local slug="$1" f="$THEMES/iterm2/$slug.itermcolors"
  if has osascript; then
    osascript -e "tell application \"iTerm2\" to open file \"$(cd "$(dirname "$f")" && pwd)/$(basename "$f")\"" >/dev/null 2>&1 \
      && say "  iTerm2       -> imported '$slug' (Preferences > Profiles > Colors > Color Presets)" \
      || warn "  iTerm2       -> open $f manually (double-click to import)"
  else
    warn "  iTerm2       -> open $f manually (double-click to import)"
  fi
}

install_windows_terminal() {
  local slug="$1" settings dest
  settings="${WT_SETTINGS:-$HOME/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json}"
  if [ -f "$settings" ]; then
    python3 - "$slug" "$settings" "$THEMES/windows-terminal/$slug.json" <<'PY'
import json, sys
slug, settings_path, theme_path = sys.argv[1], sys.argv[2], sys.argv[3]
with open(settings_path, encoding="utf-8") as f:
    cfg = json.load(f)
scheme = json.load(open(theme_path, encoding="utf-8"))
names = [s["name"] for s in cfg.setdefault("schemes", [])]
if scheme["name"] not in names:
    cfg["schemes"].append(scheme)
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"  Windows Terminal -> added '{scheme['name']}' to schemes (pick it in Settings > Color scheme)")
else:
    print(f"  Windows Terminal -> '{scheme['name']}' already installed")
PY
  else
    warn "  Windows Terminal -> settings.json not found at $settings"
  fi
}

install_kitty() {
  local slug="$1" dest
  dest="${KITTY_CONFIG_DIRECTORY:-$HOME/.config/kitty}/themes"
  mkdir -p "$dest"
  cp "$THEMES/kitty/$slug.conf" "$dest/"
  say "  kitty        -> $dest/$slug.conf   (add 'include themes/$slug.conf' to kitty.conf)"
}

install_neovim() {
  local slug="$1" dest="$HOME/.config/nvim/colors"
  mkdir -p "$dest"
  cp "$THEMES/neovim/$slug.lua" "$dest/"
  say "  Neovim       -> $dest/$slug.lua    (set 'colorscheme $(echo "$slug" | tr - _ )' in init.lua)"
}

install_omp() {
  local slug="$1" dest
  dest="${POSH_THEMES_PATH:-$HOME/.poshthemes}"
  mkdir -p "$dest"
  cp "$THEMES/oh-my-posh/$slug.omp.json" "$dest/"
  say "  Oh My Posh   -> $dest/$slug.omp.json   (eval \"\$(oh-my-posh init bash --config '$dest/$slug.omp.json')\")"
}

# ---------------------------------------------------------------- main

[ -d "$THEMES" ] || die "themes/ not found — run './generate_hub.py' first (needs python3 + yaml + Pillow)"

if [ "${1:-}" = "--list" ]; then
  echo "Available themes ($(themes_list | wc -l | tr -d ' ')):"
  themes_list | column -c 100 2>/dev/null || themes_list
  exit 0
fi

if [ "${1:-}" = "--list-tools" ]; then
  echo "Detected on this machine:"
  for tool in claude opencode hermes code zed iTerm osascript wt kitty nvim oh-my-posh; do
    case "$tool" in
      claude) has claude && echo "  Claude Code (claude)";;
      opencode) has opencode && echo "  OpenCode";;
      hermes) has hermes && echo "  Hermes";;
      code) has code && echo "  VS Code (code)";;
      zed) has zed && echo "  Zed";;
      iTerm) [ "$(uname -s)" = "Darwin" ] && echo "  iTerm2 (macOS)";;
      osascript) has osascript && echo "  AppleScript (for iTerm2 import)";;
      wt) has wt && echo "  Windows Terminal";;
      kitty) has kitty && echo "  kitty";;
      nvim) has nvim && echo "  Neovim";;
      oh-my-posh) has oh-my-posh && echo "  Oh My Posh";;
    esac
  done
  exit 0
fi

SLUG="${1:-}"
if [ -z "$SLUG" ]; then
  echo "Pick a theme (or run with a name, e.g. ./install.sh naruto):"
  select SLUG in $(themes_list); do
    [ -n "$SLUG" ] && break
  done
fi
check_slug "$SLUG"

say "Installing '$SLUG':"
[ -d "$HOME/.claude/themes" ] || [ -d "$HOME/.claude" ] && install_claude_code "$SLUG"
has opencode && install_opencode "$SLUG"
has hermes && install_hermes "$SLUG"
has code && install_vscode "$SLUG"
has zed && install_zed "$SLUG"
[ "$(uname -s)" = "Darwin" ] && install_iterm2 "$SLUG"
[ -n "${WT_SETTINGS:-}" ] && install_windows_terminal "$SLUG"
has kitty && install_kitty "$SLUG"
has nvim && install_neovim "$SLUG"
has oh-my-posh && install_omp "$SLUG"
say "Done. Restart your tools to see the theme."
