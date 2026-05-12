"""
Global CSS for Commodity Pulse dashboard.
Dark industrial theme — high visibility, data-forward design.
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Base reset ────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #080a0f; color: #c8c2b8; }
.block-container { padding: 0.4rem 0.9rem 0.8rem 0.9rem !important; max-width: 100% !important; }
header[data-testid="stHeader"] { display: none !important; }

div[data-testid="stVerticalBlockSeparator"] { display: none !important; }
.element-container:empty { margin: 0 !important; padding: 0 !important; display: none !important; }

/* ── Global title bar ──────────────────────────────────── */
.dash-global-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.88rem;
    letter-spacing: 0.28em;
    color: #ff8a4c;
    padding: 9px 1.8rem 7px 1.8rem;
    border-bottom: 1px solid #1a2035;
    margin-bottom: 0;
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
    font-size: 0.78rem;
    letter-spacing: 0.18em;
}

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0a0d14 !important;
    border-right: 1px solid #1a2035 !important;
    width: 15vw !important;
    min-width: 230px !important;
    max-width: 270px !important;
}
[data-testid="stSidebarContent"] { padding: 0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }
}
[data-testid="collapsedControl"],
button[data-testid="stSidebarCollapseButton"] {
    background: #0a0d14 !important;
    border: 1px solid #1a2035 !important;
    color: #ff8a4c !important;
    position: fixed !important;
    top: 10px !important;
    left: 0px !important;
    z-index: 9999 !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}
[data-testid="collapsedControl"] svg,
button[data-testid="stSidebarCollapseButton"] svg { fill: #ff8a4c !important; }

/* ── Main content ─────────────────────────────────────── */
.main-content { padding: 0rem 1.8rem 3.2rem 1.8rem; max-width: 14200px; margin: 0 auto; }

/* ── Page header ──────────────────────────────────────── */
.page-header {
    padding: 10px 0 8px 0;
    border-bottom: 1px solid #1a2035;
    margin-bottom: 8px;
    display: flex;
    flex-direction: column;
    gap: 3px;
}
.page-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 0.1em;
    color: #e8e2d8;
    line-height: 1;
    margin: 0;
}
.page-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #ff8a4c;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Category badge on page header ───────────────────── */
.cat-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
    border: 1px solid;
    margin-bottom: 6px;
}

/* ── Filter bar ───────────────────────────────────────── */
.filter-bar {
    background: #0c0f18;
    border: 1px solid #1e2640;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 8px;
    margin-top: 4px;
}
.filter-bar div[data-baseweb="select"] > div,
.filter-bar div[data-baseweb="input"] {
    background: #111520 !important;
    border: 1px solid #1e2640 !important;
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
.filter-bar .stCheckbox {
    display: flex !important; align-items: center !important;
    padding: 0 8px !important; height: 36px !important;
    background: #111520 !important; border: 1px solid #1e2640 !important;
    border-radius: 4px !important; margin-top: 2px !important;
}
.filter-bar .stCheckbox label span {
    color: #c8d3ea !important; font-size: 12px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── KPI Grid — 5 across ──────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin-top: 14px;
    margin-bottom: 18px;
}
.kpi-card {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-top: 3px solid var(--kpi-accent, #ff8a4c);
    border-radius: 4px;
    padding: 14px 16px 12px;
    height: 112px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: border-color 0.2s ease;
}
.kpi-card:hover { border-color: #2a3350; }
.kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #8a9bbf;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.9rem;
    color: #e8e2d8;
    letter-spacing: 0.04em;
    line-height: 1;
}
.kpi-delta { font-family: 'IBM Plex Mono', monospace; font-size: 11px; }
.kpi-delta.up   { color: #ef4444; }
.kpi-delta.down { color: #22c55e; }
.kpi-delta.neu  { color: #6b7fa8; }
.kpi-note { font-family: 'IBM Plex Mono', monospace; font-size: 9.5px; color: #4a5878; margin-top: 2px; }

/* ── Section headings ─────────────────────────────────── */
.sec-head {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 0.1em;
    color: #e8e2d8;
    border-bottom: 1px solid #1a2035;
    padding-bottom: 4px;
    margin: 20px 0 4px;
}
.sec-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px;
    color: #6b7fa8;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* ── Alerts ───────────────────────────────────────────── */
.alert {
    padding: 10px 14px; border-radius: 3px; border-left: 3px solid;
    font-size: 12.5px; margin-bottom: 8px; line-height: 1.55;
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
    padding: 12px 16px;
    border-radius: 3px;
    font-size: 12px;
    color: #8a9bbf;
    line-height: 1.65;
    margin-bottom: 10px;
}
.ctx-box strong { color: #e8e2d8; }
.ctx-box .ctx-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8a4c;
    margin-bottom: 4px;
    display: block;
}

/* ── Ripple chain card ────────────────────────────────── */
.ripple-chain {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-radius: 6px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.ripple-chain .chain-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #ff8a4c;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.ripple-arrow {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
}
.ripple-node {
    background: #111520;
    border: 1px solid #2a3350;
    border-radius: 3px;
    padding: 4px 10px;
    color: #e8e2d8;
    font-size: 11px;
}
.ripple-node.source { border-color: #ff8a4c; color: #ff8a4c; }
.ripple-sep { color: #2a3350; font-size: 14px; }

/* ── Sidebar styles ───────────────────────────────────── */
.sb-brand {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.2em;
    color: #ff8a4c;
    padding: 12px 10px 2px;
    display: block;
}
.sb-tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #8a9bbf;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    padding: 0 10px 10px;
    display: block;
    border-bottom: 1px solid #1a2035;
}
.sb-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #8a9bbf;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 10px 10px 4px;
}
.sb-cat-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #2a3350;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 6px 10px 2px;
    border-top: 1px solid #1a2035;
    margin-top: 4px;
}

[data-testid="stSidebar"] button {
    text-align: left !important;
    justify-content: flex-start !important;
    padding-left: 12px !important;
}

[data-testid="stSidebar"] button p {
    text-align: left !important;
    font-size: 12px !important;
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
    padding: 8px 10px 8px 10px !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 !important;
    color: #8a9bbf !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.02em !important;
    line-height: 1.35 !important;
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
    color: #6b7fa8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-bottom: 1px solid #1a2035 !important;
}
.stDataFrame tbody tr td {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11.5px !important;
    color: #8a9bbf !important;
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
    font-size: 12px !important;
    border-radius: 3px !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #6b7fa8 !important;
    font-size: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.stCheckbox label span { color: #8a9bbf !important; font-size: 12px !important; }
.stCheckbox label span p { color: #8a9bbf !important; }

/* ── Stat row (inline metrics) ───────────────────────── */
.stat-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}
.stat-pill {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-radius: 3px;
    padding: 6px 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #8a9bbf;
    display: flex;
    gap: 8px;
    align-items: center;
}
.stat-pill .stat-val { color: #e8e2d8; font-weight: 600; }
.stat-pill .stat-up  { color: #ef4444; }
.stat-pill .stat-dn  { color: #22c55e; }

/* ── Overview category cards ─────────────────────────── */
.cat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 16px 0;
}
.cat-card {
    background: #0c0f18;
    border: 1px solid #1a2035;
    border-radius: 5px;
    padding: 16px 18px;
    cursor: pointer;
    transition: all 0.15s ease;
}
.cat-card:hover { background: #111520; border-color: #2a3350; }
.cat-card .cat-icon { font-size: 1.6rem; margin-bottom: 6px; }
.cat-card .cat-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 0.08em;
    color: #e8e2d8;
}
.cat-card .cat-count {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #4a5878;
    letter-spacing: 0.12em;
}
.cat-card .cat-change {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    margin-top: 6px;
}

/* ── Sidebar breathing room ───────────────────────────── */
[data-testid="stSidebar"] + section.main .block-container {
    padding-left: 1.4rem !important;
}

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080a0f; }
::-webkit-scrollbar-thumb { background: #1a2035; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #2a3350; }
</style>
"""