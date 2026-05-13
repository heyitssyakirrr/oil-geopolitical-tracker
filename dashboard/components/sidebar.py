"""
sidebar.py
----------
Sidebar navigation renderer.

Navigation groups:
    MAIN          — Overview
    BY CATEGORY   — Energy · Agriculture · Livestock · Macro
    ANALYSIS      — Ripple Effects · Event Intelligence · Price Analysis · Comparison
    SYSTEM        — Pipeline
"""

import streamlit as st


_NAV_GROUPS = [
    ("MAIN", [
        ("🏠", "Overview"),
    ]),
    ("BY CATEGORY", [
        ("⚡", "Energy"),
        ("🌾", "Agriculture"),
        ("🐄", "Livestock"),
        ("📊", "Macro"),
    ]),
    ("ANALYSIS", [
        ("🔗", "Ripple Effects"),
        ("💥", "Event Intelligence"),
        ("📈", "Price Analysis"),
        ("🔄", "Comparison"),
    ]),
    ("SYSTEM", [
        ("🔧", "Pipeline"),
    ]),
]


def render_sidebar(runs) -> None:
    """Render the sidebar — brand, nav groups, last-run status."""
    # with —> activates the sidebar context before the block, deactivates it after
    with st.sidebar:
        
        # Brand
        st.markdown(
            '<div class="sb-header-row">'
            '<span class="sb-brand">📡 GLOBAL CRISIS<br>COMMODITY TRACKER</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        
        # Navigation groups
        for group_label, pages in _NAV_GROUPS:
            st.markdown(
                f'<div class="sb-section">{group_label}</div>',
                unsafe_allow_html=True,
            )
            for icon, page_name in pages:
                if st.button(
                    f"{icon}  {page_name}",
                    key=f"nav_{page_name}",
                ):
                    st.session_state.page = page_name
                    st.rerun()

        # Last pipeline run status
        if runs is not None and not runs.empty:
            last = runs.iloc[0]
            status = last.get("status", "unknown")
            status_color = {"success": "#22c55e", "failed": "#ef4444", "running": "#f59e0b"}.get(
                status, "#6b7fa8"
            )
            rows = last.get("rows_loaded", 0) or 0
            st.markdown(
                f'<div style="padding:10px 10px 8px;border-top:1px solid #1c2030;margin-top:10px">'
                f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:9px;'
                f'color:#4a5878;letter-spacing:0.15em;text-transform:uppercase;'
                f'margin-bottom:4px">LAST PIPELINE RUN</div>'
                f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;'
                f'color:{status_color}">'
                f'● {status.upper()} · {int(rows):,} rows</div>'
                f'</div>',
                unsafe_allow_html=True,
            )