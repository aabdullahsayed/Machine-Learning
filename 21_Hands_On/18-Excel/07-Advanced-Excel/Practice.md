# Practice — Advanced Excel

1. Rebuild a VLOOKUP formula from earlier practice using XLOOKUP instead — confirm it still works if you insert a new column between the lookup and return columns (VLOOKUP would break; XLOOKUP referencing table columns should not).
2. Write the same lookup a third way using INDEX-MATCH, and compare all three approaches side by side.
3. Try `=UNIQUE()` and `=FILTER()` on your sample sales dataset — build a spilling, always-current unique list of product categories.
4. Record a macro that applies a specific formatting style (header bold, autofit columns, freeze top row) to any new dataset, then run it on a fresh sheet.
5. Open the VBA editor (`Alt+F11`) and read through the code your recorded macro generated — try modifying one line (e.g., change the highlight color) and re-run it.
6. Wrap 3 different formulas prone to errors (a lookup, a division, a date calculation) in appropriate `IFERROR`/`IFNA` handling.
7. Convert your sample dataset into an Excel Table (`Ctrl+T`), and rewrite a formula to use structured references (`Table[Column]`) instead of raw cell ranges.

✅ Done? Move to `08-Statistics-in-Excel`.
