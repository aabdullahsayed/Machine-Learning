# Chart Types — Choosing the Right One

## What is it?
Excel offers many chart types (bar, line, pie, scatter, etc.) — each is suited to a different kind of question. Choosing the wrong chart type is one of the most common data communication mistakes.

## Why care?
A chart's job is to make a pattern instantly obvious. The wrong chart type buries the insight (or actively misleads) even if the underlying data is correct — this is a real, evaluated skill in analyst roles.

## Chart type cheat sheet
| Chart type | Best for | Avoid when |
|---|---|---|
| **Column/Bar** | Comparing categories (sales by region) | Too many categories (>10-15) — gets cluttered |
| **Line** | Trends over time (revenue by month) | Comparing unrelated/non-sequential categories |
| **Pie/Donut** | Parts of a whole, FEW categories (≤5) | More than 5-6 slices — impossible to compare accurately |
| **Scatter** | Relationship between two numeric variables | Categorical data |
| **Stacked Bar/Column** | Parts of a whole ACROSS categories | Too many segments — hard to compare individual segment sizes |
| **Combo Chart** | Two different metrics with different scales (e.g., revenue + growth %) | Simple single-metric data |
| **Waterfall** | Sequential positive/negative changes (e.g., profit bridge) | Non-sequential data |
| **Box Plot** | Distribution/spread + outliers | Simple category comparisons |

## Common mistakes to avoid
- **3D charts**: distort visual perception of size/proportion — almost always avoid them in professional reporting.
- **Pie charts with many slices**: humans are bad at comparing angles; a bar chart communicates the same data more accurately with more than a handful of categories.
- **Dual Y-axes without clear labeling**: can visually mislead by aligning unrelated scales — label clearly or use a combo chart with clear legends.
- **Truncated Y-axis (not starting at 0)** on bar charts: exaggerates differences — a well-known way charts can (even unintentionally) mislead.

## Creating a chart
Select data → **Insert → Charts** group → pick a type, or use **Recommended Charts** (Excel suggests options based on your data's shape).

## Practical example
Monthly revenue over 2 years → **Line chart** (shows the trend clearly). Revenue by 5 product categories in one month → **Bar chart** (easy side-by-side comparison). Market share of top 4 competitors → **Pie chart** is acceptable here since there are few categories and the "parts of a whole" framing fits naturally.
