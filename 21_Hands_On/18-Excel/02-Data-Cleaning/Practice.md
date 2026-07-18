# Practice — Data Cleaning

1. Create a column of messy full names with inconsistent spacing/casing (e.g., `"  john SMITH"`, `"JANE doe  "`). Clean them with a single `=TRIM(PROPER(A1))` formula.
2. Split a "Full Name" column into "First Name" and "Last Name" using both a formula approach (`LEFT`/`FIND`/`MID`) and `Text to Columns` — compare the results.
3. Create a dataset with 20 rows, deliberately including 5 exact duplicate rows. Use `Data → Remove Duplicates` on a COPY, and separately use `=UNIQUE()` on the original — compare outputs.
4. Set up a dropdown list (Data Validation) for a "Status" column with options `Open, In Progress, Closed`. Try typing an invalid value manually and confirm Excel rejects it.
5. Practice Flash Fill: type a column of full addresses, manually extract the ZIP code for the first 2 rows, then press `Ctrl+E` to fill the rest.
6. Create a formula that divides two columns where some denominators are 0. Wrap it in `IFERROR` to replace the `#DIV/0!` with `0` or a custom message.

✅ Done? Move to `03-Formulas-and-Functions`.
