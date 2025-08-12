import pandas as pd
import os

def clean_data(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    for ticker in ["TSLA", "BND", "SPY"]:
        file_path = os.path.join(input_path, f"{ticker}_raw.csv")
        if not os.path.exists(file_path):
            print(f"No raw data file for {ticker}")
            continue
        print(f"Cleaning data for {ticker}...")
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df = df.astype({'Open': 'float64', 'High': 'float64', 'Low': 'float64', 'Close': 'float64', 'Adj Close': 'float64', 'Volume': 'int64'})
        print(f"{ticker} data types:\n{df.dtypes}")
        print(f"{ticker} missing values:\n{df.isnull().sum()}")
        df[['Open', 'High', 'Low', 'Close', 'Adj Close']] = df[['Open', 'High', 'Low', 'Close', 'Adj Close']].interpolate()
        df['Volume'] = df['Volume'].ffill()
        for col in ['Open', 'High', 'Low', 'Close', 'Adj Close']:
            min_val = df[col].min()
            max_val = df[col].max()
            df[col] = (df[col] - min_val) / (max_val - min_val)
        print(f"{ticker} date range: {df.index.min()} to {df.index.max()}")
        df.to_csv(os.path.join(output_path, f"{ticker}_cleaned.csv"))
        print(f"Saved cleaned {ticker} data to {output_path}/{ticker}_cleaned.csv")
    
    for col in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
        if df[col].isin([float('inf'), float('-inf')]).any():
            df[col] = df[col].replace([float('inf'), float('-inf')], float('nan'))
            df[col] = df[col].interpolate()
    return True

def basic_statistics(input_path):
    for ticker in ["TSLA", "BND", "SPY"]:
        file_path = os.path.join(input_path, f"{ticker}_cleaned.csv")
        if not os.path.exists(file_path):
            print(f"No cleaned data file for {ticker}")
            continue
        print(f"\nBasic statistics for {ticker}:")
        df = pd.read_csv(file_path)
        print(df.describe())

if __name__ == "__main__":
    raw_path = "data/raw"
    processed_path = "data/processed"
    clean_data(raw_path, processed_path)
    basic_statistics(processed_path)