# Portfolio Project: HR Analytics Dashboard

## Goal
Analyze an employee dataset to surface headcount trends, attrition (turnover) patterns, and diversity metrics — demonstrates a different analytical domain than sales, showing versatility.

## Skills this project demonstrates
Pivot analysis on categorical/demographic data, calculated attrition rate metrics, cohort-style analysis, more nuanced/sensitive data visualization choices.

## Step-by-step outline

### 1. Get / simulate the data
Search "HR analytics attrition sample dataset" (a well-known public IBM HR dataset exists) or simulate: `EmployeeID, Department, JobRole, HireDate, TerminationDate (blank if active), Age, Gender, Salary, PerformanceRating`.

### 2. Clean and prepare
- Calculate `Tenure (years) = (TerminationDate or TODAY()) - HireDate`, converted to years.
- Create an `Active/Terminated` status flag.
- Bucket `Age` and `Tenure` into ranges (e.g., using `IFS` or a lookup table) for cleaner group-based analysis.

### 3. Key metrics to calculate
```
Headcount by Department (current, active employees only)
Attrition Rate = Terminated Employees / Average Headcount, over a period
Average Tenure by Department
Average Salary by Job Role (watch for pay equity patterns across demographics — handle sensitively and factually)
```

### 4. Build the analysis
- PivotTable: headcount by department by month (using a Date table, grouped) — visualize as a line chart to show growth/decline trends.
- PivotTable: attrition rate by department — a bar chart highlighting departments with above-average turnover (conditional formatting to flag outliers).
- A tenure distribution histogram (Excel's built-in Histogram chart type, or bucketed bar chart).

### 5. Dashboard layout
KPI cards: Total Headcount, Attrition Rate, Average Tenure, Open Positions (if data available). Charts: headcount trend, attrition by department, tenure distribution.

## A note on responsible analysis
HR/demographic data is sensitive — in a real (non-portfolio) context, always follow your organization's data privacy policies, avoid drawing unsupported causal conclusions from correlational patterns (e.g., "Department X has high attrition" needs follow-up investigation, not an assumed cause), and be mindful that demographic breakdowns can surface real equity issues that deserve careful, factual handling rather than sensationalized presentation.

## What to say about it in an interview
This project is a good opportunity to demonstrate you can work with non-financial, categorical/demographic data and calculate a genuinely non-trivial metric (attrition rate, correctly handling the "average headcount over a period" denominator) — walk through how you defined and validated that calculation specifically, since it's a common point of genuine ambiguity real analysts have to resolve.
