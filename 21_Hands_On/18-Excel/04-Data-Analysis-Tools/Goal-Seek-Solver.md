# Goal Seek & Solver

## What is it?
**Goal Seek** finds the input value needed to make a formula hit a specific target result (single variable, single goal). **Solver** is the more powerful version — optimizes toward a goal by adjusting MULTIPLE variables, optionally subject to constraints.

## Why care?
Instead of manually guessing-and-checking "what sales number do I need to hit $1M profit?", these tools solve it directly — a genuinely time-saving, precise tool for target-driven business questions.

## Goal Seek
**Data → What-If Analysis → Goal Seek**
- **Set cell**: the formula cell you want to hit a target value (e.g., `Profit` cell).
- **To value**: the target (e.g., `1000000`).
- **By changing cell**: the single input Excel should adjust (e.g., `Units Sold`).

Excel iteratively adjusts the input until the formula's result matches your target as closely as possible.

## Solver (more powerful, needs enabling first)
Enable via **File → Options → Add-ins → Manage: Excel Add-ins → Go → check "Solver Add-in"**. Then find it under **Data → Solver**.

- **Set Objective**: the cell to maximize, minimize, or set to a specific value.
- **By Changing Variable Cells**: multiple input cells Solver can adjust.
- **Subject to Constraints**: rules like `Units ≤ 500` (limited inventory) or `Budget ≤ 10000`.

Solver uses optimization algorithms (e.g., Simplex LP for linear problems) to find the best combination of inputs satisfying all constraints.

## Practical example
**Goal Seek**: "What price do I need to charge to hit exactly $50,000 in monthly revenue, given expected demand at different price points?"

**Solver**: "I have a $10,000 ad budget across 4 marketing channels, each with different expected return rates and a max spend limit per channel — how should I allocate the budget to maximize total expected return?" — this is a genuine linear programming problem, solvable directly inside Excel via Solver, no external tools needed.
