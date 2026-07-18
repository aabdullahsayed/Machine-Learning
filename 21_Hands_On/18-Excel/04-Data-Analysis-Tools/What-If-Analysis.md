# What-If Analysis

## What is it?
A set of Excel tools (Data Tables, Scenario Manager, Goal Seek) for exploring "what happens to my result if I change this input?" — essential for financial modeling and sensitivity analysis.

## Why care?
Business stakeholders constantly ask "what if we increase price by 10%?" or "what if churn drops to 5%?" — What-If Analysis tools let you answer these systematically instead of manually re-typing numbers over and over.

## Data Tables (sensitivity analysis)
Shows how a formula's result changes across a range of input values, all at once, in a grid.
- **One-variable data table**: vary ONE input (e.g., price), see the effect on one or more outputs (e.g., revenue, profit).
- **Two-variable data table**: vary TWO inputs simultaneously (e.g., price AND quantity), see the effect on ONE output, in a grid/matrix format.

Setup: **Data → What-If Analysis → Data Table**, referencing the row/column input cells that feed your formula.

## Scenario Manager
Save and compare multiple named "scenarios" — different sets of input assumptions (e.g., "Best Case," "Worst Case," "Most Likely") — and instantly switch between them or generate a summary comparing all scenarios side-by-side.
**Data → What-If Analysis → Scenario Manager → Add** to define each scenario's input values.

## Practical example
A financial model projecting next year's revenue based on `Price × Units Sold`. Build a two-variable data table varying Price (rows) and Units Sold (columns), instantly seeing a full grid of possible revenue outcomes — far faster than manually testing combinations one at a time, and this exact table is what gets pasted into a board presentation as a "sensitivity analysis."

See `Goal-Seek-Solver.md` for the reverse problem: "what input do I need to hit a specific target output?"
