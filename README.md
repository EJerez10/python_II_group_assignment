# 📈 Raviolution – AI-Powered Trading Dashboard
A web-based stock analysis platform combining financial data visualization and machine learning predictions.

## 🚀 Quick Access

👉 **Live App:** https://ie2026mbdsg6.streamlit.app  

Raviolution is a Streamlit-based web application that combines financial data analysis and machine learning to help users explore stock performance, monitor selected companies, and generate model-based trading recommendations.

The project connects a trained machine learning pipeline with an interactive web dashboard. Users can view market data, analyze recent trading patterns, and generate stock-specific predictions through a simple interface.

---

## 👥 Team Members

- Enzo Jerez  
- Roberto Cummings  
- Jia Yi Rachel Lee  
- Thomas-Christian Manteco  
- Maria-Irina Popa  

---

## 🚀 Main Features

### 🏠 Home
- Overview of the platform
- Summary of the project purpose and navigation

### 👥 Team
- Team members and roles
- Brief explanation of the project background

### 👀 Watchlist
- View selected stocks in a watchlist format
- Filter by stock and snapshot date
- Display:
  - Last Price
  - Daily Change (%)
  - Volume (formatted in millions)

### 📊 Stock Overview
- Interactive dashboard for individual stocks
- Features:
  - Line and candlestick charts
  - 10-day and 20-day moving averages
  - Timeframe selection
  - Optional custom date range
- Displays:
  - Current Price
  - Period High / Low
  - Average Volume
  - Latest Volume
  - Recent Trading Patterns

### 🤖 Recommendations
- Machine learning–based trading signals
- Uses ticker-specific Gradient Boosting models
- Displays:
  - Predicted direction (UP / DOWN)
  - Recommendation (BUY / HOLD / SELL)
  - 5-day price change
  - Probability of price increase
- Includes a visual signal chart and model summary

---

## 🧠 Machine Learning Component

The machine learning component of the project predicts whether a stock’s closing price will go **up or down the next trading day** using historical share price data.

### Models Used
- Logistic Regression (baseline comparison)
- Gradient Boosting Classifier (final model)

### Feature Engineering
The ETL pipeline prepares the input data by transforming raw price data into model-ready features, including:
- Daily price movement
- Moving averages
- Volume-related trends
- Other derived short-term technical indicators

### Prediction Output
- `1` → Price expected to increase
- `0` → Price expected to decrease or remain flat

## ⚙️ Running the App Locally

### 🚀 Quick Start

```bash
git clone https://github.com/EJerez10/python_II_group_assignment.git
cd python_II_group_assignment
pip install -r requirements.txt
```

Create a `.env` file in the project root (same folder as `app.py`):

```text
SIMFIN_API_KEY=YOUR_API_KEY_HERE
```

Run the app:
```bash
streamlit run app.py
```

---

## 🗂 Project Structure

```text
python_II_group_assignment/
│
├── app.py                     # Streamlit app entry point
├── etl_pipeline.py            # Feature engineering / ETL logic
├── pysimfin.py                # SimFin wrapper for loading data
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── AI_Usage_Log.md            # AI usage documentation
├── .gitignore
├── .env                       # Local API key file (not to be shared)
│
├── assets/                    # Images used in the app
├── models/                    # Saved trained .joblib models
├── pages/                     # Multipage Streamlit app pages
├── docs/                      # Project documentation (Executive Summary PDF)
│   └── Executive Summary.pdf
│
├── GroupAssignment_Instructions.ipynb
└── .devcontainer/