# Combo Charts

## What is it?
A single chart combining two or more chart types (e.g., columns + a line) — typically used when you want to show two related metrics with different units or scales together.

## Why care?
Real business questions often involve two related-but-different metrics (e.g., "Revenue" in dollars and "Growth %" as a percentage) — a combo chart tells that combined story in one visual instead of forcing the viewer to cross-reference two separate charts.

## Creating a combo chart
1. Select your data (e.g., Month, Revenue, Growth %).
2. **Insert → Charts → Combo Chart** (or "Insert Combo Chart" icon).
3. Excel lets you assign a different chart type PER SERIES: e.g., Revenue as Clustered Column, Growth % as Line.
4. Critically: put Growth % on a **Secondary Axis** (checkbox in the combo chart setup) since its scale (percentages, small numbers) is wildly different from Revenue (large dollar amounts) — without this, the smaller series would look flat/invisible next to the larger one.

## Common combo chart patterns
- **Bar + Line**: actuals (bars) vs. target/trend line (line) — instantly shows performance against a benchmark.
- **Column + Line with secondary axis**: volume (bars, left axis) vs. price/rate (line, right axis).
- **Stacked column + line**: category breakdown (stacked bars) with a total/trend overlay (line).

## Practical example
A monthly sales report showing **Revenue** (columns, left axis, in dollars) and **Number of Transactions** (line, right axis, a count) on the same chart — reveals whether revenue growth is driven by more transactions or bigger average deal sizes, a genuinely useful business insight that two separate charts would make harder to see at a glance.
