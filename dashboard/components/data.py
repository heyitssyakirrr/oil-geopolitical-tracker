"""
Database helpers and cached data loaders.
Single source of truth for all DB access in the dashboard.
"""

import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def get_engine():
    """
    Cache the engine for the app lifetime to reuse connections efficiently
    Streamlit reruns script on every interaction, so without caching we'd create a new engine each time
    if 10 users interact with the app, that could create 10 engines and exhaust DB connections. Caching prevents this.
    if each of them click 5 times, it would create 50 engines without caching
    """
    db_url = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}"
        f"/{os.getenv('DB_NAME')}"
        f"?sslmode=require"
    )
    return create_engine(db_url)

"""
the first user to trigger each of these functions will cause the SQL query to run 
and the result to be cached for subsequent users and interactions for 1 hour (3600 seconds)
"""
@st.cache_data(ttl=3600)
def load_prices() -> pd.DataFrame:
    df = pd.read_sql("SELECT * FROM commodity_prices ORDER BY date ASC", get_engine())
    df["date"] = pd.to_datetime(df["date"]) # python date parsing for easier filtering and plotting in Streamlit
    return df


@st.cache_data(ttl=3600)
def load_events() -> pd.DataFrame:
    df = pd.read_sql("SELECT * FROM geopolitical_events ORDER BY date ASC", get_engine())
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(ttl=3600)
def load_runs() -> pd.DataFrame:
    return pd.read_sql(
        "SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT 20",
        get_engine(),
    )