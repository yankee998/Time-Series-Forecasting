import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

# Load and prepare data
input_path = "data/processed"
df_tsla = pd.read_csv(os.path.join(input_path, "TSLA_cleaned.csv"))
df_tsla['Date'] = pd.to_datetime(df_tsla['Date'])
df_tsla.set_index('Date', inplace=True)
data = df_tsla['Close'].values.reshape(-1, 1)

# Normalize the data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Create sequences
lookback = 60
X, y = [], []
for i in range(lookback, len(data_scaled)):
    X.append(data_scaled[i-lookback:i, 0])
    y.append(data_scaled[i, 0])
X, y = np.array(X), np.array(y)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# Split into train and test
train_size = len(df_tsla.loc['2015-07-01':'2023-12-31'])
X_train, X_test = X[:train_size-lookback], X[train_size-lookback:]
y_train, y_test = y[:train_size-lookback], y[train_size-lookback:]

# Build and train LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(lookback, 1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

# Predict and reshape
forecast_scaled = model.predict(X_test)
forecast = scaler.inverse_transform(forecast_scaled).flatten()  # Flatten to 1D

# Align test data
test_values = df_tsla['Close'].iloc[train_size:].values[:len(forecast)]

# Calculate metrics
mae = mean_absolute_error(test_values, forecast)
rmse = np.sqrt(mean_squared_error(test_values, forecast))
mask = test_values != 0
mape = np.mean(np.abs((test_values[mask] - forecast[mask]) / test_values[mask])) * 100 if mask.any() else np.nan

print(f"LSTM MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%")