import pandas as pd
import numpy as np

def build_etl_dataset(company_df, live_inference=False):
    # Copy
    df = company_df.copy()

    # Convert index to proper datetime, then sort by date
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Keep only needed raw columns
    df = df[['Open', 'Close', 'Volume']].copy()

    # Count rows before cleaning
    rows_before = len(df)

    # Daily price change during the same day
    df['Daily_Change_Pct'] = (df['Close'] - df['Open']) / df['Open']

    # Moving averages based on closing price
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_10'] = df['Close'].rolling(window=10).mean()

    # Only create target for training, not for live inference
    if not live_inference:
        df['Close_tomorrow'] = df['Close'].shift(-1)
        df['Target'] = (df['Close_tomorrow'] > df['Close']).astype(int)
        df = df.drop(columns=['Close_tomorrow'])

    # Remove invalid rows
    df = df.dropna()

    # Count rows after cleaning
    rows_after = len(df)
    rows_dropped = rows_before - rows_after

    print(f"ETL complete: {rows_before} rows -> {rows_after} rows ({rows_dropped} dropped)")

    # Return columns depending on mode
    if live_inference:
        return df[['Open', 'Close', 'Daily_Change_Pct', 'MA_5', 'MA_10', 'Volume']]
    else:
        return df[['Open', 'Close', 'Daily_Change_Pct', 'MA_5', 'MA_10', 'Volume', 'Target']]