import pandas as pd
import numpy as np

def build_etl_dataset(company_df, live_inference=False):

    df = company_df.copy().sort_index()

    # Keep only the core columns
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()

    # Feature engineering
    df['Return_1d'] = df['Close'].pct_change()
    df['Return_2d'] = df['Close'].pct_change(2)
    df['Return_5d'] = df['Close'].pct_change(5)

    df['Range'] = df['High'] - df['Low']
    df['OC_Change'] = df['Close'] - df['Open']

    df['MA_5'] = df['Close'].rolling(5).mean()
    df['MA_10'] = df['Close'].rolling(10).mean()

    df['MA_5_over_MA_10'] = df['MA_5'] / df['MA_10']
    df['Close_over_MA_5'] = df['Close'] / df['MA_5']
    df['Close_over_MA_10'] = df['Close'] / df['MA_10']

    df['Volume_Change'] = df['Volume'].pct_change()
    df['Volatility_5d'] = df['Return_1d'].rolling(5).std()

    # Only calculate the Target and drop the last row if we are in training mode
    if not live_inference:
        # Target: whether tomorrow closes above today
        df['Close_tomorrow'] = df['Close'].shift(-1)
        df['Target'] = (df['Close_tomorrow'] > df['Close']).astype(int)
        
        # Remove last row (no tomorrow)
        df = df.iloc[:-1]

    # Drop rows with NaN from rolling/pct_change
    df = df.dropna()

    return df