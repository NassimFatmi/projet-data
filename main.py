import pandas as pd
import yfinance as yf
from datetime import datetime as dt
import pytz


data = yf.download("AAPL.PA")

print(data)