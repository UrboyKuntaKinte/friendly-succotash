import requests
import pandas as pd

def fetch_and_display_dataframe_with_shape(url):
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

        # Display the DataFrame
        print("=== Retrieved Data as DataFrame ===")
        print(df)

        # Print the number of rows and columns
        rows, columns = df.shape
        print(f"\nThe DataFrame has {rows} rows and {columns} columns.")

        # Optionally save to CSV
        df.to_csv("output1.csv", index=False)
        print("\nData has been saved to 'output1.csv'.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making the GET request: {e}")
    except ValueError as e:
        print(f"Error processing data: {e}")

# Updated URL

#maxborder       
#url = "https://publicationtool.jao.eu/nordic/api/data/maxBorderFlow?FromUtc=2023-12-31T23%3A00%3A59.000Z&ToUtc=2024-11-29T23%3A00%3A00.000Z"

#maxbexchange  
#url = "https://publicationtool.jao.eu/nordic/api/data/maxExchanges?FromUtc=2023-07-31T22%3A00%3A59.000Z&ToUtc=2024-11-30T23%3A00%3A00.000Z"
url = "https://publicationtool.jao.eu/nordic/api/data/fbDomainShadowPrice?Filter=%7B%22Tso%22%3A%5B%2210X1001A1001A248%22%5D%2C%22NonRedundant%22%3Atrue%7D&Skip=0&Take=10000&FromUtc=2024-10-29T23%3A00%3A00.000Z&ToUtc=2024-12-17T00%3A00%3A00.000Z"
fetch_and_display_dataframe_with_shape(url)

#maxbordertestrun 

#maxbexchangetestrun

