# Portfolio Project: 3-Statement Financial Model / Budget Tracker

## Goal
Build either (a) a simplified 3-statement financial model (Income Statement, Balance Sheet, Cash Flow) or (b) a budget vs. actual tracker with variance analysis — demonstrates financial modeling literacy, valuable for Data Analyst roles in finance-adjacent teams (FP&A, business operations).

## Skills this project demonstrates
Formula-driven modeling (not just PivotTables), named ranges/assumptions, What-If analysis, scenario comparison, variance analysis, professional formatting conventions used in finance.

## Step-by-step outline (Budget vs. Actual Tracker — the more approachable option)

### 1. Structure the model
- **Assumptions sheet**: named ranges for key inputs (e.g., `MonthlyBudget`, `GrowthRate`) — see `07-Advanced-Excel/Named-Ranges.md`.
- **Data sheet**: monthly actual spend by category (Marketing, Payroll, Operations, etc.).
- **Analysis sheet**: Budget vs. Actual comparison, with variance calculations.

### 2. Core calculations
```
Variance ($) = Actual - Budget
Variance (%) = Variance ($) / Budget
Status = IF(Variance % > 0.10, "Over Budget", IF(Variance % < -0.10, "Under Budget", "On Track"))
```

### 3. Visualize
- A combo chart: Budget (columns) vs Actual (line) by month, by category.
- Conditional formatting on the Variance % column (red for over-budget, green for under/on-track) — a classic, expected pattern in financial reporting.
- A waterfall chart showing how each category's variance contributes to total variance from budget.

### 4. Add What-If capability
Use a Data Table (`04-Data-Analysis-Tools/What-If-Analysis.md`) to show how total year-end spend changes under different assumed monthly growth rates — a realistic "what if costs grow 5% vs 10% vs 15% monthly" sensitivity view.

### 5. Professional formatting conventions (finance-specific)
- Negative numbers in **parentheses and/or red**, not just a minus sign — standard financial convention.
- Consistent use of `$` and `%` number formats, right-aligned.
- Clear distinction between **hardcoded inputs** (often blue font) and **formulas** (black font) — a widely recognized financial modeling convention that instantly tells a reviewer what's an assumption vs. a calculation.

## What to say about it in an interview
Emphasize the modeling discipline: clean separation of assumptions from calculations, the blue-input/black-formula convention, and how you validated the model (e.g., checking that Budget vs Actual totals tie out correctly, sense-checking the variance calculation against a manual example). Financial modeling interviews often probe exactly this kind of "how do you make sure your model doesn't have a silent error" reasoning.
