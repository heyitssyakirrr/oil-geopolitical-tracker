import streamlit as st

from components import GLOBAL_CSS, load_events, load_prices, load_runs, render_sidebar
from pages import (
    overview,
    energy,
    agriculture,
    livestock,
    macro,
    ripple_effects,
    event_intelligence,
    price_analysis,
    commodity_comparison,
    pipeline,
)

st.set_page_config(
    page_title="War & Oil Tracker",
    page_icon="🛢️",
    layout="wide", # use the full browser width instead of the default narrow centred column
    initial_sidebar_state="auto",
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Overview"

# these three calls will be cached by Streamlit, 
# so they won't hit the database on every interaction, 
# just the first load and when the underlying data changes
prices = load_prices()
events = load_events()
runs   = load_runs()

# receives runs to display the last pipeline run status
# uses with st.sidebar: to place everything inside sidebar panel
render_sidebar(runs)

# lambda functions to be called when a page is selected from the sidebar
PAGE_RENDERERS = {
    # Main
    "Overview":           lambda: overview.render(prices, events),
    # By category
    "Energy":             lambda: energy.render(prices, events),
    "Agriculture":        lambda: agriculture.render(prices, events),
    "Livestock":          lambda: livestock.render(prices, events),
    "Macro":              lambda: macro.render(prices, events),
    # Analysis
    "Ripple Effects":     lambda: ripple_effects.render(prices, events),
    "Event Intelligence": lambda: event_intelligence.render(prices, events),
    "Price Analysis":     lambda: price_analysis.render(prices, events),
    "Comparison":         lambda: commodity_comparison.render(prices, events),
    # System
    "Pipeline":           lambda: pipeline.render(runs),
}

st.markdown(
    '<div class="dash-global-title">'
    '🛢️ WAR &amp; OIL TRACKER &nbsp;·&nbsp; GEOPOLITICAL COMMODITY DASHBOARD'
    '</div>',
    unsafe_allow_html=True,
)

# dict dispatch here is cleaner than long if/elif chains for routing
# dict.get(key, default)
renderer = PAGE_RENDERERS.get(st.session_state.page, PAGE_RENDERERS["Overview"]) # now is a function
renderer() # call the function to render the selected page