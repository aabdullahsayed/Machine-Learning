# Building Dashboards

## What is it?
A dashboard is a single-screen summary combining multiple charts, KPIs, and interactive filters (slicers) — designed to give a decision-maker the full picture at a glance, without scrolling through raw data.

## Why care?
Building a clean, interactive dashboard is one of the most visible, portfolio-worthy Excel skills for a Data Analyst — it's often literally the deliverable stakeholders see and judge your work by.

## Planning before building
1. **Identify the audience and their key question(s)** — a sales VP wants different things than an operations manager. Don't build a dashboard before knowing what decisions it needs to support.
2. **Pick 4-8 key metrics (KPIs)** — too many and it becomes noise, too few and it's not useful.
3. **Sketch the layout on paper first** — top-left is where eyes land first; put the most important KPI there.

## Building blocks
- **PivotTables** (hidden on a separate "data" sheet) as the calculation engine.
- **PivotCharts / regular charts** linked to those PivotTables, placed on the dashboard sheet.
- **Slicers and Timelines** (`Slicers-Timelines.md`) for interactive filtering across all charts at once.
- **KPI cards**: a cell or small group of cells showing a single big number (e.g., "Total Revenue: $1.2M") with conditional formatting/icons showing trend vs. a target.
- **Named ranges + form controls** (dropdown lists, option buttons) for more advanced custom interactivity.

## Layout & design best practices
- Use a consistent color palette — 2-3 main colors, used consistently for the same meaning throughout (e.g., always blue = actuals, orange = target).
- Align everything to a grid — use **View → Gridlines** off, but keep charts/cards visually aligned using cell borders as guides.
- Remove ALL unnecessary clutter: no gridlines, no unnecessary borders, no default chart titles like "Chart 1."
- Freeze the dashboard to one screen — avoid requiring scrolling to see the full picture.

## Making it interactive
Insert **Slicers** connected to your PivotTables (see `Slicers-Timelines.md`) — a viewer clicks "Region: West" and every chart/KPI on the dashboard updates simultaneously, since they're all built on the same underlying PivotTable data model.

## Practical example
A Sales Dashboard with: 4 KPI cards (Total Revenue, Total Units, Avg Deal Size, YoY Growth %) across the top, a line chart of monthly revenue trend, a bar chart of revenue by region, a table of top 10 salespeople, and a slicer for Year/Quarter/Region filtering everything at once — this exact structure is a very common, realistic Data Analyst portfolio project (see `09-Reporting-and-Dashboards` and `10-Real-World-Projects`).
