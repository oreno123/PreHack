---
name: radix-colors
description: Browse and pick colors from the Radix UI color system. Generates an interactive HTML color browser with all 31 color families, light/dark mode toggle, selection, pairing suggestions, and copy-to-clipboard export.
---

# Radix Colors Browser

Opens an interactive HTML color browser for the Radix UI color system.

## When to use

- User wants to browse, pick, or choose colors for a project
- User mentions "radix colors", "色板", "选色", "配色", "color picker", "color browser"
- User needs to select a color palette before building a frontend
- User asks "what colors should I use" or "help me pick colors"

## Instructions

1. Check if the HTML file already exists at `~/.claude/skills/radix-colors/references/radix-color-browser.html`
2. If it doesn't exist, copy it from the references directory or generate it
3. Copy the HTML file to the user's working directory as `radix-color-browser.html`
4. Open it in the browser using `start radix-color-browser.html` (Windows) or `open radix-color-browser.html` (macOS)
5. Tell the user:
   > Radix color browser opened in your browser. Browse the palettes, click to select colors, switch light/dark mode, and check pairing suggestions. When done, click "Copy Selection" at the bottom and paste the result back here.

6. Wait for the user to paste their color selections back
7. Use their selections in the current project work

## What the HTML provides

- All 31 Radix color families (gray, mauve, slate, sage, olive, sand, tomato, red, ruby, crimson, pink, plum, purple, violet, iris, indigo, blue, cyan, teal, jade, green, grass, mint, sky, bronze, gold, brown, orange, amber, yellow, lime)
- Each family shows 12 scale steps with hex values and CSS variable names
- Light/dark mode toggle
- Click to select colors, click again to deselect
- Pairing suggestions panel: when a primary color is selected, shows recommended background/text/border/interactive colors
- "Copy Selection" button exports selected colors as plain text for pasting back to Claude

## Output format from user

The user will paste something like:
```
Selected colors: blue 9, slate 12, blue 3, blue 6, blue 11
```

Parse this and use the corresponding CSS variables or hex values in the project.
