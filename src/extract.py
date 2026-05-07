import yfinance as yf
import pandas as pd
from src.utils import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Commodity tickers grouped by category
# ---------------------------------------------------------------------------
TICKERS = {
    # ENERGY
    "brent_crude":  "BZ=F",
    "wti_crude":    "CL=F",
    "natural_gas":  "NG=F",
    "heating_oil":  "HO=F",

    # AGRICULTURE
    "wheat":        "ZW=F",
    "corn":         "ZC=F",
    "soybeans":     "ZS=F",
    "sugar":        "SB=F",

    # LIVESTOCK
    "live_cattle":  "LE=F",
    "feeder_cattle":"GF=F",
    "lean_hogs":    "HE=F",

    # TRANSPORT / METALS (macro transmission)
    "gold":         "GC=F",
    "copper":       "HG=F",
}

# Category mapping — used by dashboard for page routing
COMMODITY_CATEGORIES = {
    "brent_crude":   "energy",
    "wti_crude":     "energy",
    "natural_gas":   "energy",
    "heating_oil":   "energy",
    "wheat":         "agriculture",
    "corn":          "agriculture",
    "soybeans":      "agriculture",
    "sugar":         "agriculture",
    "live_cattle":   "livestock",
    "feeder_cattle": "livestock",
    "lean_hogs":     "livestock",
    "gold":          "macro",
    "copper":        "macro",
}


def fetch_commodity_prices(ticker_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical OHLCV price data for a single commodity from Yahoo Finance.

    Args:
        ticker_symbol: Yahoo Finance ticker symbol (e.g. 'BZ=F')
        start_date:    Start date string 'YYYY-MM-DD'
        end_date:      End date string 'YYYY-MM-DD'

    Returns:
        DataFrame with columns: date, open, high, low, close, volume, ticker

    Raises:
        ValueError: If no data is returned for the ticker/date range
    """
    logger.info(f"Fetching {ticker_symbol} from {start_date} to {end_date}")

    try:
        df = yf.download(ticker_symbol, start=start_date, end=end_date, progress=False)
        if df.empty:
            raise ValueError(f"No data found for {ticker_symbol} between {start_date} and {end_date}")

        df = df.reset_index()
        df.columns = ["date", "open", "high", "low", "close", "volume"]
        df["ticker"] = ticker_symbol
        df["date"]   = pd.to_datetime(df["date"]).dt.date
        logger.info(f"Fetched {len(df)} rows for {ticker_symbol}")
        return df

    except Exception as e:
        logger.error(f"Error fetching {ticker_symbol}: {e}")
        raise


def fetch_all_commodities(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches price data for all commodities in TICKERS and combines them.

    Args:
        start_date: Start date string 'YYYY-MM-DD'
        end_date:   End date string 'YYYY-MM-DD'

    Returns:
        Combined DataFrame with commodity_name and category columns added

    Raises:
        RuntimeError: If no data could be fetched for any commodity
    """
    all_data = []

    for commodity, ticker in TICKERS.items():
        try:
            df = fetch_commodity_prices(ticker, start_date, end_date)
            df["commodity_name"] = commodity
            df["category"]       = COMMODITY_CATEGORIES.get(commodity, "other")
            all_data.append(df)
        except Exception as e:
            logger.error(f"Skipping {commodity} ({ticker}) due to error: {e}")

    if not all_data:
        raise RuntimeError("No data fetched for any commodity — check tickers and network connection")

    combined = pd.concat(all_data, ignore_index=True)
    logger.info(f"Combined fetch: {len(combined)} total rows across {len(all_data)} commodities")
    return combined