import requests
import pandas as pd
from IPython.display import display, HTML

# School District Characteristics 2022-23 https://data-nces.opendata.arcgis.com/datasets/nces::school-district-characteristics-2022-23/about


# Define the URL for the API query
url = "https://nces.ed.gov/opengis/rest/services/School_District_Boundaries/EDGE_ADMINDATA_SCHOOLDISTRICTS_SY2223/MapServer/1/query"

# Define the parameters for the query
params = {
    'outFields': '*',
    'where': "statename='MARYLAND'",
    'f': 'geojson'
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Extract the features from the GeoJSON
features = data['features']

# Convert the features into a pandas DataFrame
rows = [feature['properties'] for feature in features]
df = pd.DataFrame(rows)

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
# SCH = School Count =  number of schools in the LEA | MEMBER = Total students

# Define the path to save the CSV file
csv_file_path = 'maryland_school_districts.csv'

# Export the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

# Confirmation message
print(f"DataFrame exported as '{csv_file_path}'")
