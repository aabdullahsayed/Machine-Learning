# Data Validation

## What is it?
Rules that restrict what can be entered into a cell — dropdown lists, number ranges, date ranges, custom formula-based rules.

## Why care?
Prevents bad data from entering your spreadsheet in the first place ("garbage in, garbage out") — especially important for shared workbooks where multiple people enter data manually.

## Setting up basic validation
```
Select cells → Data tab → Data Validation → Settings
```

### Dropdown list (most common use)
```
Allow: List
Source: Yes,No,Maybe        (comma-separated, or reference a range like =$F$1:$F$5)
```
Prevents typos like "Yse" instead of "Yes" — critical for keeping categorical data clean for later PivotTables/COUNTIFS.

### Number range restriction
```
Allow: Whole number  (or Decimal)
Data: between
Minimum: 0
Maximum: 100
```
Useful for percentage fields, ratings (1-5), ages, etc. — rejects impossible values at entry time.

### Date range restriction
```
Allow: Date
Data: between
Start date / End date
```

### Custom formula-based validation (most powerful)
```excel
=AND(LEN(A1)=10, ISNUMBER(VALUE(A1)))     ' e.g., enforce a 10-digit phone number
=COUNTIF($A$2:$A$100, A1)=1                  ' enforce no duplicates in this column
```

## Input message & error alert (guides the user)
```
Data Validation → Input Message tab: "Enter a value between 0 and 100"
Data Validation → Error Alert tab: "Please enter a valid percentage"
```
These show a tooltip when the cell is selected, and a clear error if invalid data is entered — much friendlier than a silent rejection.

## Practical example
Building a data-entry template for a sales team to log daily deals: use a dropdown (`Data Validation → List`) for "Product Category" and "Sales Rep Name" fields, sourced from a master list on a hidden sheet — guarantees consistent spelling across hundreds of manual entries, which is exactly what your future PivotTable/VLOOKUP analysis depends on.
