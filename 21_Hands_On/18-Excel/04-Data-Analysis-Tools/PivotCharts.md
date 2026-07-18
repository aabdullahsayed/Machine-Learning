# PivotCharts

## What is it?
A chart directly linked to a PivotTable — as you change the PivotTable's fields/filters, the chart updates automatically. It's the visual counterpart to a PivotTable.

## Why care?
Stakeholders rarely want to read a table of numbers — a PivotChart turns your PivotTable summary into an instantly digestible visual, and because it's linked, it stays accurate as underlying data changes (no manually re-drawing charts every reporting period).

## Creating one
- From an existing PivotTable: **PivotTable Analyze → PivotChart**, choose a chart type.
- Or directly from raw data: **Insert → PivotChart** (creates the PivotTable and chart together).

## Interacting with it
A PivotChart includes built-in **field buttons** (dropdown filters directly on the chart) — viewers can filter the chart interactively without touching the underlying PivotTable, useful for interactive reports.

## Best practices
- Keep it simple: bar/column charts for comparisons, line charts for trends over time — avoid 3D or overly decorated chart types (they distort perception of the data, a common data-viz mistake).
- Sort the PivotTable data before charting (e.g., descending by value) so the chart tells a clear story instead of showing bars in an arbitrary order.
- Combine with **Slicers** (see `05-Data-Visualization/Slicers-Timelines.md`) for an interactive filtering experience nicer than the default field-button dropdowns.

## Practical example
A monthly sales report: PivotTable summarizing `Sum of Revenue by Month`, with a linked PivotChart as a line graph — every month, refresh the PivotTable with new data, and the chart updates instantly, ready to paste into a stakeholder email or slide deck.
