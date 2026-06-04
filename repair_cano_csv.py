# When initially loading the csv, encoding error caused some characters to be misinterpreted, resulting in mojibake.
# This script uses ftfy to fix the text and includes a manual patch for one remaining corrupted row.
# It saves the cleaned dataset to a new CSV file.

import pandas as pd
import ftfy

df = pd.read_csv(
    r"C:\Users\tyler\OneDrive\Desktop\School\CSE 143\MoodyLyrics4Q\MoodyLyrics4Q_UTF8.csv",
    encoding="latin1"
)

# Fix BOM
df.columns = [col.replace("\ufeff", "") for col in df.columns]

# Apply ftfy to ALL text columns
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].apply(lambda x: ftfy.fix_text(x) if isinstance(x, str) else x)

# Manual patch for the one remaining corrupted row
df.loc[df['title'] == "MÃ¥ndagsbarn", 'title'] = "Måndagsbarn"


# Show any remaining mojibake
print(df[df.apply(lambda row: row.astype(str).str.contains("Ã").any(), axis=1)])

df.to_csv("moodylyrics_clean.csv", index=False, encoding="utf-8")
