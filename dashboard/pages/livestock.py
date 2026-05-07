"""Livestock category page — Live Cattle, Feeder Cattle, Lean Hogs."""
import pandas as pd
from ._category_page import render_category_page


def render(prices: pd.DataFrame, events: pd.DataFrame) -> None:
    render_category_page("livestock", prices, events)