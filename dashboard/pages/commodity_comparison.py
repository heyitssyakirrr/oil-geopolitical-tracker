"""
commodity_comparison.py
-----------------------
Cross-commodity normalized comparison + volatility ranking + correlation heatmap.
Works across all 13 commodities regardless of category.
"""

import pandas as pd
import streamlit as st

from components import (
    correlation_heatmap,
    label_map,
    normalized_comparison_chart,
    render_filter_bar,
    volatility_ranking_bar,
)


def render(prices, events):
    filters  = render_filter_bar("cc", prices, show_commodity=False, show_ma_toggle=False)
    start_dt = filters.start_dt
    end_dt   = filters.end_dt
    show_ev  = filters.show_ev

    comp_df = prices[
        (prices["date"] >= start_dt)
        & (prices["date"] <= end_dt)
    ].copy()

    result_parts = []
    for name, group in comp_df.groupby("commodity_name"):
        base = group["close"].iloc[0]
        if base != 0:
            group = group.copy()
            group["norm"] = group["close"] / base * 100
        result_parts.append(group)
    comp_df = pd.concat(result_parts, ignore_index=True)
    comp_df["label"] = comp_df["commodity_name"].map(label_map).fillna(comp_df["commodity_name"])

    st.markdown(
        '<div class="page-header">'
        '<div class="page-title">🔄 COMMODITY COMPARISON</div>'
        '<div class="page-subtitle">'
        '▸ normalized co-movement and volatility ranking across all 13 commodities'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        normalized_comparison_chart(comp_df, events, start_dt, end_dt, show_ev),
        width='stretch',
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-head">Volatility Ranking</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sec-sub">30-day rolling std dev — most to least volatile</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(volatility_ranking_bar(comp_df), width='stretch')

    with c2:
        st.markdown('<div class="sec-head">Correlation Heatmap</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sec-sub">'
            'Pearson correlation of daily returns · 1 = perfect positive · -1 = perfect inverse'
            '</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(correlation_heatmap(comp_df), width='stretch')

    st.markdown('</div>', unsafe_allow_html=True)