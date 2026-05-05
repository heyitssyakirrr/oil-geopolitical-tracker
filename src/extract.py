import yfinance as yf
import pandas as pd
from src.utils import get_logger

logger = get_logger(__name__)

TICKERS = {
    # "commodity_name": "TICKER_SYMBOL"
    "brent_crude": "BZ=F",
    "wti_crude": "CL=F",
    "natural_gas": "NG=F",
    "gold": "GC=F",
    "wheat": "ZW=F",
}

def fetch_commodity_prices(ticker_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical price data for a specified commodity from Yahoo Finance.
    """
    logger.info(f"Fetching price data for {ticker_symbol} from {start_date} to {end_date}")
    
    try:
        df = yf.download(ticker_symbol, start=start_date, end=end_date)
        if df.empty:
            raise ValueError(f"No data found for {ticker_symbol} between {start_date} and {end_date}")
        
        df = df.reset_index()
        df.columns = ["date", "open", "high", "low", "close", "volume"]
        df["ticker"] = ticker_symbol
        df["date"] = pd.to_datetime(df["date"]).dt.date # strips timezone
        logger.info(f"Successfully fetched {len(df)} rows for {ticker_symbol}")
        return df
    except Exception as e:
        logger.error(f"Error fetching price data for {ticker_symbol}: {e}")
        raise

def fetch_all_commodities(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical price data for all commodities defined in TICKERS.
    """
    all_data = []
    for commodity, ticker in TICKERS.items():
        try:
            df = fetch_commodity_prices(ticker, start_date, end_date)
            df["commodity_name"] = commodity
            all_data.append(df)
        except Exception as e:
            logger.error(f"Skipping {commodity} due to error: {e}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        logger.info(f"Combined data contains {len(combined_df)} rows")
        return combined_df
    else:
        logger.warning("No data fetched for any commodities")
        return pd.DataFrame()