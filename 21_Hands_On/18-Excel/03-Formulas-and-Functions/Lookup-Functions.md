# Lookup Functions (VLOOKUP, INDEX-MATCH, XLOOKUP)

## What is it?
Functions to find and retrieve data from another table/range based on a matching value — arguably THE most important skill category for a Data Analyst.

## Why care?
Joining/merging data from different sources or tabs (e.g., matching a Product ID to its Price from a separate lookup table) is one of the most common real-world analyst tasks. Interviewers test this heavily.

## VLOOKUP — the classic (still widely used, know it even if better alternatives exist)
```excel
=VLOOKUP(lookup_value, table_array, col_index_num, range_lookup)
=VLOOKUP(A2, ProductTable, 3, FALSE)
```
- `A2`: the value you're searching for
- `ProductTable`: the range/table to search in (lookup value must be in its FIRST column)
- `3`: which column to return, counting from the left of the table (1 = first column)
- `FALSE`: exact match (ALWAYS use FALSE unless you specifically need approximate matching)

**Key limitation**: VLOOKUP can only look **rightward** — the column you're searching must be to the LEFT of the column you want to return. This is its biggest weakness.

## INDEX-MATCH — the classic, more flexible alternative
```excel
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
=INDEX(PriceColumn, MATCH(A2, ProductIDColumn, 0))
```
- `MATCH(A2, ProductIDColumn, 0)`: finds the ROW POSITION of A2 within ProductIDColumn (0 = exact match)
- `INDEX(PriceColumn, that_row_position)`: returns the value at that row position from PriceColumn

**Why it's better than VLOOKUP**: works in ANY direction (can look leftward), doesn't break if columns are inserted/reordered within the table (since you reference the lookup and return columns separately, not a fixed column-index-number), and is generally faster on large datasets.

## XLOOKUP — the modern replacement (Excel 365 / 2021+)
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])
=XLOOKUP(A2, ProductIDColumn, PriceColumn, "Not Found")
```
Combines the simplicity of VLOOKUP with the flexibility of INDEX-MATCH: works leftward or rightward, has a clean built-in "not found" fallback (no need to wrap in `IFERROR`), and can return multiple columns at once. **This is the recommended default for any modern Excel version that supports it.**

## Multi-criteria lookup (matching on more than one column)
```excel
' INDEX-MATCH with an array formula (matches on Region AND Product together)
=INDEX(PriceColumn, MATCH(1, (A2=RegionColumn)*(B2=ProductColumn), 0))
' (enter with Ctrl+Shift+Enter in older Excel, or just Enter in 365)

' XLOOKUP equivalent, cleaner:
=XLOOKUP(1, (A2=RegionColumn)*(B2=ProductColumn), PriceColumn)
```

## Quick comparison
| | VLOOKUP | INDEX-MATCH | XLOOKUP |
|---|---|---|---|
| Direction | Rightward only | Any direction | Any direction |
| Column insert safety | Breaks (fixed column index) | Safe | Safe |
| Error handling | Needs `IFERROR` wrap | Needs `IFERROR` wrap | Built-in `if_not_found` |
| Availability | All versions | All versions | 365/2021+ only |

## Practical example
Merging a "Sales" table (with just Product IDs) against a "Product Catalog" table (with Product ID, Name, Category, Price) to pull in the product name and category for every sale:
```excel
=XLOOKUP(A2, ProductCatalog[ProductID], ProductCatalog[ProductName], "Unknown Product")
```
This single pattern — looking up a reference table by ID — appears in nearly every real-world Excel analysis task you'll encounter as a Data Analyst.
