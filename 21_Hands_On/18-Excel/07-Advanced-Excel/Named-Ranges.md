# Named Ranges

## What is it?
Assigning a memorable name (e.g., `TaxRate`, `SalesData`) to a specific cell or range, instead of referring to it by its raw cell reference (`$B$2`, `A2:D500`).

## Why care?
Named ranges make formulas dramatically more readable, reduce reference errors when copying formulas, and (via dynamic named ranges) can automatically expand as new data is added — a small habit that pays off constantly in larger, shared workbooks.

## Creating a named range
- Select a cell/range → type a name directly into the **Name Box** (top-left, next to the formula bar) → Enter.
- Or: **Formulas → Define Name** for more control (including scope: workbook-wide vs. specific worksheet only).

## Using it in formulas
```excel
=SUM(SalesData)              -- instead of =SUM(A2:A500)
=B2*TaxRate                    -- instead of =B2*$D$1, and self-documenting what D1 actually represents
```

## Named ranges vs. Excel Tables (a related, often-better alternative)
Converting a range to an **Excel Table** (`Ctrl+T`) gives you automatic "structured references" that behave similarly to named ranges but auto-expand as rows are added, without any manual setup:
```excel
=SUM(Sales[Revenue])          -- automatically includes new rows added to the "Sales" table
```
**For most tabular data, prefer converting to a Table over manually creating named ranges** — Tables give you this auto-expansion behavior "for free," plus automatic formatting and easier PivotTable/chart integration.

## Dynamic named ranges (for non-Table use cases)
Using `OFFSET` or `INDEX` inside a name's definition to make it automatically resize as data grows:
```excel
=OFFSET(Sheet1!$A$2, 0, 0, COUNTA(Sheet1!$A:$A)-1, 1)
```
More fragile and less commonly needed now that Tables handle most of these use cases more robustly — good to recognize in legacy workbooks, but Tables are the modern best practice.

## Practical example
A financial model with named ranges `TaxRate`, `DiscountRate`, `GrowthAssumption` at the top of the sheet — every formula throughout the model references these by name (`=Revenue*(1+GrowthAssumption)`), making the model dramatically easier to audit and update (change the assumption once, in one clearly-labeled cell, instead of hunting for every hardcoded `0.05` scattered through dozens of formulas).
