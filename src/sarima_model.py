import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

# Load and prepare data
input_path = "data/processed"
df_tsla = pd.read_csv(os.path.join(input_path, "TSLA_cleaned.csv"))
df_tsla['Date'] = pd.to_datetime(df_tsla['Date'])
df_tsla.set_index('Date', inplace=True)
df_tsla = df_tsla.asfreq('D')  # Set daily frequency

# Split into training and testing sets
train = df_tsla['Close'].loc['2015-07-01':'2023-12-31']
test = df_tsla['Close'].loc['2024-01-01':'2025-07-31']

# Fit SARIMA model
model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
results = model.fit()

# Forecast
forecast = results.forecast(steps=len(test))

# Ensure test and forecast are aligned and numeric
test_values = test.dropna().values
forecast_values = forecast[:len(test_values)].values

# Calculate metrics, handling zeros in test
mae = mean_absolute_error(test_values, forecast_values)
rmse = np.sqrt(mean_squared_error(test_values, forecast_values))
mask = test_values != 0  # Avoid division by zero
mape = np.mean(np.abs((test_values[mask] - forecast_values[mask]) / test_values[mask])) * 100 if mask.any() else np.nan

print(f"SARIMA MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%")