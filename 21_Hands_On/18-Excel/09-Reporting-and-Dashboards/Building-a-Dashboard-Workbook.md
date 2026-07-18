# Building a Dashboard Workbook (End-to-End Structure)

## What is it?
The standard multi-sheet architecture professional analysts use to organize a dashboard-delivering Excel workbook, from raw data to polished output.

## Why care?
A haphazardly-organized workbook (formulas mixed with raw data mixed with charts on one giant sheet) is fragile and hard to maintain. A clean, standard structure makes your work easier to build, debug, hand off to a colleague, and update month after month.

## The standard sheet structure
```
1. "ReadMe" (optional but professional) — brief notes: data source, last refresh date, contact/owner
2. "Raw Data" — the untouched, original data (or a Power Query-connected Table) — never manually edited
3. "Data Model" / "Calculations" — PivotTables, helper columns, DAX measures — the "engine room," usually hidden from end viewers
4. "Dashboard" — the final, polished, presentation-ready sheet — this is the ONLY sheet most viewers should ever see
```

## Why this separation matters
- **Raw Data stays untouched**: if you ever need to debug "why does this number look wrong," you can always trace back to a clean, unmodified source.
- **Calculations sheet(s) can be hidden**: right-click the sheet tab → Hide — keeps the workbook navigable for end-users without exposing the "engine room" clutter.
- **The Dashboard sheet only contains links/charts referencing the Calculations sheet** — never raw formulas mixed directly into the presentation layer. This means updating the underlying logic never risks accidentally breaking the visual layout.

## Protecting the final output
- **Protect Sheet** (Review → Protect Sheet) on the Dashboard sheet prevents accidental edits by viewers, while still allowing slicers/filters to function.
- Consider **locking cells vs. leaving specific input cells unlocked** (e.g., an assumption cell users are meant to adjust) — Format Cells → Protection tab, before applying Protect Sheet.

## Refresh workflow (documenting it matters)
Include a brief note (or automate via a macro) describing exactly how to refresh the workbook for the next reporting period: "1. Replace file in [folder]. 2. Data → Refresh All. 3. Confirm 'Data as of' date updates." This single documentation habit is what separates a report that survives you going on vacation from one that breaks the moment you're unavailable.

## Practical example
A monthly sales dashboard workbook: `Raw Data` sheet is Power Query-connected to a shared folder of monthly CSV exports; `Calculations` sheet holds the PivotTables and DAX measures (hidden); `Dashboard` sheet has the 4 KPI cards, 3 charts, and slicers, fully protected except for the slicer controls. Each month, someone drops the new CSV in the folder, opens the workbook, clicks **Data → Refresh All**, and the entire report updates end-to-end — this is the realistic, professional target to build toward.
