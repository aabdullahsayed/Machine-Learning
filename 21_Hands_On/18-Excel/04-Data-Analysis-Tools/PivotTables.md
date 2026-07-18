# PivotTables

## What is it?
A PivotTable summarizes large datasets by dragging fields into **Rows**, **Columns**, **Values**, and **Filters** — instantly producing sums, counts, averages, etc., grouped however you like, without writing a single formula.

## Why care?
**This is the single most important tool for a Data Analyst in Excel.** It's how you go from "10,000 raw transaction rows" to "total sales by region by month" in about 10 seconds. If you learn only one thing from this entire roadmap, make it PivotTables.

## Creating one
1. Click anywhere inside your data → **Insert → PivotTable**
2. Confirm the data range and where to place the PivotTable (new worksheet recommended).
3. In the PivotTable Fields pane, drag fields into:
   - **Rows**: categories to group by (e.g., Region)
   - **Columns**: a second grouping dimension (e.g., Year)
   - **Values**: what to aggregate (e.g., Sum of Sales)
   - **Filters**: fields to filter the whole table by (e.g., only show Product = "Widget")

## Changing the aggregation
By default, numeric fields sum; text fields count. Click the field in **Values → Value Field Settings** to change to Average, Count, Max, Min, % of Total, etc.

## Grouping (dates, numbers)
Right-click a date field in Rows → **Group** → group by Month/Quarter/Year automatically — extremely useful for turning daily transaction data into monthly/quarterly summaries without any formulas.

## Calculated Fields
**PivotTable Analyze → Fields, Items & Sets → Calculated Field** — add a new computed field (e.g., `Profit = Revenue - Cost`) directly inside the PivotTable, without modifying your source data.

## Refreshing
If your source data changes, the PivotTable does NOT auto-update — right-click → **Refresh** (or `Alt+F5`), or set it to auto-refresh on file open in PivotTable Options.

## Practical example
Raw data: 50,000 rows of individual retail transactions (Date, Region, Product, Salesperson, Amount). A 2-minute PivotTable answers: "What was total revenue by region, by quarter, filtered to just the Electronics category?" — a query that would take a SQL analyst a `GROUP BY` + `WHERE` clause, done here by dragging 3 fields.
