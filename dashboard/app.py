import streamlit as st

from components import GLOBAL_CSS, load_events, load_prices, load_runs, render_sidebar
from pages import commodity_comparison, event_intelligence, overview, pipeline, price_analysis

st.set_page_config(
    page_title="War & Oil Tracker",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Overview"

prices = load_prices()
events = load_events()
runs = load_runs()

render_sidebar(runs)

PAGE_RENDERERS = {
    "Overview": lambda: overview.render(prices, events),
    "Price Analysis": lambda: price_analysis.render(prices, events),
    "Event Intelligence": lambda: event_intelligence.render(prices, events),
    "Commodity Comparison": lambda: commodity_comparison.render(prices, events),
    "Pipeline": lambda: pipeline.render(runs),
}

renderer = PAGE_RENDERERS.get(st.session_state.page, PAGE_RENDERERS["Overview"])
renderer()