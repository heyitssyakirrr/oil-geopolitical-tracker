"""
sidebar.py
----------
Sidebar navigation renderer.
Uses Streamlit's native sidebar header area so the collapse button
renders in its natural position (top-right of sidebar header row),
next to the brand title — not floating outside the viewport.
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
    """Render the sidebar — brand (via st.logo), nav groups, last-run status."""

    # st.logo() renders into stSidebarHeader — the same row that holds the
    # native collapse button.  We pass a tiny transparent PNG so Streamlit
    # uses that slot, then we overlay our own brand text with CSS.
    # The collapse button stays in normal document flow next to the logo slot.
    st.logo(
        "https://raw.githubusercontent.com/streamlit/streamlit/develop/frontend/public/favicon.png",
        size="small",
        link=None,
    )

    with st.sidebar:
        # Brand title — sits just below the header row (logo + collapse button)
        st.markdown(
            '<div class="sb-brand-block">'
            '<span class="sb-brand">📡 GLOBAL CRISIS</span>'
            '<span class="sb-brand">COMMODITY TRACKER</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        # Navigation groups
        for group_label, pages in _NAV_GROUPS:
            st.markdown(
                f'<p class="sb-section">{group_label}</p>',
                unsafe_allow_html=True,
            )
            for icon, page_name in pages:
                active = st.session_state.get("page") == page_name
                btn_cls = "sb-btn-active" if active else ""
                # Render a styled div that acts as the button label,
                # but still use st.button for the click handler
                st.markdown(f'<div class="sb-btn-wrap {btn_cls}">', unsafe_allow_html=True)
                if st.button(
                    f"{icon}  {page_name}",
                    key=f"nav_{page_name}",
                    use_container_width=True,
                ):
                    st.session_state.page = page_name
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # Last pipeline run status
        if runs is not None and not runs.empty:
            last = runs.iloc[0]
            status = last.get("status", "unknown")
            status_color = {
                "success": "#22c55e",
                "failed":  "#ef4444",
                "running": "#f59e0b",
            }.get(status, "#6b7fa8")
            rows = last.get("rows_loaded", 0) or 0
            st.markdown(
                f'<div class="sb-run-status">'
                f'<div class="sb-run-label">LAST PIPELINE RUN</div>'
                f'<div class="sb-run-value" style="color:{status_color}">'
                f'● {status.upper()} · {int(rows):,} rows</div>'
                f'</div>',
                unsafe_allow_html=True,
            )