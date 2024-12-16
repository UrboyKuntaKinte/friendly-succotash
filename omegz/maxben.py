######
######
######
###### this code from the jao maxben thing where im fetching data from mid 2022 to today. im printing out first 5 rows,
###### 5 middle rows and 5 end rows. in total ther are 24000 +  rows 

import requests
import pandas as pd

def fetch_data(url):
    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("data", [])

        # Convert the JSON data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Print the columns for debugging purposes
        print("Columns in the dataset:", df.columns.tolist())

        # Print the number of rows and columns
        print(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

        # Print the first 5 rows
        print("First 5 rows of the dataset:")
        print(df.head())

        # Print the middle 5 rows
        middle_idx = len(df) // 2
        print("Middle 5 rows of the dataset:")
        print(df.iloc[middle_idx-2:middle_idx+3])

        # Print the last 5 rows
        print("Last 5 rows of the dataset:")
        print(df.tail())

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error making the GET request: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Updated URL
url = "https://parallelrun-publicationtool.jao.eu/nordic/api/data/maxExchanges?FromUtc=2022-01-06T23%3A00%3A00.000Z&ToUtc=2024-12-15T23%3A00%3A00.000Z"
df = fetch_data(url)


############
############
############
############

## LOOK HERE G

# HOW TO RUN THIS FILE:

# IN TERMINAL (CMD + J)

# YOU CAN WRITE CD OMEGZ (THIS TAKES YOU INTO THE OMEGZ FILE)

# THEN RUN python3 maxben.py

###### OTHERWISE ########

# python3 omegz/maxben.py





