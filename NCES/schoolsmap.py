import requests
import pandas as pd
from IPython.display import display, HTML

# Define the URL for the API query
url = "https://nces.ed.gov/opengis/rest/services/K12_School_Locations/EDGE_GEOCODE_PUBLICSCH_2223/MapServer/0/query"

# Define the parameters for the query
params = {
    'outFields': '*',
    'where': "STFIP='24'",  # Filter for Maryland (STFIP=24)
    'f': 'json',
    'returnGeometry': 'false'  # We don't need the geometry data
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Check if 'features' key exists in the response
if 'features' not in data:
    print("Error: 'features' not found in the API response.")
    print("API response:", data)
else:
    # Extract the features from the JSON
    features = data['features']

    # Convert the features into a pandas DataFrame
    rows = [feature['attributes'] for feature in features]
    df = pd.DataFrame(rows)

    # Display the DataFrame with scrolling enabled
    display(HTML(df.to_html(notebook=True, table_id="dataframe", border=0)))

    # Add some CSS to make the table scrollable
    display(HTML("""
    <style>
    #dataframe {
        width: 100%;
        max-height: 500px;
        overflow: auto;
        display: block;
    }
    </style>
    """))

    # Define the path to save the CSV file
    csv_file_path = 'maryland_schools.csv'

    # Export the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    # Confirmation message
    print(f"DataFrame exported as '{csv_file_path}'")
    print(f"Number of schools found: {len(features)}")

import requests
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Define the URL for the API query
url = "https://nces.ed.gov/opengis/rest/services/K12_School_Locations/EDGE_GEOCODE_PUBLICSCH_2223/MapServer/0/query"

# Define the parameters for the query
params = {
    'where': "STATE='MD'",  # Filter for Maryland
    'outFields': '*',
    'f': 'json'
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Extract the features from the JSON
features = data.get('features', [])

# Convert the features into a pandas DataFrame
rows = [feature['attributes'] for feature in features]
df = pd.DataFrame(rows)

# Print the column names to inspect the DataFrame structure
print("Column names:", df.columns)

# Check if the required columns are present
if 'LON' in df.columns and 'LAT' in df.columns:
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df['LON'], df['LAT']), crs="EPSG:4326"
    )

    # Create a map centered on Maryland
    m = folium.Map(location=[39.0458, -76.6413], zoom_start=8)

    # Add a marker cluster layer
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers for each school
    for idx, row in gdf.iterrows():
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=f"Name: {row['NAME']}<br>Type: {row.get('TYPE', 'N/A')}<br>Level: {row.get('LEVEL_', 'N/A')}"
        ).add_to(marker_cluster)

    # Save the map
    m.save("maryland_schools_map.html")

    # Display some information about the data
    print(f"Total number of schools: {len(df)}")
    print("\nFirst few rows of the data:")
    print(df[['NAME', 'LAT', 'LON']].head())

    # Save the data to a CSV file
    df.to_csv('maryland_schools.csv', index=False)
    print("\nData saved to 'maryland_schools.csv'")
    print("Map saved to 'maryland_schools_map.html'")
else:
    print("The required columns 'LON' and 'LAT' are not in the data.")

m

