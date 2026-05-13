"""
sidebar.py
----------
Sidebar navigation using Streamlit's native elements.

DOM structure (Streamlit):
    [data-testid="stSidebarHeader"]   ← st.logo() (brand SVG) + collapse button
    [data-testid="stSidebarContent"]  ← nav groups + pipeline footer

The brand title is rendered as an SVG inside st.logo() so it lives in the
header row, right next to the collapse button.  When the sidebar collapses,
CSS hides stSidebarHeader entirely so only the expand arrow remains visible.
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

    # ── Brand SVG in st.logo() → renders inside stSidebarHeader ─────────────
    # size="large" ensures the logo image is tall enough to be legible at the
    # 52px header height we set in CSS.  The SVG encodes the full title so no
    # external fonts are needed.
    BRAND_SVG = (
        "data:image/svg+xml,"
        "%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='44' viewBox='0 0 200 44'%3E"
        # Icon circle background
        "%3Ccircle cx='20' cy='22' r='18' fill='%230c0f18' stroke='%231e2640' stroke-width='1.2'/%3E"
        # 📡 emoji
        "%3Ctext x='20' y='28' font-size='18' text-anchor='middle' "
        "font-family='Apple Color Emoji%2CSegoe UI Emoji%2Csans-serif'%3E%F0%9F%93%A1%3C/text%3E"
        # Line 1
        "%3Ctext x='46' y='18' font-size='15' font-family='Arial Black%2CArial%2Csans-serif' "
        "font-weight='900' letter-spacing='2' fill='%23ff8a4c'%3EGLOBAL CRISIS%3C/text%3E"
        # Line 2
        "%3Ctext x='46' y='36' font-size='12' font-family='Arial Black%2CArial%2Csans-serif' "
        "font-weight='900' letter-spacing='2' fill='%23ff8a4c'%3ECOMMODITY TRACKER%3C/text%3E"
        "%3C/svg%3E"
    )
    st.logo(BRAND_SVG, size="large")

    # ── Sidebar content ───────────────────────────────────────────────────────
    with st.sidebar:

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