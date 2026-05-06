"""
Global CSS styles for the War & Oil dashboard.
Centralised here so layout changes don't require hunting through page files.
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ─────────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0b0d11; color: #c8c2b8; }
.block-container { padding: 0.4rem 0.9rem 0.8rem 0.9rem !important; max-width: 100% !important; }
header[data-testid="stHeader"] { display: none !important; }

/* Kill Streamlit's auto-injected vertical gaps */
.main-content .stVerticalBlock > [data-testid="stVerticalBlock"] > div:empty {
    display: none !important;
}
div[data-testid="stVerticalBlockSeparator"] {
    display: none !important;
}
.element-container:empty {
    margin: 0 !important;
    padding: 0 !important;
    display: none !important;
}

/* ── Dashboard Title ───────────────────────────────────── */

.dash-global-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.95rem;
    letter-spacing: 0.22em;
    color: #e25c2e;
    padding: 8px 1.8rem 6px 1.8rem;
    border-bottom: 1px solid #1c2030;
    margin-bottom: 0;
    background: #0b0d11;
}

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0e1017 !important;
    border-right: 1px solid #1c2030 !important;
    width: 15vw !important;
    min-width: 240px !important;
    max-width: 280px !important;
}

[data-testid="stSidebarContent"] { padding: 0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }

/* Fully hide sidebar panel when collapsed to avoid phantom scrollbar rail */
[data-testid="stSidebar"][aria-expanded="false"] {
    min-width: 0 !important;
    width: 0 !important;
    border-right: none !important;
    overflow: hidden !important;
}
[data-testid="stSidebar"][aria-expanded="false"] > div {
    width: 0 !important;
    min-width: 0 !important;
    overflow: hidden !important;
}

/* Collapsed sidebar toggle button */
[data-testid="collapsedControl"] {
    background: #0e1017 !important;
    border-right: 1px solid #1c2030 !important;
    color: #ff8a4c !important;
    top: 10px !important;
    left: 0px !important;
    position: fixed !important;
    z-index: 9999 !important;
}
[data-testid="collapsedControl"] svg { fill: #ff8a4c !important; }

/* Keep sidebar visually stable: hide close button so layout doesn't collapse away */
button[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* ── Main content ─────────────────────────────────────── */
.main-content { padding: 0rem 1.8rem 3.2rem 1.8rem; max-width: 14200px; margin: 0 auto; }

/* ── Page header ──────────────────────────────────────── */
.page-header { padding: xpx 0 4px 0; border-bottom: 1px solid #1c2030; margin-bottom: 6px; }
.page-title  { font-family: 'Bebas Neue', sans-serif; font-size: 2.4rem; letter-spacing: 0.12em; color: #e8e2d8; line-height: 1; margin: 0; display: flex; align-items: center; gap: 12px; }
.page-subtitle { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #e25c2e; letter-spacing: 0.22em; text-transform: uppercase; margin-top: 5px; }

/* ── Filter bar ───────────────────────────────────────── */
.filter-bar {
    background: #0e1017;
    border: 1px solid #252d42;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 6px;
    margin-top: 4px;
}

/* Make selectbox and date input same height and style */
.filter-bar div[data-baseweb="select"] > div,
.filter-bar div[data-baseweb="input"] {
    background: #13161f !important;
    border: 1px solid #252d42 !important;
    border-radius: 4px !important;
    min-height: 36px !important;
    height: 36px !important;
}

.filter-bar input {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    color: #c8d3ea !important;
    height: 36px !important;
}

/* Checkbox alignment inside filter bar */
.filter-bar .stCheckbox {
    display: flex !important;
    align-items: center !important;
    padding: 0 8px !important;
    height: 36px !important;
    background: #13161f !important;
    border: 1px solid #252d42 !important;
    border-radius: 4px !important;
    margin-top: 2px !important;
}

.filter-bar .stCheckbox label span {
    color: #c8d3ea !important;
    font-size: 12px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── KPI Grid ─────────────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px;margin-top: 18px; margin-bottom: 20px; }
.kpi-card {
    background: #0e1017; border: 1px solid #1c2030; border-top: 3px solid #e25c2e;
    border-radius: 3px; padding: 16px 18px 14px;
    height: 120px; box-sizing: border-box;
    display: flex; flex-direction: column; justify-content: space-between;
}
.kpi-label { font-family: 'IBM Plex Mono', monospace; font-size: 9.5px; color: #c8d3ea; letter-spacing: 0.18em; text-transform: uppercase; }
.kpi-value { font-family: 'Bebas Neue', sans-serif; font-size: 2rem; color: #e8e2d8; letter-spacing: 0.04em; line-height: 1; }
.kpi-delta { font-family: 'IBM Plex Mono', monospace; font-size: 11px; }
.kpi-delta.up   { color: #ef4444; }
.kpi-delta.down { color: #22c55e; }
.kpi-delta.neu  { color: #C2cde0; }
.kpi-note { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #7a8ba8; margin-top: 3px; }

/* ── Section headings ─────────────────────────────────── */
.sec-head { font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; letter-spacing: 0.1em; color: #e8e2d8; border-bottom: 1px solid #1c2030; padding-bottom: 5px; margin: 24px 0 4px; }
.sec-sub  { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #c8d3ea; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 14px; }

/* ── Alerts ───────────────────────────────────────────── */
.alert { padding: 10px 14px; border-radius: 2px; border-left: 3px solid; font-size: 12.5px; margin-bottom: 8px; line-height: 1.5; }
.alert-red   { background:#160b0b; border-color:#ef4444; color:#fca5a5; }
.alert-amber { background:#15110a; border-color:#f59e0b; color:#fcd34d; }
.alert-blue  { background:#0a0e18; border-color:#3b82f6; color:#93c5fd; }
.alert-green { background:#0a120b; border-color:#22c55e; color:#86efac; }

/* ── Context box ──────────────────────────────────────── */
.ctx-box {
    background: #0e1017; border: 1px solid #1c2030; border-left: 3px solid #e25c2e;
    padding: 12px 16px; border-radius: 2px; font-size: 12px; color: #9ba3b5;
    line-height: 1.65; margin-bottom: 10px;
}
.ctx-box strong { color: #e8e2d8; }

/* ── Sidebar nav items ────────────────────────────────── */
.sb-brand   { font-family: 'Bebas Neue', sans-serif; font-size: 1.15rem; letter-spacing: 0.18em; color: #e25c2e; padding: 10px 8px 4px; display: block; }
.sb-tagline { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #8a9bbf; letter-spacing: 0.2em; text-transform: uppercase; padding: 0 10px 8px; display: block; border-bottom: 1px solid #1c2030; }
.sb-section { font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #8a9bbf; letter-spacing: 0.15em; text-transform: uppercase; padding: 8px 10px 4px; }

.sb-nav-active {
    border-left: 3px solid #e25c2e; background: #13161f;
    font-family: 'IBM Plex Mono', monospace; font-size: 13px; color: #e25c2e;
    padding: 10px 14px; letter-spacing: 0.06em; cursor: default;
    display: flex; align-items: center; gap: 6px;
}
.sb-nav-item {
    font-family: 'IBM Plex Mono', monospace; font-size: 12px;
    color: #e8e2d8; padding: 10px 14px; letter-spacing: 0.06em;
    border-left: 3px solid transparent;
    display: flex; align-items: center; gap: 6px;
    transition: all 0.15s ease;
}
.sb-nav-item:hover { background: #13161f; color: #c8c2b8; border-left-color: #e25c2e; }

div[data-testid="stButton"] > button {
    width: 100%; background: transparent !important; border: none !important;
    border-left: 3px solid transparent !important; border-radius: 0 !important;
    color: #C2cde0 !important; font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important; letter-spacing: 0.06em !important;
    text-align: left !important; padding: 10px 14px !important;
    transition: all 0.15s ease !important; line-height: 1.4 !important;
    height: auto !important; min-height: 40px !important;
}
div[data-testid="stButton"] > button:hover {
    background: #13161f !important; color: #c8c2b8 !important;
    border-left-color: #e25c2e !important;
}
div[data-testid="stButton"] > button:focus {
    box-shadow: none !important; outline: none !important;
}

/* ── Sidebar radio navigation ───────────────────────── */
div[role="radiogroup"] label[data-baseweb="radio"] {
    margin: 0 !important;
    padding: 0 !important;
}
div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
    display: none !important;
}
div[role="radiogroup"] label[data-baseweb="radio"] > div:last-child {
    width: 100% !important;
    padding: 9px 10px 9px 10px !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 !important;
    color: #e8e2d8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    letter-spacing: 0.02em !important;
    line-height: 1.35 !important;
}
div[role="radiogroup"] label[data-baseweb="radio"]:hover > div:last-child {
    background: #13161f !important;
    border-left-color: #ff8a4c !important;
}
div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] > div:last-child {
    background: #151a27 !important;
    border-left-color: #e25c2e !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* ── Table styles ─────────────────────────────────────── */
.stDataFrame thead tr th {
    background: #0b0d11 !important; color: #a5b4cf !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 0.1em;
    text-transform: uppercase; border-bottom: 1px solid #1c2030 !important;
}
.stDataFrame tbody tr td {
    font-family: 'IBM Plex Mono', monospace !important; font-size: 11.5px !important;
    color: #9ba3b5 !important; background: #0e1017 !important;
    border-bottom: 1px solid #13161f !important;
}
.stDataFrame { background: #0e1017 !important; }

/* ── Inputs ───────────────────────────────────────────── */
.stSelectbox > div > div,
.stDateInput > div > div input,
.stDateInput input {
    background: #13161f !important; border: 1px solid #1c2030 !important;
    color: #c8c2b8 !important; font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important; border-radius: 3px !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #a5b4cf !important; font-size: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    letter-spacing: 0.1em; text-transform: uppercase;
}
.stCheckbox label span { color: #9ba3b5 !important; font-size: 12px !important; }
.stCheckbox label span p { color: #9ba3b5 !important; }

/* Keep breathing room between sidebar and content */
[data-testid="stSidebar"] + section.main .block-container {
    padding-left: 1.4rem !important;
}
</style>
"""