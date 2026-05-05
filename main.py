import os
from datetime import datetime
from src.extract import fetch_all_commodities
from src.transform import run_transform
from src.load import get_engine, run_load, log_pipeline_run
from src.utils import get_logger

os.makedirs("logs", exist_ok=True)
logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Pipeline configuration
# Change START_DATE for a longer/shorter historical window
# ---------------------------------------------------------------------------
START_DATE = "2020-01-01"
END_DATE   = datetime.today().strftime("%Y-%m-%d")


def run_pipeline():
    started_at = datetime.utcnow()
    engine     = get_engine()
    rows_loaded = 0

    logger.info("=" * 60)
    logger.info("PIPELINE STARTED")
    logger.info(f"Date range: {START_DATE} → {END_DATE}")
    logger.info("=" * 60)

    try:
        # Step 1 — Extract
        logger.info("STEP 1: Extracting data from Yahoo Finance")
        raw_df = fetch_all_commodities(START_DATE, END_DATE)

        # Step 2 — Transform
        logger.info("STEP 2: Transforming data")
        enriched_df, events_df = run_transform(raw_df)

        # Step 3 — Load
        logger.info("STEP 3: Loading data into PostgreSQL")
        rows_loaded = run_load(enriched_df, events_df, engine)

        # Log successful run
        finished_at = datetime.utcnow()
        log_pipeline_run(
            engine      = engine,
            started_at  = started_at,
            finished_at = finished_at,
            status      = "success",
            rows_loaded = rows_loaded
        )

        logger.info("=" * 60)
        logger.info(f"PIPELINE COMPLETED — {rows_loaded} new rows loaded")
        logger.info(f"Duration: {(finished_at - started_at).seconds}s")
        logger.info("=" * 60)

    except Exception as e:
        finished_at = datetime.utcnow()
        log_pipeline_run(
            engine        = engine,
            started_at    = started_at,
            finished_at   = finished_at,
            status        = "failed",
            rows_loaded   = rows_loaded,
            error_message = str(e)
        )

        logger.error("=" * 60)
        logger.error(f"PIPELINE FAILED: {e}")
        logger.error("=" * 60)
        raise


if __name__ == "__main__":
    run_pipeline()