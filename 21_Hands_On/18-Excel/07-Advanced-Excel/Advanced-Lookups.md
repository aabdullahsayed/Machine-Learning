# Advanced Lookups (XLOOKUP, INDEX-MATCH, Dynamic Arrays)

## What is it?
Beyond basic VLOOKUP (`03-Formulas-and-Functions/Lookup-Functions.md`), modern Excel offers more powerful, flexible lookup tools — XLOOKUP and INDEX-MATCH — that fix VLOOKUP's real limitations, plus dynamic array functions that spill results across multiple cells automatically.

## Why care?
VLOOKUP is fragile (breaks if columns are inserted, can't look leftward, defaults to approximate match if you forget the 4th argument). Professional analysts default to XLOOKUP (or INDEX-MATCH in older files/shared templates) for reliability.

## XLOOKUP — the modern default (Excel 365 / 2021+)
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
```
Advantages over VLOOKUP:
- Can look in **any direction** (left or right of the lookup column) — VLOOKUP can only look rightward.
- Doesn't break if columns are inserted/deleted between the lookup and return columns (VLOOKUP's column-index-number argument does break).
- Built-in `[if_not_found]` argument avoids needing to wrap in `IFERROR`.
- Defaults to **exact match** (safer default than VLOOKUP's approximate-match default).
```excel
=XLOOKUP(A2, Products[ProductID], Products[Price], "Not Found")
```

## INDEX-MATCH — the classic, still-relevant alternative
```excel
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
```
Same benefits as XLOOKUP (look in any direction, resilient to inserted columns) — worth knowing because many companies still use older Excel versions without XLOOKUP, and INDEX-MATCH remains extremely common in existing templates/interview questions.
```excel
=INDEX(Products[Price], MATCH(A2, Products[ProductID], 0))
```

## Dynamic Arrays (Excel 365) — functions that "spill"
Modern Excel functions can return MULTIPLE values that automatically "spill" into neighboring cells, without needing to copy-paste a formula down:
```excel
=UNIQUE(A2:A100)               -- list of unique values, spills down automatically
=SORT(UNIQUE(A2:A100))          -- unique values, sorted
=FILTER(A2:D100, C2:C100="West")  -- all rows matching a condition, spills as a full block
```
These fundamentally change how you build formulas — instead of one formula per cell copied down, ONE formula can produce an entire dynamic result range that automatically resizes as source data changes.

## Practical example
A dashboard needs a live, always-current list of unique product categories for a dropdown: `=SORT(UNIQUE(Sales[Category]))` — this single formula spills a sorted, de-duplicated list that automatically updates whenever new categories appear in the source data, replacing what used to require manual list maintenance or a much clunkier formula.
