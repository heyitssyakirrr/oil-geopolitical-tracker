"""
sidebar.py
----------
Sidebar navigation using Streamlit's native elements.

Structure (mirrors Streamlit's DOM):
    stSidebarHeader     ← st.logo() renders here, collapse button lives here too
    stSidebarContent    ← everything inside `with st.sidebar:` goes here
        nav groups      ← section labels + st.button rows
        pipeline status ← last run footer
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
    """
    Render sidebar navigation.

    - st.logo() injects into stSidebarHeader so the collapse button and
      the brand logo/text share the same native header row.
    - Navigation groups and the pipeline footer live in stSidebarContent
      via `with st.sidebar:`.
    """

    # ── Header row (stSidebarHeader) ─────────────────────────────────────────
    # st.logo() is the only official way to place content in the header row
    # next to the collapse button.  We use an SVG data URI so there is no
    # external dependency.  The CSS in styles.py hides the <img> and shows
    # the .sb-logo-label text pseudo-element instead.
    LOGO_SVG = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "width='32' height='32' viewBox='0 0 32 32'%3E"
        "%3Crect width='32' height='32' rx='4' fill='%23ff8a4c'/%3E"
        "%3Ctext x='16' y='22' font-size='18' text-anchor='middle' "
        "font-family='serif' fill='%230a0d14'%3E💻%3C/text%3E"
        "%3C/svg%3E"
    )
    st.logo(LOGO_SVG, size="medium")

    # ── Sidebar content (stSidebarContent) ───────────────────────────────────
    with st.sidebar:

        # Nav groups
        for group_label, pages in _NAV_GROUPS:
            st.markdown(
                f'<p class="sb-section-label">{group_label}</p>',
                unsafe_allow_html=True,
            )
            for icon, page_name in pages:
                is_active = st.session_state.get("page") == page_name
                # Wrap in a div so CSS can target active state
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