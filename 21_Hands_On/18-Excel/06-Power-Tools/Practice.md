# Practice — Power Tools

1. Take a messy CSV (inconsistent headers, extra blank rows, a combined "Full Name" column) — build a Power Query pipeline that: removes blanks, fixes column types, and splits the name column. Load the result as a Table.
2. Create 3 small related tables (Sales, Products, Customers, as in `Data-Model.md`'s example) and add all 3 to the Data Model.
3. Build relationships between them in Power Pivot's Diagram View.
4. Build a PivotTable from the Data Model, pulling fields from all 3 tables into one unified view.
5. Write a basic DAX measure: `Total Revenue = SUM(Sales[Revenue])`.
6. Write a `CALCULATE`-based measure: revenue filtered to one specific region, shown as a separate column regardless of the PivotTable's own filter/slicer state.
7. Build a simple Date table and create a `YoY Growth %` measure using `SAMEPERIODLASTYEAR`.
8. Refresh your Power Query source data (change a value in the original CSV) and confirm the entire pipeline + PivotTable updates with one click.

✅ Done? Move to `07-Advanced-Excel`.
