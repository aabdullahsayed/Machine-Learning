# Excel Data Types

## What is it?
Excel treats data differently depending on its type: numbers, text, dates, booleans, errors — and this affects how formulas, sorting, and formatting behave.

## Why care?
The #1 source of "why isn't my formula working" bugs for beginners is a data-type mismatch (e.g., a number stored as text, or a date that's actually just a text string that looks like a date).

## Core data types
| Type | Example | Notes |
|---|---|---|
| **Number** | `42`, `3.14`, `-7` | Right-aligned by default |
| **Text** | `"Hello"`, `"A123"` | Left-aligned by default |
| **Date/Time** | `1/15/2026` | Actually stored internally as a serial number (days since Jan 1, 1900) |
| **Boolean** | `TRUE`, `FALSE` | Used in logical formulas |
| **Error** | `#N/A`, `#DIV/0!`, `#VALUE!` | See `Handling-Errors.md` in Folder 02 |

## The "number stored as text" trap
```
If a cell shows a green triangle in the top-left corner and the number
is left-aligned instead of right-aligned, it's likely TEXT, not a real number.
SUM() and other math functions will silently ignore it.
```
**Fix**: select the range → Data tab → Text to Columns → Finish (forces re-parsing as numbers). Or use `=VALUE(A1)` to convert a single cell.

## Checking a cell's actual type
```excel
=ISTEXT(A1)
=ISNUMBER(A1)
=ISBLANK(A1)
=TYPE(A1)          ' returns 1=number, 2=text, 4=boolean, 16=error
```

## Dates are just numbers underneath
```excel
=VALUE("1/15/2026")    ' returns a big number like 46032 (days since 1900-01-01)
```
This is WHY you can do date math like `=EndDate - StartDate` to get a number of days — dates are secretly numbers, formatted to display as dates.

## Practical example
Imported a CSV where a "Sales" column looks numeric but `=SUM(range)` returns 0? Almost always: the numbers were imported as text (common with CSVs from certain systems). Fix with Text to Columns, or `=SUMPRODUCT(VALUE(range))` as a formula workaround.
