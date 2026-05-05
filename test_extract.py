import yfinance as yf
yf.set_tz_cache_location("UTC")
from src.extract import fetch_all_commodities

df = fetch_all_commodities("2026-01-01", "2026-04-30")
print(df.head())
print(df.shape)
print(df["commodity_name"].unique())