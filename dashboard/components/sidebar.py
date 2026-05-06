"""
Sidebar navigation component.
Call render_sidebar() from app.py — updates st.session_state.page.
"""

import streamlit as st
from .constants import PAGES, SEV_COLORS


def render_sidebar(runs) -> None:
    """Render the full sidebar: brand, live status, nav, unit guide, severity legend."""
    page_names = [name for _, name in PAGES]
    page_icons = {name: icon for icon, name in PAGES}

    with st.sidebar:
        # Brand
        st.markdown('<span class="sb-brand">WAR & OIL</span>', unsafe_allow_html=True)
        st.markdown('<span class="sb-tagline">Geopolitical Commodity Tracker</span>', unsafe_allow_html=True)

        # Live status pill
        if not runs.empty:
            last = runs.iloc[0]
            ok   = last["status"] == "success"
            st.markdown(
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:10px;'
                f'color:{"#22c55e" if ok else "#ef4444"};padding:8px 16px 0">'
                f'{"🟢 Live" if ok else "🔴 Failed"} · {last["started_at"].strftime("%d %b %Y %H:%M")}</div>'
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:9px;color:#6b7fa8;padding:2px 16px 14px">'
                f'{last["rows_loaded"]:,} rows</div>',
                unsafe_allow_html=True,
            )

        # Navigation
        st.markdown('<div class="sb-section">▸ NAVIGATE</div>', unsafe_allow_html=True)

        current = st.session_state.get("page", "Overview")
        selected = st.radio(
            "Navigation",
            options=page_names,
            index=page_names.index(current) if current in page_names else 0,
            format_func=lambda n: f"{page_icons[n]}  {n}",
            key="sidebar_navigation",
            label_visibility="collapsed",
        )

        if selected != current:
            st.session_state.page = selected
            st.rerun()

        st.markdown(
            '<div class="sb-section" style="margin-top:18px">▸ UNIT GUIDE</div>',
              unsafe_allow_html=True
        )

        st.markdown(
            '<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#c8d3ea;padding:0 16px;line-height:1.9">'
            '🛢️ Oil → per barrel (159 L)<br>'
            '🥇 Gold → per troy oz (31g)<br>'
            '🌾 Wheat → per bushel (27kg)<br>'
            '🔥 Gas → per MMBtu</div>',
            unsafe_allow_html=True,
        )

        # Severity legend
        st.markdown(
            '<div class="sb-section" style="margin-top:14px">▸ SEVERITY</div>', 
            unsafe_allow_html=True
        )

        for sev, col in SEV_COLORS.items():
            st.markdown(
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:{col};padding:2px 16px">■ {sev.upper()}</div>',
                unsafe_allow_html=True,
            )