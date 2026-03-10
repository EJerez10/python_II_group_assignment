# pysimfin.py

import simfin as sf
import pandas as pd

class PySimFin:

    def __init__(self, api_key, data_dir="~/simfin_data"):
        sf.set_api_key(api_key)
        sf.set_data_dir(data_dir)

    def get_share_prices(self, ticker, start, end):
        df = sf.load_shareprices(market='us')
        df = df.loc[ticker]
        return df.loc[start:end]

    def get_financial_statement(self, ticker, start, end):
        df = sf.load_income(variant='annual', market='us')
        df = df.loc[ticker]
        return df.loc[start:end]