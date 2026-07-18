# The Data Model

## What is it?
The **Data Model** is the underlying relational engine (introduced above in `Power-Pivot.md`) that stores multiple tables and the relationships between them, inside a single Excel workbook — the foundation that Power Pivot, and PivotTables built from "Add this to the Data Model," rely on.

## Why care?
Understanding the Data Model conceptually — not just clicking through the UI — is what lets you correctly design multi-table analyses instead of fighting confusing, wrong PivotTable results caused by bad relationships (a very common real-world debugging scenario for analysts).

## Key concepts

### Relationships
A relationship connects a column in one table to a matching column in another — almost always a "one-to-many" relationship (e.g., one row per `Product` in a Products table, but many matching rows in a Sales table).
```
Products (1) ────< (many) Sales
   ProductID              ProductID
```
The "1" side is called the **lookup table** (dimension table); the "many" side is the **fact table** (transactional data). This exact structure is the foundation of "star schema" data modeling — a concept used identically in Power BI, SQL data warehouses, and general BI/analytics work.

### Why direction matters
Relationships in Excel's Data Model filter in ONE direction by default: filtering the "1" side (Products) filters the connected "many" side (Sales), but not automatically the reverse — an important, commonly-confusing detail when your PivotTable results don't look right.

### Fact tables vs Dimension tables
- **Fact table**: the "many" side — transactional, event-level data (Sales, Orders, Clicks). Usually the largest table.
- **Dimension table**: the "1" side — descriptive attributes about an entity (Products, Customers, Dates). Usually smaller, used to slice/filter/group the fact table.

### The Date table (a special, very common dimension table)
Serious analysis over time (year-over-year comparisons, fiscal quarters, etc.) works much better with a **dedicated Date table** (a list of every date in your range, plus columns like Year, Month, Quarter, Weekday) related to your fact table's date column — rather than relying on the raw date field directly. This is standard practice in both Excel's Data Model and Power BI.

## Practical example
Designing the Data Model for a retail analysis: `Sales` (fact table, one row per transaction) relates to `Products` (dimension), `Stores` (dimension), and a `Date` table (dimension) — this exact "star schema" structure (one central fact table surrounded by dimension tables) is the industry-standard pattern for building any serious multi-table analysis, whether in Excel, Power BI, or a SQL data warehouse.
