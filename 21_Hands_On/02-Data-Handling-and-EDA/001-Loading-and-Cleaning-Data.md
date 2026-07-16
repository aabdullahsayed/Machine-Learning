# 001 - Loading and Cleaning Data

## Concept
Real data is messy: wrong types, inconsistent formatting, duplicate rows, and encoding issues. Loading and cleaning is the first, unglamorous, and most important step of any ML pipeline — garbage in, garbage out.

## Why It Matters
No model can compensate for badly cleaned input data. This lesson sets up the dataset you'll reuse conceptually across missing values (002), outliers (003), EDA (004), and splitting (005).

## Hands-On

```python
import pandas as pd
import numpy as np
import io

# Simulate a messy raw CSV (typical of real-world exports)
raw_csv = """id,name,age,salary,signup_date,active
1,Alice,25,50000,2022-01-15,Yes
2, bob ,32,62000.5,2022-03-22,yes
3,Carol,forty-five,58000,2022-05-01,No
4,Dave,29,,2022-07-11,Yes
5,Alice,25,50000,2022-01-15,Yes
6,Eve,-5,71000,not_a_date,No
"""

df = pd.read_csv(io.StringIO(raw_csv))
print(df)
print(df.dtypes)

# 1. Fix inconsistent text formatting
df["name"] = df["name"].str.strip().str.title()

# 2. Fix inconsistent categorical casing
df["active"] = df["active"].str.strip().str.lower().map({"yes": True, "no": False})

# 3. Coerce numeric columns, turning invalid entries into NaN instead of crashing
df["age"] = pd.to_numeric(df["age"], errors="coerce")

# 4. Parse dates, invalid ones become NaT (Not a Time)
df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")

# 5. Remove impossible values (negative age)
df.loc[df["age"] < 0, "age"] = np.nan

# 6. Remove exact duplicate rows
print("Duplicates found:", df.duplicated().sum())
df = df.drop_duplicates()

# 7. Check the cleaned result
print("\nCleaned DataFrame:")
print(df)
print(df.dtypes)
print("\nRemaining missing values:\n", df.isna().sum())
```

## Exercise
1. Add a `country` column with mixed-case entries like `"usa"`, `"USA"`, `"U.S.A"` and write code to standardize them to one value.
2. Detect rows where `signup_date` failed to parse and print just those rows.
3. Write a reusable function `clean_dataframe(df, numeric_cols, date_cols)` that applies the coercion steps above generically.

## Key Takeaways
- `errors="coerce"` is your friend: it converts unparseable values to NaN/NaT instead of crashing the whole pipeline.
- Always check `.dtypes` after loading — a numeric column stored as `object` (string) will silently break downstream math.
- Clean before you explore: EDA (004) on dirty data gives misleading plots and statistics.
