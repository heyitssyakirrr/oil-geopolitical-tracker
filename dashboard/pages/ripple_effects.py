"""
ripple_effects.py
-----------------
Dedicated page for exploring cross-commodity price transmission.

Layout:
    1. Source commodity selector + lag slider
    2. Ripple chain visualisation (who is downstream)
    3. Correlation bar — Pearson r of source vs all other commodities at N-day lag
    4. Scatter plot — source returns vs selected target returns
    5. Context box explaining each source commodity's transmission mechanism
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components import (
    COMMODITY_META,
    CATEGORY_COMMODITIES,
    CATEGORIES,
    label_map,
    color_map,
    render_filter_bar,
    ripple_scatter,
    ripple_lag_bar,
)


def _ripple_chain_html(source: str, targets: list[str]) -> str:
    if not targets:
        return '<div class="ctx-box">No direct downstream ripple targets defined for this commodity.</div>'
    nodes = (
        f'<span class="ripple-node source">'
        f'{COMMODITY_META.get(source, {}).get("icon", "")} '
        f'{COMMODITY_META.get(source, {}).get("label", source)}</span>'
    )
    for t in targets:
        tmeta = COMMODITY_META.get(t, {})
        nodes += (
            f'<span class="ripple-sep">→</span>'
            f'<span class="ripple-node">'
            f'{tmeta.get("icon", "")} {tmeta.get("label", t)}</span>'
        )
    return (
        '<div class="ripple-chain">'
        '<div class="chain-title">▸ RIPPLE CHAIN — direct downstream transmission</div>'
        f'<div class="ripple-arrow">{nodes}</div>'
        '</div>'
    )


def _category_badge(commodity: str) -> str:
    meta     = COMMODITY_META.get(commodity, {})
    cat      = meta.get("category", "")
    cat_meta = CATEGORIES.get(cat, {})
    color    = cat_meta.get("color", "#888")
    icon     = cat_meta.get("icon", "")
    label    = cat_meta.get("label", cat.title())
    return (
        f'<span class="cat-badge" '
        f'style="color:{color};border-color:{color}30;background:{color}10">'
        f'{icon} {label}</span>'
    )


def render(prices: pd.DataFrame, events: pd.DataFrame) -> None:
    # ── Controls ──────────────────────────────────────────────────────────────
    # Build a full filter bar just for date range, then add custom controls
    filters  = render_filter_bar(
        "rip", prices,
        show_commodity=True,
        show_events_toggle=False,
        show_ma_toggle=False,
    )
    sel_com  = filters.commodity
    start_dt = filters.start_dt
    end_dt   = filters.end_dt

    # Lag slider in a second row
    lag_days = st.slider(
        "Lag window (days)",
        min_value=7, max_value=90, value=30, step=7,
        key="rip_lag",
        help="How many days ahead to measure the downstream price change after a shock in the source.",
    )

    meta           = COMMODITY_META.get(sel_com, {})
    ripple_targets = meta.get("ripple", [])

    # Filter prices to window
    window = prices[
        (prices["date"] >= start_dt)
        & (prices["date"] <= end_dt)
    ].copy()

    all_other = [c for c in prices["commodity_name"].unique() if c != sel_com]

    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown(
        '<div class="page-header">'
        '<div class="page-title">🔗 RIPPLE EFFECTS</div>'
        '<div class="page-subtitle">'
        '▸ cross-commodity price transmission · lag correlation analysis'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Source summary ────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="ctx-box">'
        f'{_category_badge(sel_com)}<br>'
        f'<strong>{meta.get("icon", "")} {meta.get("label", sel_com)}</strong> — '
        f'{meta.get("why", "No description available.")}<br><br>'
        f'<strong>⚡ War signal:</strong> {meta.get("war_signal", "—")}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Ripple chain ──────────────────────────────────────────────────────────
    st.markdown(_ripple_chain_html(sel_com, ripple_targets), unsafe_allow_html=True)

    # ── Correlation bar — all commodities ─────────────────────────────────────
    st.markdown('<div class="sec-head">Cross-Commodity Correlation</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sec-sub">'
        f'Pearson r — {meta.get("label", sel_com)} {lag_days}-day return vs every other commodity · '
        f'Positive = move together · Negative = inverse'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        ripple_lag_bar(window, sel_com, all_other, lag_days=lag_days),
        width='stretch',
    )

    # ── Scatter matrix for direct ripple targets ──────────────────────────────
    if ripple_targets:
        st.markdown('<div class="sec-head">Scatter — Source vs Downstream Targets</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="sec-sub">'
            'Each dot is one trading day · X = source return · Y = target return at lag · '
            'Dashed line = trend · r value = Pearson correlation'
            '</div>',
            unsafe_allow_html=True,
        )

        # Lay out up to 3 per row
        cols_per_row = 3
        for i in range(0, len(ripple_targets), cols_per_row):
            batch = ripple_targets[i : i + cols_per_row]
            cols  = st.columns(len(batch))
            for col, tgt in zip(cols, batch):
                tgt_meta = COMMODITY_META.get(tgt, {})
                with col:
                    st.markdown(
                        f'<div class="sec-sub" style="margin-top:8px">'
                        f'{tgt_meta.get("icon","")} {tgt_meta.get("label", tgt)}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    st.plotly_chart(
                        ripple_scatter(window, sel_com, tgt, lag_days=lag_days),
                        width='stretch',
                    )

    # ── Category-level ripple map — text summary ──────────────────────────────
    st.markdown('<div class="sec-head">Full Ripple Map</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">All defined transmission chains across categories</div>',
        unsafe_allow_html=True,
    )

    for src, smeta in COMMODITY_META.items():
        targets = smeta.get("ripple", [])
        if not targets:
            continue
        st.markdown(_ripple_chain_html(src, targets), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)