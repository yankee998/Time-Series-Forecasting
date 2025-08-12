import yfinance as yf
import pandas as pd
import os
from time import sleep

# Set data folder path relative to src/
data_folder = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(data_folder, exist_ok=True)

# Define tickers and date range
tickers = ["TSLA", "BND", "SPY"]
start_date = "2015-07-01"
end_date = "2025-08-10"  # Adjusted to latest available date

# Fetch and save data with retry logic, ensuring all required columns
max_retries = 3
required_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
for ticker in tickers:
    print(f"Downloading {ticker} data...")
    for attempt in range(max_retries):
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=False)
            # Reset index to make Date a column and ensure all required columns
            data = data.reset_index()
            if not all(col in data.columns for col in required_columns):
                missing_cols = [col for col in required_columns if col not in data.columns]
                raise ValueError(f"Missing columns in {ticker} data: {missing_cols}")
            # Verify data types and presence
            data['Date'] = pd.to_datetime(data['Date'])
            data[required_columns] = data[required_columns].astype(float)
            data['Volume'] = data['Volume'].astype(int)
            file_path = os.path.join(data_folder, f"{ticker}_raw.csv")
            data.to_csv(file_path, index=False)
            print(f"Saved {ticker} data to {file_path} with columns: {data.columns.tolist()}")
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {ticker}: {e}")
            if attempt < max_retries - 1:
                sleep(5)  # Wait 5 seconds before retrying
            else:
                print(f"Failed to download {ticker} after {max_retries} attempts.")
print("Data download complete.")