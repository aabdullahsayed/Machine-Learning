# Cell References (Relative, Absolute, Mixed)

## What is it?
How a formula's cell references behave when you copy/drag it to other cells — this is one of THE most important concepts in Excel, and trips up beginners constantly.

## Why care?
Getting this wrong silently produces wrong numbers across an entire report — a classic real-world Excel bug that's easy to miss.

## Relative reference (default)
```excel
=A1*2
```
If you copy this formula from `B1` to `B2`, it automatically becomes `=A2*2` — the reference "shifts" relative to where you paste it. Great for repeating the same calculation down a column of different data.

## Absolute reference (`$` locks it)
```excel
=A1*$B$1
```
`$B$1` will NEVER change no matter where you copy the formula — both the column AND row are "locked" with `$`. Essential when referencing a single fixed value (like a tax rate or exchange rate) across many rows.

## Mixed reference (lock only column OR only row)
```excel
=$A1     ' column A locked, row can change
=A$1     ' row 1 locked, column can change
```
Useful for building multiplication tables or when copying formulas both across AND down.

## The `$` shortcut
Select a reference inside a formula and press `F4` repeatedly to cycle through: `A1 → $A$1 → A$1 → $A1 → A1`.

## Practical example: applying a single tax rate to a whole column
```
      A          B              C
1   Product    Price       Tax Rate: 0.08   (in cell D1)
2   Widget     100.00      =B2*$D$1     ← locked reference to D1
3   Gadget     50.00        =B3*$D$1     ← copy down: D1 stays fixed, B shifts correctly
```
If you'd used `=B2*D1` (relative) and copied down, row 3 would incorrectly try to read `D2` (empty) instead of the tax rate in `D1` — a very common real-world spreadsheet bug.
