"""
sidebar.py
----------
Sidebar navigation using Streamlit's native elements.

DOM structure (Streamlit):
    [data-testid="stSidebarHeader"]   ← st.logo() + collapse button
    [data-testid="stSidebarContent"]  ← everything inside `with st.sidebar:`
        .sb-brand-block               ← 📡 icon + two-line title
        nav groups                    ← section labels + nav buttons
        .sb-run-footer                ← last pipeline run
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
    """Render sidebar navigation with brand header, nav groups, and pipeline footer."""

    # ── Header row — st.logo() is the only official way to inject into
    #    stSidebarHeader (next to the collapse button).
    #    We use a transparent 1×1 SVG so the slot is occupied but invisible;
    #    the real branding lives in stSidebarContent below.
    BLANK_SVG = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "width='1' height='1'%3E%3C/svg%3E"
    )
    st.logo(BLANK_SVG, size="small")

    # ── Sidebar content ───────────────────────────────────────────────────────
    with st.sidebar:

        # Brand block — mirrors the dashboard's global title style
        st.markdown(
            """
            <div class="sb-brand">
                <span class="sb-brand-icon">📡</span>
                <div class="sb-brand-text">
                    <span class="sb-brand-line1">GLOBAL CRISIS</span>
                    <span class="sb-brand-line2">COMMODITY TRACKER</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Nav groups
        for group_label, pages in _NAV_GROUPS:
            st.markdown(
                f'<p class="sb-section-label">{group_label}</p>',
                unsafe_allow_html=True,
            )
            for icon, page_name in pages:
                is_active = st.session_state.get("page") == page_name
                st.markdown(
                    f'<div class="sb-nav-item{"--active" if is_active else ""}">',
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"{icon}  {page_name}",
                    key=f"nav_{page_name}",
                    use_container_width=True,
                ):
                    st.session_state.page = page_name
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        # Pipeline run footer
        if runs is not None and not runs.empty:
            last   = runs.iloc[0]
            status = last.get("status", "unknown")
            color  = {
                "success": "#22c55e",
                "failed":  "#ef4444",
                "running": "#f59e0b",
            }.get(status, "#6b7fa8")
            rows = int(last.get("rows_loaded", 0) or 0)
            st.markdown(
                f"""
                <div class="sb-run-footer">
                    <div class="sb-run-label">LAST PIPELINE RUN</div>
                    <div class="sb-run-value" style="color:{color}">
                        ● {status.upper()} · {rows:,} rows
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )