# Maryland School Districts Data

This subfolder contains a Python script to fetch, display, and export data on school districts in Maryland from the National Center for Education Statistics (NCES) API.

##URL
https://data-nces.opendata.arcgis.com/datasets/nces::school-district-characteristics-2022-23/about

## Files

- `opendata.py`: The main Python script to fetch and process the data.
- `requirements.txt`: A list of required Python packages to run the script.

## Setup

To set up the environment and run the script, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository/subfolder
    ```

2. **Create a virtual environment (optional but recommended):**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the script:**

    ```sh
    python fetch_maryland_school_districts.py
    ```

## Script Details

### `fetch_maryland_school_districts.py`

This script performs the following steps:
1. Fetches data from the NCES API on school districts in Maryland.
2. Converts the data into a pandas DataFrame.
3. Displays the data in an interactive, scrollable table using IPython widgets.
4. Exports the data to a CSV file (`maryland_school_districts.csv`).

#### Key Sections of the Script:

- **Imports and Setup:**
    ```python
    import requests
    import pandas as pd
    from IPython.display import display, HTML
    ```

- **API Request:**
    ```python
    url = "https://nces.ed.gov/opengis/rest/services/School_District_Boundaries/EDGE_ADMINDATA_SCHOOLDISTRICTS_SY2223/MapServer/1/query"
    params = {
        'outFields': '*',
        'where': "statename='MARYLAND'",
        'f': 'geojson'
    }
    response = requests.get(url, params=params)
    data = response.json()
    ```

- **Data Processing:**
    ```python
    features = data['features']
    rows = [feature['properties'] for feature in features]
    df = pd.DataFrame(rows)
    ```

- **Displaying Data:**
    ```python
    display(HTML(df.to_html(notebook=True, table_id="dataframe", border=0)))
    display(HTML("""
    <style>
        #dataframe {
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }
    </style>
    """))
    ```

- **Exporting Data:**
    ```python
    csv_file_path = 'maryland_school_districts.csv'
    df.to_csv(csv_file_path, index=False)
    print(f"DataFrame exported as '{csv_file_path}'")
    ```

## Dependencies

- `requests`
- `pandas`
- `ipython`

These dependencies are listed in the `requirements.txt` file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or comments, please open an issue or contact [your name](mailto:your.email@example.com).

