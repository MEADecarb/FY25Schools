import requests
import pandas as pd
from IPython.display import display, HTML, FileLink

# School District Characteristics 2022-23
url_school_districts = "https://nces.ed.gov/opengis/rest/services/School_District_Boundaries/EDGE_ADMINDATA_SCHOOLDISTRICTS_SY2223/MapServer/1/query"
params = {
    'outFields': '*',
    'where': "statename='MARYLAND'",
    'f': 'geojson'
}

response_school_districts = requests.get(url_school_districts, params=params)
data_school_districts = response_school_districts.json()
features = data_school_districts['features']
rows = [feature['properties'] for feature in features]
df_school_districts = pd.DataFrame(rows)

# Inspect columns of the school districts DataFrame
print("School District Columns:", df_school_districts.columns)

# Census Data
url_census = "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E,B17001_001E,B17001_002E&for=county:*&in=state:24"
response_census = requests.get(url_census)
data_census = response_census.json()
columns = ["NAME", "Median Household Income", "Total Population", "Population below poverty level", "state", "county"]
df_census = pd.DataFrame(data_census[1:], columns=columns)
df_census = df_census.drop(columns=["state", "county"])
df_census["Median Household Income"] = pd.to_numeric(df_census["Median Household Income"])
df_census["Total Population"] = pd.to_numeric(df_census["Total Population"])
df_census["Population below poverty level"] = pd.to_numeric(df_census["Population below poverty level"])

# Remove ", Maryland" from the "NAME" column in the Census Data DataFrame
df_census["NAME"] = df_census["NAME"].str.replace(", Maryland", "", regex=False)

# Inspect columns of the census DataFrame
print("Census Data Columns:", df_census.columns)

# Find a common column to merge on (assuming 'NAME' might need alignment)
if 'NAME' not in df_school_districts.columns:
    df_school_districts.rename(columns={"CONAME": "NAME"}, inplace=True)

# Merge DataFrames on the "NAME" column
df_merged = pd.merge(df_school_districts, df_census, on="NAME", how="inner")

# Display the merged DataFrame with scrolling enabled
display(HTML(df_merged.to_html(notebook=True, table_id="dataframe_merged", border=0)))

# Add some CSS to make the table scrollable
display(HTML("""
<style>
    #dataframe_merged {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
</style>
"""))

# Export the merged DataFrame to a CSV file
csv_file_merged = 'merged_data.csv'
df_merged.to_csv(csv_file_merged, index=False)

# Display link to download the CSV file
display(FileLink(csv_file_merged, result_html_prefix="Click here to download the merged CSV file: "))

# Confirmation message
print(f"Merged DataFrame exported as '{csv_file_merged}'")
