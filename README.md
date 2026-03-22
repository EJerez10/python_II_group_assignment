# 📈 Raviolution – AI-Powered Trading Dashboard

Raviolution is a Streamlit-based web application that combines financial data analysis and machine learning to help users:

- explore stock performance  
- monitor selected companies  
- generate model-based trading recommendations  

The project consists of two main components:
1. A **machine learning pipeline** for training predictive models  
2. A **web dashboard** for interacting with those models  

---

## 🌐 Live Application

The application is deployed on Streamlit Cloud:

👉 **[Launch Raviolution](https://ie2026mbdsg6.streamlit.app)**

---

## 🚀 Features

### 🏠 Home
- Overview of the platform  
- Explanation of features and navigation  

### 👥 Team
- Team members and roles  
- Project background and purpose  

### 👀 Watchlist
- Track selected stocks  
- View snapshot data for a chosen date  
- Metrics include:
  - Last Price  
  - Daily Change (%)  
  - Volume (formatted in millions)  

### 📊 Stock Overview
- Interactive stock analysis dashboard  
- Features:
  - Line and candlestick charts  
  - Moving averages (10-day, 20-day)  
  - Timeframe selection (1M, 3M, 6M, YTD, 1Y)  
  - Custom date range  
- Metrics:
  - Current Price  
  - Period High / Low  
  - Average Volume  
  - Latest Volume  
- Insights:
  - Recent Trading Patterns  
  - Volume analysis  

### 🤖 Recommendations
- Machine learning–based trading signals  
- Ticker-specific Gradient Boosting models  
- Outputs:
  - Predicted direction (UP / DOWN)  
  - Recommendation (BUY / HOLD / SELL)  
  - Probability of price increase  
- Visual signal chart with highlighted recommendation zone  

---

## 🧠 Machine Learning Component

### Objective
Predict whether a stock’s closing price will go **up or down the next trading day** using historical data.

### Models Used
- Logistic Regression (baseline)
- Gradient Boosted Trees (final model)

### Features
- Daily price changes  
- Moving averages  
- Volume trends  
- Derived technical indicators  

### Output
- `1` → Price expected to increase  
- `0` → Price expected to decrease or remain flat  

---

## 📓 Notebook Workflow

The notebook (`Group_assignment.ipynb`) includes:

1. Data loading and caching  
2. ETL and feature engineering  
3. Exploratory data analysis  
4. Model training and evaluation  
5. Hyperparameter tuning (Gradient Boosting)  
6. Final model training per ticker  
7. Exporting models as `.joblib` files  

---

## 🗂 Project Structure

```text
python_II_group_assignment/
│
├── app.py
├── etl_pipeline.py
├── pysimfin.py
├── requirements.txt
│
├── models/
│   ├── gradient_boosting_AAPL.joblib
│   ├── gradient_boosting_MSFT.joblib
│   └── ...
│
├── pages/
│   ├── Team.py
│   ├── Watchlist.py
│   ├── Overview.py
│   └── Recommendations.py
│
├── assets/
│   └── (team images)
│
├── Group_assignment.ipynb
├── CSVs/
├── saved_models/
└── README.md