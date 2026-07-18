# Case Studies (Live-Task-Style Interview Questions)

Many Data Analyst interviews include a hands-on Excel task or a "walk me through how you'd approach this" scenario question. Practice these.

## Case 1: "Here's a messy sales export. Clean it and tell me our top-performing region."
**Approach to demonstrate**:
1. Inspect the data first — check for blank rows, inconsistent formats, duplicate transactions, obviously wrong values (negative revenue, impossible dates).
2. Clean via Power Query (or formulas if Power Query isn't available): fix data types, remove duplicates, handle blanks.
3. Build a PivotTable: Sum of Revenue by Region.
4. Sort descending, identify the top region.
5. **Bonus (shows seniority)**: sanity-check the result — does the top region also have the most transactions, or just a few outlier large deals? A good analyst questions their own first answer before presenting it.

## Case 2: "Build a formula to flag customers who haven't ordered in 90+ days."
**Approach**:
```excel
=IF(TODAY() - [LastOrderDate] > 90, "Inactive", "Active")
```
Discuss: what if `LastOrderDate` is blank (never ordered)? Handle that edge case explicitly (`IF(LastOrderDate="", "Never Ordered", ...)`) — interviewers specifically watch for whether candidates consider edge cases unprompted.

## Case 3: "Our monthly report takes 3 hours to build manually. How would you speed it up?"
**Approach to discuss**:
1. Identify what's actually repetitive vs. genuinely new each month.
2. Propose Power Query for automatic data cleaning/reshaping (eliminates manual cleaning steps).
3. Propose PivotTables/Power Pivot + DAX measures instead of manually rebuilt formulas each month (refresh-and-done workflow).
4. Consider a macro for any remaining manual formatting steps.
5. Frame the answer around **time saved and error reduction**, not just "using fancier features" — interviewers want to see you connect tools to real business value.

## Case 4: "Explain a time you found an error in a dataset or model. What did you do?"
**Approach**: this is a behavioral question testing rigor/integrity, not a pure Excel-skills question. Structure your answer: what you noticed (a specific red flag — numbers not tying out, an implausible value), how you investigated (traced back through formulas/source data), what you found (the root cause), and what you changed afterward (e.g., added a validation check or reconciliation step to catch it earlier next time).

## Case 5: "Walk me through how you'd build a KPI dashboard for [some business, e.g., a coffee shop chain] from scratch."
**Approach to structure your answer**:
1. Start with the business question/audience: who's viewing this, and what decision does it inform?
2. Identify 3-5 KPIs that actually matter for that audience (not everything you COULD measure).
3. Describe your data source and cleaning approach.
4. Describe your calculation approach (PivotTables vs. Power Pivot/DAX, depending on data complexity/scale).
5. Describe your visual layout, referencing chart-type reasoning and design best practices.
6. Mention how you'd keep it updated/refreshable going forward.

**General interview tip**: for any live task, narrate your thinking out loud as you work — interviewers are evaluating your process and judgment at least as much as the final correct answer.
