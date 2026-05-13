"""
Global CSS for Commodity Pulse dashboard.
Dark industrial theme — high visibility, data-forward design.
Font sizes bumped for readability across all screen sizes.
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Base reset ────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; font-size: 15px; }
.stApp { background: #080a0f; color: #d4cfc8 ; }
.block-container { padding: 0.4rem 2.5rem 0.8rem 2.5rem !important; max-width: 100% !important; width: 100% !important; }
header[data-testid="stHeader"] { background: transparent !important; }
header[data-testid="stHeader"]::before { display: none !important; }

div[data-testid="stPlotlyChart"] { width: 100% !important; }
div[data-testid="stPlotlyChart"] > div { width: 100% !important; }

div[data-testid="stVerticalBlockSeparator"] { display: none !important; }
.element-container:empty { margin: 0 !important; padding: 0 !important; display: none !important; }

/* ── Global title bar ──────────────────────────────────── */
.dash-global-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    letter-spacing: 0.28em;
    color: #ff8a4c;
    padding: 11px 0 9px 0;
    border-bottom: 1px solid #1a2035;
    margin-bottom: 10px;
    background: #080a0f;
    display: flex;
    align-items: center;
    gap: 10px;
}
.dash-global-title .title-sep {
    color: #2a3350;
    margin: 0 4px;
}
.dash-global-title .title-sub {
    color: #4a5878;
    font-size: 1rem;
    letter-spacing: 0.18em;
}

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0a0d14 !important;
    border-right: 1px solid #1a2035 !important;
    min-width: 245px !important;
    max-width: 285px !important;
}
/* Hide the logo spacer that causes the empty gap */
[data-testid="stLogoSpacer"] {
    display: none !important;
}

/* Shrink header to just fit the collapse button — no extra space */
[data-testid="stSidebarHeader"] {
    padding: 0 !important;
    min-height: 0 !important;
    height: auto !important;          /* let it size to its content */
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    background: #0a0d14 !important;
}

/* Make the collapse button visible and styled */
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: relative !important;
    margin: 6px 8px 0 auto !important;   /* push it away from the edge */
}

/* The actual button element */
[data-testid="stSidebarCollapseButton"] > button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 32px !important;
    height: 32px !important;
    padding: 0 !important;
    background: transparent !important;
    border: 1px solid #1a2035 !important;
    border-radius: 4px !important;
    color: #8faad0 !important;
    position: relative !important;
}

/* Make the hover highlight sit ON the button, not offset from it */
[data-testid="stSidebarCollapseButton"] > button:hover {
    background: #111520 !important;
    border-color: #ff8a4c !important;
    color: #ff8a4c !important;
}

/* Neutralise Streamlit's default ripple/focus overlay that causes the offset box */
[data-testid="stSidebarCollapseButton"] > button::before,
[data-testid="stSidebarCollapseButton"] > button::after {
    display: none !important;
}

button[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] [data-testid="stElementContainer"] {
    width: 100% !important;
}
[data-testid="stSidebarContent"] { 
    padding: 0 0 0 0 !important; 
}
[data-testid="stSidebarContent"] > div:first-child {
    padding: 0 10px !important;
}
[data-testid="stSidebarNav"] { 
    height: 0 !important;   
    overflow: hidden !important; 
}
section[data-testid="stSidebar"] > div:first-child { 
    padding-top: 0 !important; 
}
[data-testid="stSidebar"] div.stButton { 
    width: 100% !important; 
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
    background: #111520 !important;
    border: 1px solid #1a2035 !important;
    border-radius: 4px !important;
    width: 100% !important;
    height: 40px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding-left: 14px !important;
}
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p {
    font-size: 14px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    color: #c8d3ea !important;
}
[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0px !important;
    min-width: 0px !important;
    overflow: hidden !important;
}

/* ── Page header ──────────────────────────────────────── */
.page-header {
    padding: 12px 0 10px 0;
    border-bottom: 1px solid #1a2035;
    margin-bottom: 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.page-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 0.1em;
    color: #e8e2d8;
    line-height: 1;
    margin: 0;
}
.page-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #ff8a4c;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 5px;
}

/* ── Category badge on page header ───────────────────── */
.cat-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 2px;
    border: 1px solid;
    margin-bottom: 6px;
}

/* ── Filter bar ───────────────────────────────────────── */
.filter-bar {
    background: #0c0f18;
    border: 1px solid #1e2640;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 0px;
    margin-top: 0px;
}
.filter-bar div[data-baseweb="select"] > div,
.filter-bar div[data-baseweb="input"] {
    background: #111520 !important;
    border: 1px solid #1e2640 !important;
    border-radius: 4px !important;
    min-height: 40px !important;
    height: 40px !important;
}
.filter-bar input {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    color: #c8d3ea !important;
    height: 40px !important;
}
.filter-bar .stCheckbox {
    display: flex !important; align-items: center !important;
    padding: 0 10px !important; height: 40px !important;
    background: #111520 !important; border: 1px solid #1e2640 !important;
    border-radius: 4px !important; margin-top: 2px !important;
}
.filter-bar .stCheckbox label span {
    color: #c8d3ea !important; font-size: 13px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.filter-bar + div,
.filter-bar + div > div {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Collapse Streamlit wrappers between filter-bar and page-header */
.filter-bar + div[data-testid="stVerticalBlockBorderWrapper"],
.filter-bar + div[data-testid="element-container"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
    min-height: 0 !important;
}

/* ── KPI Grid — 5 across ──────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-top: 16px;
    margin-bottom: 20px;
}
.kpi-card {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-top: 3px solid var(--kpi-accent, #ff8a4c);
    border-radius: 4px;
    padding: 16px 18px 14px;
    height: 128px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: border-color 0.2s ease;
}
.kpi-card:hover { border-color: #2a3350; }
.kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #a8bcdf;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.3rem;
    color: #e8e2d8;
    letter-spacing: 0.04em;
    line-height: 1;
}
.kpi-delta { font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
.kpi-delta.up   { color: #ef4444; }
.kpi-delta.down { color: #22c55e; }
.kpi-delta.neu  { color: #8a9bbf ; }
.kpi-note { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #7a8faf; margin-top: 2px; }

/* ── Section headings ─────────────────────────────────── */
.sec-head {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.1em;
    color: #e8e2d8;
    border-bottom: 1px solid #1a2035;
    padding-bottom: 5px;
    margin: 22px 0 5px;
}
.sec-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #8faad0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 14px;
}

/* ── Alerts ───────────────────────────────────────────── */
.alert {
    padding: 12px 16px; border-radius: 3px; border-left: 3px solid;
    font-size: 14px; margin-bottom: 10px; line-height: 1.6;
    font-family: 'DM Sans', sans-serif;
}
.alert-red   { background: #140a0a; border-color: #ef4444; color: #fca5a5; }
.alert-amber { background: #13100a; border-color: #f59e0b; color: #fcd34d; }
.alert-blue  { background: #080e1a; border-color: #3b82f6; color: #93c5fd; }
.alert-green { background: #08120a; border-color: #22c55e; color: #86efac; }
.alert-purple{ background: #0f0a1a; border-color: #a78bfa; color: #c4b5fd; }

/* ── Context / info box ───────────────────────────────── */
.ctx-box {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-left: 3px solid #ff8a4c;
    padding: 14px 18px;
    border-radius: 3px;
    font-size: 13px;
    color: #b0c4de;
    line-height: 1.7;
    margin-bottom: 12px;
}
.ctx-box strong { color: #ffffff; }
.ctx-box .ctx-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ff8a4c;
    margin-bottom: 5px;
    display: block;
}

/* ── Ripple chain card ────────────────────────────────── */
.ripple-chain {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-radius: 6px;
    padding: 18px 22px;
    margin-bottom: 14px;
}
.ripple-chain .chain-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #ff8a4c;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.ripple-arrow {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
}
.ripple-node {
    background: #111520;
    border: 1px solid #2a3350;
    border-radius: 3px;
    padding: 5px 12px;
    color: #ffffff;
    font-size: 13px;
}
.ripple-node.source { border-color: #ff8a4c; color: #ff8a4c; }
.ripple-sep { color: #2a3350; font-size: 16px; }

/* ── Sidebar styles ───────────────────────────────────── */
.sb-brand {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    text-align: justify;
    letter-spacing: 0.2em;
    color: #ff8a4c;
    padding: 30px 14px;
    display: block;
    line-height: 1.2;
}
.sb-tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #8faad0;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0 14px 12px;
    display: block;
    border-bottom: 1px solid #1a2035;
}
.sb-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #8faad0;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    padding: 12px 12px 5px;
}
.sb-cat-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #2a3350;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 7px 12px 3px;
    border-top: 1px solid #1a2035;
    margin-top: 4px;
}

[data-testid="stSidebar"] button {
    text-align: left !important;
    justify-content: flex-start !important;
    padding-left: 14px !important;
}

[data-testid="stSidebar"] button p {
    text-align: left !important;
    font-size: 14px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    color: #c8d3ea !important;
}

/* ── Sidebar radio nav ────────────────────────────────── */
div[role="radiogroup"] label[data-baseweb="radio"] { margin: 0 !important; padding: 0 !important; }
div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child { display: none !important; }
div[role="radiogroup"] label[data-baseweb="radio"] > div:last-child {
    width: 100% !important;
    padding: 9px 12px 9px 12px !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 !important;
    color: #8a9bbf !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    letter-spacing: 0.02em !important;
    line-height: 1.4 !important;
}
div[role="radiogroup"] label[data-baseweb="radio"]:hover > div:last-child {
    background: #111520 !important;
    border-left-color: #ff8a4c !important;
    color: #e8e2d8 !important;
}
div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] > div:last-child {
    background: #131828 !important;
    border-left-color: #ff8a4c !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ── Table ─────────────────────────────────────────────── */
.stDataFrame thead tr th {
    background: #080a0f !important;
    color: #8faad0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-bottom: 1px solid #1a2035 !important;
}
.stDataFrame tbody tr td {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    color: #b8cce4 !important;
    background: #0c0f18 !important;
    border-bottom: 1px solid #111520 !important;
}
.stDataFrame { background: #0c0f18 !important; }

/* ── Inputs ───────────────────────────────────────────── */
.stSelectbox > div > div,
.stDateInput > div > div input,
.stDateInput input {
    background: #111520 !important;
    border: 1px solid #1a2035 !important;
    color: #c8c2b8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    border-radius: 3px !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #8faad0 !important;
    font-size: 12px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.stCheckbox label span { color: #8a9bbf !important; font-size: 13px !important; }
.stCheckbox label span p { color: #8a9bbf !important; }

/* ── Stat row (inline metrics) ───────────────────────── */
.stat-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.stat-pill {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-radius: 3px;
    padding: 7px 14px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #b0c4de;
    display: flex;
    gap: 9px;
    align-items: center;
}
.stat-pill .stat-val { color: #e8e2d8; font-weight: 600; }
.stat-pill .stat-up  { color: #ef4444; }
.stat-pill .stat-dn  { color: #22c55e; }

/* ── Overview category cards ─────────────────────────── */
.cat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 18px 0;
}
.cat-card {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-radius: 5px;
    padding: 18px 20px;
    cursor: pointer;
    transition: all 0.15s ease;
}
.cat-card:hover { background: #111520; border-color: #2a3350; }
.cat-card .cat-icon { font-size: 1.8rem; margin-bottom: 7px; }
.cat-card .cat-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.08em;
    color: #e8e2d8;
}
.cat-card .cat-count {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #7a8faf;
    letter-spacing: 0.1em;
}
.cat-card .cat-change {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    margin-top: 7px;
}

/* ── Sidebar breathing room ───────────────────────────── */
[data-testid="stSidebar"] + section.main .block-container {
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080a0f; }
::-webkit-scrollbar-thumb { background: #1a2035; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #2a3350; }
</style>
"""