# Economic Need Index Calculation


## Overview
This Python script analyzes education-related data for Maryland counties, combining information from multiple sources to create a comprehensive dataset. The script calculates an Economic Need Index (ENI) for each county based on various economic indicators.

## Methodology
### Median Household Income (MHI) Normalization
Normalize the median household income data on a scale from 1 to 10, where 1 represents the highest income (lowest need) and 10 represents the lowest income (highest need).
Normalization Formula: 
MHIn = 10 x (1 - ( MHI - MHImin/ MHImax-MHImin)
Where:
MHIn = Median Household Income for the LEA
MHImin = Minimum Median Household Income among all LEAs
MHImax= Maximum Median Household Income among all LEAs
### Percentage of Population Below Poverty Line (Poverty Rate) Normalization
Normalize the poverty rate data on a scale from 1 to 10, where 1 represents the lowest poverty rate (lowest need) and 10 represents the highest poverty rate (highest need).
Normalization Formula: 
Normalized Poverty Rate=10 x (Poverty Rate - Poverty Ratemin/ Poverty Rate max - Poverty Rate min)
Where:
Poverty Rate = Percentage of Population Below Poverty Line for the LEA
Poverty Rate Min = Minimum Poverty Rate among all LEAs
Poverty RateMax = Maximum Poverty Rate among all LEAs
### Unemployment Rate (UR) Normalization
Normalize the unemployment rate data on a scale from 1 to 10, where 1 represents the lowest unemployment rate (lowest need) and 10 represents the highest unemployment rate (highest need).
Normalization Formula: 
Normalized UR=10×(UR−URmin/ URmax− URmin)
Where: 
UR = Unemployment Rate for the LEA
URmin = Minimum Unemployment Rate among all LEAs
URmax = Maximum Unemployment Rate among all LEAs
### Calculating the Economic Need Index (ENI)
ENI = (MHIN + Normalized Poverty Rate + Normalized UR) / 3 


## Data Sources
1. School District Characteristics (2022-23) from NCES
2. Census Data (2022 ACS 5-year estimates)
3. Unemployment Rate Data (2020-2023) from Maryland Manual

## Dependencies
- requests
- pandas
- IPython

## Key Features
1. Fetches school district data for Maryland from NCES API
2. Retrieves census data for Maryland counties from the Census API
3. Incorporates unemployment rate data for Maryland counties
4. Calculates an Economic Need Index (ENI) based on:
 - Normalized Median Household Income
 - Normalized Poverty Rate
 - Normalized Unemployment Rate
5. Merges all datasets into a single DataFrame
6. Exports the final merged data to a CSV file

## How it works
1. The script starts by fetching school district data for Maryland using the NCES API.
2. It then retrieves census data for Maryland counties using the Census API.
3. Unemployment rate data is incorporated from a multi-line string (could be replaced with API call or file read).
4. The script calculates various normalized economic indicators and the ENI.
5. All datasets are merged based on county names.
6. The final merged dataset is displayed in an interactive HTML table and exported as a CSV file.

## Output
- An interactive HTML table displaying the merged data
- A CSV file named 'final_merged_data.csv' containing all the merged data

## Note
Make sure you have the required libraries installed and proper API access for the NCES and Census data. The unemployment data in this script is hardcoded since MSA does not have an API (https://msa.maryland.gov/msa/mdmanual/01glance/economy/html/unemployrates.html). 

Feel free to ask if you have any questions about the script or need help modifying it for your specific needs!
