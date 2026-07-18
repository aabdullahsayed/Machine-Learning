# Power Query

## What is it?
Power Query is Excel's built-in **ETL tool** (Extract, Transform, Load) — it connects to data sources (Excel files, CSVs, databases, web pages, folders of files), lets you clean/reshape the data through a recorded series of steps, and loads the result into your workbook.

## Why care?
This is the single biggest upgrade from "someone who uses Excel formulas" to "a real data analyst." It replaces messy, error-prone manual cleaning (and fragile formulas) with a **repeatable, auditable, refreshable** transformation pipeline — the same skillset that underlies real ETL/data engineering work, just with a visual interface.

## Accessing it
**Data → Get Data** (or "Get & Transform Data" group) → choose a source: From File (Excel/CSV/Text), From Database, From Web, From Folder, etc.

## The core workflow
1. **Connect** to a data source.
2. In the **Power Query Editor**, apply transformation steps: remove columns, filter rows, split columns, change data types, merge/append other queries, group and aggregate, pivot/unpivot, etc.
3. Every step is recorded in the **Applied Steps** panel (on the right) — fully visual, and each step can be edited, reordered, or deleted.
4. Click **Close & Load** to bring the cleaned result into your workbook as a Table (or directly into the Data Model — see `Data-Model.md`).

## Why "refreshable" matters so much
Once built, if your source data changes (new month's CSV export, updated database), you just click **Refresh** — Power Query re-runs every single transformation step automatically on the new data. This turns a one-time manual cleaning chore into a **reusable pipeline** — build it once, refresh forever.

## Common transformations
```
Remove Columns          — drop unneeded fields
Filter Rows              — keep only rows matching a condition
Split Column              — e.g., split "First Last" into two columns by delimiter
Change Type                — ensure dates/numbers are the correct data type (critical for correct calculations downstream)
Group By                    — aggregate (like a mini PivotTable, but as a repeatable step)
Merge Queries                 — like a SQL JOIN, combine two tables based on a matching column
Append Queries                  — like a SQL UNION, stack multiple tables with the same columns
Unpivot Columns                   — turn wide data (many date columns) into long/tidy format (one date column, one value column) — extremely useful, and something formulas alone struggle to do well
```

## Practical example
Every month, you receive a new CSV export of transactions with inconsistent column headers and a few dirty rows. Instead of manually cleaning it each time, build ONE Power Query pipeline: connect to the file, remove blank rows, fix column types, split a combined "Name" column, filter out test/void transactions — then next month, just point it at the new file (or drop it in the same folder path) and click Refresh. Minutes of manual work become a single click.
