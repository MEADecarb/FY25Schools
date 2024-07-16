import requests
import pandas as pd
from IPython.display import display, HTML, FileLink
from io import StringIO

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

# Unemployment Rate Data as a multi-line string, from https://msa.maryland.gov/msa/mdmanual/01glance/economy/html/unemployrates.html
data = """
2020\t2021\t2022\t2023
Maryland\t6.5%\t5.3%\t3.2%\t2.1%
Allegany County\t7.5%\t5.9%\t4.0%\t2.8%
Anne Arundel County\t5.6%\t4.4%\t2.8%\t1.8%
Baltimore City\t8.5%\t7.0%\t4.3%\t2.9%
Baltimore County\t6.6%\t5.2%\t3.3%\t2.2%
Calvert County\t5.0%\t4.2%\t2.9%\t1.9%
Caroline County\t5.4%\t4.5%\t3.1%\t2.1%
Carroll County\t4.9%\t3.9%\t2.7%\t1.7%
Cecil County\t5.7%\t4.8%\t3.3%\t2.2%
Charles County\t6.4%\t5.3%\t3.3%\t2.2%
Dorchester County\t6.3%\t5.3%\t3.6%\t2.3%
Frederick County\t5.6%\t4.4%\t3.0%\t2.0%
Garrett County\t6.4%\t4.9%\t3.5%\t2.3%
Harford County\t5.5%\t4.4%\t3.0%\t2.0%
Howard County\t4.9%\t4.0%\t2.6%\t1.7%
Kent County\t6.3%\t5.1%\t3.6%\t2.4%
Montgomery County\t6.1%\t5.1%\t2.9%\t1.9%
Prince George's County\t7.8%\t6.8%\t3.5%\t2.2%
Queen Anne's County\t5.2%\t4.0%\t2.8%\t1.8%
St. Mary's County\t4.6%\t4.1%\t3.1%\t2.0%
Somerset County\t8.1%\t6.9%\t4.8%\t3.2%
Talbot County\t5.8%\t5.0%\t3.4%\t2.2%
Washington County\t6.6%\t5.0%\t3.3%\t2.3%
Wicomico County\t7.2%\t5.6%\t3.8%\t2.5%
Worcester County\t10.9%\t7.5%\t5.0%\t3.3%
"""

# Read the unemployment data into a pandas DataFrame
df_unemployment = pd.read_csv(StringIO(data), sep='\t', index_col=0)

# Select only the 2023 column
df_unemployment_2023 = df_unemployment[['2023']]

# Remove the "%" character and convert to float
df_unemployment_2023.loc[:, '2023'] = df_unemployment_2023['2023'].str.replace('%', '').astype(float)

# Rename the unemployment column
df_unemployment_2023 = df_unemployment_2023.rename(columns={'2023': 'Annual Unemployment Rate (%)'})

# Merge the unemployment DataFrame with the census DataFrame on the "NAME" column
df_census = df_census.rename(columns={"NAME": "County"})
df_merged = pd.merge(df_census, df_unemployment_2023, left_on="County", right_index=True, how="inner")

# Economic Need Index (ENI) Calculation

# Median Household Income Normalization
MHImin = df_merged["Median Household Income"].min()
MHImax = df_merged["Median Household Income"].max()
df_merged["MHIN"] = 10 * (1 - (df_merged["Median Household Income"] - MHImin) / (MHImax - MHImin))

# Poverty Rate Normalization
PovertyRate = df_merged["Population below poverty level"] / df_merged["Total Population"] * 100
PovertyRate_min = PovertyRate.min()
PovertyRate_max = PovertyRate.max()
df_merged["Normalized Poverty Rate"] = 10 * (PovertyRate - PovertyRate_min) / (PovertyRate_max - PovertyRate_min)

# Unemployment Rate Normalization
UR_min = df_merged["Annual Unemployment Rate (%)"].min()
UR_max = df_merged["Annual Unemployment Rate (%)"].max()
df_merged["Normalized UR"] = 10 * (df_merged["Annual Unemployment Rate (%)"] - UR_min) / (UR_max - UR_min)

# Calculating the Economic Need Index (ENI)
df_merged["ENI"] = (df_merged["MHIN"] + df_merged["Normalized Poverty Rate"] + df_merged["Normalized UR"]) / 3

# Use "LEA_NAME" or "CONAME" to merge the school district DataFrame with the combined DataFrame
df_final_merged = pd.merge(df_school_districts, df_merged, left_on="CONAME", right_on="County", how="inner")

# Display the merged DataFrame with scrolling enabled
display(HTML(df_final_merged.to_html(notebook=True, table_id="dataframe_final_merged", border=0)))

# Add some CSS to make the table scrollable
display(HTML("""
<style>
    #dataframe_final_merged {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
</style>
"""))

# Export the merged DataFrame to a CSV file
csv_file_final_merged = 'final_merged_data.csv'
df_final_merged.to_csv(csv_file_final_merged, index=False)

# Display link to download the CSV file
display(FileLink(csv_file_final_merged, result_html_prefix="Click here to download the merged CSV file: "))

# Confirmation message
print(f"Merged DataFrame exported as '{csv_file_final_merged}'")
