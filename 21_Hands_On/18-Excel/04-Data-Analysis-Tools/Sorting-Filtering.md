# Sorting & Filtering

## What is it?
Sorting reorders rows by one or more columns; filtering temporarily hides rows that don't meet criteria — both are non-destructive (the underlying data doesn't change).

## Why care?
Before you can spot trends or find outliers, you usually need to sort or narrow down a dataset. It's the first thing any analyst does when opening a new dataset — literally step one of exploratory analysis.

## Sorting
- Select your data → **Data → Sort**
- Sort by multiple columns: e.g., sort by `Region` then by `Sales` descending within each region — add multiple "Sort by" levels in the Sort dialog.
- `Ctrl+Shift+L` toggles filter arrows on/off (see below) — sorting is also accessible directly from those arrows.

## Filtering (AutoFilter)
- Select your data → **Data → Filter** (`Ctrl+Shift+L`)
- Click a column's dropdown arrow → check/uncheck values, or use **Text Filters** / **Number Filters** / **Date Filters** for conditions (contains, greater than, between, top 10, etc.)
- Filter by color/icon if you've applied conditional formatting.

## Advanced Filter (for complex, multi-condition criteria)
**Data → Advanced** lets you filter using a separate "criteria range" — useful for OR logic across multiple columns, which the standard AutoFilter dropdown can't easily do.

## Custom sort order (not alphabetical)
`Data → Sort → Order → Custom List` — useful for sorting things like `Low, Medium, High` in their logical order instead of alphabetically (which would give `High, Low, Medium`).

## Practical example
A sales dataset with 10,000 rows: filter to `Region = West` and `Date` in the last quarter, then sort by `Revenue` descending to quickly find your top West-region deals for the quarter — a completely routine analyst task, done in under 10 seconds once you know the shortcuts.
