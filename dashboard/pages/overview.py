"""
Overview page: global commodity risk briefing.

This page is intentionally compact. It should tell users what changed, what is
under stress, and which events matter before they choose a deeper analysis page.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components import (
    commodity_returns,
    important_events,
    label_map,
    latest_window,
    recent_event_summary,
    render_filter_bar,
    risk_label,
)


def _kpi_card(
    label: str,
    value: str,
    delta: str = "",
    note: str = "",
    delta_cls: str = "neu",
) -> str:
    return (
        '<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-delta {delta_cls}">{delta}</div>'
        f'<div class="kpi-note">{note}</div>'
        '</div>'
    )


def _format_pct(value) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{value:+.1f}%"


def _severity_badge(severity: str) -> str:
    severity = str(severity).lower()
    colors = {
        "critical": "#ef4444",
        "high": "#f59e0b",
        "medium": "#3b82f6",
        "low": "#22c55e",
    }
    color = colors.get(severity, "#8a9bbf")
    return (
        f'<span style="color:{color};font-weight:600;text-transform:uppercase">'
        f"{severity}</span>"
    )


def _render_page_header() -> None:
    st.markdown(
        '<div class="page-header">'
        '<div class="page-title">GLOBAL RISK BRIEFING</div>'
        '<div class="page-subtitle">'
        'Commodity stress, geopolitical events, and market transmission signals'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_risk_summary(events: pd.DataFrame, end_dt) -> dict:
    summary = recent_event_summary(events, end_dt=end_dt, days=60)
    risk_name, risk_class = risk_label(summary["risk_score"])

    st.markdown(
        f"""
        <div class="alert {risk_class}">
            <strong>Global commodity risk: {risk_name}</strong><br>
            {summary["critical"]} critical and {summary["high"]} high-severity events
            detected in the last 60 days of the selected window.
        </div>
        """,
        unsafe_allow_html=True,
    )
    return summary


def _render_kpis(movers: pd.DataFrame, event_summary: dict) -> None:
    if movers.empty:
        st.info("Not enough price history to calculate commodity movements.")
        return

    top_gainer = movers.iloc[0]
    top_loser = movers.iloc[-1]
    most_volatile = movers.sort_values("volatility_30d", ascending=False).iloc[0]

    top_gainer_name = label_map.get(top_gainer["commodity_name"], top_gainer["commodity_name"])