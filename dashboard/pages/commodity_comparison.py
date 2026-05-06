import streamlit as st

from components import correlation_heatmap, label_map, normalized_comparison_chart, render_filter_bar, volatility_ranking_bar


def render(prices, events):
    filters = render_filter_bar("cc", prices, show_commodity=False, show_ma_toggle=False)
    start_dt, end_dt, show_ev = filters.start_dt, filters.end_dt, filters.show_ev

    comp_df = prices[(prices["date"] >= start_dt) & (prices["date"] <= end_dt)].copy()

    def normalize(group):
        base = group["close"].iloc[0]
        if base != 0:
            group = group.copy()
            group["norm"] = group["close"] / base * 100
        return group

    comp_df = comp_df.groupby("commodity_name", group_keys=False).apply(normalize)
    comp_df["label"] = comp_df["commodity_name"].map(label_map).fillna(comp_df["commodity_name"])

    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-header"><div class="page-title">📊 COMMODITY COMPARISON</div>'
        '<div class="page-subtitle">▸ normalized co-movement and volatility ranking</div></div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(normalized_comparison_chart(comp_df, events, start_dt, end_dt, show_ev), use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(volatility_ranking_bar(comp_df), use_container_width=True)
    with c2:
        st.plotly_chart(correlation_heatmap(comp_df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)