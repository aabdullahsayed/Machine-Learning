# Formatting

## What is it?
Controlling how data LOOKS (number formats, colors, borders, fonts) without changing the underlying value.

## Why care?
Reports that look sloppy get less trust, even if the numbers are perfect. Professional formatting is a real, visible skill differentiator for analysts, and it also prevents misreading data (e.g., is that number a percentage or a raw decimal?).

## Number formatting (the most important kind)
```
Select cells → Ctrl+1 (Format Cells) → Number tab
```
| Format | Raw value | Displayed as |
|---|---|---|
| Currency | 1500 | $1,500.00 |
| Percentage | 0.15 | 15% |
| Comma/Number | 1500000 | 1,500,000 |
| Date | 46032 | 1/15/2026 |

**Key insight**: the underlying value never changes — only the display. `=A1*2` still works correctly on a cell formatted as currency, using its true numeric value underneath.

## Quick formatting shortcuts
| Shortcut | Action |
|---|---|
| `Ctrl+1` | Open Format Cells dialog |
| `Ctrl+Shift+1` | Apply number format (comma, 2 decimals) |
| `Ctrl+Shift+4` | Apply currency format |
| `Ctrl+Shift+5` | Apply percentage format |
| `Ctrl+B` / `Ctrl+I` / `Ctrl+U` | Bold / Italic / Underline |

## Conditional formatting (preview — full coverage in Folder 05)
`Home → Conditional Formatting → Highlight Cells Rules` — automatically colors cells based on their value (e.g., highlight all values > 1000 in green). Extremely useful for quickly spotting outliers/patterns in a report.

## Format Painter
Select a formatted cell, click the paintbrush icon (or `Ctrl+Shift+C` then `Ctrl+Shift+V` in some versions), then click another cell — copies ONLY the formatting, not the value.

## Practical example
A finance report with a "% Growth" column should be formatted as percentage (not raw decimals like `0.15`), and a "Revenue" column should use currency format with thousands separators — this single formatting choice is often the difference between a report that looks "analyst-built" vs "amateur."
