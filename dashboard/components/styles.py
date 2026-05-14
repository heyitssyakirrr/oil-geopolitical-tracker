"""
styles.py
---------
Global CSS for the Commodity Tracker dashboard.

PHILOSOPHY:
    Only cosmetic overrides — fonts, text colours, background colours.
    Never override layout geometry (width, height, margin, padding) on
    Streamlit's structural containers. Those differ between localhost and
    Streamlit Cloud, causing the layout bugs we are fixing.

SAFE to override:
    - font-family
    - color / background-color on leaf elements
    - scrollbar appearance

NOT SAFE (do not add these back):
    - block-container padding / max-width
    - stSidebarHeader height / positioning
    - stPlotlyChart width  →  use use_container_width=True instead
    - Any margin / padding on stVerticalBlock or stHorizontalBlock
"""

GLOBAL_CSS = """
<style>

/* ── 1. FONT IMPORT ──────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:wght@300;400;500;600&display=swap');


/* ── 2. APP-LEVEL FONT & BACKGROUND ─────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background-color: #080a0f;
    color: #d4cfc8;
}


/* ── 3. SIDEBAR BACKGROUND ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #0a0d14;
}


/* ── 4. METRIC WIDGET — colour only, no sizing ───────────────────────────── */
[data-testid="stMetricValue"] {
    color: #e8e2d8;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] {
    color: #8faad0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
[data-testid="stMetricDelta"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px !important;
}


/* ── 5. DATAFRAME — header and cell colours ──────────────────────────────── */
[data-testid="stDataFrame"] thead tr th {
    background-color: #0c0f18 !important;
    color: #8faad0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
[data-testid="stDataFrame"] tbody tr td {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    color: #b8cce4 !important;
    background-color: #0c0f18 !important;
}


/* ── 6. CAPTION (used for sidebar section labels) ───────────────────────── */
[data-testid="stSidebar"] .stCaption p {
    color: #4a6080 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    margin-top: 12px !important;
}


/* ── 7. DIVIDER ──────────────────────────────────────────────────────────── */
hr {
    border-color: #1a2035 !important;
}


/* ── 8. SCROLLBAR ────────────────────────────────────────────────────────── */
::-webkit-scrollbar       { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080a0f; }
::-webkit-scrollbar-thumb { background: #1a2035; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #2a3350; }

</style>
"""