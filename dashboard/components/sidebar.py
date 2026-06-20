"""
sidebar.py
----------
Sidebar navigation using only native Streamlit elements.

No custom HTML, no negative margins, no CSS position overrides.
Works identically on localhost and Streamlit Cloud.

Navigation groups and pages are defined in _NAV_GROUPS.
Clicking a button sets st.session_state.page and triggers st.rerun().
The active page button is rendered with type="primary" — Streamlit's
built-in primary button style — so no CSS is needed for the active state.
"""

import streamlit as st

# ── Navigation structure ──────────────────────────────────────────────────────
# Each group is (section_label, [(icon, page_name), ...])
_NAV_GROUPS = [
    ("BRIEFING", [
        ("🏠", "Overview"),
        ("💥", "Event Intelligence"),
    ]),
    ("MARKETS", [
        ("⚡", "Energy"),
        ("🌾", "Agriculture"),
        ("🐄", "Livestock"),
        ("📊", "Macro"),
    ]),
    ("ADVANCED", [
        ("📈", "Price Analysis"),
        ("🔄", "Comparison"),
        ("🔗", "Ripple Effects"),
    ]),
    ("SYSTEM", [
        ("🔧", "Pipeline"),
    ]),
]

# Severity colour mapping for pipeline run footer
_STATUS_COLORS = {
    "success": "green",
    "failed":  "red",
    "running": "orange",
}


def render_sidebar(runs) -> None:
    """
    Renders the full sidebar:
      - Brand header
      - Navigation groups with section labels and page buttons
      - Pipeline run status footer
    """
    with st.sidebar:

        # ── Brand header ──────────────────────────────────────────────────────
        # st.markdown with minimal inline style — only font and colour,
        # no layout geometry that could break across environments.
        st.markdown(
            """
            <div style="padding: 1rem 0 0.5rem 0;">
                <span style="font-size:1.6rem;">📡</span>
                <span style="
                    font-family: 'Bebas Neue', sans-serif;
                    font-size: 1.2rem;
                    letter-spacing: 0.15em;
                    color: #ff8a4c;
                    margin-left: 8px;
                    vertical-align: middle;
                ">COMMODITY TRACKER</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Navigation groups ─────────────────────────────────────────────────
        current_page = st.session_state.get("page", "Overview")

        for section_label, pages in _NAV_GROUPS:
            # Section label — native Streamlit caption (small grey text)
            st.caption(section_label)

            for icon, page_name in pages:
                # Active page gets type="primary" (Streamlit's built-in highlight)
                # All other pages get type="secondary" (default)
                btn_type = "primary" if current_page == page_name else "secondary"

                if st.button(
                    f"{icon}  {page_name}",
                    key=f"nav_{page_name}",
                    use_container_width=True,
                    type=btn_type,
                ):
                    st.session_state.page = page_name
                    st.rerun()

        # ── Pipeline run footer ───────────────────────────────────────────────
        if runs is not None and not runs.empty:
            st.divider()

            last   = runs.iloc[0]
            status = str(last.get("status", "unknown"))
            rows   = int(last.get("rows_loaded", 0) or 0)
            color  = _STATUS_COLORS.get(status, "gray")

            st.caption("LAST PIPELINE RUN")
            st.markdown(
                f":{color}[● {status.upper()}] &nbsp; `{rows:,} rows`",
                unsafe_allow_html=False,
            )