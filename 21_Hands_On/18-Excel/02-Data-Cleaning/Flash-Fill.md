# Flash Fill

## What is it?
Excel's pattern-recognition feature — type an example of the output you want, and Excel automatically detects the pattern and fills the rest of the column for you, no formula needed.

## Why care?
For simple text transformations, Flash Fill is often faster than writing a formula — genuinely one of the best-kept-secret productivity tools in Excel for data cleaning.

## How to use it
1. In a column next to your messy data, type the **desired result** for the first 1-2 rows manually.
2. Press `Ctrl+E` (or `Data → Flash Fill`).
3. Excel detects the pattern from your example(s) and fills in the rest automatically.

## Common use cases
### Splitting combined data
```
Column A (raw):        Column B (type this manually, then Ctrl+E):
John Smith               John
Jane Doe                  Jane
```
Flash Fill detects "extract first word" and fills the rest.

### Combining data
```
A: John      B: Smith      C (type manually): John Smith
```
Ctrl+E fills the rest by combining columns A and B the same way.

### Reformatting
```
A: 2026-07-17    C (type manually): 07/17/2026
```
Flash Fill can detect and apply date reformatting patterns too.

### Extracting a substring pattern
```
A: INV-2026-0042    C (type manually): 0042
```
Detects "extract the last 4 digits" pattern from your example.

## Limitations (why you still need formulas too)
- Flash Fill is a **one-time, static** action — if your source data changes later, Flash Fill results do NOT update automatically (unlike a formula, which recalculates live).
- Works best with clearly consistent patterns — messy/inconsistent source data can confuse it, requiring formulas (`Text-Functions.md`) for reliable, repeatable cleaning instead.

## Practical example
Given a raw "Full Address" column, quickly extract just the ZIP code by typing the ZIP for the first 2-3 rows manually, then `Ctrl+E` — much faster than writing a `RIGHT()`/`MID()` formula for a one-off cleanup task, though for a REPEATABLE pipeline (e.g., refreshed monthly), a real formula or Power Query step is the better long-term choice.
