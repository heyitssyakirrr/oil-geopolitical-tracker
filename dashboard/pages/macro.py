"""Macro category page — Gold, Copper."""
import pandas as pd
from ._category_page import render_category_page


def render(prices: pd.DataFrame, events: pd.DataFrame) -> None:
    render_category_page("macro", prices, events)