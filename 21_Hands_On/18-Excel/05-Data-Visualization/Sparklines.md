# Sparklines

## What is it?
A **sparkline** is a tiny, in-cell chart — showing a trend for a single row of data (e.g., 12 months of revenue) compressed into the space of one cell, right next to the numbers it represents.

## Why care?
Sparklines let you show a trend for EVERY row in a table (e.g., every product's 12-month trend) without needing 50 separate full-sized charts — extremely space-efficient for tabular reports.

## Creating sparklines
1. Select the cell where you want the sparkline to appear.
2. **Insert → Sparklines** → choose Line, Column, or Win/Loss.
3. Select the **Data Range** (e.g., a row of 12 monthly values) and the **Location Range** (the cell to place it in).

## Types
- **Line**: best for showing a trend's shape/direction over time.
- **Column**: best when comparing discrete period-over-period magnitude (like a mini bar chart).
- **Win/Loss**: shows only whether each period was positive or negative — good for showing streaks (e.g., which months hit target vs missed).

## Customizing
**Sparkline Tools → Design tab**: change color, add markers for high/low points, show first/last point highlighted — useful for immediately drawing attention to the peak or the most recent value.

## Practical example
A table listing 30 products as rows, with columns for `Product Name`, `Total Revenue`, and a **Sparkline column** showing each product's 12-month revenue trend as a tiny line — a manager can scan down the sparkline column and instantly spot which products are trending up vs declining, without needing 30 separate charts cluttering the report.
