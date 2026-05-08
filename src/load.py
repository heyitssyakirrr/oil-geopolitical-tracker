import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.utils import get_logger

load_dotenv()
logger = get_logger(__name__)


def get_engine():
    """Creates and returns a SQLAlchemy engine from .env credentials."""
    db_url = (
        # psycopg2 is the PostgreSQL driver that SQLAlchemy uses to connect to the database
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}"
        f"/{os.getenv('DB_NAME')}"
        f"?sslmode=require"
    )
    # create an object that knows how to connect to the database and execute SQL commands
    return create_engine(db_url) 


def init_schema(engine):
    """
    Creates all required tables if they do not already exist.
    Safe to re-run — never overwrites existing data.

    Tables:
        commodity_prices    — OHLCV + derived metrics, includes category column
        geopolitical_events — events with severity and optional category
        pipeline_runs       — execution history for monitoring
    """
    create_prices_table = """
        CREATE TABLE IF NOT EXISTS commodity_prices (
            id                   SERIAL PRIMARY KEY,
            date                 DATE NOT NULL,
            ticker               TEXT NOT NULL,
            commodity_name       TEXT NOT NULL,
            category             TEXT,
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
            # UNIQUE (date, ticker)
            # no two rows can have the same date and ticker, ensures idempotency when upserting

    create_events_table = """
        CREATE TABLE IF NOT EXISTS geopolitical_events (
            id        SERIAL PRIMARY KEY,
            date      DATE NOT NULL,
            event     TEXT NOT NULL,
            severity  TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
            category  TEXT DEFAULT 'geopolitical',
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

    # Migration: add columns introduced after initial schema
    migrations = [
        "ALTER TABLE commodity_prices ADD COLUMN IF NOT EXISTS category TEXT;",
        "ALTER TABLE geopolitical_events ADD COLUMN IF NOT EXISTS category TEXT DEFAULT 'geopolitical';",
    ]

    with engine.connect() as conn:
        conn.execute(text(create_prices_table))
        conn.execute(text(create_events_table))
        conn.execute(text(create_pipeline_runs_table))
        for migration in migrations:
            conn.execute(text(migration))
        conn.commit()

    logger.info("Schema initialised — all tables ready")


def load_prices(df: pd.DataFrame, engine) -> int:
    """
    Upserts enriched price data into commodity_prices.
    Existing (date, ticker) pairs are skipped — safe to re-run.

    Returns:
        Number of new rows inserted
    """
    staging = "commodity_prices_staging"

    upsert_sql = f"""
        INSERT INTO commodity_prices (
            date, ticker, commodity_name, category,
            open, high, low, close, volume,
            daily_return_pct, rolling_7d_avg, rolling_30d_avg,
            volatility_30d, price_vs_30d_avg_pct,
            daily_range, daily_range_pct
        )
        SELECT
            date, ticker, commodity_name, category,
            open, high, low, close, volume,
            daily_return_pct, rolling_7d_avg, rolling_30d_avg,
            volatility_30d, price_vs_30d_avg_pct,
            daily_range, daily_range_pct
        FROM {staging}
        ON CONFLICT (date, ticker) DO NOTHING;
    """

    with engine.connect() as conn:
        before = conn.execute(text("SELECT COUNT(*) FROM commodity_prices")).scalar()

        df.to_sql(staging, conn, if_exists="replace", index=False)
        conn.execute(text(upsert_sql)) # SQLAlchemy 2.0+ need text() for raw SQL
        conn.execute(text(f"DROP TABLE IF EXISTS {staging}")) # clean up staging table after upsert
        conn.commit()

        after = conn.execute(text("SELECT COUNT(*) FROM commodity_prices")).scalar()

    rows = after - before
    logger.info(f"Prices loaded — {rows} new rows inserted")
    return rows


def load_events(df: pd.DataFrame, engine) -> int:
    """
    Upserts geopolitical events. Existing (date, event) pairs are skipped.

    Returns:
        Number of new rows inserted
    """
    staging = "geopolitical_events_staging"

    with engine.connect() as conn:
        df.to_sql(staging, conn, if_exists="replace", index=False)

        upsert_sql = f"""
            INSERT INTO geopolitical_events (date, event, severity, category)
            SELECT date, event, severity, category
            FROM {staging}
            ON CONFLICT (date, event) DO NOTHING;
        """
        result = conn.execute(text(upsert_sql))
        conn.execute(text(f"DROP TABLE IF EXISTS {staging}"))
        conn.commit()

    rows = result.rowcount
    logger.info(f"Events loaded — {rows} new rows inserted")
    return rows


def log_pipeline_run(
    engine,
    started_at,
    finished_at,
    status: str,
    rows_loaded: int = 0,
    error_message: str = None,
):
    """Records every pipeline execution result for monitoring."""
    sql = """
        INSERT INTO pipeline_runs
            (started_at, finished_at, status, rows_loaded, error_message)
        VALUES
            (:started_at, :finished_at, :status, :rows_loaded, :error_message)
    """
    # parameterized query to prevent SQL injection and handle data types correctly
    with engine.connect() as conn:
        # PostgreSQL will automatically convert Python datetime to SQL timestamp, and handle NULL for error_message if it's None
        # PostgreSQL receives the parameters as a dictionary and binds them to the query safely
        conn.execute(text(sql), {
            "started_at":    started_at,
            "finished_at":   finished_at,
            "status":        status,
            "rows_loaded":   rows_loaded,
            "error_message": error_message,
        })
        conn.commit()

    logger.info(f"Pipeline run logged — status: {status}, rows: {rows_loaded}")


def run_load(enriched_df: pd.DataFrame, events_df: pd.DataFrame, engine) -> int:
    """Master load: schema init → prices → events → return row count."""
    init_schema(engine)
    rows = load_prices(enriched_df, engine)
    load_events(events_df, engine)
    return rows