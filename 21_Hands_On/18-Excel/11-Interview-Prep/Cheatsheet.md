# Excel Cheat Sheet — Data Analyst Quick Reference

## Lookup functions
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
=VLOOKUP(lookup_value, table, col_index, FALSE)
```

## Logical functions
```excel
=IF(condition, value_if_true, value_if_false)
=IFS(cond1, val1, cond2, val2, ..., TRUE, default)
=AND(cond1, cond2)  /  =OR(cond1, cond2)
=IFERROR(formula, fallback)  /  =IFNA(formula, fallback)
```

## Aggregate & conditional aggregate functions
```excel
=SUM(range)  /  =SUMIF(range, criteria, sum_range)  /  =SUMIFS(sum_range, crit_range1, crit1, ...)
=COUNTIF(range, criteria)  /  =COUNTIFS(...)
=AVERAGEIF(range, criteria, avg_range)
```

## Text functions
```excel
=TRIM(text)          -- remove extra spaces
=CONCAT(a, b)  or  =a&b     -- combine text
=LEFT(text,n) / RIGHT(text,n) / MID(text,start,n)
=TEXTSPLIT(text, delimiter)   -- dynamic array split (modern Excel)
=PROPER(text) / UPPER(text) / LOWER(text)
```

## Date functions
```excel
=TODAY()  /  =NOW()
=DATEDIF(start, end, "Y")     -- years between dates
=EOMONTH(date, 0)               -- last day of the month
=WORKDAY(start, days)             -- add business days
```

## Dynamic arrays (Excel 365)
```excel
=UNIQUE(range)
=SORT(range)
=FILTER(range, condition)
```

## PivotTable quick reference
```
Insert → PivotTable → drag fields into Rows/Columns/Values/Filters
Right-click a date field → Group (Month/Quarter/Year)
Value Field Settings → change aggregation (Sum/Average/Count/% of Total)
Alt+F5 → Refresh
```

## Power Query / Power Pivot
```
Data → Get Data → choose source → Power Query Editor → transform → Close & Load
Power Pivot → Add to Data Model → Diagram View → create relationships
DAX measure: Total Revenue = SUM(Sales[Revenue])
DAX with filter override: CALCULATE(SUM(Sales[Revenue]), Sales[Region]="West")
```

## Shortcuts
```
Ctrl+T          Convert range to Table
Ctrl+Shift+L     Toggle filters
Alt+F11           Open VBA Editor
Alt+F5             Refresh PivotTable
Ctrl+1              Format Cells
F4                    Toggle absolute/relative reference while editing a formula
Ctrl+Arrow             Jump to edge of data region
```

## Golden interview one-liners
- "XLOOKUP over VLOOKUP: any-direction search, resilient to inserted columns, safer exact-match default."
- "Power Query cleans and reshapes; Power Pivot models relationships and calculates via DAX."
- "A measure recalculates dynamically based on filter context; a calculated column is fixed per row."
- "Correlation isn't causation — always sanity-check a statistical relationship against real business logic."
- "Separate raw data, calculations, and the presentation dashboard into different sheets — never mix them."
