"""Agriculture category page — Wheat, Corn, Soybeans, Sugar."""
import pandas as pd

try:
    from ._category_page import render_category_page
except ImportError:
    from pages._category_page import render_category_page


def render(prices: pd.DataFrame, events: pd.DataFrame) -> None:
    render_category_page("agriculture", prices, events)