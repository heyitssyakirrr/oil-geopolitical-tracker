"""Energy category page — Brent, WTI, Natural Gas, Heating Oil."""
import pandas as pd
import streamlit as st

try:
    from ._category_page import render_category_page
except ImportError:
    from old_pages._category_page import render_category_page


def render(prices: pd.DataFrame, events: pd.DataFrame) -> None:
    render_category_page("energy", prices, events)