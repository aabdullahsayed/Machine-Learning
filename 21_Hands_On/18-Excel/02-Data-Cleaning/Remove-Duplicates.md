# Removing Duplicates

## What is it?
Identifying and eliminating repeated rows/values in a dataset — a fundamental data-quality step before analysis.

## Why care?
Duplicate rows silently inflate totals, averages, and counts — one of the most common causes of "why don't my numbers match the source system" issues in real analyst work.

## Built-in Remove Duplicates tool
```
Select your data range → Data tab → Remove Duplicates
→ choose which columns define a "duplicate" → OK
```
Excel tells you how many duplicate rows were removed and how many unique rows remain.

**Important**: this PERMANENTLY deletes rows. Always work on a copy, or use a formula-based approach first to review what would be removed.

## Formula-based duplicate detection (safer — review before deleting)
```excel
=COUNTIF(A:A, A2) > 1              ' TRUE if this value appears more than once in column A
=COUNTIFS(A:A, A2, B:B, B2) > 1      ' TRUE if this combination of columns A+B is duplicated
```
Add this as a helper column, filter to `TRUE`, review, THEN decide whether to delete.

## Highlighting duplicates without deleting (visual review)
```
Home → Conditional Formatting → Highlight Cells Rules → Duplicate Values
```
Great first step — see duplicates highlighted in the sheet before committing to any deletion.

## Modern approach: UNIQUE() function (Excel 365, non-destructive)
```excel
=UNIQUE(A2:A100)          ' spills a list of unique values, doesn't touch original data
=UNIQUE(A2:B100)            ' unique COMBINATIONS across multiple columns
```
This is often preferred over "Remove Duplicates" in modern workflows because it doesn't destroy your original data — you get a clean list in a new range while keeping the raw data intact for audit purposes.

## Practical example
An email list exported from 3 different marketing campaigns has overlapping subscribers. Before calculating "total unique subscribers reached":
```excel
=COUNTA(UNIQUE(A2:A5000))      ' correct unique count
=COUNTA(A2:A5000)                ' WRONG — counts duplicates too, inflates the true reach number
```
