"""
Global CSS for the Global Crisis · Commodity Tracker dashboard.
Dark industrial theme — high visibility, data-forward design.

CSS sections:
    1.  Base reset & app shell
    2.  Global title bar
    3.  Sidebar — shell & header row
    4.  Sidebar — brand block
    5.  Sidebar — nav section labels
    6.  Sidebar — nav buttons (default + active)
    7.  Sidebar — pipeline run footer
    8.  Page header & category badge
    9.  Filter bar
    10. KPI grid & cards
    11. Section headings
    12. Alerts & context boxes
    13. Ripple chain
    14. Stat pills
    15. Category cards (overview grid)
    16. Form inputs & labels
    17. Data table
    18. Scrollbar
"""

GLOBAL_CSS = """
<style>
/* ─────────────────────────────────────────────────────────────
   FONTS
───────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');


/* ─────────────────────────────────────────────────────────────
   1. BASE RESET & APP SHELL
───────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
}
.stApp {
    background: #080a0f;
    color: #d4cfc8;
}
.block-container {
    padding: 0.4rem 2.5rem 0.8rem 2.5rem !important;
    max-width: 100% !important;
    width: 100% !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
}
header[data-testid="stHeader"]::before {
    display: none !important;
}
div[data-testid="stPlotlyChart"],
div[data-testid="stPlotlyChart"] > div {
    width: 100% !important;
}
div[data-testid="stVerticalBlockSeparator"],
.element-container:empty {
    display: none !important;
    margin: 0 !important;
    padding: 0 !important;
}


/* ─────────────────────────────────────────────────────────────
   2. GLOBAL TITLE BAR  (top of main content area)
───────────────────────────────────────────────────────────── */
.dash-global-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.3rem;
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


/* ─────────────────────────────────────────────────────────────
   3. SIDEBAR — SHELL & HEADER ROW

   Strategy: give stSidebarHeader a fixed height that matches
   the brand block height exactly.  The brand block in
   stSidebarContent uses a negative top margin to pull itself
   up behind the header row, so the collapse button (inside
   stSidebarHeader) and the brand text appear on the same
   visual row with zero gap between them.

   stSidebarHeader: 52px tall, holds only the collapse button
   .sb-brand:       margin-top: -52px to slide up behind it
   Result:          one seamless row — icon+title on left,
                    collapse button on right.

   FIX: overflow changed from visible → hidden, width/box-sizing
   added, and stSidebarCollapseButton explicitly constrained so
   the collapse button cannot escape the sidebar's bounds.
───────────────────────────────────────────────────────────── */

/* Sidebar shell */
[data-testid="stSidebar"] {
    background: #0a0d14 !important;
    border-right: 1px solid #1e2640 !important;
    min-width: 248px !important;
    max-width: 268px !important;
}

/* Collapsed: zero width, nothing visible */
[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0 !important;
    min-width: 0 !important;
    overflow: hidden !important;
}

/* Header row — real height, matches brand block height.
   Transparent so the brand block behind it shows through.
   overflow:hidden + width:100% keeps the collapse button
   from spilling outside the sidebar's visible area. */
[data-testid="stSidebarHeader"] {
    background: transparent !important;
    border-bottom: none !important;
    height: 52px !important;
    min-height: 52px !important;
    padding: 0 8px 0 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    position: relative !important;
    z-index: 10 !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    width: 100% !important;
}

/* Collapse button container — keep it in-flow and visible */
[data-testid="stSidebarCollapseButton"] {
    position: relative !important;
    z-index: 11 !important;
    flex-shrink: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    margin-right: 4px !important;
}

/* Style the collapse button to match our theme */
[data-testid="stSidebarHeader"] button {
    background: transparent !important;
    border: none !important;
    color: #4a5878 !important;
    padding: 4px !important;
    border-radius: 4px !important;
}
[data-testid="stSidebarHeader"] button:hover {
    background: #1a2035 !important;
    color: #c8d3ea !important;
}

/* Expand button (when sidebar is collapsed) — also themed */
[data-testid="stSidebarCollapsedControl"] button {
    background: #0a0d14 !important;
    border: 1px solid #1e2640 !important;
    border-radius: 4px !important;
    color: #7a8faf !important;
}
[data-testid="stSidebarCollapsedControl"] button:hover {
    background: #111520 !important;
    color: #c8d3ea !important;
}

/* Hide logo — not used */
[data-testid="stLogo"],
[data-testid="stLogoSpacer"] {
    display: none !important;
}

/* Sidebar content */
[data-testid="stSidebarContent"] {
    padding: 0 !important;
    overflow-y: auto !important;
}
[data-testid="stSidebarContent"] > div:first-child {
    padding: 0 20px 16px !important;
}
[data-testid="stSidebar"] [data-testid="stElementContainer"] {
    width: 100% !important;
}

/* Kill the default vertical gap Streamlit sets on stVerticalBlock inside
   the sidebar — this is what makes every element inside the sidebar have
   a large gap between it and the next one */
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* Hide Streamlit's auto-generated page nav */
[data-testid="stSidebarNav"] {
    height: 0 !important;
    overflow: hidden !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}


/* ─────────────────────────────────────────────────────────────
   4. SIDEBAR — BRAND BLOCK

   Pulled up by margin-top: -52px to sit behind stSidebarHeader.
   Its own height is 52px so the border-bottom lands exactly
   where the header row ends — creating one seamless header band.
   The collapse button (z-index: 11) renders on top of it.
───────────────────────────────────────────────────────────── */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    height: 52px;                   /* match stSidebarHeader height */
    margin-top: -52px;              /* pull up behind the header row */
    padding: 0 8px 0 14px;
    border-bottom: 1px solid #1e2640;
    background: #0a0d14;            /* same as sidebar bg */
    position: relative;
    z-index: 1;                     /* below the collapse button */
    box-sizing: border-box;
}
.sb-brand-icon {
    font-size: 1.5rem;
    line-height: 1;
    flex-shrink: 0;
}
.sb-brand-text {
    display: flex;
    flex-direction: column;
    gap: 0;
    line-height: 1.15;
}
.sb-brand-line1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 0.18em;
    color: #ff8a4c;
    display: block;
}
.sb-brand-line2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 0.18em;
    color: #ff8a4c;
    display: block;
}


/* ─────────────────────────────────────────────────────────────
   5. SIDEBAR — NAV SECTION LABELS  (MAIN / BY CATEGORY / …)
   Color updated to #8faad0 to match filter label brightness
───────────────────────────────────────────────────────────── */
p.sb-section-label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    color: #8faad0 !important;          /* ↑ was #4a5878 — now matches filter labels */
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 10px 4px 3px !important;
    margin: 0 !important;
    line-height: 1 !important;
}


/* ─────────────────────────────────────────────────────────────
   6. SIDEBAR — NAV BUTTONS
   Changes:
     • margin-bottom reduced from 2px → 1px  (tighter gap)
     • padding changed to 0 10px             (breathing room from sidebar edges)
     • text-align and justify-content set to left-align button content
───────────────────────────────────────────────────────────── */

/* Wrapper — controls left/right gap between button and sidebar edge */
div.sb-nav-item,
div.sb-nav-item--active {
    padding: 0 10px;
    margin-bottom: 1px;
}

/* Collapse Streamlit's own stElementContainer margin inside nav items —
   THIS is the real source of the large gap between buttons */
div.sb-nav-item [data-testid="stElementContainer"],
div.sb-nav-item--active [data-testid="stElementContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    min-height: unset !important;
    gap: 0 !important;
}

/* Also collapse the vertical block wrappers Streamlit uses inside sidebar */
div.sb-nav-item [data-testid="stVerticalBlock"],
div.sb-nav-item--active [data-testid="stVerticalBlock"],
div.sb-nav-item [data-testid="stVerticalBlockBorderWrapper"],
div.sb-nav-item--active [data-testid="stVerticalBlockBorderWrapper"] {
    gap: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* ── Default button ── */
div.sb-nav-item [data-testid="stBaseButton-secondary"] {
    width: 100% !important;
    height: 30px !important;
    min-height: unset !important;
    text-align: left !important;
    justify-content: flex-start !important;
    border-radius: 5px !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    transition: background 0.12s, border-color 0.12s;
}
div.sb-nav-item [data-testid="stBaseButton-secondary"]:hover {
    background: #111827 !important;
    border-color: #1e2a40 !important;
}

/* ── Active button ── */
div.sb-nav-item--active [data-testid="stBaseButton-secondary"] {
    width: 100% !important;
    height: 30px !important;
    min-height: unset !important;
    text-align: left !important;
    justify-content: flex-start !important;
    background: #0f1520 !important;
    border: 1px solid #1e2640 !important;
    border-left: 3px solid #ff8a4c !important;
    border-radius: 5px !important;
}

/* ── Kill Streamlit's internal span padding — this is what was blocking all changes ── */
div.sb-nav-item [data-testid="stBaseButton-secondary"] span,
div.sb-nav-item--active [data-testid="stBaseButton-secondary"] span {
    padding: 0 8px !important;     /* ← left/right padding inside button */
    line-height: 30px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;     /* ← left-align icon + text */
    width: 100% !important;
}

/* ── Button label text ── */
div.sb-nav-item [data-testid="stBaseButton-secondary"] p,
div.sb-nav-item--active [data-testid="stBaseButton-secondary"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 30px !important;
    text-align: left !important;    /* ← ensure text left-aligns inside the p tag */
    width: 100% !important;
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

/* ─────────────────────────────────────────────────────────────
   7. SIDEBAR — PIPELINE RUN FOOTER
───────────────────────────────────────────────────────────── */
.sb-run-footer {
    padding: 12px 4px 8px;
    border-top: 1px solid #1a2035;
    margin-top: 16px;
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


/* ─────────────────────────────────────────────────────────────
   8. PAGE HEADER & CATEGORY BADGE
───────────────────────────────────────────────────────────── */
.page-header {
    padding: 12px 0 10px;
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


/* ─────────────────────────────────────────────────────────────
   9. FILTER BAR
───────────────────────────────────────────────────────────── */
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
.filter-bar + div > div {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
.filter-bar + div[data-testid="stVerticalBlockBorderWrapper"],
.filter-bar + div[data-testid="element-container"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
    min-height: 0 !important;
}


/* ─────────────────────────────────────────────────────────────
   10. KPI GRID & CARDS
───────────────────────────────────────────────────────────── */
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
.kpi-delta.neu  { color: #8a9bbf; }
.kpi-note {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #7a8faf;
    margin-top: 2px;
}


/* ─────────────────────────────────────────────────────────────
   11. SECTION HEADINGS
───────────────────────────────────────────────────────────── */
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


/* ─────────────────────────────────────────────────────────────
   12. ALERTS & CONTEXT BOXES
───────────────────────────────────────────────────────────── */
.alert {
    padding: 12px 16px;
    border-radius: 3px;
    border-left: 3px solid;
    font-size: 14px;
    margin-bottom: 10px;
    line-height: 1.6;
    font-family: 'DM Sans', sans-serif;
}
.alert-red    { background: #140a0a; border-color: #ef4444; color: #fca5a5; }
.alert-amber  { background: #13100a; border-color: #f59e0b; color: #fcd34d; }
.alert-blue   { background: #080e1a; border-color: #3b82f6; color: #93c5fd; }
.alert-green  { background: #08120a; border-color: #22c55e; color: #86efac; }
.alert-purple { background: #0f0a1a; border-color: #a78bfa; color: #c4b5fd; }

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


/* ─────────────────────────────────────────────────────────────
   13. RIPPLE CHAIN
───────────────────────────────────────────────────────────── */
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


/* ─────────────────────────────────────────────────────────────
   14. STAT PILLS
───────────────────────────────────────────────────────────── */
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


/* ─────────────────────────────────────────────────────────────
   15. CATEGORY CARDS  (overview grid)
───────────────────────────────────────────────────────────── */
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


/* ─────────────────────────────────────────────────────────────
   16. FORM INPUTS & LABELS
───────────────────────────────────────────────────────────── */
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


/* ─────────────────────────────────────────────────────────────
   17. DATA TABLE
───────────────────────────────────────────────────────────── */
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


/* ─────────────────────────────────────────────────────────────
   18. SCROLLBAR
───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080a0f; }
::-webkit-scrollbar-thumb { background: #1a2035; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #2a3350; }
</style>
"""