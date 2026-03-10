from pysimfin import PySimFin

API_KEY = "97d9a61d-5dd4-4023-a8a7-5bfd9dbcd50b"

sf_wrapper = PySimFin(API_KEY)

prices = sf_wrapper.get_share_prices("AAPL", "2023-01-01", "2023-03-01")

print(prices.head())