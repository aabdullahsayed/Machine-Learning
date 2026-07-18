# Logical Functions

## What is it?
Functions that evaluate conditions and return different results based on TRUE/FALSE logic — the backbone of decision-making formulas.

## Why care?
Nearly every real business rule ("flag as high-priority if revenue > $10k AND region = West") is expressed via logical functions. This is one of the most-used categories in daily analyst work.

## IF — the fundamental building block
```excel
=IF(A1 > 100, "High", "Low")
```
Syntax: `IF(condition, value_if_true, value_if_false)`

## Nested IF (chaining multiple conditions)
```excel
=IF(A1>=90, "A", IF(A1>=80, "B", IF(A1>=70, "C", "F")))
```
Works, but gets unreadable fast with many conditions — prefer `IFS()` for 3+ conditions (Excel 2019+/365).

## IFS — cleaner multi-condition logic
```excel
=IFS(A1>=90, "A", A1>=80, "B", A1>=70, "C", TRUE, "F")
```
Evaluates conditions top to bottom, returns the first TRUE match. The final `TRUE, "F"` acts as a catch-all "else" case.

## AND / OR — combining conditions
```excel
=IF(AND(A1>50, B1="West"), "Priority", "Normal")     ' BOTH conditions must be true
=IF(OR(A1>1000, B1="VIP"), "Flag", "Normal")            ' EITHER condition can be true
```

## NOT — invert a condition
```excel
=IF(NOT(A1="Closed"), "Still Open", "Done")
```

## SWITCH — clean alternative to nested IFs for exact-match cases
```excel
=SWITCH(A1, "N", "North", "S", "South", "E", "East", "Unknown")
```
Cleaner than nested IFs when checking one value against several exact possibilities.

## Combining with COUNTIF/SUMIF for conditional aggregation (preview)
```excel
=IF(COUNTIF(A:A, A1)>1, "Duplicate", "Unique")
```

## Practical example — a real business rule
Flag orders as "Urgent" if the order value is over $5,000 AND the customer is in the "Enterprise" tier, OR if it's flagged manually as rush:
```excel
=IF(OR(AND(C2>5000, D2="Enterprise"), E2="Rush"), "Urgent", "Standard")
```
This exact pattern — combining `IF`, `AND`, `OR` — is how most real-world business logic gets expressed in a spreadsheet.
