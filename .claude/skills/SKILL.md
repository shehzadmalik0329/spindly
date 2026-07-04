---
name: spendly-ui-designer
description: Use this skill whenever the user asks to design, create, build, redesign, or improve any UI page or component for Spendly (a personal expense tracker app) — e.g. "design the dashboard page", "create UI for the add-expense form", "build a component for monthly summary", "redesign the transactions list". Generates modern, production-ready, fintech-style UI using vanilla CSS (no framework/utility libraries) with clean component structure, an 8px spacing grid, card-based layouts, and Lucide icons. Always trigger this for any Spendly-related frontend/UI/page/component work, even if the user doesn't say the word "design" explicitly (e.g. "make the settings page look better", "I need a card to show recent transactions").
---

# Spendly UI Designer

Generates modern, clean, fintech-style UI components and pages for Spendly, a personal expense tracker. Every output should look like it belongs in a polished, modern SaaS product — never generic, dated, or boilerplate-heavy.

## Workflow

1. **Identify the target.** Confirm the page/component name and its purpose (e.g. "Add Expense form", "Monthly Summary card", "Transactions list page").
2. **Check for existing design context first.** Before generating anything:
   - Look for existing project files (CSS files, component files, a style guide, design tokens) in the current working directory or repo.
   - If found, extract and reuse: color palette, font stack, spacing values, border-radius, shadow style, existing component patterns/naming conventions.
   - If no existing design context is available and this isn't the first component being built for the project, **ask the user for a screenshot/photo of the existing UI** before proceeding, so the new piece matches rather than introduces a clashing style. Don't guess at an established palette — ask.
   - If this is genuinely the first UI piece in the project (nothing to match yet), proceed using the Design Rules below to establish the baseline style, and mention that this output is setting the visual foundation other pages should follow.
3. **Clarify inputs if missing.** At minimum you need the page/component name. If the user hasn't specified data shape, key fields, or constraints (e.g. "should this support multiple currencies?"), make reasonable assumptions explicit in the UI Structure summary rather than blocking on it — only stop and ask if the ambiguity would significantly change the layout (e.g. unclear whether it's a list view or a detail view).
4. **Generate the output** in the four parts below, in order.

## Output Format

### 1. UI Structure (brief)
A short summary, not a wall of text:
- Layout and key sections (e.g. "header with total balance, filterable transaction list, floating add button")
- 2-4 notable UX decisions and why (e.g. "grouped transactions by date to reduce scanning effort")

### 2. Code
- Vanilla CSS only — no Tailwind, no CSS-in-JS, no utility-class frameworks. Use real class names (BEM-ish or simple semantic naming, e.g. `.expense-card`, `.expense-card__amount`).
- Modular: one component = one clearly delineated block of markup + its own CSS section/file. Don't entangle unrelated components.
- Minimal boilerplate — no unused wrapper divs, no commented-out scaffolding, no placeholder lorem ipsum unless explicitly asked for sample data.
- Use CSS custom properties (`--color-primary`, `--space-2`, etc.) for anything reused more than once, so theming stays consistent across components.
- If the component needs interactivity, use plain JS (no framework assumed) unless the user has indicated otherwise.

### 3. Design Quality Checklist (apply, don't just state)
- Modern fintech/SaaS look: restrained color palette, generous whitespace, clear visual hierarchy (size/weight/color used deliberately, not decoratively)
- Card-based layout where it suits the content (transactions, summaries, stats)
- Subtle color and shadow use — avoid saturated colors and heavy drop shadows; prefer soft, low-opacity shadows and muted accent colors
- Rounded corners (consistent radius scale, e.g. 8px / 12px / 16px — pick one system and stick to it)
- Consistent spacing on an 8px grid (8, 16, 24, 32, 40...) — no arbitrary pixel values like 13px or 22px
- Clear typographic hierarchy (1-2 font families max, a defined scale of sizes/weights)

### 4. Icons
- Use Lucide icons wherever an icon adds clarity (navigation, actions, categories, status). Reference icons by their Lucide name (e.g. `lucide:arrow-up-right`, `lucide:wallet`) and note how they're imported/rendered based on what's already used in the project — if unknown, default to the Lucide SVG sprite or `<svg>` markup directly rather than assuming a package is installed.
- Icons should be meaningful, not decorative filler — every icon should reinforce what the element does (e.g. a trending-down icon next to a spending decrease, not a random icon for visual interest).
- Keep icon sizing consistent (e.g. 16px for inline/label icons, 20-24px for buttons/nav).

## Design Rules (defaults when no existing style is found)

- Palette: 1 primary brand color, 1-2 neutral grays for text/borders, sparing use of semantic colors (green for income/positive, red for expense/negative) — keep saturation low/muted, not neon
- Border radius: pick one scale and apply consistently (e.g. 8px small elements, 12px cards, 16px modals)
- Shadows: soft and subtle (e.g. `0 1px 2px rgba(0,0,0,0.05)` for resting cards, slightly stronger on hover/elevated elements) — never heavy or dark drop shadows
- Spacing: strict 8px grid for margins, padding, and gaps
- Typography: one primary sans-serif font, a small defined type scale (e.g. 12/14/16/20/24/32px), consistent line-heights

## What to Avoid

- Generic, dated, or "default Bootstrap" looking UI
- Unstructured code dumps — always organize into the 4-part output format above, even for small components
- Decorative icons that don't map to meaning
- Arbitrary spacing/sizing values that break the 8px grid
- Introducing a new color palette or component style that clashes with an existing, already-established design — always check for and match existing patterns first (see Workflow step 2)

## When Ambiguous

If you genuinely can't tell what the existing design looks like and the project already has UI elsewhere, ask the user for a screenshot before generating new components. Don't silently invent a style that might clash — this is the one thing worth pausing the workflow for.