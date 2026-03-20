# pysimfin.py

import simfin as sf
import pandas as pd


class PySimFin:
    def __init__(self, api_key, data_dir="~/simfin_data"):
        sf.set_api_key(api_key)
        sf.set_data_dir(data_dir)

    def get_share_prices(self, ticker, start, end):
        try:
            df = sf.load_shareprices(
                variant="daily",
                market="us",
                start_date=start,
                end_date=end
            ).reset_index()

            df["Date"] = pd.to_datetime(df["Date"])

            filtered = df[df["Ticker"] == ticker].copy()
            filtered = filtered.sort_values("Date")

            return filtered

        except Exception as e:
            print(f"Error retrieving share prices: {e}")
            return pd.DataFrame()

    def get_financial_statement(self, ticker, start, end):
        try:
            df = sf.load_income(
                variant="annual",
                market="us",
                start_date=start,
                end_date=end
            ).reset_index()

            filtered = df[df["Ticker"] == ticker].copy()
            return filtered

        except Exception as e:
            print(f"Error retrieving financial statements: {e}")
            return pd.DataFrame()