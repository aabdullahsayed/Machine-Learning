# Slicers & Timelines

## What is it?
**Slicers** are clickable filter buttons connected to a PivotTable (or Table) — a more visual, user-friendly alternative to the small dropdown filter arrows. **Timelines** are a specialized slicer just for date fields, with a draggable date-range selector.

## Why care?
Slicers are what make a dashboard feel genuinely "interactive" rather than a static picture — this is the feature that lets a non-technical stakeholder explore the data themselves (click "Region: East," instantly see updated charts) without needing to know any Excel formulas.

## Adding a Slicer
1. Click inside a PivotTable → **PivotTable Analyze → Insert Slicer**.
2. Choose the field(s) to filter by (e.g., Region, Product Category).
3. Style/resize the slicer buttons as needed (**Slicer → Options** for colors/columns).

## Adding a Timeline (for date fields)
**PivotTable Analyze → Insert Timeline** → choose a date field → get a draggable, zoomable date-range selector (by Day/Month/Quarter/Year).

## Connecting one slicer to MULTIPLE PivotTables/charts (the dashboard superpower)
By default, a slicer only filters the PivotTable it was inserted from. To make ONE slicer control MULTIPLE PivotTables (essential for dashboards with several charts):
**Slicer → Report Connections** (right-click the slicer, or Slicer tab in the ribbon) → check every PivotTable you want it to also filter.

This is precisely the mechanism that lets a single "Region" slicer on a dashboard simultaneously filter a revenue chart, a units-sold chart, and a top-salesperson table, all at once.

## Practical example
A dashboard with 3 charts (all built from PivotTables sharing the same underlying data source) and one Region slicer, connected to all 3 via Report Connections — clicking "West" on the slicer instantly updates every chart on the dashboard to show only West-region data, giving stakeholders a genuinely self-service exploration experience.
