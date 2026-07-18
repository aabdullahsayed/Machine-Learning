# DAX Basics (Data Analysis Expressions)

## What is it?
**DAX** is the formula language used inside Power Pivot (and Power BI) to create **calculated columns** and **measures** — think of it as "Excel formulas, but aware of the Data Model's tables and relationships."

## Why care?
Regular Excel formulas operate cell-by-cell. DAX measures operate on the CURRENT FILTER CONTEXT of a PivotTable — meaning one single DAX formula automatically recalculates correctly no matter how a user slices/filters the PivotTable. This is a fundamentally different (and much more powerful) way of thinking about calculations, and it's the same language/skillset used in Power BI.

## Calculated Columns vs Measures
- **Calculated Column**: computed row-by-row, stored physically in the table (like an Excel formula column) — e.g., `Profit = Sales[Revenue] - Sales[Cost]`.
- **Measure**: computed dynamically, on-the-fly, based on whatever's currently in the PivotTable (filters, rows, columns) — e.g., `Total Revenue = SUM(Sales[Revenue])`. Measures are the more commonly used, more powerful tool for real analysis.

## Common DAX functions
```
SUM(Sales[Revenue])                          -- total of a column
AVERAGE(Sales[Revenue])                        -- average
COUNTROWS(Sales)                                -- row count
DISTINCTCOUNT(Sales[CustomerID])                  -- unique count

CALCULATE(SUM(Sales[Revenue]), Sales[Region]="West")   -- SUM with an override filter — THE most important DAX function
```

## `CALCULATE` — the most important DAX function to understand
`CALCULATE` lets you evaluate an expression under a MODIFIED filter context — this is how you build things like "% of total," "same period last year," or "West region revenue, shown as a separate column even when the PivotTable is sliced by all regions."
```
West Revenue = CALCULATE(SUM(Sales[Revenue]), Sales[Region] = "West")
```

## Time intelligence (a major reason to use DAX at all)
```
YTD Revenue = TOTALYTD(SUM(Sales[Revenue]), 'Date'[Date])
Prior Year Revenue = CALCULATE(SUM(Sales[Revenue]), SAMEPERIODLASTYEAR('Date'[Date]))
YoY Growth % = DIVIDE([Total Revenue] - [Prior Year Revenue], [Prior Year Revenue])
```
These "time intelligence" functions (which require a proper Date table — see `Data-Model.md`) make year-over-year, quarter-over-quarter, and running-total calculations dramatically simpler than trying to replicate them with plain Excel formulas.

## Practical example
A single measure, `YoY Growth % = DIVIDE([Total Revenue] - [Prior Year Revenue], [Prior Year Revenue])`, dropped into a PivotTable — as a user slices by Region, Product, or Month, this ONE measure automatically recalculates the correct year-over-year growth for whatever slice they're viewing, with zero additional formulas needed. This dynamic, context-aware recalculation is the core reason DAX/Power Pivot is a major step up from flat-table Excel formulas for serious analysis.
