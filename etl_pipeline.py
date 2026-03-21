import pandas as pd
import numpy as np

def build_etl_dataset(company_df):
    # Copy
    df = company_df.copy()

    # Convert index to proper datetime, then sort by date
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Keep only needed raw columns
    df = df[['Open', 'Close', 'Volume']].copy()

    # Daily price change during the same day
    df['Daily_Change_Pct'] = (df['Close'] - df['Open']) / df['Open']

    # Moving averages based on closing price
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_10'] = df['Close'].rolling(window=10).mean()

    # Tomorrow's close
    df['Close_tomorrow'] = df['Close'].shift(-1)

    # Target: 1 if tomorrow closes higher than today, else 0
    df['Target'] = (df['Close_tomorrow'] > df['Close']).astype(int)

    # Remove helper column
    df = df.drop(columns=['Close_tomorrow'])

    # Remove invalid rows
    df = df.dropna()

    print(f"ETL complete: {rows_before} rows -> {rows_after} rows ({rows_dropped} dropped)")
    
    # Return consistent column order
    return df[['Open', 'Close', 'Daily_Change_Pct', 'MA_5', 'MA_10', 'Volume', 'Target']]