# Error Handling in Formulas

## What is it?
Techniques for gracefully catching and handling formula errors (`#N/A`, `#DIV/0!`, `#VALUE!`, etc.) instead of letting them break your spreadsheet or downstream calculations.

## Why care?
A single unhandled error can cascade — a `#N/A` from a broken VLOOKUP feeding into a SUM formula turns the whole total into an error too. Professional spreadsheets anticipate and handle these gracefully, especially in dashboards/reports where a stakeholder shouldn't ever see a raw error code.

## Common error types (know what each means)
| Error | Common cause |
|---|---|
| `#N/A` | Lookup value not found (VLOOKUP/XLOOKUP/MATCH) |
| `#DIV/0!` | Division by zero |
| `#VALUE!` | Wrong data type used in a formula (e.g., adding text to a number) |
| `#REF!` | Formula refers to a cell that's been deleted |
| `#NAME?` | Excel doesn't recognize a function name or named range (often a typo) |
| `#NUM!` | Invalid numeric value (e.g., square root of a negative number) |

## IFERROR — the standard fix
```excel
=IFERROR(VLOOKUP(A2, Table1, 2, FALSE), "Not Found")
```
Replaces any error result with a custom fallback value — the cleanest, most common way to handle expected errors gracefully.

## IFNA — more precise (only catches #N/A specifically)
```excel
=IFNA(VLOOKUP(A2, Table1, 2, FALSE), "Not Found")
```
Preferred over IFERROR when you specifically expect "not found" lookups, but still want OTHER unexpected error types (like a genuine formula bug) to surface visibly rather than being silently hidden — an important distinction: `IFERROR` can accidentally mask real bugs, not just expected "not found" cases.

## Preventing division-by-zero errors
```excel
=IFERROR(B2/C2, 0)
-- or, more explicit and often preferred:
=IF(C2=0, 0, B2/C2)
```

## Practical example
A commission calculation `=Sales/Target` breaks with `#DIV/0!` for any salesperson without a target yet assigned. Wrapping it as `=IFERROR(Sales/Target, "No Target Set")` prevents this from breaking any downstream SUM/AVERAGE formulas relying on this column, and gives a much clearer, self-explanatory message than a raw Excel error code when the report is shared with stakeholders.
