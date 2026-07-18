# Descriptive Statistics in Excel

## What is it?
Summarizing a dataset's central tendency (mean, median, mode) and spread (standard deviation, variance, range) using built-in Excel functions — the numeric foundation of any real analysis.

## Why care?
Before building any chart or drawing any conclusion, a competent analyst checks these basic numbers first — they reveal data quality issues (implausible values, huge spread) and set the baseline for everything downstream.

## Core functions
```excel
=AVERAGE(range)         -- mean
=MEDIAN(range)            -- middle value (robust to outliers, unlike mean)
=MODE.SNGL(range)           -- most frequent value
=STDEV.S(range)               -- sample standard deviation (use for a sample of a larger population)
=STDEV.P(range)                 -- population standard deviation (use if your range IS the entire population)
=VAR.S(range)                     -- sample variance
=MIN(range) / =MAX(range)           -- range boundaries
=COUNT(range) / =COUNTA(range)        -- count of numeric / non-blank cells
```

## Percentiles and Quartiles
```excel
=QUARTILE.INC(range, 1)     -- 25th percentile (Q1)
=QUARTILE.INC(range, 3)      -- 75th percentile (Q3)
=PERCENTILE.INC(range, 0.90)   -- 90th percentile — e.g., "90% of deliveries completed within X days"
```

## The Analysis ToolPak (one-click full summary)
**File → Options → Add-ins → Manage: Excel Add-ins → Go → check "Analysis ToolPak"**. Then: **Data → Data Analysis → Descriptive Statistics** — instantly generates mean, median, mode, std dev, range, min, max, count, and more for an entire column, without writing individual formulas.

## Interquartile Range (IQR) — for outlier detection
```
IQR = Q3 - Q1
Outlier bounds: [Q1 - 1.5*IQR,  Q3 + 1.5*IQR]
```
Values outside this range are conventionally flagged as statistical outliers — a standard, defensible rule of thumb used across data analysis, not just in Excel.

## Practical example
Before building a sales dashboard, run descriptive statistics on the `Revenue` column: if `MAX` is 100x larger than the `MEDIAN`, that's a signal to investigate — likely either a genuine huge outlier deal worth flagging separately, or a data entry error (e.g., a misplaced decimal point) that needs fixing before it skews every chart and average in the dashboard.
