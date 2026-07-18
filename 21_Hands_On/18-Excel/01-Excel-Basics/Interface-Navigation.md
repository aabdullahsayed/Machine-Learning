# Excel Interface & Navigation

## What is it?
Understanding the ribbon, worksheets, workbooks, and how to move around efficiently — the foundation before touching a single formula.

## Why care?
Analysts who fumble around the interface waste real time daily. Fast navigation is a genuine productivity multiplier once you're working with large datasets.

## Key concepts
- **Workbook**: the entire Excel file (`.xlsx`).
- **Worksheet (sheet/tab)**: one page within a workbook — you can have many.
- **Cell**: intersection of a column (letter) and row (number), e.g. `B7`.
- **Ribbon**: the toolbar at top — Home, Insert, Page Layout, Formulas, Data, Review, View.
- **Name Box**: top-left, shows/lets you jump to a cell or named range.
- **Formula Bar**: shows the actual formula/content of the selected cell.

## Essential navigation shortcuts
| Shortcut | Action |
|---|---|
| `Ctrl + Arrow key` | Jump to edge of data region |
| `Ctrl + Home` | Go to A1 |
| `Ctrl + End` | Go to last used cell |
| `Ctrl + Page Up/Down` | Switch between sheets |
| `Ctrl + F` | Find |
| `Ctrl + G` (or `F5`) | Go To (jump to a specific cell/range) |
| `Ctrl + Shift + End` | Select from current cell to last used cell |
| `Ctrl + Space` | Select entire column |
| `Shift + Space` | Select entire row |
| `Alt + =` | AutoSum |
| `Ctrl + \`` (backtick) | Toggle formula view (see actual formulas, not results) |

## Freeze Panes (essential for large datasets)
`View → Freeze Panes → Freeze Top Row` — keeps header row visible while scrolling through thousands of rows. Real analysts use this constantly.

## Practical example
Opening a 50,000-row sales dataset: `Ctrl+Home` to get to the top, `View → Freeze Top Row` to lock headers, then `Ctrl+Shift+End` to select all your data at once for formatting or a PivotTable source range.
