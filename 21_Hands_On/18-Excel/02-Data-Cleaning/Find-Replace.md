# Find & Replace

## What is it?
A tool (and formula equivalent) to locate and swap out specific values across a sheet or workbook.

## Why care?
Fast, safe bulk corrections — fixing a misspelled category across 10,000 rows manually would take hours; Find & Replace takes seconds.

## Basic usage
```
Ctrl+H opens Find & Replace
Find what: "Nort"
Replace with: "North"
Replace All
```

## Useful options (click "Options >>")
- **Match case**: distinguishes `Apple` from `apple`.
- **Match entire cell contents**: only replaces if the ENTIRE cell equals your search term (prevents accidentally replacing a substring inside a longer word).
- **Within: Sheet vs Workbook**: control scope — be careful with Workbook scope, it affects every tab.
- **Wildcards** (`*` and `?`): `*` matches any number of characters, `?` matches exactly one.
```
Find: "Product*"     matches "Product A", "Product123", etc.
Find: "200?"          matches "2001", "2002", but not "20010"
```

## Finding formulas vs values
```
Options → Look in: Formulas    (searches the actual formula text, e.g. finds every cell referencing "Sheet2")
Options → Look in: Values         (searches the displayed/calculated result)
```

## Formula equivalent (when you need conditional/formula-based replace)
```excel
=SUBSTITUTE(A1, "old text", "new text")     ' replace within a formula, doesn't touch original data
```

## ⚠️ Golden rule before bulk replace
**Always work on a COPY of your data**, or use "Find All" first to preview matches before "Replace All" — an overly broad Find & Replace (e.g., replacing "CA" with "California" when "CA" appears inside unrelated words) is a classic way to silently corrupt a dataset.

## Practical example
A dataset has inconsistent region labels: "USA", "U.S.A.", "United States" all meaning the same thing. Standardize with 2 quick Find & Replace passes (`"U.S.A." → "USA"`, `"United States" → "USA"`) before doing any PivotTable analysis by region — otherwise your totals will be silently split across 3 separate categories.
