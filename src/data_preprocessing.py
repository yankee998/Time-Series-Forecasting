import yfinance as yf
import pandas as pd
import os
import time
from datetime import datetime

def fetch_yfinance_data(tickers, start_date, end_date, save_path):
    """Fetch historical data from YFinance with retry logic."""
    os.makedirs(save_path, exist_ok=True)
    
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        success = False
        
        for attempt in range(3):  # Retry up to 3 times
            try:
                # Download with progress=False to suppress output
                df = yf.download(
                    ticker,
                    start=start_date,
                    end=end_date,
                    progress=False,
                    timeout=10  # Add timeout parameter
                )
                
                if df.empty:
                    print(f"No data returned for {ticker}")
                    break
                
                # Reset index to include Date as a column
                df = df.reset_index()
                
                # Convert date to datetime and set as index
                df['Date'] = pd.to_datetime(df['Date'])
                
                # Save to CSV
                df.to_csv(os.path.join(save_path, f"{ticker}_raw.csv"), index=False)
                print(f"Successfully saved {ticker} data")
                success = True
                break
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {ticker}: {str(e)}")
                if attempt < 2:
                    time.sleep(5)  # Wait longer between retries
                else:
                    print(f"Failed to fetch {ticker} after 3 attempts")
        
        if not success:
            # Create empty DataFrame with expected columns if download fails
            empty_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
            empty_df.to_csv(os.path.join(save_path, f"{ticker}_raw.csv"), index=False)
            print(f"Created empty file for {ticker}")

def clean_data(input_path, output_path):
    """Clean raw YFinance data and save processed data."""
    os.makedirs(output_path, exist_ok=True)
    
    for ticker in ["TSLA", "BND", "SPY"]:
        file_path = os.path.join(input_path, f"{ticker}_raw.csv")
        print(f"\nProcessing {ticker}...")
        
        try:
            df = pd.read_csv(file_path)
            
            if df.empty:
                print(f"No data in file for {ticker}")
                continue
                
            # Convert date and numeric columns
            df['Date'] = pd.to_datetime(df['Date'])
            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
            
            # Handle missing values
            df[numeric_cols[:-1]] = df[numeric_cols[:-1]].interpolate()  # All except Volume
            df['Volume'] = df['Volume'].fillna(0)  # Fill volume with 0 if missing
            
            # Basic validation
            print(f"Data range: {df['Date'].min()} to {df['Date'].max()}")
            print(f"Missing values:\n{df.isnull().sum()}")
            
            # Save cleaned data
            df.to_csv(os.path.join(output_path, f"{ticker}_cleaned.csv"), index=False)
            print(f"Saved cleaned data for {ticker}")
            
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")

def basic_statistics(input_path):
    """Compute and display basic statistics for cleaned data."""
    for ticker in ["TSLA", "BND", "SPY"]:
        file_path = os.path.join(input_path, f"{ticker}_cleaned.csv")
        print(f"\nStatistics for {ticker}:")
        
        try:
            df = pd.read_csv(file_path)
            
            if df.empty:
                print("No data available")
                continue
                
            # Convert date and numeric columns
            df['Date'] = pd.to_datetime(df['Date'])
            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
            
            print(df.describe())
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {str(e)}")

if __name__ == "__main__":
    tickers = ["TSLA", "BND", "SPY"]
    start_date = "2015-07-01"
    end_date = datetime.now().strftime("%Y-%m-%d")  # Use current date as end date
    raw_path = "data/raw"
    processed_path = "data/processed"
    
    fetch_yfinance_data(tickers, start_date, end_date, raw_path)
    clean_data(raw_path, processed_path)
    basic_statistics(processed_path)