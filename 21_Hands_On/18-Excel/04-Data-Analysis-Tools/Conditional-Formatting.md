# Conditional Formatting

## What is it?
Automatically applying formatting (colors, icons, bars) to cells based on their values or a custom rule — lets patterns jump out visually instead of requiring manual scanning.

## Why care?
A well-placed conditional format turns a wall of numbers into an instantly-readable heatmap — a skill that separates "someone who uses Excel" from "someone who communicates data effectively" with Excel.

## Built-in options (Home → Conditional Formatting)
- **Highlight Cell Rules**: greater than, less than, between, duplicate values, text containing...
- **Top/Bottom Rules**: top 10 items, top 10%, above average...
- **Data Bars**: an in-cell bar proportional to the value — great for quick magnitude comparison down a column.
- **Color Scales**: a gradient (e.g., red = low, green = high) — a quick "heatmap" over a range.
- **Icon Sets**: arrows/traffic lights/stars based on value thresholds.

## Custom rules with formulas (the powerful option)
**Conditional Formatting → New Rule → "Use a formula to determine which cells to format"** — lets you build ANY logic.

Example: highlight an entire row if the `Status` column (say, column D) says "Overdue":
```
=$D2="Overdue"
```
Applied to the whole row's range, with the `$` locking column D but letting the row reference shift — a very common analyst pattern for "highlight the whole record, not just one cell."

## Practical example
A project tracker: use a formula rule `=AND($C2<TODAY(), $D2<>"Done")` to highlight overdue, unfinished tasks in red automatically — the sheet self-updates every day without manual re-checking.

## Managing rules
**Conditional Formatting → Manage Rules** — lets you edit, reorder (rules apply top-down, and "Stop If True" can be checked to prevent lower rules from also applying), or delete existing rules. Worth checking here if formatting looks wrong — often it's a rule-order conflict, not a formula bug.
