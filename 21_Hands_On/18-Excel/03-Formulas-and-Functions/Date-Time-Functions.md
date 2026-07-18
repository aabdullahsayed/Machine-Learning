# Date & Time Functions

## What is it?
Functions to extract, calculate, and manipulate dates and times — since Excel stores dates as serial numbers (see `01-Excel-Basics/Data-Types.md`), a whole family of functions exists to work with them meaningfully.

## Why care?
Time-based analysis (month-over-month growth, days-since-last-purchase, fiscal quarters) is extremely common in business analytics — and date handling is a frequent source of subtle bugs if not done carefully.

## Getting the current date/time
```excel
=TODAY()          ' current date (no time), updates every time the sheet recalculates
=NOW()               ' current date AND time
```

## Extracting parts of a date
```excel
=YEAR(A1)     =MONTH(A1)     =DAY(A1)
=WEEKDAY(A1)                    ' 1=Sunday, 2=Monday, ... by default
=WEEKDAY(A1, 2)                   ' 1=Monday, ..., 7=Sunday (ISO-style)
=TEXT(A1, "mmmm")                   ' full month name, e.g. "July"
=TEXT(A1, "yyyy-mm")                  ' "2026-07" — great for grouping by month
```

## Date arithmetic (works because dates are just numbers)
```excel
=B1 - A1                       ' number of days between two dates
=A1 + 30                         ' 30 days after A1
=EOMONTH(A1, 0)                     ' last day of the current month
=EOMONTH(A1, 1)                       ' last day of NEXT month
=EDATE(A1, 3)                            ' same day, 3 months later (handles month-length differences)
```

## Business-day-aware functions (skip weekends automatically)
```excel
=NETWORKDAYS(A1, B1)                       ' number of business days between two dates
=WORKDAY(A1, 10)                             ' date 10 business days after A1
=NETWORKDAYS(A1, B1, HolidayList)              ' also excludes a custom holiday list
```

## DATEDIF — calculating age/tenure (hidden but very useful function)
```excel
=DATEDIF(StartDate, TODAY(), "Y")     ' full years between two dates (e.g., age, tenure)
=DATEDIF(StartDate, TODAY(), "M")       ' full months between two dates
=DATEDIF(StartDate, TODAY(), "D")         ' full days between two dates
```
Not in the formula autocomplete dropdown (a known Excel quirk) but works perfectly when typed manually — extremely useful for HR/tenure analysis.

## Practical example — "days since last purchase" (common churn analysis metric)
```excel
=TODAY() - LastPurchaseDate
```
Combined with a conditional:
```excel
=IF(TODAY() - LastPurchaseDate > 90, "At Risk", "Active")
```
This exact pattern powers real customer-churn flags in retention dashboards.
