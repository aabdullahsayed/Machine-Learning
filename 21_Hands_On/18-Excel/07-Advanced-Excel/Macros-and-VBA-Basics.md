# Macros & VBA Basics

## What is it?
A **macro** is a recorded (or hand-written) sequence of actions that Excel can replay automatically. **VBA (Visual Basic for Applications)** is the programming language behind macros — letting you write custom logic beyond what the macro recorder alone can capture.

## Why care?
When a task is repetitive (the same 10 formatting/cleaning steps every week on a new file), a macro turns it into a single button click — genuine, measurable time savings, and a skill that stands out on a resume.

## Recording your first macro (no coding required)
1. **View → Macros → Record Macro** (or enable the Developer tab: **File → Options → Customize Ribbon → check Developer**).
2. Perform the actions you want automated (e.g., format headers, apply a filter, sort).
3. **Stop Recording**.
4. Run it anytime via **View → Macros → View Macros → Run**, or assign it to a button/keyboard shortcut.

## Reading recorded VBA (a great way to learn)
Recorded macros are viewable/editable in the **VBA Editor** (`Alt+F11`) — reading what the recorder generated is one of the best ways to learn VBA syntax organically, by seeing real generated code for actions you just performed.

## Basic VBA syntax
```vb
Sub HighlightHighSales()
    Dim cell As Range
    For Each cell In Range("B2:B100")
        If cell.Value > 10000 Then
            cell.Interior.Color = RGB(0, 255, 0)   ' green highlight
        End If
    Next cell
End Sub
```
This loops through a range and applies conditional formatting via code — the same result as `Conditional-Formatting.md`'s formula rule, but as an automatable, reusable procedure.

## Common beginner-useful VBA patterns
```vb
' Loop through all files in a folder and consolidate data
' Auto-refresh all PivotTables/queries on file open
' Export a filtered range to a new workbook, saved with today's date in the filename
' Loop through worksheets and apply the same formatting to each
```

## Practical example
Every Monday, you receive a raw export that needs: removing 2 helper columns, applying a specific header format, and sorting by date — record this once as a macro, save the workbook as a **Macro-Enabled Workbook (.xlsm)**, and from then on, running that one macro handles the entire weekly cleanup in under a second instead of a repetitive 5-minute manual chore.

**Note**: macros/VBA files can carry security risk (malicious macros are a known attack vector) — only enable/run macros from files you trust, and be aware that recipients of your `.xlsm` files may see a security warning by default.
