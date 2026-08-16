#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export every palette to every supported theme format.

Formats (all under themes/<format>/<slug>.<ext>):
  hermes/            Hermes agent skins (YAML, full 28-color schema)
  claude-code/       Claude Code themes (JSON)
  opencode/          OpenCode themes (JSON)
  vscode/            VS Code color themes (JSON)
  zed/               Zed theme families (JSON)
  iterm2/            iTerm2 color presets (itermcolors plist)
  windows-terminal/  Windows Terminal schemes (JSON)
  kitty/             kitty terminal themes (conf)
  neovim/            Neovim Lua color schemes
  oh-my-posh/        Oh My Posh prompt themes (JSON)

Usage:
  python3 generate_hub.py
"""

import json
import os
import re
import sys

import yaml

from palettes import PALETTES
from generate_skins import (  # color helpers + skin builder (CN repo)
    COLOR_KEYS, DEFAULT_TOOL_EMOJIS, LiteralStr, build_skin, derive_colors,
    dump_yaml, hex_to_rgb, rgb_to_hex, mix, lighten, darken, luminance,
    render_logo, validate_skin,
)
from generate_themes import claude_theme, opencode_theme

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "themes")

OK = "#4CAF50"
ERR = "#EF5350"
WARN = "#FFA726"


# ---------------------------------------------------------------- helpers

def dk(h, t):
    """darken for light variants"""
    return darken(h, t)


def ensure_light(h, min_lum=0.55):
    cur = h
    for _ in range(12):
        if luminance(cur) >= min_lum:
            break
        cur = lighten(cur, 0.12)
    return cur


def ansi_from(p, s, a, bg, tx):
    """Derive a 16-color ANSI palette from the 5 base colors."""
    muted = mix(bg, tx, 0.4)
    return {
        "black": darken(bg, 0.5),
        "red": ERR,
        "green": "#4CAF50",
        "yellow": WARN,
        "blue": s,
        "magenta": "#BA68C8",
        "cyan": "#4DD0E1",
        "white": lighten(tx, 0.05),
        "brightBlack": muted,
        "brightRed": lighten(ERR, 0.15),
        "brightGreen": lighten(OK, 0.15),
        "brightYellow": lighten(WARN, 0.15),
        "brightBlue": lighten(s, 0.25),
        "brightMagenta": lighten("#BA68C8", 0.2),
        "brightCyan": lighten("#4DD0E1", 0.2),
        "brightWhite": tx,
    }


# ---------------------------------------------------------------- Hermes

def export_hermes(p, outdir):
    (slug, title, desc, cat, p_, s_, a_, bg_, tx_) = p
    sym = "◆"
    show = (slug, title, desc, title + " Agent", "Welcome! Type your message or /help.",
            "Goodbye!", sym, ["working", "thinking", "processing", "rendering"],
            p_, s_, a_, bg_, tx_, cat, title)
    colors = derive_colors(show)
    muted = mix(bg_, tx_, 0.35)
    skin = {
        "name": slug,
        "description": desc,
        "colors": colors,
        "spinner": {
            "waiting_faces": [f"({sym})", "(◉)", "(◎)", "(◯)", "(●)"],
            "thinking_faces": [f"({sym})", "(◉)", "(⌁)", "(<>)"],
            "thinking_verbs": ["working", "thinking", "processing", "rendering", "almost there"],
            "wings": [[f"⟪{sym}", f"{sym}⟫"], ["⟪◉", "◉⟫"], ["⟪●", "●⟫"]],
        },
        "branding": {
            "agent_name": title + " Agent",
            "welcome": "Welcome! Type your message or /help.",
            "goodbye": "Goodbye!",
            "response_label": f" {sym} {title} ",
            "prompt_symbol": f"{sym} ❯ ",
            "help_header": f"({sym}) {title} Commands",
        },
        "tool_prefix": "┊",
        "tool_emojis": dict(DEFAULT_TOOL_EMOJIS),
        "banner_logo": LiteralStr(render_logo(title, a_, tx_, underline=muted)),
        "banner_hero": LiteralStr("\n".join([
            f"[{p_}]{'─' * 60}[/]",
            f"[bold {a_}]{title.center(60)}[/]",
            f"[{p_}]{'─' * 60}[/]",
        ])),
    }
    with open(os.path.join(outdir, slug + ".yaml"), "w", encoding="utf-8") as fh:
        fh.write(dump_yaml(skin))


# ---------------------------------------------------------------- Claude Code / OpenCode

def export_claude(p, outdir):
    (slug, title, desc, cat, p_, s_, a_, bg_, tx_) = p
    show = (slug, title, desc, "Agent", "Welcome", "Goodbye", "◆",
            ["working"], p_, s_, a_, bg_, tx_, cat, title)
    with open(os.path.join(outdir, slug + ".json"), "w", encoding="utf-8") as fh:
        json.dump(claude_theme(show), fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def export_opencode(p, outdir):
    (slug, title, desc, cat, p_, s_, a_, bg_, tx_) = p
    show = (slug, title, desc, "Agent", "Welcome", "Goodbye", "◆",
            ["working"], p_, s_, a_, bg_, tx_, cat, title)
    with open(os.path.join(outdir, slug + ".json"), "w", encoding="utf-8") as fh:
        json.dump(opencode_theme(show), fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------- VS Code

def export_vscode(p, outdir):
    slug, title, _, _, p_, s_, a_, bg_, tx_ = p
    muted = mix(bg_, tx_, 0.4)
    bar = lighten(bg_, 0.07)
    theme = {
        "name": title,
        "type": "dark",
        "colors": {
            "focusBorder": a_,
            "foreground": tx_,
            "disabledForeground": muted,
            "widget.border": p_,
            "widget.shadow": "#000000",
            "selection.background": mix(bg_, a_, 0.4),
            "errorForeground": ERR,
            "warningForeground": WARN,
            "descriptionForeground": muted,
            "editor.background": bg_,
            "editor.foreground": tx_,
            "editorLineNumber.foreground": muted,
            "editorLineNumber.activeForeground": a_,
            "editorCursor.foreground": a_,
            "editor.selectionBackground": mix(bg_, a_, 0.35),
            "editor.selectionHighlightBackground": mix(bg_, a_, 0.2),
            "editor.lineHighlightBackground": lighten(bg_, 0.05),
            "editor.lineHighlightBorder": "#00000000",
            "editorBracketHighlight.foreground1": a_,
            "editorBracketHighlight.foreground2": s_,
            "editorBracketHighlight.foreground3": WARN,
            "editorIndentGuide.background1": mix(bg_, tx_, 0.12),
            "editorIndentGuide.activeBackground1": mix(bg_, tx_, 0.3),
            "editorWhitespace.foreground": mix(bg_, tx_, 0.15),
            "editorGutter.background": bg_,
            "editorGutter.modifiedBackground": WARN,
            "editorGutter.addedBackground": OK,
            "editorGutter.deletedBackground": ERR,
            "editorError.foreground": ERR,
            "editorWarning.foreground": WARN,
            "editorInfo.foreground": a_,
            "editorHoverWidget.background": lighten(bg_, 0.08),
            "editorHoverWidget.border": p_,
            "editorSuggestWidget.background": bg_,
            "editorSuggestWidget.border": p_,
            "editorSuggestWidget.selectedBackground": mix(bg_, a_, 0.35),
            "editorSuggestWidget.highlightForeground": a_,
            "editorWidget.background": bar,
            "editorWidget.border": p_,
            "diffEditor.insertedTextBackground": mix(bg_, OK, 0.15),
            "diffEditor.removedTextBackground": mix(bg_, ERR, 0.15),
            "minimap.background": bg_,
            "minimap.selectionHighlight": mix(bg_, a_, 0.4),
            "scrollbarSlider.background": mix(bg_, tx_, 0.2),
            "scrollbarSlider.hoverBackground": mix(bg_, tx_, 0.3),
            "scrollbarSlider.activeBackground": a_,
            "badge.background": a_,
            "badge.foreground": "#0A0A0A",
            "button.background": a_,
            "button.foreground": "#0A0A0A",
            "button.hoverBackground": lighten(a_, 0.15),
            "input.background": lighten(bg_, 0.05),
            "input.foreground": tx_,
            "input.border": p_,
            "input.placeholderForeground": muted,
            "inputOption.activeBorder": a_,
            "dropdown.background": bar,
            "dropdown.border": p_,
            "list.activeSelectionBackground": mix(bg_, a_, 0.35),
            "list.activeSelectionForeground": tx_,
            "list.inactiveSelectionBackground": mix(bg_, a_, 0.2),
            "list.hoverBackground": mix(bg_, tx_, 0.12),
            "list.focusBackground": mix(bg_, a_, 0.3),
            "list.highlightForeground": a_,
            "list.errorForeground": ERR,
            "list.warningForeground": WARN,
            "tree.indentGuidesStroke": mix(bg_, tx_, 0.15),
            "activityBar.background": darken(bg_, 0.08),
            "activityBar.foreground": tx_,
            "activityBar.inactiveForeground": muted,
            "activityBar.activeBorder": a_,
            "activityBarBadge.background": a_,
            "activityBarBadge.foreground": "#0A0A0A",
            "sideBar.background": darken(bg_, 0.04),
            "sideBar.foreground": tx_,
            "sideBarSectionHeader.background": bar,
            "sideBarSectionHeader.foreground": tx_,
            "statusBar.background": bar,
            "statusBar.foreground": tx_,
            "statusBarItem.hoverBackground": mix(bg_, tx_, 0.15),
            "statusBarItem.remoteBackground": a_,
            "statusBarItem.remoteForeground": "#0A0A0A",
            "statusBar.debuggingBackground": ERR,
            "statusBar.debuggingForeground": "#FFFFFF",
            "titleBar.activeBackground": bg_,
            "titleBar.activeForeground": tx_,
            "titleBar.inactiveBackground": darken(bg_, 0.04),
            "titleBar.inactiveForeground": muted,
            "menubar.selectionBackground": mix(bg_, a_, 0.3),
            "menu.background": bar,
            "menu.foreground": tx_,
            "menu.selectionBackground": mix(bg_, a_, 0.35),
            "panel.background": darken(bg_, 0.02),
            "panel.border": mix(bg_, tx_, 0.25),
            "panelTitle.activeForeground": a_,
            "panelTitle.inactiveForeground": muted,
            "terminal.background": bg_,
            "terminal.foreground": tx_,
            "terminalCursor.background": bg_,
            "terminalCursor.foreground": a_,
            "terminal.ansiBlack": "#0F0F0F",
            "terminal.ansiRed": ERR,
            "terminal.ansiGreen": OK,
            "terminal.ansiYellow": WARN,
            "terminal.ansiBlue": s_,
            "terminal.ansiMagenta": "#BA68C8",
            "terminal.ansiCyan": "#4DD0E1",
            "terminal.ansiWhite": lighten(tx_, 0.05),
            "terminal.ansiBrightBlack": muted,
            "terminal.ansiBrightRed": lighten(ERR, 0.15),
            "terminal.ansiBrightGreen": lighten(OK, 0.15),
            "terminal.ansiBrightYellow": lighten(WARN, 0.15),
            "terminal.ansiBrightBlue": lighten(s_, 0.25),
            "terminal.ansiBrightMagenta": lighten("#BA68C8", 0.2),
            "terminal.ansiBrightCyan": lighten("#4DD0E1", 0.2),
            "terminal.ansiBrightWhite": tx_,
            "tab.activeBackground": bg_,
            "tab.activeForeground": tx_,
            "tab.inactiveBackground": darken(bg_, 0.05),
            "tab.inactiveForeground": muted,
            "tab.activeBorder": a_,
            "tab.border": mix(bg_, tx_, 0.15),
            "tab.hoverBackground": mix(bg_, tx_, 0.08),
            "editorGroupHeader.tabsBackground": darken(bg_, 0.06),
            "editorGroup.border": mix(bg_, tx_, 0.25),
            "breadcrumb.foreground": muted,
            "breadcrumb.focusForeground": tx_,
            "breadcrumb.activeSelectionForeground": a_,
            "progressBar.background": a_,
            "peekView.border": a_,
            "peekViewEditor.background": bg_,
            "peekViewResult.background": bar,
            "peekViewTitle.background": bar,
            "statusBar.noFolderBackground": bar,
            "debugToolBar.background": bar,
            "walkThrough.embeddedEditorBackground": bg_,
            "problemsErrorIcon.foreground": ERR,
            "problemsWarningIcon.foreground": WARN,
            "problemsInfoIcon.foreground": a_,
        },
        "tokenColors": [
            {"scope": ["comment", "punctuation.definition.comment"],
             "settings": {"foreground": muted, "fontStyle": "italic"}},
            {"scope": ["keyword", "storage.type", "storage.modifier", "keyword.control"],
             "settings": {"foreground": s_}},
            {"scope": ["keyword.control.import", "keyword.control.export", "keyword.control.default"],
             "settings": {"foreground": s_, "fontStyle": "bold"}},
            {"scope": ["entity.name.function", "support.function", "meta.function-call", "entity.name.function.declaration"],
             "settings": {"foreground": a_}},
            {"scope": ["entity.name.type", "support.type", "support.class", "storage.type.class", "entity.name.class"],
             "settings": {"foreground": ensure_light(WARN)}},
            {"scope": ["variable", "variable.other", "entity.name.variable"],
             "settings": {"foreground": tx_}},
            {"scope": ["variable.language", "constant.language", "support.variable"],
             "settings": {"foreground": a_, "fontStyle": "bold"}},
            {"scope": ["constant", "constant.numeric", "constant.character", "constant.other"],
             "settings": {"foreground": WARN}},
            {"scope": ["string", "string.quoted.single", "string.quoted.double", "punctuation.definition.string"],
             "settings": {"foreground": OK}},
            {"scope": ["string.escape", "constant.character.escape"],
             "settings": {"foreground": "#4DD0E1"}},
            {"scope": ["constant.character.entity"],
             "settings": {"foreground": "#F48FB1"}},
            {"scope": ["entity.name.tag", "punctuation.definition.tag"],
             "settings": {"foreground": s_}},
            {"scope": ["entity.other.attribute-name"],
             "settings": {"foreground": "#F48FB1"}},
            {"scope": ["punctuation", "punctuation.separator", "punctuation.definition"],
             "settings": {"foreground": muted}},
            {"scope": ["operator", "keyword.operator"],
             "settings": {"foreground": lighten(a_, 0.2)}},
            {"scope": ["meta.embedded", "source.embedded"],
             "settings": {"foreground": tx_}},
            {"scope": ["markup.heading"],
             "settings": {"foreground": a_, "fontStyle": "bold"}},
            {"scope": ["markup.bold"], "settings": {"fontStyle": "bold"}},
            {"scope": ["markup.italic"], "settings": {"fontStyle": "italic"}},
            {"scope": ["markup.quote"], "settings": {"foreground": muted, "fontStyle": "italic"}},
            {"scope": ["markup.link"], "settings": {"foreground": a_, "fontStyle": "underline"}},
            {"scope": ["markup.raw", "markup.inline.raw"],
             "settings": {"foreground": OK}},
            {"scope": ["markup.list"], "settings": {"foreground": a_}},
            {"scope": ["invalid", "invalid.illegal"], "settings": {"foreground": ERR, "fontStyle": "underline"}},
            {"scope": ["deprecated"], "settings": {"foreground": WARN, "fontStyle": "underline"}},
            {"scope": ["meta.diff.header"], "settings": {"foreground": a_}},
            {"scope": ["markup.inserted"], "settings": {"foreground": OK}},
            {"scope": ["markup.deleted"], "settings": {"foreground": ERR}},
            {"scope": ["markup.changed"], "settings": {"foreground": WARN}},
            {"scope": ["source.json punctuation.definition.key"], "settings": {"foreground": a_}},
            {"scope": ["source.css property-name", "source.css property-value"],
             "settings": {"foreground": tx_}},
            {"scope": ["source.css selector"], "settings": {"foreground": s_}},
        ],
    }
    with open(os.path.join(outdir, slug + ".json"), "w", encoding="utf-8") as fh:
        json.dump(theme, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------- Zed

def export_zed(p, outdir):
    slug, title, _, _, p_, s_, a_, bg_, tx_ = p
    muted = mix(bg_, tx_, 0.4)
    syntax = {
        "comment": muted,
        "constant": WARN,
        "emphasis": "#F48FB1",
        "emphasis_strong": lighten("#F48FB1", 0.2),
        "function": a_,
        "keyword": s_,
        "label": "#F48FB1",
        "link_text": a_,
        "number": WARN,
        "operator": lighten(a_, 0.2),
        "property": "#4DD0E1",
        "punctuation": muted,
        "punctuation_brackets": muted,
        "punctuation_delimiter": muted,
        "punctuation_list_marker": a_,
        "punctuation_special": "#F48FB1",
        "string": OK,
        "string_escape": "#4DD0E1",
        "string_regexp": "#4DD0E1",
        "string_special": lighten(OK, 0.15),
        "tag": s_,
        "type": ensure_light(WARN),
        "variable": tx_,
        "variable_debug": a_,
        "variable_special": a_,
    }
    family = {
        "name": title,
        "author": "thanvish21",
        "themes": [
            {
                "name": title,
                "appearance": "dark",
                "style": {
                    "background": bg_,
                    "foreground": tx_,
                    "accent": a_,
                    "border": mix(bg_, tx_, 0.25),
                    "border.focused": a_,
                    "border.selected": a_,
                    "border.transparent": "#00000000",
                    "border.variant": mix(bg_, tx_, 0.15),
                    "elevated_surface.background": lighten(bg_, 0.08),
                    "element.background": lighten(bg_, 0.06),
                    "element.hover": mix(bg_, a_, 0.25),
                    "element.active": mix(bg_, a_, 0.35),
                    "element.selected": mix(bg_, a_, 0.35),
                    "element_selected": mix(bg_, a_, 0.35),
                    "ghost_element.background": darken(bg_, 0.05),
                    "ghost_element.hover": mix(bg_, tx_, 0.12),
                    "ghost_element.active": mix(bg_, a_, 0.2),
                    "ghost_element.selected": mix(bg_, a_, 0.2),
                    "icon.accent": a_,
                    "icon.background": lighten(bg_, 0.06),
                    "icon.border": p_,
                    "icon.disabled": muted,
                    "icon.foreground": tx_,
                    "icon.hover": a_,
                    "icon.inactive": muted,
                    "icon.muted": muted,
                    "icon.placeholder": muted,
                    "icon.selected": a_,
                    "panel.background": darken(bg_, 0.03),
                    "panel.border": mix(bg_, tx_, 0.2),
                    "panel.focused_border": a_,
                    "panel.indent_guide": mix(bg_, tx_, 0.12),
                    "panel.indent_guide_active": mix(bg_, tx_, 0.3),
                    "panel.placeholder": muted,
                    "panel.toolbar.background": darken(bg_, 0.03),
                    "panel.toolbar.border": mix(bg_, tx_, 0.2),
                    "status_bar.background": darken(bg_, 0.05),
                    "status_bar.border": mix(bg_, tx_, 0.2),
                    "status_bar.foreground": muted,
                    "status_bar.item.hover_background": mix(bg_, tx_, 0.12),
                    "status_bar.item.active_background": mix(bg_, a_, 0.3),
                    "status_bar.item.error": ERR,
                    "status_bar.item.success": OK,
                    "status_bar.item.warning": WARN,
                    "title_bar.background": darken(bg_, 0.04),
                    "title_bar.border": mix(bg_, tx_, 0.2),
                    "title_bar.foreground": tx_,
                    "tab_bar.background": darken(bg_, 0.06),
                    "tab_bar.border": mix(bg_, tx_, 0.15),
                    "tab.active_background": bg_,
                    "tab.active_border": a_,
                    "tab.active_foreground": tx_,
                    "tab.inactive_background": "transparent",
                    "tab.inactive_foreground": muted,
                    "tab.hover_background": mix(bg_, tx_, 0.08),
                    "tab.hover_foreground": tx_,
                    "editor.background": bg_,
                    "editor.foreground": tx_,
                    "editor.border": mix(bg_, tx_, 0.2),
                    "editor.active_line.background": lighten(bg_, 0.045),
                    "editor.active_line_number": a_,
                    "editor.document_highlight.bracket_background": mix(bg_, a_, 0.25),
                    "editor.document_highlight.read_background": mix(bg_, a_, 0.12),
                    "editor.document_highlight.write_background": mix(bg_, a_, 0.2),
                    "editor.find_match.background": mix(bg_, WARN, 0.4),
                    "editor.find_match.border": WARN,
                    "editor.gutter.background": bg_,
                    "editor.gutter.border": mix(bg_, tx_, 0.12),
                    "editor.gutter.foreground": muted,
                    "editor.gutter.selected_foreground": a_,
                    "editor.group_blank_lines": mix(bg_, tx_, 0.1),
                    "editor.highlighted_line.background": lighten(bg_, 0.045),
                    "editor.hover_popover.background": lighten(bg_, 0.08),
                    "editor.hover_popover.border": p_,
                    "editor.inactive_fold_placeholder": muted,
                    "editor.indent_guide": mix(bg_, tx_, 0.1),
                    "editor.indent_guide_active": mix(bg_, tx_, 0.28),
                    "editor.invisible": mix(bg_, tx_, 0.15),
                    "editor.line_number": muted,
                    "editor.lsp.background": lighten(bg_, 0.08),
                    "editor.lsp.border": p_,
                    "editor.lsp.completion_documentation.background": lighten(bg_, 0.08),
                    "editor.lsp.completion_documentation.border": p_,
                    "editor.lsp.error_background": mix(bg_, ERR, 0.15),
                    "editor.lsp.error_border": ERR,
                    "editor.lsp.hover.background": lighten(bg_, 0.08),
                    "editor.lsp.hover.border": p_,
                    "editor.lsp.rename.background": mix(bg_, a_, 0.25),
                    "editor.lsp.rename.border": a_,
                    "editor.lsp.syntax_tree.background": mix(bg_, tx_, 0.1),
                    "editor.lsp.warning_background": mix(bg_, WARN, 0.15),
                    "editor.lsp.warning_border": WARN,
                    "editor.occurrence.background": mix(bg_, a_, 0.15),
                    "editor.occurrence.border": mix(bg_, a_, 0.4),
                    "editor.selected_fold_placeholder": mix(bg_, a_, 0.25),
                    "editor.selection": mix(bg_, a_, 0.35),
                    "editor.selection_disabled": mix(bg_, a_, 0.2),
                    "editor.selection_match_background": mix(bg_, WARN, 0.3),
                    "editor.snippet_tabstop.background": mix(bg_, a_, 0.25),
                    "editor.snippet_tabstop.border": a_,
                    "editor.special_character": "#F48FB1",
                    "editor.tab.active": a_,
                    "editor.tab.inactive": muted,
                    "editor.tag_attribute.background": mix(bg_, a_, 0.12),
                    "editor.tag_attribute.border": a_,
                    "editor.tag_matching_tag.background": mix(bg_, a_, 0.2),
                    "editor.tag_matching_tag.border": a_,
                    "editor.text_highlight.background": mix(bg_, WARN, 0.25),
                    "editor.text_highlight.border": WARN,
                    "editor.whitespace": mix(bg_, tx_, 0.15),
                    "editor.window_background": bg_,
                    "terminal.background": bg_,
                    "terminal.foreground": tx_,
                    "terminal.ansi.black": "#0F0F0F",
                    "terminal.ansi.blue": s_,
                    "terminal.ansi.bright_black": muted,
                    "terminal.ansi.bright_blue": lighten(s_, 0.25),
                    "terminal.ansi.bright_cyan": lighten("#4DD0E1", 0.2),
                    "terminal.ansi.bright_green": lighten(OK, 0.15),
                    "terminal.ansi.bright_magenta": lighten("#BA68C8", 0.2),
                    "terminal.ansi.bright_red": lighten(ERR, 0.15),
                    "terminal.ansi.bright_white": tx_,
                    "terminal.ansi.bright_yellow": lighten(WARN, 0.15),
                    "terminal.ansi.cyan": "#4DD0E1",
                    "terminal.ansi.green": OK,
                    "terminal.ansi.magenta": "#BA68C8",
                    "terminal.ansi.red": ERR,
                    "terminal.ansi.white": lighten(tx_, 0.05),
                    "terminal.ansi.yellow": WARN,
                    "terminal.bright_black": muted,
                    "terminal.bright_blue": lighten(s_, 0.25),
                    "terminal.bright_cyan": lighten("#4DD0E1", 0.2),
                    "terminal.bright_green": lighten(OK, 0.15),
                    "terminal.bright_magenta": lighten("#BA68C8", 0.2),
                    "terminal.bright_red": lighten(ERR, 0.15),
                    "terminal.bright_white": tx_,
                    "terminal.bright_yellow": lighten(WARN, 0.15),
                    "terminal.dim_black": darken(bg_, 0.5),
                    "terminal.dim_blue": darken(s_, 0.3),
                    "terminal.dim_cyan": darken("#4DD0E1", 0.3),
                    "terminal.dim_green": darken(OK, 0.3),
                    "terminal.dim_magenta": darken("#BA68C8", 0.3),
                    "terminal.dim_red": darken(ERR, 0.3),
                    "terminal.dim_white": darken(tx_, 0.4),
                    "terminal.dim_yellow": darken(WARN, 0.3),
                    "terminal.flashing_background": mix(bg_, a_, 0.5),
                    "terminal.selection_background": mix(bg_, a_, 0.35),
                    "terminal.selection_foreground": tx_,
                    "toolbar.background": darken(bg_, 0.04),
                    "toolbar.border": mix(bg_, tx_, 0.2),
                    "toolbar.foreground": muted,
                    "toolbar.active_background": mix(bg_, a_, 0.3),
                    "toolbar.active_foreground": tx_,
                    "toolbar.hover_background": mix(bg_, tx_, 0.12),
                    "toolbar.hover_foreground": tx_,
                    "toolbar.selected_background": mix(bg_, a_, 0.35),
                    "toolbar.selected_foreground": tx_,
                    "pane_group.border": mix(bg_, tx_, 0.25),
                    "pane.focused_border": a_,
                    "pane.active_border": a_,
                    "scrollbar.thumb.background": mix(bg_, tx_, 0.25),
                    "scrollbar.thumb.hover_background": mix(bg_, tx_, 0.35),
                    "scrollbar.thumb.border": mix(bg_, tx_, 0.2),
                    "scrollbar.track.background": bg_,
                    "scrollbar.track.border": mix(bg_, tx_, 0.15),
                    "scrollbar.track.disabled": mix(bg_, tx_, 0.08),
                    "scrollbar_thumb.background": mix(bg_, tx_, 0.25),
                    "scrollbar_track.background": bg_,
                    "extension.background": bg_,
                    "extension.border": mix(bg_, tx_, 0.2),
                    "extension.icon.background": lighten(bg_, 0.06),
                    "extension.icon.border": p_,
                    "extension.icon.foreground": tx_,
                    "extension.foreground": tx_,
                    "extension.hover_background": mix(bg_, tx_, 0.12),
                    "extension.muted_background": darken(bg_, 0.05),
                    "extension.muted_border": mix(bg_, tx_, 0.15),
                    "extension.muted_foreground": muted,
                    "extension.selected_background": mix(bg_, a_, 0.3),
                    "extension.selected_border": a_,
                    "extension.selected_foreground": tx_,
                    "input.background": lighten(bg_, 0.05),
                    "input.border": p_,
                    "input.disabled_background": darken(bg_, 0.03),
                    "input.disabled_foreground": muted,
                    "input.focused_border": a_,
                    "input.foreground": tx_,
                    "input.placeholder": muted,
                    "input.value.background": lighten(bg_, 0.05),
                    "input.value.border": p_,
                    "input.value.foreground": tx_,
                    "menu.background": lighten(bg_, 0.08),
                    "menu.border": mix(bg_, tx_, 0.2),
                    "menu.disabled_foreground": muted,
                    "menu.foreground": tx_,
                    "menu.hover_background": mix(bg_, a_, 0.3),
                    "menu.selected_background": mix(bg_, a_, 0.35),
                    "menu.selected_foreground": tx_,
                    "menu_selected.background": mix(bg_, a_, 0.35),
                    "menu_selected.foreground": tx_,
                    "menu_selection.background": mix(bg_, a_, 0.35),
                    "menu_selection.foreground": tx_,
                    "text.accent": a_,
                    "text.background": bg_,
                    "text.border": mix(bg_, tx_, 0.25),
                    "text.disabled": muted,
                    "text.foreground": tx_,
                    "text.hover": tx_,
                    "text.info": a_,
                    "text.muted": muted,
                    "text.placeholder": muted,
                    "text.selected": tx_,
                    "text.error": ERR,
                    "text.success": OK,
                    "text.warning": WARN,
                    "text_system.foreground": tx_,
                    "text_muted.foreground": muted,
                    "text_accent.foreground": a_,
                    "text_info.foreground": a_,
                    "text_warning.foreground": WARN,
                    "text_error.foreground": ERR,
                    "text_success.foreground": OK,
                    "text_disabled.foreground": muted,
                    "text_placeholder.foreground": muted,
                    "text_border.border": mix(bg_, tx_, 0.25),
                    "text_selection.background": mix(bg_, a_, 0.35),
                    "text_highlight.background": mix(bg_, WARN, 0.3),
                    "text_highlight.border": WARN,
                    "text_highlight.foreground": tx_,
                    "text_link.foreground": a_,
                    "text_note.foreground": a_,
                    "text_title.foreground": tx_,
                    "text_heading.foreground": tx_,
                    "text_hint.foreground": a_,
                    "text_inactive.foreground": muted,
                    "text_navigation.foreground": a_,
                    "text_secondary.foreground": muted,
                    "text_tertiary.foreground": muted,
                    "text_quaternary.foreground": muted,
                    "text_faint.foreground": muted,
                    "text_plain.foreground": tx_,
                    "text_code.foreground": OK,
                    "text_quote.foreground": muted,
                    "text_meta.foreground": muted,
                    "text_label.foreground": tx_,
                    "text_keyword.foreground": s_,
                    "text_function.foreground": a_,
                    "text_variable.foreground": tx_,
                    "text_constant.foreground": WARN,
                    "text_string.foreground": OK,
                    "text_number.foreground": WARN,
                    "text_boolean.foreground": WARN,
                    "text_operator.foreground": lighten(a_, 0.2),
                    "text_type.foreground": ensure_light(WARN),
                    "text_tag.foreground": s_,
                    "text_attribute.foreground": "#F48FB1",
                    "text_property.foreground": "#4DD0E1",
                    "text_regexp.foreground": "#4DD0E1",
                    "text_escape.foreground": "#4DD0E1",
                    "text_delimiter.foreground": muted,
                    "text_comment.foreground": muted,
                    "text_emphasis.foreground": "#F48FB1",
                    "text_strong.foreground": tx_,
                    "text_link.underline": a_,
                    "text_url.foreground": a_,
                    "text_hyperlink.foreground": a_,
                    "text_unnamed.foreground": muted,
                },
                "syntax": syntax,
            }
        ],
    }
    with open(os.path.join(outdir, slug + ".json"), "w", encoding="utf-8") as fh:
        json.dump(family, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------- iTerm2

def _iterm_comp(r, g, b):
    return "%.6f" % (r / 255.0)


def export_iterm2(p, outdir):
    slug, title, _, _, p_, s_, a_, bg_, tx_ = p
    a = ansi_from(p_, s_, a_, bg_, tx_)
    colors = {
        "Ansi 0 Color": darken(bg_, 0.5),
        "Ansi 1 Color": ERR,
        "Ansi 2 Color": OK,
        "Ansi 3 Color": WARN,
        "Ansi 4 Color": s_,
        "Ansi 5 Color": "#BA68C8",
        "Ansi 6 Color": "#4DD0E1",
        "Ansi 7 Color": lighten(tx_, 0.05),
        "Ansi 8 Color": a["brightBlack"],
        "Ansi 9 Color": lighten(ERR, 0.15),
        "Ansi 10 Color": lighten(OK, 0.15),
        "Ansi 11 Color": lighten(WARN, 0.15),
        "Ansi 12 Color": lighten(s_, 0.25),
        "Ansi 13 Color": lighten("#BA68C8", 0.2),
        "Ansi 14 Color": lighten("#4DD0E1", 0.2),
        "Ansi 15 Color": tx_,
        "Background Color": bg_,
        "Foreground Color": tx_,
        "Bold Color": a_,
        "Cursor Color": a_,
        "Cursor Text Color": bg_,
        "Selection Color": mix(bg_, a_, 0.5),
        "Selected Text Color": tx_,
        "Badge Color": a_,
        "Link Color": a_,
    }
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
             '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
             '<plist version="1.0">',
             "<dict>",
             "  <key>name</key>",
             f"  <string>{title}</string>"]
    for name, c in colors.items():
        r, g, b = hex_to_rgb(c)
        lines += [f"  <key>{name}</key>", "  <dict>",
                  f"    <key>Red Component</key><real>{_iterm_comp(r, g, b)}</real>",
                  f"    <key>Green Component</key><real>{_iterm_comp(g, g, b)}</real>",
                  f"    <key>Blue Component</key><real>{_iterm_comp(b, g, b)}</real>",
                  "  </dict>"]
    lines += ["</dict>", "</plist>", ""]
    with open(os.path.join(outdir, slug + ".itermcolors"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


# ---------------------------------------------------------------- Windows Terminal

def export_wt(p, outdir):
    slug, title, _, _, p_, s_, a_, bg_, tx_ = p
    a = ansi_from(p_, s_, a_, bg_, tx_)
    scheme = {
        "name": title,
        "background": bg_,
        "foreground": tx_,
        "cursorColor": a_,
        "selectionBackground": mix(bg_, a_, 0.5),
        "black": a["black"],
        "red": a["red"],
        "green": a["green"],
        "yellow": a["yellow"],
        "blue": a["blue"],
        "purple": a["magenta"],
        "cyan": a["cyan"],
        "white": a["white"],
        "brightBlack": a["brightBlack"],
        "brightRed": a["brightRed"],
        "brightGreen": a["brightGreen"],
        "brightYellow": a["brightYellow"],
        "brightBlue": a["brightBlue"],
        "brightPurple": a["brightMagenta"],
        "brightCyan": a["brightCyan"],
        "brightWhite": a["brightWhite"],
    }
    with open(os.path.join(outdir, slug + ".json"), "w", encoding="utf-8") as fh:
        json.dump(scheme, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------- kitty

def export_kitty(p, outdir):
    slug, title, _, _, p_, s_, a_, bg_, tx_ = p
    a = ansi_from(p_, s_, a_, bg_, tx_)
    muted = mix(bg_, tx_, 0.4)
    lines = [f"# {title} — generated by themeverse",
             "background " + bg_,
             "foreground " + tx_,
             "cursor " + a_,
             "cursor_text_color " + bg_,
             "selection_background " + mix(bg_, a_, 0.5),
             "selection_foreground " + tx_,
             "active_tab_foreground " + bg_,
             "active_tab_background " + a_,
             "inactive_tab_foreground " + muted,
             "inactive_tab_background " + darken(bg_, 0.2),
             "tab_bar_background " + darken(bg_, 0.4),
             "url_color " + a_,
             "mark1_foreground " + bg_,
             "mark1_background " + ERR,
             "mark2_foreground " + bg_,
             "mark2_background " + OK,
             "mark3_foreground " + bg_,
             "mark3_background " + WARN,
             ""]
    for i, name in enumerate(["color0", "color1", "color2", "color3", "color4",
                              "color5", "color6", "color7", "color8", "color9",
                              "color10", "color11", "color12", "color13",
                              "color14", "color15"]):
        key = ["black", "red", "green", "yellow", "blue", "magenta",
               "cyan", "white", "brightBlack", "brightRed", "brightGreen",
               "brightYellow", "brightBlue", "brightMagenta", "brightCyan",
               "brightWhite"][i]
        lines.append(name + " " + a[key])
    lines.append("")
    with open(os.path.join(outdir, slug + ".conf"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


# ---------------------------------------------------------------- Neovim

def export_neovim(p, outdir):
    slug, title, _, _, p_, s_, a_, bg_, tx_ = p
    muted = mix(bg_, tx_, 0.4)
    name = slug.replace("-", "_")
    groups = {
        "Normal": (tx_, bg_),
        "NormalFloat": (tx_, lighten(bg_, 0.06)),
        "NormalNC": (muted, bg_),
        "EndOfBuffer": (muted, bg_),
        "Cursor": (bg_, a_),
        "CursorLine": (None, lighten(bg_, 0.045)),
        "CursorLineNr": (a_, None),
        "CursorColumn": (None, lighten(bg_, 0.03)),
        "ColorColumn": (None, lighten(bg_, 0.06)),
        "SignColumn": (tx_, bg_),
        "LineNr": (muted, bg_),
        "Folded": (muted, darken(bg_, 0.2)),
        "FoldColumn": (muted, bg_),
        "Pmenu": (tx_, lighten(bg_, 0.07)),
        "PmenuSel": (bg_, a_),
        "PmenuSbar": (None, mix(bg_, tx_, 0.15)),
        "PmenuThumb": (None, mix(bg_, tx_, 0.3)),
        "WildMenu": (bg_, a_),
        "VertSplit": (mix(bg_, tx_, 0.25), bg_),
        "WinSeparator": (mix(bg_, tx_, 0.25), bg_),
        "StatusLine": (tx_, darken(bg_, 0.15)),
        "StatusLineNC": (muted, darken(bg_, 0.1)),
        "TabLine": (muted, darken(bg_, 0.1)),
        "TabLineSel": (bg_, a_),
        "TabLineFill": (muted, darken(bg_, 0.15)),
        "Visual": (tx_, mix(bg_, a_, 0.4)),
        "VisualNOS": (tx_, mix(bg_, a_, 0.3)),
        "Search": (bg_, WARN),
        "CurSearch": (bg_, a_),
        "IncSearch": (bg_, a_),
        "MatchParen": (a_, mix(bg_, a_, 0.35)),
        "Error": ("#FFFFFF", ERR),
        "ErrorMsg": (ERR, None),
        "WarningMsg": (WARN, None),
        "InfoMsg": (a_, None),
        "MoreMsg": (a_, None),
        "Question": (a_, None),
        "Title": (a_, None),
        "Directory": (a_, None),
        "SpecialKey": (mix(bg_, tx_, 0.3), None),
        "NonText": (mix(bg_, tx_, 0.3), None),
        "Whitespace": (mix(bg_, tx_, 0.15), None),
        "Conceal": (muted, None),
        "Todo": (WARN, bg_),
        "DiagnosticError": (ERR, None),
        "DiagnosticWarn": (WARN, None),
        "DiagnosticInfo": (a_, None),
        "DiagnosticHint": (muted, None),
        "DiagnosticUnderlineError": (None, None),
        "DiagnosticUnderlineWarn": (None, None),
        "DiagnosticUnderlineInfo": (None, None),
        "DiffAdd": (OK, mix(bg_, OK, 0.15)),
        "DiffChange": (WARN, mix(bg_, WARN, 0.15)),
        "DiffDelete": (ERR, mix(bg_, ERR, 0.15)),
        "DiffText": (tx_, mix(bg_, WARN, 0.3)),
        "SpellBad": (ERR, None),
        "SpellCap": (WARN, None),
        "SpellRare": (a_, None),
        "SpellLocal": (a_, None),
        "Comment": (muted, None),
        "Constant": (WARN, None),
        "String": (OK, None),
        "Character": (OK, None),
        "Number": (WARN, None),
        "Boolean": (WARN, None),
        "Float": (WARN, None),
        "Identifier": (tx_, None),
        "Function": (a_, None),
        "Statement": (s_, None),
        "Conditional": (s_, None),
        "Repeat": (s_, None),
        "Label": ("#F48FB1", None),
        "Operator": (lighten(a_, 0.2), None),
        "Keyword": (s_, None),
        "Exception": (s_, None),
        "PreProc": ("#F48FB1", None),
        "Include": ("#F48FB1", None),
        "Define": ("#F48FB1", None),
        "Macro": ("#F48FB1", None),
        "PreCondit": ("#F48FB1", None),
        "Type": (ensure_light(WARN), None),
        "StorageClass": (ensure_light(WARN), None),
        "Structure": (ensure_light(WARN), None),
        "Typedef": (ensure_light(WARN), None),
        "Special": ("#4DD0E1", None),
        "SpecialChar": ("#4DD0E1", None),
        "Tag": (s_, None),
        "Delimiter": (muted, None),
        "SpecialComment": (muted, None),
        "Debug": (WARN, None),
        "Underlined": (a_, None),
        "Bold": (None, None),
        "Italic": (None, None),
        "Strikethrough": (None, None),
        "Ignore": (muted, None),
        "ModeMsg": (tx_, None),
        "MsgArea": (tx_, bg_),
        "MsgSeparator": (muted, bg_),
        "QuickFixLine": (tx_, mix(bg_, a_, 0.3)),
        "CursorIM": (bg_, a_),
        "lCursor": (bg_, a_),
        "TermCursor": (bg_, a_),
        "TermCursorNC": (muted, None),
        "healthError": (ERR, None),
        "healthSuccess": (OK, None),
        "healthWarning": (WARN, None),
    }
    L = []
    L.append(f"-- {title} — generated by themeverse")
    L.append("vim.g.colors_name = %r" % name)
    L.append("")
    for g, (fg, bgc) in groups.items():
        fg_s = ("fg = %r" % fg) if fg else "fg = 'NONE'"
        bg_s = ("bg = %r" % bgc) if bgc else "bg = 'NONE'"
        L.append("vim.api.nvim_set_hl(0, %r, { %s, %s })" % (g, fg_s, bg_s))
    L.append("")
    with open(os.path.join(outdir, slug + ".lua"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


# ---------------------------------------------------------------- Oh My Posh

def export_omp(p, outdir):
    slug, title, _, _, p_, s_, a_, bg_, tx_ = p
    muted = mix(bg_, tx_, 0.4)
    theme = {
        "$schema": "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/schema.json",
        "final_space": True,
        "blocks": [
            {
                "type": "prompt",
                "alignment": "left",
                "newline": False,
                "segments": [
                    {"type": "root", "style": "diamond", "leading_diamond": "\ue0b6",
                     "foreground": bg_, "background": a_,
                     "template": " \uf0e7 "},
                    {"type": "session", "style": "diamond", "leading_diamond": "\ue0b6",
                     "foreground": bg_, "background": p_,
                     "template": " {{ .UserName }} "},
                    {"type": "path", "style": "powerline",
                     "foreground": tx_, "background": s_,
                     "template": " \ue5ff {{ path .Path .Location }} ",
                     "properties": {"style": "agnoster_short"}},
                    {"type": "git", "style": "powerline",
                     "foreground": tx_, "background": muted,
                     "template": " {{ .HEAD }} "},
                    {"type": "executiontime", "style": "diamond",
                     "leading_diamond": "", "trailing_diamond": "\ue0b0",
                     "foreground": tx_, "background": WARN,
                     "template": " \uf252 {{ .FormattedMs }} ",
                     "properties": {"threshold": 500}},
                ],
            },
            {
                "type": "prompt",
                "alignment": "right",
                "segments": [
                    {"type": "node", "style": "diamond", "leading_diamond": "\ue0b2",
                     "foreground": bg_, "background": OK,
                     "template": " \ue718 {{ if .PackageManagerIcon }}{{ .PackageManagerIcon }} {{ end }}{{ .Full }} "},
                    {"type": "python", "style": "powerline",
                     "foreground": bg_, "background": "#4DD0E1",
                     "template": " \ue235 {{ .Full }} "},
                    {"type": "shell", "style": "diamond", "trailing_diamond": "\ue0b2",
                     "foreground": tx_, "background": a_,
                     "template": " {{ .Name }} "},
                ],
            },
            {
                "type": "prompt",
                "alignment": "left",
                "newline": True,
                "segments": [
                    {"type": "text", "style": "plain",
                     "foreground": a_, "background": "transparent",
                     "template": "❯ "},
                ],
            },
        ],
    }
    with open(os.path.join(outdir, slug + ".omp.json"), "w", encoding="utf-8") as fh:
        json.dump(theme, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------- registry

EXPORTERS = [
    ("hermes", export_hermes, ".yaml"),
    ("claude-code", export_claude, ".json"),
    ("opencode", export_opencode, ".json"),
    ("vscode", export_vscode, ".json"),
    ("zed", export_zed, ".json"),
    ("iterm2", export_iterm2, ".itermcolors"),
    ("windows-terminal", export_wt, ".json"),
    ("kitty", export_kitty, ".conf"),
    ("neovim", export_neovim, ".lua"),
    ("oh-my-posh", export_omp, ".omp.json"),
]


def main():
    for fmt, fn, ext in EXPORTERS:
        outdir = os.path.join(OUT, fmt)
        os.makedirs(outdir, exist_ok=True)
        for p in PALETTES:
            fn(p, outdir)

    # validate
    errors = 0
    for fmt, fn, ext in EXPORTERS:
        outdir = os.path.join(OUT, fmt)
        n = 0
        for fname in sorted(os.listdir(outdir)):
            if not fname.endswith(ext):
                continue
            n += 1
            path = os.path.join(outdir, fname)
            try:
                if fname.endswith(".json"):
                    json.load(open(path, encoding="utf-8"))
                elif fname.endswith(".yaml"):
                    yaml.safe_load(open(path, encoding="utf-8"))
                elif fname.endswith(".lua"):
                    open(path, encoding="utf-8").read()
                elif fname.endswith(".conf"):
                    open(path, encoding="utf-8").read()
                elif fname.endswith(".itermcolors"):
                    open(path, encoding="utf-8").read()
            except Exception as e:
                print("ERROR", fmt, fname, e)
                errors += 1
        print(f"{fmt:18s} {n} files")

    # Hermes skins get the full schema validation
    from generate_skins import validate_skin
    hermes_dir = os.path.join(OUT, "hermes")
    for fname in sorted(os.listdir(hermes_dir)):
        if fname.endswith(".yaml"):
            for e in validate_skin(os.path.join(hermes_dir, fname)):
                print("HERMES ERROR", fname, e)
                errors += 1
    print(f"\n{len(PALETTES)} palettes x {len(EXPORTERS)} formats, {errors} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
