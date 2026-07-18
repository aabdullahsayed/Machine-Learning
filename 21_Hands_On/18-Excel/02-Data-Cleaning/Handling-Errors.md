# Handling Errors

## What is it?
Understanding Excel's error codes and how to gracefully catch/handle them in formulas instead of letting them break your reports.

## Why care?
A single `#N/A` or `#DIV/0!` error can silently break downstream SUM/AVERAGE calculations, or look unprofessional in a stakeholder-facing report — knowing how to anticipate and handle these is a mark of a careful analyst.

## Common error codes and what they mean
| Error | Meaning | Common cause |
|---|---|---|
| `#N/A` | Value not available | VLOOKUP/MATCH couldn't find a match |
| `#DIV/0!` | Division by zero | Denominator is 0 or blank |
| `#VALUE!` | Wrong data type | Trying to do math on text |
| `#REF!` | Invalid cell reference | A referenced cell/row/column was deleted |
| `#NAME?` | Unrecognized formula name | Typo in a function name, or missing quotes around text |
| `#NUM!` | Invalid numeric value | E.g., `SQRT(-1)` |
| `###` | Column too narrow | (Not a real error — just widen the column) |

## Catching errors gracefully
```excel
=IFERROR(VLOOKUP(A1, table, 2, FALSE), "Not Found")
```
Instead of a raw `#N/A` showing in your report, this shows a friendly "Not Found" — much better for stakeholder-facing spreadsheets.

```excel
=IFNA(VLOOKUP(A1, table, 2, FALSE), "Not Found")
```
`IFNA` specifically catches `#N/A` only (leaves other error types, like a genuine formula mistake, visible so you notice and fix them) — often a better practice than `IFERROR`, which can accidentally hide real bugs in your formula logic.

## Preventing division-by-zero errors
```excel
=IF(B1=0, 0, A1/B1)                    ' explicit check
=IFERROR(A1/B1, 0)                        ' catch-all approach
```

## Finding all errors in a large sheet quickly
```
Home → Find & Select → Go To Special → Formulas → check only "Errors" → OK
```
Selects every cell containing an error at once — much faster than scrolling through thousands of rows manually.

## Practical example
A commission report divides `Total Sales / Number of Deals`, but some reps had 0 deals that period:
```excel
=IFERROR(TotalSales/NumberOfDeals, 0)     ' shows 0% instead of a scary #DIV/0! in the final report
```
