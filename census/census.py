
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv("CENSUS_API_KEY")

# Define the API endpoint and parameters
base_url = "https://api.census.gov/data/2022/acs/acs5"

# Define the variables we need
variables = ["B19013_001E", "B17001_001E", "B17001_002E", "NAME"]

# Define the Maryland counties we want data for
md_counties = {
  "001": "Allegany", "003": "Anne Arundel", "005": "Baltimore", "009": "Calvert",
  "011": "Caroline", "013": "Carroll", "015": "Cecil", "017": "Charles",
  "019": "Dorchester", "021": "Frederick", "023": "Garrett", "025": "Harford",
  "027": "Howard", "029": "Kent", "031": "Montgomery", "033": "Prince Georges",
  "035": "Queen Annes", "037": "St. Marys", "039": "Somerset", "041": "Talbot",
  "043": "Washington", "045": "Wicomico", "047": "Worcester", "510": "Baltimore City"
}

# Construct the API request URL
counties = ",".join([f"24{code}" for code in md_counties.keys()])
url = f"{base_url}?get={','.join(variables)}&for=county:{counties}&in=state:24&key={api_key}"

# Make the API request
response = requests.get(url)
data = response.json()

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Convert numeric columns to float
numeric_cols = ["B19013_001E", "B17001_001E", "B17001_002E"]
df[numeric_cols] = df[numeric_cols].astype(float)

# Calculate poverty rate
df["poverty_rate"] = df["B17001_002E"] / df["B17001_001E"] * 100

# Calculate Economic Need Index
max_income = df["B19013_001E"].max()
min_income = df["B19013_001E"].min()
max_poverty = df["poverty_rate"].max()
min_poverty = df["poverty_rate"].min()

df["income_index"] = (max_income - df["B19013_001E"]) / (max_income - min_income)
df["poverty_index"] = (df["poverty_rate"] - min_poverty) / (max_poverty - min_poverty)
df["economic_need_index"] = (df["income_index"] + df["poverty_index"]) / 2

# Sort by Economic Need Index in descending order
df = df.sort_values("economic_need_index", ascending=False)

# Select and rename columns for final output
result = df[["NAME", "B19013_001E", "poverty_rate", "economic_need_index"]]
result.columns = ["County", "Median Household Income", "Poverty Rate (%)", "Economic Need Index"]

# Display the results
print(result.to_string(index=False))
