# Common Interview Questions — Excel for Data Analysts

Quick-fire theory questions with concise model answers, organized by topic.

## Formulas & Functions
**Q: What's the difference between VLOOKUP and XLOOKUP?**
A: XLOOKUP can search in any direction (VLOOKUP only searches rightward), doesn't break when columns are inserted (VLOOKUP's column-index argument does), defaults to exact match (safer than VLOOKUP's approximate-match default), and has built-in error handling via its `if_not_found` argument.

**Q: When would you use INDEX-MATCH instead of VLOOKUP?**
A: When you need to look leftward, when you want a formula resilient to inserted/deleted columns, or when working in an Excel version without XLOOKUP — INDEX-MATCH offers the same core benefits as XLOOKUP via an older, still-widely-used approach.

**Q: What's the difference between absolute and relative cell references?**
A: A relative reference (`A1`) shifts when copied to another cell; an absolute reference (`$A$1`) stays fixed. Mixed references (`$A1` or `A$1`) lock only the column or only the row.

**Q: How do you handle errors in a formula gracefully?**
A: Wrap it in `IFERROR` (catches any error type) or `IFNA` (catches only `#N/A` specifically, letting genuine bugs still surface) with a sensible fallback value.

## PivotTables
**Q: Walk me through building a PivotTable.**
A: Select the data (ideally as a Table), Insert → PivotTable, then drag fields into Rows/Columns/Values/Filters based on how you want to group and aggregate. Change aggregation type via Value Field Settings, group dates via right-click → Group.

**Q: Why doesn't my PivotTable update when I change the source data?**
A: PivotTables don't auto-refresh — you need to manually refresh (right-click → Refresh, or `Alt+F5`), or set it to refresh automatically on file open in PivotTable Options.

## Power Query / Power Pivot
**Q: What's the difference between Power Query and Power Pivot?**
A: Power Query handles getting and TRANSFORMING/cleaning data (ETL) before it enters your workbook. Power Pivot handles MODELING that data — building relationships between multiple tables and writing DAX measures for analysis. They're complementary, often used together.

**Q: What is a calculated column vs a measure in DAX?**
A: A calculated column is computed row-by-row and stored physically in the table. A measure is computed dynamically based on the current filter context of a PivotTable — the same measure gives different results depending on how the PivotTable is currently sliced.

## Data Cleaning
**Q: How would you clean a messy dataset with duplicate rows, inconsistent text casing, and mixed date formats?**
A: Use Power Query (or Remove Duplicates + TRIM/PROPER/UPPER functions + a consistent date type conversion) — explain you'd first inspect the data to understand what "messy" specifically means before applying fixes, rather than blindly running a cleaning script.

**Q: What's the difference between `TRIM` and `CLEAN`?**
A: `TRIM` removes extra spaces (leading, trailing, and multiple internal spaces down to single spaces). `CLEAN` removes non-printable characters (often from data copied from other systems/web sources) — worth combining both when cleaning messy imported text.

## Dashboards & Communication
**Q: How would you decide what chart type to use for a given dataset?**
A: Depends on the question: comparisons across categories → bar/column; trends over time → line; parts of a whole (few categories) → pie/donut; relationship between two numeric variables → scatter. Reference `05-Data-Visualization/Chart-Types.md` reasoning explicitly.

**Q: A stakeholder says your dashboard is "too cluttered." What would you do?**
A: Identify the single most important takeaway/KPI and make sure it's the most visually prominent element; remove any chart or number that doesn't directly support a decision; simplify color usage; ensure a consistent layout — walk through the principles in `Report-Design-Best-Practices.md`.

See `Case-Studies.md` for scenario-style, live-task-simulation questions.
