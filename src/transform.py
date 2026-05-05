import pandas as pd
import numpy as np
from src.utils import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Geopolitical events reference csv file
# Add new events here as they happen — date format must be 'YYYY-MM-DD'
# ---------------------------------------------------------------------------
EVENTS_FILE = "data/events.csv"

def get_events_dataframe() -> pd.DataFrame:
    """
    Loads geopolitical events from a CSV file.
    To add new events, edit data/events.csv directly — no code changes needed.

    Returns:
        DataFrame with columns: date, event, severity
    """
    try:
        df = pd.read_csv(EVENTS_FILE, parse_dates=["date"])
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Events file not found at {EVENTS_FILE}. "
            f"Create it with columns: date, event, severity"
        )

    # Validate severity values
    valid_severities = {"low", "medium", "high", "critical"}
    invalid = df[~df["severity"].isin(valid_severities)]
    if not invalid.empty:
        raise ValueError(f"Invalid severity values: {invalid['severity'].tolist()}")

    df = df.sort_values("date").reset_index(drop=True)
    logger.info(f"Loaded {len(df)} geopolitical events from {EVENTS_FILE}")
    return df

# ---------------------------------------------------------------------------
# Rolling window sizes — change these in one place to affect all calculations
# ---------------------------------------------------------------------------
SHORT_WINDOW  = 7   # 7-day rolling average
LONG_WINDOW   = 30  # 30-day rolling average


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw price data from extract.py.
    - Drops rows where close price is null
    - Removes duplicate (date, ticker) pairs
    - Removes rows with zero or negative prices
    - Ensures correct data types
    - Sorts by ticker and date ascending

    Args:
        df: Raw DataFrame from fetch_all_commodities()

    Returns:
        Cleaned DataFrame ready for transformation
    """
    initial_count = len(df)
    logger.info(f"Starting clean — {initial_count} rows")

    # Drop rows with no close price — useless without it
    df = df.dropna(subset=["close"])

    # Remove duplicate rows for same date and ticker
    df = df.drop_duplicates(subset=["date", "ticker"])

    # Prices must be positive — flag and remove anything suspicious
    invalid = df[df["close"] <= 0]
    if not invalid.empty:
        logger.warning(f"Dropping {len(invalid)} rows with non-positive close prices")
        df = df[df["close"] > 0]

    # Enforce correct data types
    df["date"]   = pd.to_datetime(df["date"])
    df["open"]   = pd.to_numeric(df["open"],   errors="coerce")
    df["high"]   = pd.to_numeric(df["high"],   errors="coerce")
    df["low"]    = pd.to_numeric(df["low"],    errors="coerce")
    df["close"]  = pd.to_numeric(df["close"],  errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype(int)

    # Sort so rolling calculations work correctly
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

    logger.info(f"Clean complete — {initial_count} → {len(df)} rows")
    return df


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds analytical columns to the cleaned price DataFrame.
    All calculations are grouped by ticker so commodities never bleed into each other.

    New columns added:
        daily_return_pct     : % change in close price from previous trading day
        rolling_7d_avg       : 7-day rolling average of close price
        rolling_30d_avg      : 30-day rolling average of close price
        volatility_30d       : 30-day rolling standard deviation (measure of price instability)
        price_vs_30d_avg_pct : how far today's price is above/below the 30-day average (%)
        daily_range          : difference between high and low (intraday volatility)
        daily_range_pct      : daily range as % of close price

    Args:
        df: Cleaned DataFrame from clean_prices()

    Returns:
        DataFrame with all original columns plus derived metric columns
    """
    logger.info("Adding derived metrics")
    df = df.copy()  # never mutate the input DataFrame

    # --- Return & Moving Averages ---
    df["daily_return_pct"] = (
        df.groupby("ticker")["close"]
        .pct_change()
        .mul(100)
        .round(4)
    )

    df["rolling_7d_avg"] = (
        df.groupby("ticker")["close"]
        .transform(lambda x: x.rolling(SHORT_WINDOW, min_periods=1).mean())
        .round(4)
    )

    df["rolling_30d_avg"] = (
        df.groupby("ticker")["close"]
        .transform(lambda x: x.rolling(LONG_WINDOW, min_periods=1).mean())
        .round(4)
    )

    # --- Volatility ---
    df["volatility_30d"] = (
        df.groupby("ticker")["close"]
        .transform(lambda x: x.rolling(LONG_WINDOW, min_periods=1).std())
        .round(4)
    )

    # --- Price vs average ---
    df["price_vs_30d_avg_pct"] = (
        (df["close"] - df["rolling_30d_avg"])
        .div(df["rolling_30d_avg"])
        .mul(100)
        .round(2)
    )

    # --- Intraday range ---
    df["daily_range"]     = (df["high"] - df["low"]).round(4)
    df["daily_range_pct"] = (df["daily_range"] / df["close"] * 100).round(2)

    logger.info(f"Derived metrics added — final shape: {df.shape}")
    return df


def get_events_dataframe() -> pd.DataFrame:
    """
    Returns the geopolitical events list as a clean DataFrame.
    Validates that all required fields are present and dates are valid.

    Returns:
        DataFrame with columns: date, event, severity
    """
    df = pd.DataFrame(GEOPOLITICAL_EVENTS)
    df["date"] = pd.to_datetime(df["date"])

    # Validate severity values are within expected set
    valid_severities = {"low", "medium", "high", "critical"}
    invalid = df[~df["severity"].isin(valid_severities)]
    if not invalid.empty:
        raise ValueError(f"Invalid severity values found: {invalid['severity'].tolist()}")

    df = df.sort_values("date").reset_index(drop=True)
    logger.info(f"Loaded {len(df)} geopolitical events")
    return df


def run_transform(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Master transform function — runs the full transformation pipeline.
    Call this from main.py instead of calling individual functions.

    Args:
        raw_df: Raw DataFrame from fetch_all_commodities()

    Returns:
        Tuple of (enriched_prices_df, events_df)
    """
    clean_df    = clean_prices(raw_df)
    enriched_df = add_derived_metrics(clean_df)
    events_df   = get_events_dataframe()
    return enriched_df, events_df