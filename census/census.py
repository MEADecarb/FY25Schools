import requests
import pandas as pd
from IPython.display import display, HTML
from IPython.display import FileLink

# Define the API endpoint
url = "https://api.census.gov/data/2022/acs/acs5?get=NAME,B19013_001E,B17001_001E,B17001_002E&for=county:*&in=state:24"

# Make the API request
response = requests.get(url)
data = response.json()

# Create a DataFrame from the response data
columns = ["NAME", "Median Household Income", "Total Population", "Population below poverty level", "state", "county"]
df = pd.DataFrame(data[1:], columns=columns)

# Drop the 'state' and 'county' columns as they are not needed
df = df.drop(columns=["state", "county"])

# Convert numeric columns to appropriate data types
df["Median Household Income"] = pd.to_numeric(df["Median Household Income"])
df["Total Population"] = pd.to_numeric(df["Total Population"])
df["Population below poverty level"] = pd.to_numeric(df["Population below poverty level"])

# Save the DataFrame to a CSV file
csv_file = "/content/data.csv"
df.to_csv(csv_file, index=False)

# Display the DataFrame with scrolling enabled
display(HTML(df.to_html(notebook=True, table_id="dataframe", border=0)))

# Add some CSS to make the table scrollable
display(HTML("""
<style>
    #dataframe {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
</style>
"""))

# Display the link to download the CSV file
display(FileLink(csv_file, result_html_prefix="Click here to download the CSV file: "))
