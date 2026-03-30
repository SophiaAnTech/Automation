import pandas as pd

# Load CSV
df = pd.read_csv("messy_data.csv")

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing values
df = df.fillna({
    "name": "Unknown",
    "email": "noemail@example.com",
    "age": df["age"].median()
})

# Clean text fields
df["name"] = df["name"].str.title().str.strip()
df["email"] = df["email"].str.lower().str.strip()

# Save cleaned data
df.to_csv("cleaned_data.csv", index=False)

print("Data cleaned and saved to cleaned_data.csv")
