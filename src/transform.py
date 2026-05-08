import pandas as pd
import numpy as np
from src.utils import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Geopolitical + macro events reference file
# Edit data/events.csv to add new events — no code changes needed
# Columns: date, event, severity, category
# ---------------------------------------------------------------------------
EVENTS_FILE = "data/events.csv"

SHORT_WINDOW = 7
LONG_WINDOW  = 30


def get_events_dataframe() -> pd.DataFrame:
    """
    Loads events from CSV. Supports an optional 'category' column for
    filtering by event type (geopolitical, opec, weather, macro).

    Returns:
        DataFrame with columns: date, event, severity, [category]
    """
    try:
        df = pd.read_csv(EVENTS_FILE, parse_dates=["date"]) # converts the"date" column into Python datetime objects
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Events file not found at {EVENTS_FILE}. "
            f"Create it with columns: date, event, severity"
        )

    valid_severities = {"low", "medium", "high", "critical"}
    invalid = df[~df["severity"].isin(valid_severities)] # identify any rows where the severity value is not in the valid set
    if not invalid.empty:
        raise ValueError(f"Invalid severity values: {invalid['severity'].tolist()}")

    # just added, there is no category column in the initial events.csv, 
    # but if there is one we want to use it, otherwise default to 'geopolitical'
    if "category" not in df.columns:
        df["category"] = "geopolitical"

    df = df.sort_values("date").reset_index(drop=True) # sort events by date then reset the index
    logger.info(f"Loaded {len(df)} events from {EVENTS_FILE}")
    return df


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw OHLCV data from extract.py.
    Drops nulls, deduplicates, validates positive prices, casts types.
    """
    initial = len(df)
    logger.info(f"Cleaning — {initial} rows in")

    df = df.dropna(subset=["close"]) 
    # the combination of date + ticker is what uniquely identifies one row
    # the same commodity on the same day should only have one price record
    df = df.drop_duplicates(subset=["date", "ticker"]) 

    invalid = df[df["close"] <= 0]
    if not invalid.empty:
        logger.warning(f"Dropping {len(invalid)} rows with non-positive close prices")
        df = df[df["close"] > 0] # drop zero or negative prices which are invalid

    df["date"]   = pd.to_datetime(df["date"])
    df["open"]   = pd.to_numeric(df["open"],   errors="coerce") # if value cant be converted to number, become NaN...
    df["high"]   = pd.to_numeric(df["high"],   errors="coerce")
    df["low"]    = pd.to_numeric(df["low"],    errors="coerce")
    df["close"]  = pd.to_numeric(df["close"],  errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype(int) # if NaN, fill with 0 then convert to int

    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    logger.info(f"Clean complete — {initial} → {len(df)} rows")
    return df


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds all analytical columns to cleaned price data.

    New columns:
        daily_return_pct     — % change day-over-day
        rolling_7d_avg       — 7-day rolling mean of close
        rolling_30d_avg      — 30-day rolling mean of close
        volatility_30d       — 30-day rolling std dev
        price_vs_30d_avg_pct — % deviation from 30-day mean
        daily_range          — high - low
        daily_range_pct      — daily_range / close * 100
    """
    logger.info("Adding derived metrics")
    df = df.copy() # to avoid SettingWithCopyWarning when creating new columns

    # how much did price move today vs yesterday in %
    df["daily_return_pct"] = (
        df.groupby("ticker")["close"] # group by ticker to calculate returns separately for each commodity
        .pct_change() # calculate the percentage change in the 'close' price from the previous row (day) for each ticker
        .mul(100)
        .round(4)
    )

    '''
    A rolling window slides across the data row by row, 
    and at each position it looks back N (7/30) rows and calculates 
    something (mean) over that window.
    '''

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

    # how much is the market panicking today vs the last month? Higher volatility means more uncertainty and risk
    df["volatility_30d"] = (
        df.groupby("ticker")["close"]
        # High std = values are spread far apart = volatile market.
        .transform(lambda x: x.rolling(LONG_WINDOW, min_periods=1).std())
        .round(4)
    )

    df["price_vs_30d_avg_pct"] = (
        (df["close"] - df["rolling_30d_avg"])
        .div(df["rolling_30d_avg"])
        .mul(100)
        .round(2)
    )

    df["daily_range"]     = (df["high"] - df["low"]).round(4)
    df["daily_range_pct"] = (df["daily_range"] / df["close"] * 100).round(2)

    logger.info(f"Derived metrics done — shape: {df.shape}")
    return df


def run_transform(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Master transform: clean → enrich → load events.

    Returns:
        (enriched_df, events_df)
    """
    clean_df    = clean_prices(raw_df)
    enriched_df = add_derived_metrics(clean_df)
    events_df   = get_events_dataframe()
    return enriched_df, events_df