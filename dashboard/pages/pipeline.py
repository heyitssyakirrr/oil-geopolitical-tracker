import streamlit as st

from components import pipeline_bar


def render(runs):
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-header"><div class="page-title">🔧 PIPELINE</div>'
        '<div class="page-subtitle">▸ ingestion run status and row volume</div></div>',
        unsafe_allow_html=True,
    )
    if runs.empty:
        st.warning("No pipeline runs available.")
    else:
        st.plotly_chart(pipeline_bar(runs), use_container_width=True)
        st.dataframe(runs, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)