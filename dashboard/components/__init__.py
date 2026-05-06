"""Dashboard components package."""
from .styles import GLOBAL_CSS
from .constants import (
    COMMODITY_META, SEV_COLORS, PAGES, PLOT_BG, GRID_CLR, FONT_CLR,
    label_map, color_map,
)
from .data import get_engine, load_prices, load_events, load_runs
from .charts import (
    base_layout,
    price_history_chart,
    candlestick_chart,
    return_histogram,
    volatility_chart,
    monthly_range_bar,
    severity_avg_bar,
    event_timeline_scatter,
    normalized_comparison_chart,
    volatility_ranking_bar,
    correlation_heatmap,
    pipeline_bar,
)
from .sidebar import render_sidebar
from .filters import render_filter_bar

__all__ = [
    "GLOBAL_CSS",
    "COMMODITY_META", "SEV_COLORS", "PAGES",
    "PLOT_BG", "GRID_CLR", "FONT_CLR",
    "label_map", "color_map",
    "get_engine", "load_prices", "load_events", "load_runs",
    "base_layout",
    "price_history_chart", "candlestick_chart", "return_histogram",
    "volatility_chart", "monthly_range_bar",
    "severity_avg_bar", "event_timeline_scatter",
    "normalized_comparison_chart", "volatility_ranking_bar",
    "correlation_heatmap", "pipeline_bar",
    "render_sidebar", "render_filter_bar",
]