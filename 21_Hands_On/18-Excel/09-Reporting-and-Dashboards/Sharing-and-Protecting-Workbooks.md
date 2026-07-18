# Sharing & Protecting Workbooks

## What is it?
Excel's tools for controlling who can edit what, protecting formulas from accidental changes, and sharing workbooks safely and collaboratively.

## Why care?
A report that gets accidentally overwritten or has a formula silently broken by a well-meaning colleague undermines trust and creates real business risk — protection features are a practical safeguard analysts should know how to apply.

## Protect Sheet vs Protect Workbook
- **Protect Sheet** (Review → Protect Sheet): locks cells from editing (by default, ALL cells are locked when sheet protection is applied — you must explicitly unlock any cells you want to remain editable, via Format Cells → Protection → uncheck "Locked," BEFORE turning on protection).
- **Protect Workbook** (Review → Protect Workbook): prevents structural changes — adding/deleting/renaming/moving sheets.

## Unlocking specific input cells (the common real pattern)
1. Select the cells that SHOULD remain editable (e.g., assumption inputs in a model).
2. `Ctrl+1` → Protection tab → uncheck **Locked**.
3. THEN apply **Review → Protect Sheet** — now everything is locked EXCEPT the cells you explicitly unlocked.

## Password protection
Both sheet and workbook protection can require a password to remove — useful for controlling who can un-protect and edit the underlying formulas, though it's worth knowing Excel's built-in protection is a deterrent against casual mistakes, not robust security against a determined attacker.

## Read-only recommendations
**File → Save As → Tools → General Options → "Read-only recommended"** — prompts anyone opening the file to consider opening as read-only, a lightweight nudge to prevent accidental edits without full password protection.

## Sharing considerations (real-world workflow)
- **Cloud co-authoring** (OneDrive/SharePoint-hosted files): multiple people can edit simultaneously with live updates — the modern default for team collaboration, replacing older "shared workbook" legacy features.
- **Version history**: cloud-hosted files keep automatic version history (**File → Info → Version History**) — a safety net if something gets accidentally broken, letting you restore a prior version without needing your own manual backups.
- **Before sending externally**: use **File → Info → Inspect Document** to check for and remove hidden data, personal information, or leftover comments before sharing a workbook outside your organization.

## Practical example
A shared budget model: assumption cells (growth rate, headcount plan) are left unlocked and highlighted yellow so users know exactly what they're meant to edit; every other cell (all the underlying formulas) is locked via Protect Sheet — this prevents the all-too-common real-world incident of someone accidentally typing over a formula cell and silently breaking the entire model without anyone noticing until numbers look wrong weeks later.
