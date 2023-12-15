import pandas as pd
import yfinance as yf


data = yf.download("TSLA", start="2022-01-01", end="2022-12-31")

print(data)