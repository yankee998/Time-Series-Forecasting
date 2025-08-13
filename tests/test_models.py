import pytest
from src.sarima_model import mae, rmse, mape  # Adjust based on actual variable names
from src.lstm_model import mae, rmse, mape

def test_sarima_metrics():
    assert mae > 0 and rmse > 0 and mape > 0

def test_lstm_metrics():
    assert mae > 0 and rmse > 0 and mape > 0