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
