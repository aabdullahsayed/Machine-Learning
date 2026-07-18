# Practice — Data Analysis Tools

1. Download or create a sample sales dataset (Date, Region, Product, Salesperson, Revenue — at least 200 rows; you can generate this quickly with `=RANDBETWEEN()` formulas).
2. Sort it by Region, then by Revenue descending within each region.
3. Apply a filter to show only `Region = "West"` and `Revenue > 5000`.
4. Add conditional formatting: a color scale on the Revenue column, plus a formula-based rule highlighting entire rows where Revenue is below 1000.
5. Build a PivotTable: `Sum of Revenue` by `Region` (rows) and `Month` (columns, grouped from the Date field).
6. Build a PivotChart from that PivotTable — a clustered column chart comparing regions across months.
7. Use Goal Seek: find what average deal size you'd need (by changing an assumption cell) to hit a target total revenue.
8. If you have Solver enabled: set up a simple budget allocation problem (3 channels, different returns, a total budget constraint) and let Solver optimize it.

✅ Done? Move to `05-Data-Visualization`.
