# Portfolio Project: Sales Dashboard

## Goal
Build a complete, interactive Sales Dashboard from raw transaction data — the single most common portfolio project for a Data Analyst role, because nearly every company has some version of this exact need.

## Skills this project demonstrates
Power Query cleaning, PivotTables/Power Pivot, DAX measures, chart selection, slicers, dashboard layout/design — effectively the entire roadmap, applied together.

## Step-by-step outline

### 1. Get / simulate the data
Use a public sample dataset (e.g., search "sample superstore sales dataset") or generate synthetic data with columns: `OrderDate, Region, Category, Product, Salesperson, Units, Revenue, Cost`.

### 2. Clean it with Power Query
- Fix data types (dates as dates, numbers as numbers, not text).
- Remove any test/void transactions.
- Add a calculated column: `Profit = Revenue - Cost`.

### 3. Build the Data Model
- Load into the Data Model.
- Create a separate Date table, relate it to your Sales table (see `06-Power-Tools/Data-Model.md`).

### 4. Write core DAX measures
```
Total Revenue = SUM(Sales[Revenue])
Total Profit = SUM(Sales[Profit])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
YoY Growth % = DIVIDE([Total Revenue] - CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date])), CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date])))
```

### 5. Design the dashboard layout
- **Top row**: 4 KPI cards — Total Revenue, Total Profit, Profit Margin %, YoY Growth %.
- **Middle**: a line chart of monthly revenue trend, a bar chart of revenue by region.
- **Bottom**: a table of top 10 products/salespeople by revenue, with sparklines showing each one's trend.
- **Slicers**: Region, Category, Year — connected to every PivotTable/chart on the sheet.

### 6. Polish
Apply the design principles from `09-Reporting-and-Dashboards/Report-Design-Best-Practices.md` — consistent colors, no chart clutter, clear labels, a "data as of" note.

### 7. Protect and document
Hide the raw data/calculation sheets, protect the dashboard sheet, add a brief ReadMe explaining the data source and how to refresh.

## What to say about it in an interview
Be ready to explain: what business question the dashboard answers, why you chose the specific KPIs and chart types, how the DAX YoY measure works conceptually, and what you'd add next with more time (e.g., a forecast, a drill-down page) — interviewers care as much about your reasoning as the final polished output.
