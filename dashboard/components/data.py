"""
Database helpers and cached data loaders.
Single source of truth for all DB access in the dashboard.
"""

import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

REQUIRED_DB_VARS = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME")


def _get_db_config() -> dict:
    missing = [key for key in REQUIRED_DB_VARS if not os.getenv(key)]
    if missing:
        raise RuntimeError(f"Missing database config: {', '.join(missing)}")

    return {
        "username": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME"),
    }


@st.cache_resource
def get_engine():
    """
    Cache the engine for the app lifetime to reuse connections efficiently
    Streamlit reruns script on every interaction, so without caching we'd create a new engine each time
    if 10 users interact with the app, that could create 10 engines and exhaust DB connections. Caching prevents this.
    if each of them click 5 times, it would create 50 engines without caching
    """
    cfg = _get_db_config()
    db_url = URL.create(
        "postgresql+psycopg2",
        username=cfg["username"],
        password=cfg["password"],
        host=cfg["host"],
        port=cfg["port"],
        database=cfg["database"],
        query={"sslmode": "require"},
    )
    return create_engine(db_url, pool_pre_ping=True, pool_size=5, max_overflow=5)


def _read_sql_safe(query: str) -> pd.DataFrame:
    try:
        return pd.read_sql(query, get_engine())
    except (RuntimeError, SQLAlchemyError, ValueError) as exc:
        st.error("Dashboard data is temporarily unavailable.")
        st.caption("Check database credentials, network access, and table availability.")
        st.caption(str(exc))
        return pd.DataFrame()

"""
the first user to trigger each of these functions will cause the SQL query to run 
and the result to be cached for subsequent users and interactions for 1 hour (3600 seconds)
"""
@st.cache_data(ttl=3600)
def load_prices() -> pd.DataFrame:
    df = _read_sql_safe("SELECT * FROM commodity_prices ORDER BY date ASC")
    if not df.empty and "date" in df:
        df["date"] = pd.to_datetime(df["date"]) # python date parsing for easier filtering and plotting in Streamlit
    return df


@st.cache_data(ttl=3600)
def load_events() -> pd.DataFrame:
    df = _read_sql_safe("SELECT * FROM geopolitical_events ORDER BY date ASC")
    if not df.empty and "date" in df:
        df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(ttl=3600)
def load_runs() -> pd.DataFrame:
    return _read_sql_safe(
        "SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT 20",
    )