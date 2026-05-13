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
.stApp { background: #080a0f; color: #d4cfc8; }
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
    margin-bottom: 8px;
    background: #080a0f;
    display: flex;
    align-items: center;
    gap: 10px;
}
.dash-global-title .title-sep { color: #2a3350; margin: 0 4px; }
.dash-global-title .title-sub { color: #4a5878; font-size: 1rem; letter-spacing: 0.18em; }

/* ══════════════════════════════════════════════════════════
   SIDEBAR
   DOM order:
     [data-testid="stSidebarHeader"]   ← logo + collapse button
     [data-testid="stSidebarContent"]  ← nav + footer
   ══════════════════════════════════════════════════════════ */

/* Sidebar shell */
[data-testid="stSidebar"] {
    background: #0a0d14 !important;
    border-right: 1px solid #1a2035 !important;
    min-width: 240px !important;
    max-width: 270px !important;
}

/* ── Header row ───────────────────────────────────────────
   Contains: logo slot (left)  |  collapse button (right)
   We style this row so both items sit on the same baseline.
   ────────────────────────────────────────────────────────*/
[data-testid="stSidebarHeader"] {
    background: #0a0d14 !important;
    border-bottom: 1px solid #1a2035 !important;
    padding: 0 10px 0 12px !important;
    min-height: 52px !important;
    height: 52px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 8px !important;
    box-sizing: border-box !important;
}

/* Logo container — icon only, left side of header row */
[data-testid="stLogo"] {
    flex: 0 0 auto !important;
    display: flex !important;
    align-items: center !important;
}
[data-testid="stLogo"] img {
    width: 32px !important;
    height: 32px !important;
    display: block !important;
}
/* Hide logo in the collapsed sidebar bar — only expand arrow should show */
[data-testid="collapsedControl"] [data-testid="stLogo"],
[data-testid="collapsedControl"] img {
    display: none !important;
}

/* stLogoSpacer appears when there is no logo — hide it */
[data-testid="stLogoSpacer"] {
    display: none !important;
}

/* Collapse / expand button — right side of header row */
/* ── Sidebar title block ──────────────────────────────
   Inside stSidebarContent so it vanishes on collapse.
   ──────────────────────────────────────────────────── */
.sb-title-block {
    display: flex;
    flex-direction: column;
    gap: 0px;
    padding: 14px 4px 12px;
    border-bottom: 1px solid #1a2035;
    margin-bottom: 4px;
}
.sb-title-line1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.25rem;
    letter-spacing: 0.2em;
    color: #ff8a4c;
    line-height: 1.25;
    display: block;
}
.sb-title-line2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.25rem;
    letter-spacing: 0.2em;
    color: #ff8a4c;
    line-height: 1.25;
    display: block;
}

/* ── Sidebar content area ─────────────────────────────── */
[data-testid="stSidebarContent"] {
    padding: 0 !important;
    overflow-y: auto !important;
}
[data-testid="stSidebarContent"] > div:first-child {
    padding: 8px 12px 16px !important;
}
[data-testid="stSidebar"] [data-testid="stElementContainer"] {
    width: 100% !important;
}
/* Hide Streamlit's auto-generated nav (we build our own) */
[data-testid="stSidebarNav"] {
    height: 0 !important;
    overflow: hidden !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
/* Collapsed sidebar — zero width */
[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0 !important;
    min-width: 0 !important;
    overflow: hidden !important;
}

/* ── Section labels ───────────────────────────────────── */
p.sb-section-label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    color: #4a5878 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 14px 4px 5px !important;
    margin: 0 !important;
    line-height: 1 !important;
}

/* ── Nav item wrapper ─────────────────────────────────── */
div.sb-nav-item,
div.sb-nav-item--active {
    margin-bottom: 2px !important;
}

/* Default button style */
div.sb-nav-item [data-testid="stBaseButton-secondary"],
div.sb-nav-item--active [data-testid="stBaseButton-secondary"] {
    width: 100% !important;
    height: 38px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding-left: 10px !important;
    border-radius: 4px !important;
    transition: background 0.12s, border-color 0.12s !important;
}
div.sb-nav-item [data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    border: 1px solid transparent !important;
}
div.sb-nav-item [data-testid="stBaseButton-secondary"]:hover {
    background: #111827 !important;
    border-color: #1e2a40 !important;
}

/* Active page — orange left accent */
div.sb-nav-item--active [data-testid="stBaseButton-secondary"] {
    background: #0f1520 !important;
    border: 1px solid #1e2640 !important;
    border-left: 3px solid #ff8a4c !important;
    padding-left: 8px !important;   /* compensate for thicker left border */
}

/* Button label text */
div.sb-nav-item [data-testid="stBaseButton-secondary"] p,
div.sb-nav-item--active [data-testid="stBaseButton-secondary"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
div.sb-nav-item [data-testid="stBaseButton-secondary"] p {
    color: #7a8faf !important;
}
div.sb-nav-item [data-testid="stBaseButton-secondary"]:hover p {
    color: #c8d3ea !important;
}
div.sb-nav-item--active [data-testid="stBaseButton-secondary"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ── Pipeline run footer ──────────────────────────────── */
.sb-run-footer {
    padding: 12px 4px 8px;
    border-top: 1px solid #1a2035;
    margin-top: 12px;
}
.sb-run-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #4a5878;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.sb-run-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.04em;
}

/* ── Sidebar breathing room ───────────────────────────── */
[data-testid="stSidebar"] + section.main .block-container {
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
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

/* ── Category badge ───────────────────────────────────── */
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
    margin-bottom: 0;
    margin-top: 0;
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
    display: flex !important;
    align-items: center !important;
    padding: 0 10px !important;
    height: 40px !important;
    background: #111520 !important;
    border: 1px solid #1e2640 !important;
    border-radius: 4px !important;
    margin-top: 2px !important;
}
.filter-bar .stCheckbox label span {
    color: #c8d3ea !important;
    font-size: 13px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.filter-bar + div,
.filter-bar + div > div { margin-top: 0 !important; padding-top: 0 !important; }
.filter-bar + div[data-testid="stVerticalBlockBorderWrapper"],
.filter-bar + div[data-testid="element-container"] { margin-top: 0 !important; padding-top: 0 !important; min-height: 0 !important; }

/* ── KPI grid ─────────────────────────────────────────── */
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
.kpi-label { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #a8bcdf; letter-spacing: 0.15em; text-transform: uppercase; }
.kpi-value { font-family: 'Bebas Neue', sans-serif; font-size: 2.3rem; color: #e8e2d8; letter-spacing: 0.04em; line-height: 1; }
.kpi-delta { font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
.kpi-delta.up   { color: #ef4444; }
.kpi-delta.down { color: #22c55e; }
.kpi-delta.neu  { color: #8a9bbf; }
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
.alert { padding: 12px 16px; border-radius: 3px; border-left: 3px solid; font-size: 14px; margin-bottom: 10px; line-height: 1.6; font-family: 'DM Sans', sans-serif; }
.alert-red    { background: #140a0a; border-color: #ef4444; color: #fca5a5; }
.alert-amber  { background: #13100a; border-color: #f59e0b; color: #fcd34d; }
.alert-blue   { background: #080e1a; border-color: #3b82f6; color: #93c5fd; }
.alert-green  { background: #08120a; border-color: #22c55e; color: #86efac; }
.alert-purple { background: #0f0a1a; border-color: #a78bfa; color: #c4b5fd; }

/* ── Context box ──────────────────────────────────────── */
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
.ctx-box .ctx-label { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: #ff8a4c; margin-bottom: 5px; display: block; }

/* ── Ripple chain ─────────────────────────────────────── */
.ripple-chain { background: #0c0f18; border: 1px solid #1a2035; border-radius: 6px; padding: 18px 22px; margin-bottom: 14px; }
.ripple-chain .chain-title { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #ff8a4c; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 14px; }
.ripple-arrow { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; font-family: 'IBM Plex Mono', monospace; font-size: 13px; }
.ripple-node { background: #111520; border: 1px solid #2a3350; border-radius: 3px; padding: 5px 12px; color: #ffffff; font-size: 13px; }
.ripple-node.source { border-color: #ff8a4c; color: #ff8a4c; }
.ripple-sep { color: #2a3350; font-size: 16px; }

/* ── Stat row ─────────────────────────────────────────── */
.stat-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 12px; }
.stat-pill { background: #0c0f18; border: 1px solid #1a2035; border-radius: 3px; padding: 7px 14px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #b0c4de; display: flex; gap: 9px; align-items: center; }
.stat-pill .stat-val { color: #e8e2d8; font-weight: 600; }
.stat-pill .stat-up  { color: #ef4444; }
.stat-pill .stat-dn  { color: #22c55e; }

/* ── Category cards ───────────────────────────────────── */
.cat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 18px 0; }
.cat-card { background: #0c0f18; border: 1px solid #1a2035; border-radius: 5px; padding: 18px 20px; cursor: pointer; transition: all 0.15s ease; }
.cat-card:hover { background: #111520; border-color: #2a3350; }
.cat-card .cat-icon { font-size: 1.8rem; margin-bottom: 7px; }
.cat-card .cat-name { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 0.08em; color: #e8e2d8; }
.cat-card .cat-count { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #7a8faf; letter-spacing: 0.1em; }
.cat-card .cat-change { font-family: 'IBM Plex Mono', monospace; font-size: 13px; margin-top: 7px; }

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
label[data-testid="stWidgetLabel"] p { color: #8faad0 !important; font-size: 12px !important; font-family: 'IBM Plex Mono', monospace !important; letter-spacing: 0.08em; text-transform: uppercase; }
.stCheckbox label span { color: #8a9bbf !important; font-size: 13px !important; }
.stCheckbox label span p { color: #8a9bbf !important; }

/* ── Table ────────────────────────────────────────────── */
.stDataFrame thead tr th { background: #080a0f !important; color: #8faad0 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important; letter-spacing: 0.08em; text-transform: uppercase; border-bottom: 1px solid #1a2035 !important; }
.stDataFrame tbody tr td { font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; color: #b8cce4 !important; background: #0c0f18 !important; border-bottom: 1px solid #111520 !important; }
.stDataFrame { background: #0c0f18 !important; }

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080a0f; }
::-webkit-scrollbar-thumb { background: #1a2035; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #2a3350; }
</style>
"""