# Math & Statistical Functions

## What is it?
Functions for aggregating, conditionally summarizing, and statistically summarizing numeric data — the daily bread-and-butter of quantitative analysis.

## Why care?
Nearly every business question ("total sales in the West region," "average deal size for VIP customers," "how many orders were over $500") is answered with these functions.

## Conditional aggregation (extremely commonly used)
```excel
=SUMIF(range, criteria, sum_range)
=SUMIF(B:B, "West", C:C)                          ' sum column C where column B = "West"

=COUNTIF(range, criteria)
=COUNTIF(B:B, "West")                                ' count rows where column B = "West"

=AVERAGEIF(range, criteria, average_range)
=AVERAGEIF(B:B, "West", C:C)                            ' average of column C where B = "West"
```

## Multi-condition versions (SUMIFS, COUNTIFS, AVERAGEIFS)
```excel
=SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...)
=SUMIFS(C:C, B:B, "West", D:D, ">1000")     ' sum C where B="West" AND D>1000
```
**Note the argument order difference**: `SUMIF` puts `sum_range` last; `SUMIFS` puts it FIRST. A very common source of formula errors when switching between the two.

## Statistical functions
```excel
=MEDIAN(range)               ' middle value
=MODE.SNGL(range)              ' most frequent value
=STDEV.S(range)                  ' sample standard deviation
=VAR.S(range)                      ' sample variance
=PERCENTILE.INC(range, 0.9)          ' 90th percentile
=QUARTILE.INC(range, 3)                ' 3rd quartile (75th percentile)
=RANK.EQ(A1, range, 0)                   ' rank of A1 within range (0 = descending)
```

## SUMPRODUCT — the flexible, powerful multi-purpose tool
```excel
=SUMPRODUCT((B:B="West")*(D:D>1000))          ' count rows matching BOTH conditions (like COUNTIFS but more flexible)
=SUMPRODUCT((B2:B100="West")*(C2:C100))          ' sum with a condition, works in older Excel versions too
```
`SUMPRODUCT` multiplies arrays element-wise then sums the result — TRUE/FALSE conditions become 1/0 when multiplied, making it a powerful, flexible alternative to SUMIFS/COUNTIFS, especially for more complex conditions.

## AGGREGATE and SUBTOTAL — ignore filtered/hidden rows
```excel
=SUBTOTAL(9, C2:C100)          ' SUM (9), but ignores rows hidden by a FILTER
=SUBTOTAL(1, C2:C100)            ' AVERAGE (1), same filter-aware behavior
```
Critical when your data has an active filter applied — a plain `SUM()` includes hidden/filtered-out rows, while `SUBTOTAL` correctly only totals the VISIBLE rows, which is almost always what you actually want in a filtered report.

## Practical example
A regional sales dashboard needs: total revenue for the West region, orders over $1,000 in the West region, and the average deal size, filtered live as the user changes a slicer:
```excel
=SUMIFS(Revenue, Region, "West")
=COUNTIFS(Region, "West", Revenue, ">1000")
=AVERAGEIFS(Revenue, Region, "West")
```
