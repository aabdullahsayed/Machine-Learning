# Basic Formulas

## What is it?
Every Excel formula starts with `=` and can combine cell references, operators, and functions to calculate a result.

## Why care?
This is the literal foundation everything else in this repo builds on.

## Arithmetic operators
```excel
=A1+B1        ' addition
=A1-B1        ' subtraction
=A1*B1        ' multiplication
=A1/B1        ' division
=A1^2         ' exponent (power)
=A1&B1        ' text concatenation (joins as text)
```

## Order of operations (PEMDAS applies)
```excel
=2+3*4        ' = 14, NOT 20 (multiplication before addition)
=(2+3)*4      ' = 20 (parentheses force order)
```

## Essential starter functions
```excel
=SUM(A1:A10)             ' total of a range
=AVERAGE(A1:A10)          ' mean
=COUNT(A1:A10)              ' counts numeric cells only
=COUNTA(A1:A10)               ' counts non-empty cells (any type)
=MAX(A1:A10)                    ' largest value
=MIN(A1:A10)                      ' smallest value
=ROUND(A1, 2)                       ' round to 2 decimal places
```

## AutoSum shortcut
Select a cell below/beside a range of numbers, press `Alt + =` — Excel guesses the range and inserts `=SUM(...)` automatically. Huge time-saver.

## Comparison operators (return TRUE/FALSE)
```excel
=A1>B1     =A1<B1     =A1>=B1     =A1<=B1     =A1=B1     =A1<>B1  (not equal)
```

## Practical example
A sales report with a "Revenue" column `B2:B500`:
```excel
=SUM(B2:B500)            ' total revenue
=AVERAGE(B2:B500)         ' average sale amount
=MAX(B2:B500)               ' biggest single sale
```
These three formulas alone answer the most common first questions any stakeholder asks about a dataset.
