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
# Rolling window sizes
# ---------------------------------------------------------------------------
SHORT_WINDOW = 7
LONG_WINDOW  = 30


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw price data from extract.py.
    """
    initial_count = len(df)
    logger.info(f"Starting clean - {initial_count} rows")

    df = df.dropna(subset=["close"])
    df = df.drop_duplicates(subset=["date", "ticker"])

    invalid = df[df["close"] <= 0]
    if not invalid.empty:
        logger.warning(f"Dropping {len(invalid)} rows with non-positive close prices")
        df = df[df["close"] > 0]

    df["date"]   = pd.to_datetime(df["date"])
    df["open"]   = pd.to_numeric(df["open"],   errors="coerce")
    df["high"]   = pd.to_numeric(df["high"],   errors="coerce")
    df["low"]    = pd.to_numeric(df["low"],    errors="coerce")
    df["close"]  = pd.to_numeric(df["close"],  errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype(int)

    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

    logger.info(f"Clean complete - {initial_count} -> {len(df)} rows")
    return df


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds analytical columns to the cleaned price DataFrame.
    """
    logger.info("Adding derived metrics")
    df = df.copy()

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

    df["volatility_30d"] = (
        df.groupby("ticker")["close"]
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

    logger.info(f"Derived metrics added - final shape: {df.shape}")
    return df


def run_transform(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Master transform function — runs the full transformation pipeline.
    """
    clean_df    = clean_prices(raw_df)
    enriched_df = add_derived_metrics(clean_df)
    events_df   = get_events_dataframe()
    return enriched_df, events_df