"""
Sidebar navigation component.
Call render_sidebar() from app.py — it returns nothing but sets
st.session_state.page on button clicks.
"""

import streamlit as st
from .constants import PAGES, SEV_COLORS


def render_sidebar(runs) -> None:
    """Render the full sidebar: brand, live status, nav, unit guide, severity legend."""
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
                f'{"🟢 Live" if ok else "🔴 Failed"}'
                f' · {last["started_at"].strftime("%d %b %Y %H:%M")}</div>'
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:9px;'
                f'color:#3a4060;padding:2px 16px 14px">'
                f'{last["rows_loaded"]:,} rows</div>',
                unsafe_allow_html=True,
            )

        # Navigation
        st.markdown('<div class="sb-section">▸ NAVIGATE</div>', unsafe_allow_html=True)

        for icon, name in PAGES:
            is_active = st.session_state.page == name
            if is_active:
                st.markdown(
                    f'<div class="sb-nav-active">{icon}&nbsp;&nbsp;{name}</div>',
                    unsafe_allow_html=True,
                )
            else:
                if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
                    st.session_state.page = name
                    st.rerun()

        # Unit guide
        st.markdown(
            '<div class="sb-section" style="margin-top:20px">▸ UNIT GUIDE</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-family:IBM Plex Mono,monospace;font-size:10px;'
            'color:#6b7894;padding:0 16px;line-height:2">'
            '🛢️ Oil → per barrel (159 L)<br>'
            '🥇 Gold → per troy oz (31g)<br>'
            '🌾 Wheat → per bushel (27kg)<br>'
            '🔥 Gas → per MMBtu</div>',
            unsafe_allow_html=True,
        )

        # Severity legend
        st.markdown(
            '<div class="sb-section" style="margin-top:16px">▸ SEVERITY</div>',
            unsafe_allow_html=True,
        )
        for sev, col in SEV_COLORS.items():
            st.markdown(
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:10px;'
                f'color:{col};padding:2px 16px">■ {sev.upper()}</div>',
                unsafe_allow_html=True,
            )