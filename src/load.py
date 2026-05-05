import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.utils import get_logger

load_dotenv()
logger = get_logger(__name__)


def get_engine():
    """
    Creates and returns a SQLAlchemy engine using credentials from .env file.
    Called once and reused across all load functions.

    Returns:
        SQLAlchemy engine connected to the oil_tracker database
    """
    db_url = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 5432)}"
        f"/{os.getenv('DB_NAME')}"
    )
    return create_engine(db_url)


def init_schema(engine):
    """
    Creates all required tables if they do not already exist.
    Safe to run multiple times — will never overwrite existing data.

    Tables created:
        commodity_prices    : stores all OHLCV data + derived metrics
        geopolitical_events : stores conflict events with severity level
        pipeline_runs       : tracks every pipeline execution for monitoring
    """
    create_prices_table = """
        CREATE TABLE IF NOT EXISTS commodity_prices (
            id                   SERIAL PRIMARY KEY,
            date                 DATE NOT NULL,
            ticker               TEXT NOT NULL,
            commodity_name       TEXT NOT NULL,
            open                 NUMERIC(12, 4),
            high                 NUMERIC(12, 4),
            low                  NUMERIC(12, 4),
            close                NUMERIC(12, 4) NOT NULL,
            volume               BIGINT,
            daily_return_pct     NUMERIC(8,  4),
            rolling_7d_avg       NUMERIC(12, 4),
            rolling_30d_avg      NUMERIC(12, 4),
            volatility_30d       NUMERIC(12, 4),
            price_vs_30d_avg_pct NUMERIC(8,  2),
            daily_range          NUMERIC(12, 4),
            daily_range_pct      NUMERIC(8,  2),
            loaded_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (date, ticker)
        );
    """

    create_events_table = """
        CREATE TABLE IF NOT EXISTS geopolitical_events (
            id        SERIAL PRIMARY KEY,
            date      DATE NOT NULL,
            event     TEXT NOT NULL,
            severity  TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
            UNIQUE (date, event)
        );
    """

    create_pipeline_runs_table = """
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id            SERIAL PRIMARY KEY,
            started_at    TIMESTAMP NOT NULL,
            finished_at   TIMESTAMP,
            status        TEXT CHECK (status IN ('running', 'success', 'failed')),
            rows_loaded   INTEGER,
            error_message TEXT
        );
    """

    with engine.connect() as conn:
        conn.execute(text(create_prices_table))
        conn.execute(text(create_events_table))
        conn.execute(text(create_pipeline_runs_table))
        conn.commit()

    logger.info("Schema initialised — all tables ready")


def load_prices(df: pd.DataFrame, engine) -> int:
    """
    Loads cleaned and enriched price data into commodity_prices table.
    Uses upsert logic — if a record with the same (date, ticker) already
    exists, it is skipped. This makes the pipeline safe to run multiple
    times without creating duplicates.

    Args:
        df:     Enriched DataFrame from run_transform()
        engine: SQLAlchemy engine from get_engine()

    Returns:
        Number of new rows inserted
    """
    staging_table = "commodity_prices_staging"

    with engine.connect() as conn:
        # Step 1 — write to a temporary staging table
        df.to_sql(staging_table, conn, if_exists="replace", index=False)

        # Step 2 — upsert from staging into main table
        upsert_sql = f"""
            INSERT INTO commodity_prices (
                date, ticker, commodity_name,
                open, high, low, close, volume,
                daily_return_pct, rolling_7d_avg, rolling_30d_avg,
                volatility_30d, price_vs_30d_avg_pct,
                daily_range, daily_range_pct
            )
            SELECT
                date, ticker, commodity_name,
                open, high, low, close, volume,
                daily_return_pct, rolling_7d_avg, rolling_30d_avg,
                volatility_30d, price_vs_30d_avg_pct,
                daily_range, daily_range_pct
            FROM {staging_table}
            ON CONFLICT (date, ticker) DO NOTHING;
        """
        result = conn.execute(text(upsert_sql))
        conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))
        conn.commit()

    rows_inserted = result.rowcount
    logger.info(f"Prices loaded — {rows_inserted} new rows inserted (duplicates skipped)")
    return rows_inserted


def load_events(df: pd.DataFrame, engine) -> int:
    """
    Loads geopolitical events into geopolitical_events table.
    Uses upsert logic — existing events are never duplicated.

    Args:
        df:     Events DataFrame from get_events_dataframe()
        engine: SQLAlchemy engine from get_engine()

    Returns:
        Number of new rows inserted
    """
    staging_table = "geopolitical_events_staging"

    with engine.connect() as conn:
        df.to_sql(staging_table, conn, if_exists="replace", index=False)

        upsert_sql = f"""
            INSERT INTO geopolitical_events (date, event, severity)
            SELECT date, event, severity
            FROM {staging_table}
            ON CONFLICT (date, event) DO NOTHING;
        """
        result = conn.execute(text(upsert_sql))
        conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))
        conn.commit()

    rows_inserted = result.rowcount
    logger.info(f"Events loaded — {rows_inserted} new rows inserted")
    return rows_inserted


def log_pipeline_run(
    engine,
    started_at,
    finished_at,
    status: str,
    rows_loaded: int = 0,
    error_message: str = None
):
    """
    Records the result of every pipeline execution into pipeline_runs table.
    This gives you a history of when the pipeline ran, whether it succeeded,
    and how many rows were loaded — essential for monitoring.

    Args:
        engine:        SQLAlchemy engine
        started_at:    datetime when pipeline started
        finished_at:   datetime when pipeline finished
        status:        'success' or 'failed'
        rows_loaded:   number of rows inserted in this run
        error_message: error details if status is 'failed'
    """
    sql = """
        INSERT INTO pipeline_runs
            (started_at, finished_at, status, rows_loaded, error_message)
        VALUES
            (:started_at, :finished_at, :status, :rows_loaded, :error_message)
    """
    with engine.connect() as conn:
        conn.execute(text(sql), {
            "started_at":    started_at,
            "finished_at":   finished_at,
            "status":        status,
            "rows_loaded":   rows_loaded,
            "error_message": error_message
        })
        conn.commit()

    logger.info(f"Pipeline run logged — status: {status}, rows: {rows_loaded}")


def run_load(enriched_df: pd.DataFrame, events_df: pd.DataFrame, engine) -> int:
    """
    Master load function — runs the full load pipeline.
    Call this from main.py instead of calling individual functions.

    Args:
        enriched_df: Enriched prices DataFrame from run_transform()
        events_df:   Events DataFrame from run_transform()
        engine:      SQLAlchemy engine from get_engine()

    Returns:
        Total number of new rows inserted
    """
    init_schema(engine)
    rows = load_prices(enriched_df, engine)
    load_events(events_df, engine)
    return rows