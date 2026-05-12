"""
Price Analysis page — OHLC candlestick, return distribution,
volatility timeline, monthly range bar.
"""

import pandas as pd
import streamlit as st

from components import (
    COMMODITY_META,
    render_filter_bar,
    candlestick_chart,
    return_histogram,
    volatility_chart,
    monthly_range_bar,
)


def _prepare_price_analysis_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure required columns exist for chart rendering and derive safe fallbacks."""
    out = df.sort_values("date").copy()

    if "open" not in out:
        out["open"] = out["close"].shift(1).fillna(out["close"])
    if "high" not in out:
        out["high"] = out[["open", "close"]].max(axis=1)
    if "low" not in out:
        out["low"] = out[["open", "close"]].min(axis=1)

    if "daily_return_pct" not in out:
        out["daily_return_pct"] = out["close"].pct_change(fill_method=None) * 100
    if "volatility_30d" not in out:
        out["volatility_30d"] = out["daily_return_pct"].rolling(30, min_periods=5).std()
    if "daily_range" not in out:
        out["daily_range"] = (out["high"] - out["low"]).abs()
    if "rolling_7d_avg" not in out:
        out["rolling_7d_avg"] = out["close"].rolling(7, min_periods=1).mean()
    if "rolling_30d_avg" not in out:
        out["rolling_30d_avg"] = out["close"].rolling(30, min_periods=1).mean()

    return out


def render(prices: pd.DataFrame, _events=None) -> None:
    filters  = render_filter_bar("pa", prices, show_events_toggle=False, show_ma_toggle=True)
    sel_com  = filters.commodity
    start_dt = filters.start_dt
    end_dt   = filters.end_dt
    show_ma  = filters.show_ma

    meta     = COMMODITY_META.get(sel_com, {})
    accent   = meta.get("color", "#e25c2e")
    filtered = prices[
        (prices["commodity_name"] == sel_com)
        & (prices["date"] >= start_dt)
        & (prices["date"] <= end_dt)
    ].copy()
    filtered = _prepare_price_analysis_frame(filtered)

    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-header">'
        f'<div class="page-title">📈 PRICE ANALYSIS</div>'
        f'<div class="page-subtitle">▸ Deep dive — {meta.get("label","")} · OHLC · Returns · Volatility</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No data for selected range.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Candlestick
    st.markdown('<div class="sec-head">OHLC Candlestick</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">'
        'Open · High · Low · Close each trading day · Green = price rose · Red = price fell'
        '</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(candlestick_chart(filtered, meta, show_ma), use_container_width=True)

    # Return distribution + Volatility timeline (side by side)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-head">Daily Return Distribution</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sec-sub">Histogram of daily % price changes · Fat tails = more extreme moves</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(return_histogram(filtered, accent), use_container_width=True)

    with col2:
        st.markdown('<div class="sec-head">Volatility Timeline</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sec-sub">30-day rolling volatility · Spikes = event-driven panic</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(volatility_chart(filtered), use_container_width=True)

    # Monthly range
    st.markdown('<div class="sec-head">Monthly Average Daily Range</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">'
        'How wide was High–Low each month? Wider = more intraday uncertainty'
        '</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(monthly_range_bar(filtered, meta), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)