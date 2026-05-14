import streamlit as st

from old_components import pipeline_bar

def _prepare_runs_table(runs):
    """Normalize pipeline runs for stable rendering in Streamlit table."""
    table = runs.copy()
    if "started_at" in table.columns:
        table["started_at"] = table["started_at"].astype("datetime64[ns]").dt.strftime("%Y-%m-%d %H:%M:%S")
    if "rows_loaded" in table.columns:
        table["rows_loaded"] = table["rows_loaded"].fillna(0).astype(int)
    return table


def render(runs):
    st.markdown(
        '<div class="page-header"><div class="page-title">🔧 PIPELINE</div>'
        '<div class="page-subtitle">▸ ingestion run status and row volume</div></div>',
        unsafe_allow_html=True,
    )
    if runs.empty:
        st.warning("No pipeline runs available.")
    else:
        st.plotly_chart(pipeline_bar(runs), width='stretch')
        st.dataframe(
            _prepare_runs_table(runs),
            width='stretch',
            hide_index=True,
            height=360,
        )
    st.markdown('</div>', unsafe_allow_html=True)