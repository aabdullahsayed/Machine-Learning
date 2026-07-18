# Report Design Best Practices

## What is it?
The principles of designing a spreadsheet-based report so it's clear, trustworthy, and fast to read by someone who is NOT you and has 30 seconds of attention to give it.

## Why care?
A technically-correct report that's confusing or cluttered fails at its actual job — communicating information clearly to drive a decision. This is a genuinely evaluated, real-world skill difference between junior and senior analysts.

## Structural principles
1. **Separate raw data from presentation.** Keep a "Data" sheet (or hidden helper sheets) with PivotTables/calculations, and a clean "Dashboard"/"Report" sheet with only the final, polished output. Never make a viewer scroll through raw formulas to find the summary.
2. **One clear takeaway per chart/section.** If a chart needs a paragraph to explain what it's showing, it's probably the wrong chart or needs a clearer title.
3. **Most important number goes top-left.** Eyes scan top-left first (in left-to-right reading cultures) — put your single most important KPI there.
4. **Consistent formatting throughout**: same date format, same currency format, same decimal precision everywhere in the report — inconsistency undermines trust in the numbers even if they're all correct.

## Visual principles
- **Remove chartjunk**: no unnecessary gridlines, borders, 3D effects, or default titles like "Chart 1" left unedited.
- **Use color with purpose, not decoration**: color should encode meaning (e.g., red = below target) consistently, not just look nice — and use a limited palette (2-4 colors) throughout.
- **Round numbers appropriately**: `$1.2M` communicates faster than `$1,247,382.19` in a summary view — save full precision for the detailed data sheet, not the headline dashboard.
- **Label axes and units clearly** — never leave a viewer guessing whether a number is in dollars, thousands of dollars, or percent.

## Trust and transparency principles
- **Show the data's "as of" date** — every report should clearly state when it was last refreshed, especially in a business context where stale data can lead to bad decisions.
- **Document your assumptions** — if a forecast relies on assumptions (a growth rate, a conversion assumption), state them visibly rather than burying them in a hidden formula.
- **Make it auditable**: a colleague (or your future self) should be able to trace any final number back to its source data without needing to ask you "how did you calculate this?"

## Practical example
Compare two versions of the same revenue report: Version A is a dense grid of every raw transaction with 15 columns and no formatting. Version B has 3 KPI cards up top, one clean trend chart, a filtered top-10 table, and a clearly labeled "Data as of: [date]" note. Version B communicates the same underlying insight in 10 seconds instead of 10 minutes — this is the entire point of report design as a distinct analyst skill, separate from just "knowing the formulas."
