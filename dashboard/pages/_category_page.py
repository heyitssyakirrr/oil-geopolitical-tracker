"""
_category_page.py
-----------------
Generic category page renderer.  Each category page (energy, agriculture,
livestock, macro) calls render_category_page() with its category key and
the shared prices/events DataFrames.

Layout per page:
    1. Filter bar  (commodity selector scoped to this category + date range)
    2. Page header with category badge
    3. War-signal banner for selected commodity
    4. KPI cards  (spot price, 7d MA, 30d MA, vs 30d avg, 30d vol)
    5. Category normalized chart  (all commodities in this category)
    6. Price history of selected commodity
    7. Ripple targets — which downstream commodities are affected
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components import (
    CATEGORIES,
    CATEGORY_COMMODITIES,
    COMMODITY_META,
    SEV_COLORS,
    category_price_chart,
    price_history_chart,
    render_filter_bar,
    label_map,
)


# ─────────────────────────────────────────────────────────────────────────────
# KPI card helper
# ─────────────────────────────────────────────────────────────────────────────

def _kpi(label: str, value: str, delta: str = "",
         note: str = "", cls: str = "neu", accent: str = "#ff8a4c") -> str:
    return (
        f'<div class="kpi-card" style="--kpi-accent:{accent}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-delta {cls}">{delta}</div>'
        f'<div class="kpi-note">{note}</div>'
        f'</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Ripple chain HTML
# ─────────────────────────────────────────────────────────────────────────────

def _ripple_chain_html(source: str, targets: list[str]) -> str:
    if not targets:
        return ""
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
        '<div class="chain-title">▸ RIPPLE CHAIN — downstream price transmission</div>'
        f'<div class="ripple-arrow">{nodes}</div>'
        '</div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main renderer
# ─────────────────────────────────────────────────────────────────────────────

def render_category_page(
    category: str,
    prices: pd.DataFrame,
    events: pd.DataFrame,
) -> None:
    """
    Render a full category page.

    Args:
        category: one of 'energy' | 'agriculture' | 'livestock' | 'macro'
        prices:   full commodity_prices DataFrame
        events:   full geopolitical_events DataFrame
    """
    cat_meta      = CATEGORIES.get(category, {})
    cat_label     = cat_meta.get("label", category.title())
    cat_icon      = cat_meta.get("icon", "🔹")
    cat_color     = cat_meta.get("color", "#ff8a4c")
    cat_accent    = cat_meta.get("accent", "#ff8a4c")
    cat_commodities = CATEGORY_COMMODITIES.get(category, [])

    # ── Filter bar scoped to this category ───────────────────────────────────
    # Only show commodities belonging to this category
    cat_prices = prices[prices["commodity_name"].isin(cat_commodities)].copy()

    filters  = render_filter_bar(
        page_key=f"cat_{category}",
        prices=cat_prices,
        show_commodity=True,
        show_events_toggle=True,
        show_ma_toggle=True,
    )
    sel_com  = filters.commodity
    start_dt = filters.start_dt
    end_dt   = filters.end_dt
    show_ev  = filters.show_ev
    show_ma  = filters.show_ma

    meta     = COMMODITY_META.get(sel_com, {})
    filtered = cat_prices[
        (cat_prices["commodity_name"] == sel_com)
        & (cat_prices["date"] >= start_dt)
        & (cat_prices["date"] <= end_dt)
    ].copy()

    cat_window = cat_prices[
        (cat_prices["date"] >= start_dt)
        & (cat_prices["date"] <= end_dt)
    ].copy()

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="page-header">'
        f'<div class="cat-badge" style="color:{cat_color};border-color:{cat_color}20;background:{cat_color}0d">'
        f'{cat_icon} {cat_label.upper()}</div>'
        f'<div class="page-title">{cat_icon} {cat_label.upper()}</div>'
        f'<div class="page-subtitle">'
        f'▸ {" · ".join(label_map.get(c, c) for c in cat_commodities)}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── War signal banner ─────────────────────────────────────────────────────
    war_signal = meta.get("war_signal", "")
    if war_signal:
        sev_cls_map = {
            "energy": "alert-red",
            "agriculture": "alert-amber",
            "livestock": "alert-amber",
            "macro": "alert-blue",
        }
        alert_cls = sev_cls_map.get(category, "alert-blue")
        st.markdown(
            f'<div class="alert {alert_cls}">'
            f'<strong>⚡ WAR SIGNAL — {meta.get("icon","")}'
            f' {meta.get("label", sel_com)}:</strong> {war_signal}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── KPI cards ─────────────────────────────────────────────────────────────
    if not filtered.empty:
        latest  = filtered.iloc[-1]
        prev    = filtered.iloc[-2] if len(filtered) > 1 else latest
        delta   = latest["close"] - prev["close"]
        pct_d   = delta / prev["close"] * 100 if prev["close"] else 0
        is_oil  = sel_com in ("brent_crude", "wti_crude")
        per_l   = latest["close"] / 159 if is_oil else None
        d_cls   = "up" if delta > 0 else ("down" if delta < 0 else "neu")
        d_sym   = "▲" if delta > 0 else ("▼" if delta < 0 else "─")
        vs      = latest.get("price_vs_30d_avg_pct", 0)
        vol     = latest.get("volatility_30d", 0)

        st.markdown(
            '<div class="kpi-grid">'
            + _kpi(
                f"Spot Price ({meta.get('unit_short', '')})",
                f"${latest['close']:.2f}",
                f"{d_sym} ${abs(delta):.2f} ({pct_d:+.1f}%) today",
                f"≈ ${per_l:.3f}/litre" if per_l else meta.get("unit", ""),
                d_cls, cat_accent,
            )
            + _kpi("7-Day Average",   f"${latest['rolling_7d_avg']:.2f}",
                   "", "Short-term trend", "neu", cat_accent)
            + _kpi("30-Day Average",  f"${latest['rolling_30d_avg']:.2f}",
                   "", "Medium-term baseline", "neu", cat_accent)
            + _kpi(
                "vs 30-Day Avg", f"{vs:+.1f}%", "",
                "Above avg → demand pressure" if vs > 0 else "Below avg → supply surplus",
                "up" if vs > 0 else "down", cat_accent,
            )
            + _kpi("30-Day Volatility", f"{vol:.2f}", "",
                   "Higher = more uncertainty", "neu", cat_accent)
            + '</div>',
            unsafe_allow_html=True,
        )

    # ── Category normalized chart ─────────────────────────────────────────────
    st.markdown('<div class="sec-head">Category Overview — Normalized Co-movement</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">'
        'All commodities in this category indexed to 100 at period start · '
        'Divergence = relative supply/demand pressure'
        '</div>',
        unsafe_allow_html=True,
    )
    if not cat_window.empty:
        st.plotly_chart(
            category_price_chart(cat_window, events, start_dt, end_dt, show_ev),
            use_container_width=True,
        )

    # ── Selected commodity price history ─────────────────────────────────────
    st.markdown(
        f'<div class="sec-head">'
        f'{meta.get("icon", "")} {meta.get("label", sel_com)} — Price History'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sec-sub">'
        'Red = critical event · Amber = high · Blue = medium · Green = low'
        '</div>',
        unsafe_allow_html=True,
    )
    if not filtered.empty:
        st.plotly_chart(
            price_history_chart(filtered, events, meta, start_dt, end_dt, show_ma, show_ev),
            use_container_width=True,
        )

    # ── Ripple chain ──────────────────────────────────────────────────────────
    ripple_targets = meta.get("ripple", [])
    if ripple_targets:
        st.markdown('<div class="sec-head">Ripple Effects</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sec-sub">'
            'Downstream commodities whose prices are historically driven by this one'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(_ripple_chain_html(sel_com, ripple_targets), unsafe_allow_html=True)

        # Context box
        st.markdown(
            f'<div class="ctx-box">'
            f'<strong>{meta.get("icon", "🔹")} {meta.get("label", sel_com)}</strong><br>'
            f'{meta.get("why", "")}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)