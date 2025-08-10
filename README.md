# Time Series Forecasting Project

Welcome to the Time Series Forecasting repository! This project, developed by [Yared Genanaw](mailto:yaredgenanaw99@gmail.com), focuses on fetching, preprocessing, and performing exploratory data analysis (EDA) on historical financial data for TSLA, BND, and SPY stocks/ETFs from July 1, 2015, to July 31, 2025, sourced from Yahoo Finance. Due to API issues with `yfinance` and a missing "Download" option on the Yahoo Finance website, manual downloads or Alpha Vantage (as a Yahoo data proxy) were used to ensure real data compliance.

## Table of Contents
- [Project Overview](#project-overview)
- [How to Reproduce](#how-to-reproduce)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
  - [Running the Project](#running-the-project)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
This repository contains code and notebooks for Task 1 of a time series forecasting project, including:
- **Data Fetching**: Manual CSV downloads from Yahoo Finance or via Alpha Vantage API due to connectivity and UI issues.
- **Data Preprocessing**: Cleaning and interpolating data, saving to `data/processed/`.
- **EDA**: Visualizations (closing prices, daily returns, volatility), statistical tests (ADF, VaR, Sharpe Ratio), and outlier detection.
- **Testing**: Unit tests for data preprocessing.
- **CI/CD**: Automated testing via GitHub Actions.

The project is set up in a virtual environment using Python 3.11.9, with VS Code and Windows PowerShell, following the structure from last week's projects.

## How to Reproduce

### Prerequisites
- **Operating System**: Windows (tested on Windows 10/11)
- **Python**: Version 3.11.9
- **Git**: Installed and configured
- **VS Code**: With Python extension
- **Internet Connection**: Required for initial data fetching
- **Optional**: VPN (e.g., ProtonVPN) if facing regional restrictions

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yankee998/Time-Series-Forecasting.git
   cd Time-Series-Forecasting
   ```

2. **Set Up Virtual Environment**:
   - Create and activate a virtual environment:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Verify Python version:
     ```powershell
     python --version
     ```
     (Should output `Python 3.11.9`)

3. **Install Dependencies**:
   - Install required packages from `requirements.txt`:
     ```powershell
     pip install -r requirements.txt
     ```

4. **Fetch Data**:
   - **Option 1: Manual Yahoo Finance Download** (if "Download" option is available):
     - Visit https://finance.yahoo.com/quote/TSLA/history?p=TSLA, set "Time Period" to "Max" or custom (July 1, 2015, to July 31, 2025), click "Apply," and look for the "Download" link.
     - Repeat for BND and SPY.
     - Save as `TSLA.csv`, `BND.csv`, `SPY.csv` and move to `data/raw/`.
   - **Option 2: Alpha Vantage Fallback** (if "Download" is missing):
     - Sign up at https://www.alphavantage.co/ for a free API key.
     - Update `fetch_alpha_vantage_data.py` with your API key.
     - Run:
       ```powershell
       python fetch_alpha_vantage_data.py
       ```
     - This saves data to `data/raw/`.

5. **Verify Project Structure**:
   - Ensure all files and directories are present (see below).

### Running the Project
1. **Preprocess Data**:
   - Run the preprocessing script:
     ```powershell
     python src/data_preprocessing.py
     ```
   - Check `data/processed/` for cleaned CSVs.

2. **Perform EDA**:
   - Run the EDA script:
     ```powershell
     python src/eda.py
     ```
   - View plots in `data/processed/plots/`.

3. **Run Tests**:
   - Execute unit tests:
     ```powershell
     pytest tests/
     ```

4. **Explore Notebook**:
   - Open `notebooks/01_data_exploration.ipynb` in VS Code and run cells to reproduce analysis.

5. **Commit Changes**:
   - Stage, commit, and push:
     ```powershell
     git add .
     git commit -m "Reproduced Task 1 with [manual/Alpha Vantage] data"
     git push origin main
     ```

## Project Structure
```
Time-Series-Forecasting/
├── data/
│   ├── raw/              # Raw CSV files (TSLA_raw.csv, BND_raw.csv, SPY_raw.csv)
│   ├── processed/        # Processed CSV files (TSLA_cleaned.csv, etc.) and plots/
│   │   ├── plots/        # Generated plots (closing_prices.png, etc.)
├── notebooks/            # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
├── src/                  # Source code
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── eda.py
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_data_preprocessing.py
├── .gitignore            # Ignores virtual env, pyc files, etc.
├── README.md             # This file
├── requirements.txt      # Dependency list
├── setup.py              # Project setup configuration
├── fetch_alpha_vantage_data.py  # Optional data fetching script
├── .github/              # CI/CD configuration
│   ├── workflows/
│       ├── ci.yml        # GitHub Actions workflow
├── venv/                 # Virtual environment (ignored by .gitignore)
```

## Contributing
- Fork the repository.
- Create a feature branch: `git checkout -b feature-name`.
- Commit changes: `git commit -m "Description"`.
- Push to the branch: `git push origin feature-name`.
- Open a pull request.
- Contact [Yared Genanaw](mailto:yaredgenanaw99@gmail.com) for collaboration.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.