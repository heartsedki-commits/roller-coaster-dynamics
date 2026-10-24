import pandas as pd
import matplotlib.pyplot as plt

FILE = "survey_responses.csv"
df = pd.read_csv(FILE)

print("Responses:", len(df))
print("\nColumns:")
print(df.columns.tolist())

# Edit these column names to match the exported Google Forms CSV.
numeric_cols = [
    c for c in df.columns
    if any(k in c.lower() for k in ["smoothness", "acceleration", "g-force", "g force", "safety"])
]

for c in numeric_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

print("\nNumeric summary:")
print(df[numeric_cols].describe())

for c in numeric_cols:
    plt.figure(figsize=(7,4))
    df[c].dropna().plot(kind="hist", bins=5)
    plt.title(c)
    plt.xlabel("Rating")
    plt.tight_layout()
    plt.show()

# Example: willingness to use the app
possible = [c for c in df.columns if "use an app" in c.lower() or "app" in c.lower()]
if possible:
    print("\nApp-use responses:")
    print(df[possible[0]].value_counts())
