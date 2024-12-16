import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_data(url):
    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("data", [])

        # Convert the JSON data to a pandas DataFrame
        df = pd.DataFrame(data)

        # Expand the 'pages' list into a comma-separated string for readability
        if "pages" in df:
            df["pages"] = df["pages"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

        # Print the columns for debugging purposes
        print("Columns in the dataset:", df.columns.tolist())

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error making the GET request: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def preprocess_and_plot_time_series(url):
    # Fetch the data
    df = fetch_data(url)

    # Check if required columns exist
    required_columns = ["minFlow", "maxFlow", "flowFb", "fall", "biddingZoneFrom", "biddingZoneTo", "dateTimeUtc"]
    if not all(col in df.columns for col in required_columns):
        print("Missing required columns in the dataset.")
        return

    # Filter rows where biddingZoneFrom equals biddingZoneTo
    df = df[df["biddingZoneFrom"] != df["biddingZoneTo"]]

    # Adjust flowFb by subtracting fall
    df["flowFb"] = df["flowFb"] - df["fall"]

    # Convert timestamp to datetime
    df["dateTimeUtc"] = pd.to_datetime(df["dateTimeUtc"], errors="coerce")

    # Filter out rows with missing timestamps
    df = df.dropna(subset=["dateTimeUtc"])

    # Create a time-series plot for each combination of biddingZoneFrom and biddingZoneTo
    combinations = df.groupby(["biddingZoneFrom", "biddingZoneTo"])

    for (zone_from, zone_to), group in combinations:
        plt.figure(figsize=(12, 6))

        # Add a thick horizontal line at zero without adding it to the legend
        plt.axhline(0, color="black", linewidth=2)

        # Plot flowFb as thick bars
        plt.bar(group["dateTimeUtc"], group["flowFb"], width=0.01, color="blue", alpha=0.7, label=f"FlowFb ({zone_from} to {zone_to})")

        # Plot minFlow and maxFlow as step lines
        plt.step(group["dateTimeUtc"], group["minFlow"], label=f"MinFlow ({zone_from} to {zone_to})", linestyle="--", color="green", where="mid")
        plt.step(group["dateTimeUtc"], group["maxFlow"], label=f"MaxFlow ({zone_from} to {zone_to})", linestyle="--", color="red", where="mid")

        plt.title(f"Time Series for {zone_from} to {zone_to}")
        plt.xlabel("Timestamp")
        plt.ylabel("Flow Values")
        plt.legend(loc="lower left")
        plt.tight_layout()
        plt.show()

# Updated URL
url = "https://publicationtool.jao.eu/nordic/api/data/fbDomainShadowPrice?Filter=%7B%22Tso%22%3A%5B%2210X1001A1001A248%22%5D%2C%22NonRedundant%22%3Atrue%7D&Skip=0&Take=450000&FromUtc=2024-10-28T23%3A00%3A00.000Z&ToUtc=2024-12-17T00%3A00%3A00.000Z"
preprocess_and_plot_time_series(url)

############
############
############
############

## LOOK HERE G

# HOW TO RUN THIS FILE:

# IN TERMINAL (CMD + J)

# YOU CAN WRITE CD OMEGZ (THIS TAKES YOU INTO THE OMEGZ FILE)

# THEN RUN python3 timeseries.py

###### OTHERWISE ########

# python3 omegz/timeseries.py


