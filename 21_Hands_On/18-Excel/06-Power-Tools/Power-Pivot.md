# Power Pivot

## What is it?
Power Pivot is Excel's add-in for building a **Data Model** — letting you work with MULTIPLE related tables (like a mini relational database) inside Excel, create relationships between them, and build PivotTables that pull from all of them together, without ever needing a single `VLOOKUP` to merge them first.

## Why care?
Regular PivotTables need all your data flattened into ONE table. Real business data usually lives in several related tables (Sales, Products, Customers, Regions) — Power Pivot lets you analyze them together properly, the way a real database/BI tool would, directly inside Excel.

## Enabling it
**File → Options → Add-ins → Manage: COM Add-ins → Go → check "Microsoft Power Pivot for Excel"**. Then find it as a new **Power Pivot** tab in the ribbon.

## Core workflow
1. **Add tables to the Data Model**: select a table → **Power Pivot → Add to Data Model** (or load data via Power Query directly into the Data Model instead of a worksheet).
2. **Create relationships**: in the Power Pivot window, **Diagram View** lets you drag a connection between matching columns across tables (e.g., `Sales[ProductID]` → `Products[ProductID]`) — just like a foreign key relationship in a real database.
3. **Build measures with DAX** (see `DAX-Basics.md`) — custom calculations that work correctly across the related tables.
4. **Build a PivotTable from the Data Model**: Insert → PivotTable → "Use this workbook's Data Model" — now you can drag fields from ANY connected table into one unified PivotTable.

## Why this beats VLOOKUP-ing everything into one giant table
- **Performance**: Power Pivot's engine (the same "xVelocity"/VertiPaq engine used in Power BI) is built to handle millions of rows efficiently — far beyond what formula-heavy flat tables can handle without massive slowdown.
- **Data integrity**: relationships are defined once, cleanly — no risk of a broken VLOOKUP formula silently pulling wrong data after a sort/insert.
- **This is literally the same skillset as Power BI** — if you learn Power Pivot's data modeling + DAX, transitioning to Power BI (a very common next step in a Data Analyst's toolkit) is much easier, since the underlying engine and language are the same.

## Practical example
Three tables: `Sales` (transaction-level, with ProductID and CustomerID), `Products` (ProductID, Category, Price), `Customers` (CustomerID, Region, Signup Date). Load all three into the Data Model, create relationships, then build ONE PivotTable showing "Total Sales by Product Category by Customer Region" — a query that would otherwise require several VLOOKUP columns bolted onto your raw Sales table just to get there.
