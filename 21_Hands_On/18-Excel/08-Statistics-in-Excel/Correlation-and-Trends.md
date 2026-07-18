# Correlation & Trend Analysis

## What is it?
Measuring whether (and how strongly) two variables move together (correlation), and fitting a line/curve through data to describe or predict a trend (regression/trendlines).

## Why care?
"Is marketing spend actually related to sales?" "Is there a trend in customer churn over time?" — these are core business questions, and Excel has built-in tools to answer them without needing a separate statistics package.

## Correlation
```excel
=CORREL(range1, range2)
```
Returns a value between **-1 and +1**:
- **+1**: perfect positive relationship (as one increases, so does the other)
- **-1**: perfect negative relationship (as one increases, the other decreases)
- **0**: no linear relationship

**Correlation Matrix** (comparing many variables at once): **Data → Data Analysis → Correlation** (Analysis ToolPak) — generates a full grid of pairwise correlations across multiple columns at once.

### Important caveat: correlation ≠ causation
A strong correlation between two variables doesn't prove one causes the other — there could be a confounding third factor, or it could be coincidental. This is a critical, frequently-tested analyst concept: always sanity-check a correlation finding against real business logic before presenting it as a causal insight.

## Trendlines (visual regression, directly on a chart)
Right-click a data series on a chart → **Add Trendline** → choose Linear, Exponential, Polynomial, etc. Check **"Display Equation on chart"** and **"Display R-squared value"** to see the fitted formula and how well it fits.

- **R² (R-squared)**: ranges 0 to 1 — how much of the variation in your data the trendline explains. Closer to 1 = better fit.

## Forecasting with `FORECAST.LINEAR` / `TREND`
```excel
=FORECAST.LINEAR(new_x_value, known_y_values, known_x_values)
```
Predicts a future value based on a linear trend fit to historical data — a lightweight, formula-based way to do simple forecasting directly in a cell, without needing a full statistical model.

Excel also has a dedicated **Forecast Sheet** tool (**Data → Forecast Sheet**), which automatically fits a more sophisticated model (including seasonality) to a time series and generates a forecast chart with confidence intervals.

## Practical example
Testing whether advertising spend correlates with monthly sales: `=CORREL(AdSpend_range, Sales_range)` returns `0.82` — a strong positive correlation. Adding a linear trendline to a scatter chart of the same data, with R² displayed, visually confirms and quantifies how well a straight line explains the relationship — but before concluding "more ad spend causes more sales," check whether other factors (seasonality, promotions) might be driving both simultaneously.
