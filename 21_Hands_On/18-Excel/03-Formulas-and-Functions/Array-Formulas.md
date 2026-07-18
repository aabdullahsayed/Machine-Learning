# Array Formulas & Dynamic Arrays

## What is it?
Formulas that operate on and return MULTIPLE values at once (an "array"), instead of a single cell result — modern Excel (365) makes this dramatically easier via "dynamic arrays" that automatically "spill" results into neighboring cells.

## Why care?
Array formulas let you solve problems that would otherwise require complex multi-step helper columns, and dynamic arrays (365) have made many advanced techniques far more accessible than the older `Ctrl+Shift+Enter` era.

## Legacy array formulas (older Excel, `Ctrl+Shift+Enter`)
```excel
{=SUM(IF(B2:B100="West", C2:C100))}     ' entered with Ctrl+Shift+Enter, shown with {} braces
```
This is functionally similar to `SUMIF(B2:B100,"West",C2:C100)` but shows the general pattern: array formulas can apply a condition and calculation across a whole range in one formula, without a helper column.

## Modern dynamic arrays (Excel 365 — no Ctrl+Shift+Enter needed)
```excel
=UNIQUE(A2:A100)                    ' spills a list of unique values automatically
=SORT(A2:A100)                        ' spills a sorted list
=FILTER(A2:C100, B2:B100="West")        ' spills only rows matching a condition
=SEQUENCE(10)                              ' spills numbers 1 through 10
=SORT(FILTER(A2:C100, B2:B100="West"))       ' functions can be nested together
```
These automatically "spill" into as many cells as needed — if the source data grows, the formula automatically expands to cover it, no manual dragging required.

## FILTER — a genuinely transformative function for analysts
```excel
=FILTER(A2:D100, (B2:B100="West")*(C2:C100>1000))
```
Returns every row where BOTH conditions are true (multiply conditions together for AND logic, add them for OR logic) — replaces what used to require a full AutoFilter + copy-paste workflow with a single, live-updating formula.

## Referencing a spilled array (the `#` operator)
```excel
=SUM(A2#)      ' sums the entire spilled range starting at A2, wherever it currently extends to
```
The `#` ("spill reference") automatically adjusts if the array grows or shrinks — extremely useful for building formulas that reference dynamic array outputs safely.

## Practical example
Building a live "Top 10 customers by revenue" list that automatically updates as new sales data comes in:
```excel
=SORT(UNIQUE(CustomerRevenueTable), 2, -1)     ' unique customers, sorted by revenue (col 2) descending
```
No PivotTable refresh needed — this dynamic array formula recalculates live whenever the source data changes, spilling the updated ranked list automatically.
