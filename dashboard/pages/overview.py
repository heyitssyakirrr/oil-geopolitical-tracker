"""
Overview page — cross-category summary + selected commodity KPIs + price history.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components import (
    CATEGORIES,
    CATEGORY_COMMODITIES,
    COMMODITY_META,
    label_map,
    render_filter_bar,
    price_history_chart,
    overview_normalized_chart,
)


def _kpi_card(label: str, value: str, delta: str = "",
               note: str = "", delta_cls: str = "neu") -> str:
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-delta {delta_cls}">{delta}</div>'
        f'<div class="kpi-note">{note}</div>'
        f'</div>'
    )


def _category_summary_cards(prices: pd.DataFrame, end_dt) -> str:
    """
    Renders 4 category summary cards showing the avg 30-day return
    across all commodities in each category.
    """
    html = '<div class="cat-grid">'
    for cat_key, cat_meta in CATEGORIES.items():
        commodities = CATEGORY_COMMODITIES.get(cat_key, [])
        cat_prices  = prices[
            (prices["commodity_name"].isin(commodities))
            & (prices["date"] <= end_dt)
        ]
        if cat_prices.empty:
            continue

        # Avg period return across commodities in this category
        returns = []
        for com in commodities:
            sub = cat_prices[cat_prices["commodity_name"] == com].sort_values("date")
            if len(sub) >= 2:
                r = (sub["close"].iloc[-1] - sub["close"].iloc[0]) / sub["close"].iloc[0] * 100
                returns.append(r)

        avg_return = sum(returns) / len(returns) if returns else 0
        sign       = "+" if avg_return >= 0 else ""
        chg_color  = "#ef4444" if avg_return > 0 else "#22c55e"

        com_labels = " · ".join(
            label_map.get(c, c) for c in commodities[:3]
        ) + (" · …" if len(commodities) > 3 else "")

        html += (
            f'<div class="cat-card">'
            f'<div class="cat-icon">{cat_meta["icon"]}</div>'
            f'<div class="cat-name">{cat_meta["label"].upper()}</div>'
            f'<div class="cat-count">{len(commodities)} commodities · {com_labels}</div>'
            f'<div class="cat-change" style="color:{chg_color}">'
            f'{sign}{avg_return:.1f}% avg period return</div>'
            f'</div>'
        )
    html += '</div>'
    return html


def render(prices: pd.DataFrame, events: pd.DataFrame) -> None:
    filters  = render_filter_bar("ov", prices, show_ma_toggle=True)
    sel_com  = filters.commodity
    start_dt = filters.start_dt
    end_dt   = filters.end_dt
    show_ev  = filters.show_ev
    show_ma  = filters.show_ma

    meta     = COMMODITY_META.get(sel_com, {})
    filtered = prices[
        (prices["commodity_name"] == sel_com)
        & (prices["date"] >= start_dt)
        & (prices["date"] <= end_dt)
    ].copy()

    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="page-header">'
        f'<div class="page-title">{meta.get("icon","🛢️")} OVERVIEW — {meta.get("label","")}</div>'
        f'<div class="page-subtitle">'
        f'▸ {meta.get("unit","")} · Geopolitical Commodity Tracker · Updated daily'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── War signal banner ─────────────────────────────────────────────────────
    st.markdown(
        f'<div class="alert alert-red">'
        f'<strong>⚡ WAR SIGNAL:</strong> {meta.get("war_signal","")}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Category summary cards ────────────────────────────────────────────────
    st.markdown('<div class="sec-head">Market Overview by Category</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">'
        'Average period return across all commodities in each category'
        '</div>',
        unsafe_allow_html=True,
    )
    window_prices = prices[
        (prices["date"] >= start_dt) & (prices["date"] <= end_dt)
    ]
    st.markdown(_category_summary_cards(window_prices, end_dt), unsafe_allow_html=True)

    # ── Summary alerts + KPI cards ────────────────────────────────────────────
    if not filtered.empty:
        latest_vol = filtered["volatility_30d"].iloc[-1]
        avg_vol    = filtered["volatility_30d"].mean()
        vol_pct    = (latest_vol - avg_vol) / avg_vol * 100 if avg_vol else 0

        rec_ev = events[
            (events["date"] >= end_dt - pd.Timedelta(days=60))
            & (events["date"] <= end_dt)
        ]
        n_crit = (rec_ev["severity"] == "critical").sum()
        n_high = (rec_ev["severity"] == "high").sum()
        pch    = (
            (filtered["close"].iloc[-1] - filtered["close"].iloc[0])
            / filtered["close"].iloc[0] * 100
            if len(filtered) > 1 else 0
        )

        a1, a2, a3 = st.columns(3)
        with a1:
            cls  = "alert-red" if vol_pct > 30 else ("alert-amber" if vol_pct > 10 else "alert-green")
            icon = "🚨" if vol_pct > 30 else ("⚠️" if vol_pct > 10 else "✅")
            st.markdown(
                f'<div class="alert {cls}"><strong>{icon} Volatility {vol_pct:+.0f}% vs avg</strong>'
                f'<br>Current 30-day vol: <strong>{latest_vol:.2f}</strong></div>',
                unsafe_allow_html=True,
            )
        with a2:
            cls = "alert-red" if n_crit > 0 else ("alert-amber" if n_high > 0 else "alert-blue")
            st.markdown(
                f'<div class="alert {cls}"><strong>{"🔴" if n_crit>0 else "🟠"}'
                f' {n_crit} critical · {n_high} high events</strong>'
                f'<br>In the last 60 days of selected window</div>',
                unsafe_allow_html=True,
            )
        with a3:
            cls = "alert-red" if pch > 10 else ("alert-green" if pch < -5 else "alert-blue")
            st.markdown(
                f'<div class="alert {cls}"><strong>{"📈" if pch>0 else "📉"}'
                f' Period return: {pch:+.1f}%</strong>'
                f'<br>{meta.get("label","")} moved {pch:+.1f}% over this window</div>',
                unsafe_allow_html=True,
            )

        latest  = filtered.iloc[-1]
        prev    = filtered.iloc[-2] if len(filtered) > 1 else latest
        delta   = latest["close"] - prev["close"]
        pct_d   = delta / prev["close"] * 100 if prev["close"] else 0
        is_oil  = sel_com in ("brent_crude", "wti_crude")
        per_l   = latest["close"] / 159 if is_oil else None
        d_cls   = "up" if delta > 0 else ("down" if delta < 0 else "neu")
        d_sym   = "▲" if delta > 0 else ("▼" if delta < 0 else "─")
        vs      = latest["price_vs_30d_avg_pct"]

        st.markdown(
            '<div class="kpi-grid">'
            + _kpi_card(
                f"Spot Price ({meta.get('unit_short', '')})",
                f"${latest['close']:.2f}",
                f"{d_sym} ${abs(delta):.2f} ({pct_d:+.1f}%) today",
                f"≈ ${per_l:.3f}/litre" if per_l else meta.get("unit", ""),
                d_cls,
            )
            + _kpi_card("7-Day Average",   f"${latest['rolling_7d_avg']:.2f}",
                        "", "Short-term trend")
            + _kpi_card("30-Day Average",  f"${latest['rolling_30d_avg']:.2f}",
                        "", "Medium-term baseline")
            + _kpi_card(
                "vs 30-Day Avg", f"{vs:+.1f}%", "",
                "Above avg → demand pressure" if vs > 0 else "Below avg → supply surplus",
                "up" if vs > 0 else "down",
            )
            + _kpi_card("30-Day Volatility", f"{latest['volatility_30d']:.2f}",
                        "", "Higher = more uncertainty")
            + '</div>',
            unsafe_allow_html=True,
        )

    # ── All-commodity normalized chart ────────────────────────────────────────
    st.markdown('<div class="sec-head">All Commodities — Normalized</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">'
        'All 13 commodities indexed to 100 at period start · '
        'Vertical lines = geopolitical events'
        '</div>',
        unsafe_allow_html=True,
    )
    if not window_prices.empty:
        st.plotly_chart(
            overview_normalized_chart(prices, events, start_dt, end_dt, show_ev),
            width='stretch',
        )

    # ── Selected commodity price history ──────────────────────────────────────
    st.markdown('<div class="sec-head">Price History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">'
        'Vertical lines = conflict/geopolitical events · '
        'Red = critical · Amber = high · Blue = medium · Green = low'
        '</div>',
        unsafe_allow_html=True,
    )
    if not filtered.empty:
        st.plotly_chart(
            price_history_chart(filtered, events, meta, start_dt, end_dt, show_ma, show_ev),
            width='stretch',
        )

    st.markdown('</div>', unsafe_allow_html=True)