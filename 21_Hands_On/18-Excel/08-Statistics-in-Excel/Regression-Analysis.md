# Regression Analysis in Excel

## What is it?
**Linear regression** fits a straight-line equation (`y = mx + b`) that best predicts a dependent variable (`y`) from one or more independent variables (`x`) — a core statistical modeling technique, available directly in Excel via the Analysis ToolPak or the `LINEST` function.

## Why care?
Regression lets you go beyond "these two things seem related" (correlation) to a genuine predictive model with quantified confidence — e.g., "for every $1,000 in ad spend, we predict $4,200 in additional sales, with X% confidence" — a much more actionable, decision-ready insight.

## Running regression via the Analysis ToolPak
**Data → Data Analysis → Regression**
- **Input Y Range**: your dependent variable (what you're predicting, e.g., Sales).
- **Input X Range**: your independent variable(s) (predictors, e.g., Ad Spend, Price) — can be multiple columns for multiple regression.
- Check "Labels" if your ranges include header row.

## Reading the output
- **R Square**: how much of the variation in Y is explained by the X variable(s) — closer to 1 is a better fit.
- **Coefficients table**: the `Intercept` and slope coefficient(s) for each X variable — these ARE your regression equation: `Sales = Intercept + (Coefficient × AdSpend)`.
- **P-value** (per coefficient): whether that variable's relationship to Y is statistically significant (conventionally, `p < 0.05` is considered significant) — see `04-Statistics/Hypothesis-Testing.md`-style logic; a high p-value suggests that variable might not genuinely be predictive.

## Formula-based alternative: LINEST
```excel
=LINEST(known_y_range, known_x_range, TRUE, TRUE)
```
Returns the regression coefficients (and, with the full statistics option, R², standard errors) directly as an array formula — useful when you want the regression numbers to update live/dynamically as source data changes, rather than needing to re-run the Analysis ToolPak each time (the ToolPak's output is a static snapshot, not a live formula).

## Multiple regression (more than one predictor)
Simply select multiple adjacent columns as the **Input X Range** — Excel fits a coefficient for EACH predictor simultaneously: `Sales = Intercept + (Coef1 × AdSpend) + (Coef2 × Price) + (Coef3 × Season)`.

## Practical example
A retailer wants to predict monthly sales based on ad spend, average price, and a seasonality indicator. Running multiple regression via the Analysis ToolPak produces an equation and coefficients directly usable in a forecasting model — and the p-values reveal, for instance, that "Price" isn't statistically significant while "Ad Spend" and "Season" are, guiding which factors are worth focusing future analysis and business decisions on.
