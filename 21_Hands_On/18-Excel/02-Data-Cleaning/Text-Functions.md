# Text Functions

## What is it?
Functions to extract, combine, clean, and reformat text data — critical because real-world data is messy (extra spaces, inconsistent casing, combined fields that need splitting).

## Why care?
Data cleaning is genuinely the majority of an analyst's real workload. Mastering text functions turns hours of manual cleanup into seconds of formula work.

## Essential text functions
```excel
=LEFT(A1, 3)              ' first 3 characters
=RIGHT(A1, 4)                ' last 4 characters
=MID(A1, 2, 5)                 ' 5 characters, starting at position 2
=LEN(A1)                          ' length (character count) of text
=TRIM(A1)                            ' removes extra/leading/trailing spaces
=UPPER(A1)  =LOWER(A1)  =PROPER(A1)    ' change casing
=CONCATENATE(A1, " ", B1)                 ' join text (older function)
=A1 & " " & B1                              ' join text (modern, preferred shorthand)
=TEXTJOIN(", ", TRUE, A1:A10)                 ' join a whole range with a delimiter, skip blanks
=SUBSTITUTE(A1, "old", "new")                   ' replace all instances of a substring
=FIND("@", A1)                                    ' position of a character (case-sensitive)
=SEARCH("@", A1)                                     ' position of a character (NOT case-sensitive)
```

## Splitting a full name into first/last (classic real-world task)
```excel
' "John Smith" in A1
=LEFT(A1, FIND(" ", A1) - 1)          ' → "John"  (everything before the space)
=MID(A1, FIND(" ", A1) + 1, LEN(A1))   ' → "Smith" (everything after the space)
```
Modern alternative (Excel 365): `Data → Text to Columns` (delimiter: space) does this without formulas at all, or use the new `TEXTBEFORE()`/`TEXTAFTER()` functions:
```excel
=TEXTBEFORE(A1, " ")     ' → "John"
=TEXTAFTER(A1, " ")       ' → "Smith"
```

## Cleaning inconsistent data (very common real task)
```excel
=TRIM(PROPER(A1))     ' fixes "  john SMITH " -> "John Smith"
```

## Practical example
A raw customer export has emails with inconsistent casing and extra spaces (`" John.Doe@EMAIL.com  "`). Clean it in one formula:
```excel
=LOWER(TRIM(A1))     ' -> "john.doe@email.com"
```
This exact pattern — clean before analyzing — prevents subtle bugs like "John.Doe@email.com" and "john.doe@email.com " being treated as two different customers in a COUNTIF or VLOOKUP.
