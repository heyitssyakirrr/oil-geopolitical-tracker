import pandas as pd
import streamlit as st

from components import COMMODITY_META, event_timeline_scatter, render_filter_bar, severity_avg_bar


def render(prices: pd.DataFrame, events: pd.DataFrame) -> None:
    filters = render_filter_bar("ei", prices, show_events_toggle=False, show_ma_toggle=False)
    sel_com, start_dt, end_dt = filters.commodity, filters.start_dt, filters.end_dt

    filtered = prices[
        (prices["commodity_name"] == sel_com)
        & (prices["date"] >= start_dt)
        & (prices["date"] <= end_dt)
    ].copy()

    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-header"><div class="page-title">💥 EVENT INTELLIGENCE</div>'
        '<div class="page-subtitle">▸ 30-day post-event market impact analysis</div></div>',
        unsafe_allow_html=True,
    )

    impact_rows = []
    sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🔵", "low": "🟢"}

    for _, ev in events.iterrows():
        if not (start_dt <= ev["date"] <= end_dt):
            continue
        d30 = ev["date"] + pd.Timedelta(days=30)
        p0 = filtered.loc[filtered["date"] == ev["date"], "close"]
        p30 = filtered.loc[filtered["date"] <= d30, "close"]
        if p0.empty or p30.empty:
            continue

        base_price, after_price = p0.iloc[0], p30.iloc[-1]
        pct = (after_price - base_price) / base_price * 100
        impact_rows.append(
            {
                "Date": ev["date"].strftime("%d %b %Y"),
                "Event": ev["event"],
                "Severity": f"{sev_icon.get(ev['severity'], '')} {ev['severity'].title()}",
                "At Event": f"${base_price:.2f}",
                "+30 Days": f"${after_price:.2f}",
                "Impact": f"{pct:+.1f}%",
                "_pct": pct,
                "_sev": ev["severity"],
                "_date": ev["date"],
            }
        )

    if not impact_rows:
        st.info("No event impact rows found for selected commodity and range.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    c1, c2 = st.columns([3, 2])
    with c1:
        table_df = pd.DataFrame(impact_rows).drop(columns=["_pct", "_sev", "_date"])
        st.dataframe(table_df, use_container_width=True, hide_index=True, height=360)

    with c2:
        st.plotly_chart(severity_avg_bar(impact_rows), use_container_width=True)

    st.plotly_chart(event_timeline_scatter(impact_rows), use_container_width=True)

    meta = COMMODITY_META.get(sel_com, {})
    st.markdown(
        f'<div class="ctx-box"><strong>{meta.get("icon", "🛢️")} {meta.get("label", sel_com)}</strong><br>'
        f'{meta.get("war_signal", "")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)