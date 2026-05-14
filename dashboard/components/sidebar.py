"""
sidebar.py
----------
Sidebar navigation using Streamlit's native elements.

Brand mark is rendered as plain HTML inside `with st.sidebar:` so it
lives inside stSidebarContent and disappears naturally when the sidebar
collapses.  st.logo() is NOT used — it renders in a sticky top-bar above
the entire app and cannot be moved into the sidebar with CSS.
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

    with st.sidebar:

        # ── Brand block ───────────────────────────────────────────────────────
        # Rendered as HTML inside stSidebarContent so it collapses with the
        # sidebar automatically — no st.logo() needed or wanted.
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

        # ── Nav groups ────────────────────────────────────────────────────────
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

        # ── Pipeline run footer ───────────────────────────────────────────────
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