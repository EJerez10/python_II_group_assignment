from pysimfin import PySimFin, SimFinError

API_KEY = "PUT_YOUR_KEY_HERE"

sf = PySimFin(api_key=API_KEY)

try:
    prices = sf.get_share_prices("AAPL", "2023-01-01", "2023-03-01")
    print(prices.head())

    fin = sf.get_financial_statement("AAPL", "2022-01-01", "2023-12-31")
    print(fin.head())

except SimFinError as e:
    print("SimFin wrapper error:", e)