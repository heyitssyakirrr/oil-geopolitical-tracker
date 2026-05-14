"""
app.py
------
Streamlit entry point for the Global Crisis — Commodity Tracker dashboard.

Routing uses a PAGE_RENDERERS dict so adding a new page is a single line:
    1. Add the import at the top of the imports block
    2. Add one entry to PAGE_RENDERERS

Data is loaded once per session via @st.cache_data / @st.cache_resource
in components/data.py — all page renderers receive the same DataFrames.
"""

import streamlit as st

from old_components.styles import GLOBAL_CSS
from old_components.data import load_prices, load_events, load_runs
from old_components.sidebar import render_sidebar

# ── Page imports ──────────────────────────────────────────────────────────────
# Grouped by nav section to mirror the sidebar structure.
# To add a page: import it here and add one entry to PAGE_RENDERERS below.
from pages.overview             import render as overview
from pages.energy               import render as energy
from pages.agriculture          import render as agriculture
from pages.livestock            import render as livestock
from pages.macro                import render as macro
from pages.ripple_effects       import render as ripple_effects
from pages.event_intelligence   import render as event_intelligence
from pages.price_analysis       import render as price_analysis
from pages.commodity_comparison import render as commodity_comparison
from pages.pipeline             import render as pipeline

# ── Must be the very first Streamlit call ─────────────────────────────────────
st.set_page_config(
    page_title="Commodity Tracker",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject cosmetic CSS (fonts + colours only, no layout overrides) ───────────
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Overview"

# ── Load data (cached — runs once, not on every interaction) ──────────────────
prices = load_prices()
events = load_events()
runs   = load_runs()

# ── Sidebar navigation (sets st.session_state.page on click) ─────────────────
render_sidebar(runs)

# ── Page renderer registry ────────────────────────────────────────────────────
# Keys match exactly what render_sidebar() writes to st.session_state.page.
# Values are zero-argument callables — lambdas bind the correct DataFrames
# so every render function keeps its own signature (prices, events) or (runs).
#
# To add a page:
#   1. Import its render function above
#   2. Add one line here: "Page Name": lambda: new_page(prices, events)
PAGE_RENDERERS = {
    # Main
    "Overview":           lambda: overview(prices, events),
    # By category
    "Energy":             lambda: energy(prices, events),
    "Agriculture":        lambda: agriculture(prices, events),
    "Livestock":          lambda: livestock(prices, events),
    "Macro":              lambda: macro(prices, events),
    # Analysis
    "Ripple Effects":     lambda: ripple_effects(prices, events),
    "Event Intelligence": lambda: event_intelligence(prices, events),
    "Price Analysis":     lambda: price_analysis(prices, events),
    "Comparison":         lambda: commodity_comparison(prices, events),
    # System
    "Pipeline":           lambda: pipeline(runs),
}

# ── Route to the active page ──────────────────────────────────────────────────
# dict.get(key, default) falls back to Overview for any unknown page name,
# so a stale session_state value can never produce a crash.
renderer = PAGE_RENDERERS.get(
    st.session_state.page,
    PAGE_RENDERERS["Overview"],
)
renderer()