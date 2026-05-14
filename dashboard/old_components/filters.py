"""
Filter bar component — renders the top filter strip for each page.
Returns (sel_com, start_dt, end_dt, show_ev, show_ma) as a named tuple.
"""

from collections import namedtuple
import pandas as pd
import streamlit as st

from .constants import COMMODITY_META

FilterResult = namedtuple("FilterResult", ["commodity", "start_dt", "end_dt", "show_ev", "show_ma"])


def render_filter_bar(
    page_key: str,
    prices: pd.DataFrame,
    show_commodity: bool = True,
    show_events_toggle: bool = True,
    show_ma_toggle: bool = False,
) -> FilterResult:
    """
    Renders a contained filter bar with a border/background so it doesn't
    appear to float.  Returns a FilterResult namedtuple.
    """
    min_d = prices["date"].min().date()
    max_d = prices["date"].max().date()
    all_commodities = sorted(prices["commodity_name"].unique())

    # Wrap in a styled container
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)

    # Build column widths dynamically
    col_widths = []
    if show_commodity:
        col_widths.append(2)
    col_widths.append(3)
    if show_events_toggle:
        col_widths.append(1)
    if show_ma_toggle:
        col_widths.append(1)

    cols = st.columns(col_widths)
    ci   = 0

    sel_com = "brent_crude"
    if show_commodity:
        with cols[ci]:
            default_idx = all_commodities.index("brent_crude") if "brent_crude" in all_commodities else 0
            sel_com = st.selectbox(
                "Commodity",
                all_commodities,
                index=default_idx,
                format_func=lambda c: (
                    f"{COMMODITY_META.get(c, {}).get('icon', '🔹')} "
                    f"{COMMODITY_META.get(c, {}).get('label', c)}"
                ),
                key=f"{page_key}_com",
                label_visibility="visible",
            )
        ci += 1

    with cols[ci]:
        dr = st.date_input(
            "Range",
            value=[min_d, max_d],
            min_value=min_d,
            max_value=max_d,
            key=f"{page_key}_dr",
            label_visibility="visible",
        )
        start_dt = pd.to_datetime(dr[0])
        end_dt   = pd.to_datetime(dr[1]) if len(dr) == 2 else pd.to_datetime(max_d)
    ci += 1

    show_ev = True
    show_ma = True

    if show_events_toggle:
        with cols[ci]:
            st.markdown('<div style="height:21px"></div>', unsafe_allow_html=True)  # spacer to match label height
            show_ev = st.checkbox("Events", value=True, key=f"{page_key}_ev")
        ci += 1

    if show_ma_toggle:
        with cols[ci]:
            st.markdown('<div style="height:21px"></div>', unsafe_allow_html=True)  # spacer to match label height
            show_ma = st.checkbox("Moving Avg", value=True, key=f"{page_key}_ma")

    st.markdown("</div>", unsafe_allow_html=True)

    return FilterResult(sel_com, start_dt, end_dt, show_ev, show_ma)