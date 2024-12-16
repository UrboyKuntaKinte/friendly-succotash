import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_elspot_prices():
    # API endpoint
    url = "https://api.energidataservice.dk/dataset/Elspotprices"

    # Parameters to request maximum data
    params = {
        'limit': 450000  # Large limit to fetch a substantial amount of records
    }

    try:
        # Make a GET request to the API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the JSON response
        data = response.json()

        # Extract records from the response
        records = data.get('records', [])

        # Convert to DataFrame
        df = pd.DataFrame(records)

        return df

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def create_violin_plot():
    # Fetch the data
    df = fetch_elspot_prices()

    # Check if required columns exist
    required_columns = ['SpotPriceEUR', 'HourDK', 'PriceArea']
    if not all(col in df.columns for col in required_columns):
        print("Missing required columns in the dataset.")
        return

    # Filter for only DK1 and DK2 areas
    df = df[df['PriceArea'].isin(['DK1', 'DK2'])]

    # Convert HourDK to datetime and extract the year
    df['HourDK'] = pd.to_datetime(df['HourDK'], errors='coerce')
    df['Year'] = df['HourDK'].dt.year

    # Filter for data from 2018 onwards
    df = df[df['Year'] >= 2018]

    # Filter out rows with missing values in required columns
    df = df.dropna(subset=['SpotPriceEUR', 'Year', 'PriceArea'])

    # Create the violin plot
    plt.figure(figsize=(16, 8))
    sns.violinplot(
        data=df,
        x='Year',
        y='SpotPriceEUR',
        hue='PriceArea',
        split=True,
        inner='quart',  # Adds quartiles to the plot for more detail
        scale='width',  # Makes the width proportional to the number of observations
        palette="coolwarm"
    )

    plt.title("Prisfordeling for DK1 og DK2 ", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("EUR/MWh)", fontsize=14)
    plt.legend(title="Price Area", fontsize=12)
    plt.tight_layout()
    plt.show()

# Fetch and display the data
df = fetch_elspot_prices()
print(df)

# Create the violin plot
create_violin_plot()