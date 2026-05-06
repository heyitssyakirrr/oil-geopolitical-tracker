import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="War & Oil Tracker",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL CSS — mini-rail sidebar + polished dark theme
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #080a0f; color: #e2e8f0; }
.block-container { padding: 0 !important; max-width: 100% !important; }
header[data-testid="stHeader"] { display: none !important; }
.stDeployButton { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1e2738 !important;
    min-width: 56px !important;
}
[data-testid="stSidebarContent"] {
    padding: 0 !important;
    overflow: hidden !important;
}
[data-testid="stSidebarNav"] { display: none !important; }

/* When sidebar is collapsed Streamlit hides it fully — we keep a mini rail */
[data-testid="collapsedControl"] {
    background: #0d1117 !important;
    border-right: 1px solid #1e2738 !important;
}

/* ── SIDEBAR BRAND ── */
.sb-brand-wrap {
    padding: 20px 14px 12px;
    border-bottom: 1px solid #1e2738;
    display: flex; align-items: center; gap: 10px;
}
.sb-logo {
    width: 32px; height: 32px; min-width: 32px;
    background: linear-gradient(135deg, #e25c2e, #f59e0b);
    border-radius: 6px; display: flex; align-items: center;
    justify-content: center; font-size: 16px; flex-shrink: 0;
}
.sb-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.15rem; letter-spacing: 0.14em;
    color: #f1f5f9; white-space: nowrap; overflow: hidden;
    line-height: 1.1;
}
.sb-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px; color: #3d4f6b; letter-spacing: 0.18em;
    text-transform: uppercase; white-space: nowrap;
}

/* ── SIDEBAR STATUS ── */
.sb-status {
    padding: 10px 14px 12px;
    border-bottom: 1px solid #1e2738;
}
.sb-status-dot {
    display: flex; align-items: center; gap: 7px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: #64748b;
}
.dot-live  { width: 6px; height: 6px; border-radius: 50%; background: #22c55e; flex-shrink:0; box-shadow: 0 0 6px #22c55e88; }
.dot-fail  { width: 6px; height: 6px; border-radius: 50%; background: #ef4444; flex-shrink:0; }

/* ── SIDEBAR SECTION LABEL ── */
.sb-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px; letter-spacing: 0.22em; text-transform: uppercase;
    color: #2e3f58; padding: 14px 14px 5px;
}

/* ── NAV BUTTONS ── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: transparent !important;
    border: none !important;
    border-left: 2px solid transparent !important;
    border-radius: 0 !important;
    color: #64748b !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11.5px !important;
    letter-spacing: 0.04em !important;
    text-align: left !important;
    padding: 10px 14px !important;
    transition: all 0.12s ease !important;
    line-height: 1.3 !important;
}
div[data-testid="stButton"] > button:hover {
    background: #13192a !important;
    color: #e2e8f0 !important;
    border-left-color: #e25c2e !important;
}

/* ── SIDEBAR UNIT GUIDE ── */
.sb-units {
    padding: 0 14px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px; color: #3d4f6b; line-height: 2.1;
}
.sb-sev-row {
    display: flex; align-items: center; gap: 7px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px; padding: 2px 14px;
}

/* ── MAIN CONTENT ── */
.main-wrap { padding: 0 28px 40px 28px; max-width: 1400px; margin: 0 auto; }

/* ── PAGE HEADER ── */
.page-hdr {
    padding: 28px 0 20px;
    border-bottom: 1px solid #1e2738;
    margin-bottom: 24px;
}
.page-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem; letter-spacing: 0.1em;
    color: #f1f5f9; line-height: 1; margin: 0;
}
.page-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: #e25c2e;
    letter-spacing: 0.18em; text-transform: uppercase;
    margin-top: 7px;
}

/* ── ALERT BANNERS ── */
.alert-banner {
    padding: 13px 18px; border-radius: 4px; border-left: 3px solid;
    font-size: 13px; margin-bottom: 10px; line-height: 1.55;
    font-family: 'Inter', sans-serif;
}
.alert-red    { background: #1a0a0a; border-color: #ef4444; color: #fca5a5; }
.alert-amber  { background: #1a1204; border-color: #f59e0b; color: #fcd34d; }
.alert-blue   { background: #070e1e; border-color: #3b82f6; color: #93c5fd; }
.alert-green  { background: #050f08; border-color: #22c55e; color: #86efac; }

/* ── KPI GRID ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 28px;
}
.kpi-card {
    background: #0d1117;
    border: 1px solid #1e2738;
    border-top: 3px solid #e25c2e;
    border-radius: 6px;
    padding: 18px 20px 16px;
    display: flex; flex-direction: column; gap: 8px;
}
.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px; color: #475569;
    letter-spacing: 0.2em; text-transform: uppercase;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.1rem; color: #f1f5f9;
    letter-spacing: 0.04em; line-height: 1;
}
.kpi-delta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px; font-weight: 500;
}
.kpi-note {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px; color: #2e3f58;
}
.delta-up   { color: #ef4444; }
.delta-down { color: #22c55e; }
.delta-neu  { color: #64748b; }

/* ── SECTION HEADS ── */
.sec-head {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem; letter-spacing: 0.1em;
    color: #e2e8f0;
    border-bottom: 1px solid #1e2738;
    padding-bottom: 6px;
    margin: 28px 0 5px;
}
.sec-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px; color: #475569;
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 14px;
}

/* ── CONTEXT BOX ── */
.ctx-box {
    background: #0d1117; border: 1px solid #1e2738;
    border-left: 3px solid #e25c2e; padding: 13px 18px;
    border-radius: 4px; font-size: 12.5px; color: #94a3b8;
    line-height: 1.7; margin-bottom: 10px;
}
.ctx-box strong { color: #e2e8f0; }

/* ── ALERT ROW (3-col) ── */
.alert-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-bottom: 20px; }

/* ── DATAFRAME ── */
.stDataFrame { background: #0d1117 !important; }
.stDataFrame thead tr th {
    background: #080a0f !important; color: #64748b !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9.5px !important; letter-spacing: 0.1em;
    text-transform: uppercase; border-bottom: 1px solid #1e2738 !important;
}
.stDataFrame tbody tr td {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important; color: #94a3b8 !important;
    background: #0d1117 !important;
    border-bottom: 1px solid #111827 !important;
}

/* ── INPUTS ── */
.stSelectbox > div > div, .stDateInput > div > div input {
    background: #111827 !important; border: 1px solid #1e2738 !important;
    color: #e2e8f0 !important; font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important; border-radius: 4px !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #64748b !important; font-size: 9.5px !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.12em; text-transform: uppercase;
}
.stCheckbox label span { color: #94a3b8 !important; font-size: 12px !important; }

/* ── FILTER BAR ── */
.filter-bar {
    background: #0d1117; border: 1px solid #1e2738;
    border-radius: 6px; padding: 12px 16px;
    margin-bottom: 20px; display: flex; gap: 16px; align-items: center;
}

/* ── DIVIDER ── */
hr { border-color: #1e2738 !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
PAGES = [
    ("🏠", "Overview"),
    ("📈", "Price Analysis"),
    ("💥", "Event Intelligence"),
    ("📊", "Commodity Comparison"),
    ("🔧", "Pipeline"),
]
if "page" not in st.session_state:
    st.session_state.page = "Overview"

# ============================================================
# DB HELPERS
# ============================================================
@st.cache_resource
def get_engine():
    db_url = (
        f"postgresql+psycopg2://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 5432)}"
        f"/{os.getenv('DB_NAME')}"
    )
    return create_engine(db_url)

@st.cache_data(ttl=3600)
def load_prices():
    df = pd.read_sql("SELECT * FROM commodity_prices ORDER BY date ASC", get_engine())
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data(ttl=3600)
def load_events():
    df = pd.read_sql("SELECT * FROM geopolitical_events ORDER BY date ASC", get_engine())
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data(ttl=3600)
def load_runs():
    return pd.read_sql(
        "SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT 20",
        get_engine()
    )

prices = load_prices()
events = load_events()
runs   = load_runs()

# ============================================================
# CONSTANTS
# ============================================================
COMMODITY_META = {
    "brent_crude": {
        "label": "Brent Crude", "unit": "USD / barrel (159 L)", "unit_short": "bbl",
        "icon": "🛢️", "color": "#e25c2e",
        "why": "Global oil benchmark, priced per barrel (159 litres). Sets baseline for petrol prices worldwide.",
        "war_signal": "Supply shock indicator — rises when Middle East or Russian supply is threatened.",
    },
    "wti_crude": {
        "label": "WTI Crude", "unit": "USD / barrel (159 L)", "unit_short": "bbl",
        "icon": "⛽", "color": "#f59e0b",
        "why": "US domestic benchmark. Usually $2–5 below Brent. Gap widening = US shielded from global shock.",
        "war_signal": "US energy independence gauge — smaller spike vs. Brent means US is shielded.",
    },
    "natural_gas": {
        "label": "Natural Gas", "unit": "USD / MMBtu", "unit_short": "MMBtu",
        "icon": "🔥", "color": "#3b82f6",
        "why": "Russia weaponised gas supply in 2021–22. Priced per million BTU.",
        "war_signal": "Energy weaponisation indicator — Russia used gas as political leverage.",
    },
    "gold": {
        "label": "Gold", "unit": "USD / troy oz (31g)", "unit_short": "oz",
        "icon": "🥇", "color": "#eab308",
        "why": "Safe-haven asset. Rising gold = rising fear.",
        "war_signal": "Fear & flight-to-safety indicator — gold and oil rising together = prolonged conflict priced in.",
    },
    "wheat": {
        "label": "Wheat", "unit": "USD / bushel (27 kg)", "unit_short": "bu",
        "icon": "🌾", "color": "#84cc16",
        "why": "Russia + Ukraine = ~30% of global wheat exports.",
        "war_signal": "Food security crisis indicator — wheat spikes signal disrupted agricultural supply chains.",
    },
}

SEV_COLORS      = {"critical": "#ef4444", "high": "#f59e0b", "medium": "#3b82f6", "low": "#22c55e"}
PLOT_BG         = "rgba(0,0,0,0)"
GRID_CLR        = "rgba(255,255,255,0.05)"
FONT_CLR        = "#94a3b8"
AXIS_CLR        = "#475569"

all_commodities = sorted(prices["commodity_name"].unique())
label_map       = {k: v["label"] for k, v in COMMODITY_META.items()}
color_map       = {k: v["color"] for k, v in COMMODITY_META.items()}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sb-brand-wrap">
        <div class="sb-logo">🛢️</div>
        <div>
            <div class="sb-title">WAR &amp; OIL</div>
            <div class="sb-sub">Geopolitical Tracker</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Live status
    if not runs.empty:
        last = runs.iloc[0]
        ok   = last["status"] == "success"
        dot  = '<span class="dot-live"></span>' if ok else '<span class="dot-fail"></span>'
        label = "Live · " + pd.to_datetime(last["started_at"]).strftime("%d %b %H:%M")
        rows  = f'{last["rows_loaded"]:,} rows'
        st.markdown(f"""
        <div class="sb-status">
            <div class="sb-status-dot">{dot} {label}</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#2e3f58;padding-left:13px">{rows}</div>
        </div>
        """, unsafe_allow_html=True)

    # Nav
    st.markdown('<div class="sb-section-label">▸ Navigate</div>', unsafe_allow_html=True)
    for icon, name in PAGES:
        is_active = st.session_state.page == name
        if is_active:
            st.markdown(
                f'<div style="border-left:2px solid #e25c2e;background:#13192a;'
                f'font-family:JetBrains Mono,monospace;font-size:11.5px;color:#e25c2e;'
                f'padding:10px 14px;letter-spacing:0.04em">{icon}&nbsp;&nbsp;{name}</div>',
                unsafe_allow_html=True
            )
        else:
            if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
                st.session_state.page = name
                st.rerun()

    # Divider
    st.markdown('<hr style="margin:16px 0 4px;border-color:#1e2738">', unsafe_allow_html=True)

    # Unit guide
    st.markdown('<div class="sb-section-label">▸ Units</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sb-units">
        🛢️&nbsp; Oil → per barrel (159 L)<br>
        🥇&nbsp; Gold → per troy oz (31g)<br>
        🌾&nbsp; Wheat → per bushel (27kg)<br>
        🔥&nbsp; Gas → per MMBtu
    </div>
    """, unsafe_allow_html=True)

    # Severity
    st.markdown('<div class="sb-section-label">▸ Severity</div>', unsafe_allow_html=True)
    for sev, col in SEV_COLORS.items():
        st.markdown(
            f'<div class="sb-sev-row">'
            f'<span style="width:8px;height:8px;border-radius:2px;background:{col};display:inline-block;flex-shrink:0"></span>'
            f'<span style="font-family:JetBrains Mono,monospace;font-size:9.5px;color:{col}">{sev.upper()}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

# ============================================================
# CHART LAYOUT HELPER
# ============================================================
def base_layout(**kw):
    d = dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PLOT_BG,
        font=dict(family="Inter", color=FONT_CLR, size=11),
        xaxis=dict(
            showgrid=True, gridcolor=GRID_CLR, gridwidth=1,
            color=AXIS_CLR, zeroline=False,
            tickfont=dict(family="JetBrains Mono", size=10, color=AXIS_CLR),
            linecolor="#1e2738",
        ),
        yaxis=dict(
            showgrid=True, gridcolor=GRID_CLR, gridwidth=1,
            color=AXIS_CLR, zeroline=False,
            tickfont=dict(family="JetBrains Mono", size=10, color=AXIS_CLR),
            linecolor="#1e2738",
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#0d1117", bordercolor="#1e2738",
            font=dict(family="JetBrains Mono", size=11, color="#e2e8f0")
        ),
        margin=dict(l=55, r=20, t=35, b=45),
    )
    d.update(kw)
    return d

# ============================================================
# FILTER ROW HELPER
# ============================================================
def filter_row(page_key, show_commodity=True, show_events_toggle=True, show_ma_toggle=False):
    min_d = prices["date"].min().date()
    max_d = prices["date"].max().date()

    cols_spec = []
    if show_commodity:       cols_spec.append(2)
    cols_spec.append(3)
    if show_events_toggle:   cols_spec.append(1)
    if show_ma_toggle:       cols_spec.append(1)
    cols_spec.append(4)

    cols = st.columns(cols_spec)
    ci   = 0

    sel_com = "brent_crude"
    if show_commodity:
        with cols[ci]:
            default_idx = all_commodities.index("brent_crude") if "brent_crude" in all_commodities else 0
            sel_com = st.selectbox(
                "Commodity", all_commodities, index=default_idx,
                format_func=lambda c: f"{COMMODITY_META.get(c, {}).get('icon', '🔹')} {COMMODITY_META.get(c, {}).get('label', c)}",
                key=f"{page_key}_com", label_visibility="collapsed"
            )
        ci += 1

    with cols[ci]:
        dr = st.date_input(
            "Range", value=[min_d, max_d], min_value=min_d, max_value=max_d,
            key=f"{page_key}_dr", label_visibility="collapsed"
        )
        start_dt = pd.to_datetime(dr[0])
        end_dt   = pd.to_datetime(dr[1]) if len(dr) == 2 else pd.to_datetime(max_d)
    ci += 1

    show_ev = True
    show_ma = True
    if show_events_toggle:
        with cols[ci]:
            show_ev = st.checkbox("Events", value=True, key=f"{page_key}_ev")
        ci += 1
    if show_ma_toggle:
        with cols[ci]:
            show_ma = st.checkbox("Moving Avg", value=True, key=f"{page_key}_ma")

    return sel_com, start_dt, end_dt, show_ev, show_ma

# ============================================================
# KPI CARD BUILDER
# ============================================================
def kpi_card(label, value, delta="", note="", delta_cls="delta-neu", accent="#e25c2e"):
    return (
        f'<div class="kpi-card" style="border-top-color:{accent}">'
        f'  <div class="kpi-label">{label}</div>'
        f'  <div class="kpi-value">{value}</div>'
        f'  <div class="kpi-delta {delta_cls}">{delta}</div>'
        f'  <div class="kpi-note">{note}</div>'
        f'</div>'
    )

# ============================================================
# PAGE: OVERVIEW
# ============================================================
def page_overview():
    sel_com, start_dt, end_dt, show_ev, show_ma = filter_row("ov", show_ma_toggle=True)

    meta     = COMMODITY_META.get(sel_com, {})
    accent   = meta.get("color", "#e25c2e")
    filtered = prices[
        (prices["commodity_name"] == sel_com) &
        (prices["date"] >= start_dt) &
        (prices["date"] <= end_dt)
    ].copy()

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    # Page header
    st.markdown(
        f'<div class="page-hdr">'
        f'<div class="page-title">{meta.get("icon", "🛢️")} Overview — {meta.get("label", "")}</div>'
        f'<div class="page-sub">▸ {meta.get("unit", "")} · Geopolitical commodity tracker · Updated daily</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # War signal banner
    st.markdown(
        f'<div class="alert-banner alert-red">'
        f'<strong>⚡ WAR SIGNAL:</strong> {meta.get("war_signal", "")}'
        f'</div>',
        unsafe_allow_html=True
    )

    if not filtered.empty:
        latest   = filtered.iloc[-1]
        prev     = filtered.iloc[-2] if len(filtered) > 1 else latest
        delta_p  = latest["close"] - prev["close"]
        pct_d    = delta_p / prev["close"] * 100 if prev["close"] else 0
        is_oil   = sel_com in ("brent_crude", "wti_crude")
        per_l    = latest["close"] / 159 if is_oil else None
        d_cls    = "delta-up" if delta_p > 0 else ("delta-down" if delta_p < 0 else "delta-neu")
        d_sym    = "▲" if delta_p > 0 else ("▼" if delta_p < 0 else "─")

        # 3 alert cards
        avg_vol   = filtered["volatility_30d"].mean()
        latest_vol = filtered["volatility_30d"].iloc[-1]
        vol_pct   = (latest_vol - avg_vol) / avg_vol * 100 if avg_vol else 0
        rec_ev    = events[(events["date"] >= end_dt - pd.Timedelta(days=60)) & (events["date"] <= end_dt)]
        n_crit    = (rec_ev["severity"] == "critical").sum()
        n_high    = (rec_ev["severity"] == "high").sum()
        pch       = (filtered["close"].iloc[-1] - filtered["close"].iloc[0]) / filtered["close"].iloc[0] * 100 if len(filtered) > 1 else 0

        c1, c2, c3 = st.columns(3)
        with c1:
            cls  = "alert-red" if vol_pct > 30 else ("alert-amber" if vol_pct > 10 else "alert-green")
            icon = "🚨" if vol_pct > 30 else ("⚠️" if vol_pct > 10 else "✅")
            st.markdown(
                f'<div class="alert-banner {cls}">'
                f'<strong>{icon} Volatility {vol_pct:+.0f}% vs avg</strong><br>'
                f'Current 30-day vol: <strong>{latest_vol:.2f}</strong>'
                f'</div>',
                unsafe_allow_html=True
            )
        with c2:
            cls  = "alert-red" if n_crit > 0 else ("alert-amber" if n_high > 0 else "alert-blue")
            icon = "🔴" if n_crit > 0 else "🟠"
            st.markdown(
                f'<div class="alert-banner {cls}">'
                f'<strong>{icon} {n_crit} critical · {n_high} high events</strong><br>'
                f'In the last 60 days of selected window'
                f'</div>',
                unsafe_allow_html=True
            )
        with c3:
            cls  = "alert-red" if pch > 10 else ("alert-green" if pch < -5 else "alert-blue")
            icon = "📈" if pch > 0 else "📉"
            st.markdown(
                f'<div class="alert-banner {cls}">'
                f'<strong>{icon} Period return: {pch:+.1f}%</strong><br>'
                f'{meta.get("label", "")} moved {pch:+.1f}% over this window'
                f'</div>',
                unsafe_allow_html=True
            )

        # KPI grid
        vs = latest["price_vs_30d_avg_pct"]
        vs_cls = "delta-up" if vs > 0 else "delta-down"
        note_oil = f"≈ ${per_l:.3f}/litre" if per_l else meta.get("unit", "")

        st.markdown(
            '<div class="kpi-grid">'
            + kpi_card(
                f"Spot Price ({meta.get('unit_short', '')})",
                f"${latest['close']:.2f}",
                f"{d_sym} ${abs(delta_p):.2f} ({pct_d:+.1f}%) today",
                note_oil, d_cls, accent
            )
            + kpi_card("7-Day Average", f"${latest['rolling_7d_avg']:.2f}", "", "Short-term trend", accent=accent)
            + kpi_card("30-Day Average", f"${latest['rolling_30d_avg']:.2f}", "", "Medium-term baseline", accent=accent)
            + kpi_card(
                "vs 30-Day Avg", f"{vs:+.1f}%",
                "Above avg → demand pressure" if vs > 0 else "Below avg → supply surplus",
                "", vs_cls, accent
            )
            + kpi_card("30-Day Volatility", f"{latest['volatility_30d']:.2f}", "", "Higher = more uncertainty", accent=accent)
            + '</div>',
            unsafe_allow_html=True
        )

    # Price chart
    st.markdown('<div class="sec-head">Price History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">Vertical lines = conflict/geopolitical events · '
        'Red = critical · Amber = high · Blue = medium · Green = low</div>',
        unsafe_allow_html=True
    )

    if not filtered.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered["date"],
            y=filtered["close"],
            name=f"{meta.get('label', '')}",
            fill="tozeroy",
            fillcolor=f"rgba({int(accent[1:3],16)},{int(accent[3:5],16)},{int(accent[5:7],16)},0.08)",
            line=dict(color=accent, width=2),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>$%{y:.2f} / " + meta.get("unit_short", "") + "<extra></extra>",
        ))
        if show_ma and "rolling_7d_avg" in filtered.columns:
            fig.add_trace(go.Scatter(
                x=filtered["date"], y=filtered["rolling_7d_avg"],
                name="7-day MA",
                line=dict(color="#64748b", width=1.3, dash="dash"),
                hovertemplate="7d MA: $%{y:.2f}<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=filtered["date"], y=filtered["rolling_30d_avg"],
                name="30-day MA",
                line=dict(color="#94a3b8", width=1.6, dash="dot"),
                hovertemplate="30d MA: $%{y:.2f}<extra></extra>"
            ))
        if show_ev:
            ev_in_range = events[(events["date"] >= start_dt) & (events["date"] <= end_dt)]
            for _, e in ev_in_range.iterrows():
                c  = SEV_COLORS.get(e["severity"], "#888")
                ts = int(pd.Timestamp(e["date"]).timestamp() * 1000)
                txt = e["event"][:30] + ("…" if len(e["event"]) > 30 else "")
                fig.add_vline(
                    x=ts,
                    line_dash="dot", line_color=c, line_width=1.2,
                    annotation_text=txt,
                    annotation_position="top left",
                    annotation_font_size=8, annotation_font_color=c
                )
        fig.update_layout(**base_layout(
            height=440,
            yaxis_title=f"Price ({meta.get('unit_short', 'USD')})",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                font=dict(family="JetBrains Mono", size=10, color=FONT_CLR),
                bgcolor="rgba(0,0,0,0)"
            )
        ))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: PRICE ANALYSIS
# ============================================================
def page_price_analysis():
    sel_com, start_dt, end_dt, _, show_ma = filter_row("pa", show_events_toggle=False, show_ma_toggle=True)

    meta     = COMMODITY_META.get(sel_com, {})
    accent   = meta.get("color", "#e25c2e")
    filtered = prices[
        (prices["commodity_name"] == sel_com) &
        (prices["date"] >= start_dt) &
        (prices["date"] <= end_dt)
    ].copy()

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-hdr">'
        f'<div class="page-title">📈 Price Analysis</div>'
        f'<div class="page-sub">▸ Deep dive — {meta.get("label", "")} · OHLC · Returns · Volatility</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    if filtered.empty:
        st.info("No data for selected range.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Candlestick
    st.markdown('<div class="sec-head">OHLC Candlestick</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Green = price rose · Red = price fell</div>', unsafe_allow_html=True)

    fig_c = go.Figure()
    fig_c.add_trace(go.Candlestick(
        x=filtered["date"],
        open=filtered["open"], high=filtered["high"],
        low=filtered["low"],   close=filtered["close"],
        increasing_line_color="#22c55e", decreasing_line_color="#ef4444",
        increasing_fillcolor="rgba(34,197,94,0.25)",
        decreasing_fillcolor="rgba(239,68,68,0.25)",
        name="OHLC",
    ))
    if show_ma:
        fig_c.add_trace(go.Scatter(
            x=filtered["date"], y=filtered["rolling_7d_avg"],
            name="7d MA", line=dict(color="#f59e0b", width=1.4, dash="dash"),
            hovertemplate="7d MA: $%{y:.2f}<extra></extra>"
        ))
        fig_c.add_trace(go.Scatter(
            x=filtered["date"], y=filtered["rolling_30d_avg"],
            name="30d MA", line=dict(color="#94a3b8", width=1.6, dash="dot"),
            hovertemplate="30d MA: $%{y:.2f}<extra></extra>"
        ))
    fig_c.update_layout(**base_layout(height=430, yaxis_title=f"Price ({meta.get('unit_short', '')})"))
    fig_c.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig_c, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-head">Daily Return Distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Histogram of daily % price changes · Fat tails = more extreme moves</div>', unsafe_allow_html=True)
        ret_data = filtered["daily_return_pct"].dropna()
        fig_d = go.Figure(go.Histogram(
            x=ret_data, nbinsx=60,
            marker_color=accent, opacity=0.82,
            hovertemplate="Return: %{x:.2f}%<br>Days: %{y}<extra></extra>"
        ))
        fig_d.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.15)")
        fig_d.update_layout(**base_layout(
            height=290, xaxis_title="Daily return (%)", yaxis_title="# Trading days"
        ))
        st.plotly_chart(fig_d, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-head">Volatility Timeline</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">30-day rolling volatility · Spikes = event-driven panic</div>', unsafe_allow_html=True)
        fig_v = go.Figure(go.Scatter(
            x=filtered["date"], y=filtered["volatility_30d"],
            fill="tozeroy", fillcolor="rgba(239,68,68,0.08)",
            line=dict(color="#ef4444", width=1.8),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Vol: %{y:.2f}<extra></extra>"
        ))
        fig_v.update_layout(**base_layout(height=290, yaxis_title="Volatility (30d)"))
        st.plotly_chart(fig_v, use_container_width=True)

    # Monthly bar
    st.markdown('<div class="sec-head">Monthly Average Daily Range</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">How wide was High–Low each month? Wider = more intraday uncertainty</div>', unsafe_allow_html=True)
    monthly = filtered.copy()
    monthly["ym"] = monthly["date"].dt.to_period("M").astype(str)
    mr = monthly.groupby("ym")["daily_range"].mean().reset_index()
    if not mr.empty:
        fig_mr = go.Figure(go.Bar(
            x=mr["ym"], y=mr["daily_range"],
            marker=dict(
                color=mr["daily_range"],
                colorscale=[[0, "#1e2738"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            ),
            text=[f"${v:.2f}" for v in mr["daily_range"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=9, color=FONT_CLR),
            hovertemplate="<b>%{x}</b><br>Avg daily range: $%{y:.2f}<extra></extra>"
        ))
        fig_mr.update_layout(**base_layout(height=270, yaxis_title=f"Avg daily range ({meta.get('unit_short', '')})"))
        st.plotly_chart(fig_mr, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: EVENT INTELLIGENCE
# ============================================================
def page_event_intelligence():
    sel_com, start_dt, end_dt, _, _ = filter_row("ei", show_events_toggle=False)

    meta     = COMMODITY_META.get(sel_com, {})
    filtered = prices[
        (prices["commodity_name"] == sel_com) &
        (prices["date"] >= start_dt) &
        (prices["date"] <= end_dt)
    ].copy()

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-hdr">'
        '<div class="page-title">💥 Event Intelligence</div>'
        '<div class="page-sub">▸ How each conflict event moved the market · 30-day post-event impact</div>'
        '</div>',
        unsafe_allow_html=True
    )

    impact_rows = []
    SEV_ICON = {"critical": "🔴", "high": "🟠", "medium": "🔵", "low": "🟢"}
    for _, ev in events.iterrows():
        if not (start_dt <= ev["date"] <= end_dt):
            continue
        d30 = ev["date"] + pd.Timedelta(days=30)
        p0  = filtered[filtered["date"] == ev["date"]]["close"]
        p30 = filtered[filtered["date"] <= d30]["close"]
        if not p0.empty and not p30.empty:
            pb  = p0.iloc[0]; pa = p30.iloc[-1]
            pct = (pa - pb) / pb * 100
            impact_rows.append({
                "Date":     ev["date"].strftime("%d %b %Y"),
                "Event":    ev["event"],
                "Severity": f"{SEV_ICON.get(ev['severity'], '')} {ev['severity'].title()}",
                "At Event": f"${pb:.2f}",
                "+30 Days": f"${pa:.2f}",
                "Impact":   f"{pct:+.1f}%",
                "_pct": pct, "_sev": ev["severity"], "_date": ev["date"],
            })

    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown('<div class="sec-head">Impact Table</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Price 30 days after event vs price on event day · Red = spiked · Green = fell</div>', unsafe_allow_html=True)
        if impact_rows:
            idf = pd.DataFrame(impact_rows).drop(columns=["_pct", "_sev", "_date"])

            def color_impact(val):
                try:
                    v = float(str(val).replace("%", "").replace("+", ""))
                    if v > 5:   return "color:#ef4444;font-weight:600"
                    if v < -5:  return "color:#22c55e;font-weight:600"
                    return "color:#94a3b8"
                except:
                    return ""

            st.dataframe(
                idf.style.map(color_impact, subset=["Impact"]),
                use_container_width=True, hide_index=True, height=360
            )

            if impact_rows:
                best  = max(impact_rows, key=lambda r: r["_pct"])
                worst = min(impact_rows, key=lambda r: r["_pct"])
                st.markdown(
                    f'<div class="ctx-box">'
                    f'<strong>Biggest spike:</strong> {best["Event"]} ({best["Date"]}) → <strong style="color:#ef4444">{best["Impact"]}</strong> in 30 days<br>'
                    f'<strong>Biggest drop:</strong> {worst["Event"]} ({worst["Date"]}) → <strong style="color:#22c55e">{worst["Impact"]}</strong> in 30 days'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No events overlap with selected date range.")

    with col_r:
        st.markdown('<div class="sec-head">Avg Impact by Severity</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Critical events cause the most disruption on average</div>', unsafe_allow_html=True)
        if impact_rows:
            idf_full = pd.DataFrame(impact_rows)
            sev_avg  = idf_full.groupby("_sev")["_pct"].mean().reset_index()
            sev_avg  = sev_avg.sort_values("_pct", ascending=True)
            sev_avg["color"] = sev_avg["_sev"].map(SEV_COLORS)
            sev_avg["label"] = sev_avg["_sev"].str.title()
            fig_sev = go.Figure(go.Bar(
                x=sev_avg["_pct"], y=sev_avg["label"], orientation="h",
                marker_color=sev_avg["color"].tolist(),
                text=[f"{v:+.1f}%" for v in sev_avg["_pct"]],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=11, color=FONT_CLR),
                hovertemplate="<b>%{y}</b><br>Avg 30d impact: %{x:+.1f}%<extra></extra>"
            ))
            fig_sev.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.1)")
            fig_sev.update_layout(**base_layout(height=210, xaxis_title="Avg 30-day price change (%)"))
            st.plotly_chart(fig_sev, use_container_width=True)

        st.markdown('<div class="sec-head" style="margin-top:8px">Commodity War Signals</div>', unsafe_allow_html=True)
        for key, m in COMMODITY_META.items():
            if key in all_commodities:
                st.markdown(
                    f'<div class="ctx-box">'
                    f'<strong style="color:{m["color"]}">{m["icon"]} {m["label"]}</strong> '
                    f'<span style="color:#2e3f58;font-size:9.5px"> · {m["unit_short"]}</span><br>'
                    f'<span style="font-size:12px">{m["war_signal"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # Timeline scatter
    if impact_rows:
        st.markdown('<div class="sec-head">Event Timeline — Severity vs Price Impact</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Each dot = one event · Larger dot = higher severity · Above 0 = price rose after event</div>', unsafe_allow_html=True)
        idf_f = pd.DataFrame(impact_rows)
        idf_f["dot_color"] = idf_f["_pct"].apply(lambda v: "#ef4444" if v > 0 else "#22c55e")
        idf_f["size"]      = idf_f["_sev"].map({"critical": 20, "high": 14, "medium": 9, "low": 5}).fillna(8)
        fig_tl = go.Figure(go.Scatter(
            x=idf_f["_date"], y=idf_f["_pct"], mode="markers",
            marker=dict(
                size=idf_f["size"],
                color=idf_f["dot_color"],
                opacity=0.85,
                line=dict(width=1, color="rgba(255,255,255,0.1)")
            ),
            customdata=list(zip(idf_f["Event"], idf_f["_pct"], idf_f["_sev"])),
            hovertemplate=(
                "<b>%{x|%d %b %Y}</b><br>%{customdata[0]}<br>"
                "Severity: %{customdata[2]}<br>Impact: %{customdata[1]:+.1f}%<extra></extra>"
            )
        ))
        fig_tl.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.08)")
        fig_tl.update_layout(**base_layout(height=290, yaxis_title="30-day price impact (%)"))
        st.plotly_chart(fig_tl, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: COMMODITY COMPARISON
# ============================================================
def page_commodity_comparison():
    _, start_dt, end_dt, show_ev, _ = filter_row("cc", show_commodity=False)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-hdr">'
        '<div class="page-title">📊 Commodity Comparison</div>'
        '<div class="page-sub">▸ All 5 commodities normalized · War co-movement analysis · Correlation matrix</div>'
        '</div>',
        unsafe_allow_html=True
    )

    comp_df = prices[(prices["date"] >= start_dt) & (prices["date"] <= end_dt)].copy()

    def normalize(g):
        fv = g["close"].iloc[0]
        if fv == 0:
            return g
        g = g.copy()
        g["norm"] = g["close"] / fv * 100
        return g

    comp_df = comp_df.groupby("commodity_name", group_keys=False).apply(normalize)
    comp_df["label"] = comp_df["commodity_name"].map(label_map).fillna(comp_df["commodity_name"])

    st.markdown('<div class="sec-head">Normalized Price Index (Base = 100)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sec-sub">Oil + Gold + Wheat all above 130 simultaneously = systemic war/supply shock · '
        'Red shaded zone = major disruption territory</div>',
        unsafe_allow_html=True
    )

    fig2 = go.Figure()
    for com in comp_df["commodity_name"].unique():
        sub = comp_df[comp_df["commodity_name"] == com]
        m   = COMMODITY_META.get(com, {})
        fig2.add_trace(go.Scatter(
            x=sub["date"], y=sub["norm"],
            name=m.get("label", com),
            line=dict(color=m.get("color", "#888"), width=2),
            customdata=list(zip(sub["close"], sub["norm"])),
            hovertemplate=(
                f"<b>%{{x|%d %b %Y}}</b><br>{m.get('label', com)}: "
                f"<b>${{customdata[0]:.2f}}</b> ({m.get('unit_short', '')})<br>"
                f"Index: %{{customdata[1]:.1f}}<extra></extra>"
            )
        ))

    fig2.add_hline(
        y=100, line_dash="dash",
        line_color="rgba(255,255,255,0.08)",
        annotation_text="Baseline",
        annotation_font_size=9, annotation_font_color="#475569"
    )
    if not comp_df.empty and "norm" in comp_df.columns:
        max_n = comp_df["norm"].max()
        if max_n > 130:
            fig2.add_hrect(
                y0=130, y1=max_n * 1.02,
                fillcolor="rgba(239,68,68,0.04)", line_width=0,
                annotation_text="SYSTEMIC SHOCK ZONE",
                annotation_font_size=8, annotation_font_color="#ef4444",
                annotation_position="top left"
            )

    if show_ev:
        ev_in_range = events[(events["date"] >= start_dt) & (events["date"] <= end_dt)]
        for _, e in ev_in_range.iterrows():
            c  = SEV_COLORS.get(e["severity"], "#888")
            ts = int(pd.Timestamp(e["date"]).timestamp() * 1000)
            txt = e["event"][:22] + ("…" if len(e["event"]) > 22 else "")
            fig2.add_vline(
                x=ts, line_dash="dot", line_color=c, line_width=1,
                annotation_text=txt, annotation_position="top left",
                annotation_font_size=7, annotation_font_color=c
            )

    fig2.update_layout(**base_layout(
        height=440,
        yaxis_title="Normalized index (100 = start)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            font=dict(family="JetBrains Mono", size=10, color=FONT_CLR),
            bgcolor="rgba(0,0,0,0)"
        )
    ))
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        '<div class="ctx-box">'
        '<strong>Reading guide:</strong> Oil + Gold + Wheat rising together → war-driven supply shock. '
        'Gold rising alone → financial fear (no physical disruption). '
        'Oil + Wheat without Gold → localized production disruption. '
        'All falling → demand collapse / recession signal.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown('<div class="sec-head">Volatility Ranking</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Highest vol = most affected by current events</div>', unsafe_allow_html=True)
        ld = prices["date"].max()
        lv = prices[prices["date"] == ld][["commodity_name", "volatility_30d"]].copy()
        lv = lv.sort_values("volatility_30d", ascending=True)
        lv["label"] = lv["commodity_name"].map(label_map).fillna(lv["commodity_name"])
        lv["color"] = lv["commodity_name"].map(color_map).fillna("#94a3b8")
        if not lv.empty:
            fig3 = go.Figure(go.Bar(
                x=lv["volatility_30d"], y=lv["label"], orientation="h",
                marker_color=lv["color"].tolist(),
                text=[f"{v:.2f}" for v in lv["volatility_30d"]],
                textposition="outside",
                textfont=dict(family="JetBrains Mono", size=11, color=FONT_CLR),
                hovertemplate="<b>%{y}</b><br>30d vol: %{x:.2f}<extra></extra>"
            ))
            fig3.update_layout(**base_layout(
                height=290, xaxis_title="30-day Volatility",
                margin=dict(l=10, r=70, t=10, b=40), showlegend=False
            ))
            st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-head">Return Correlation Matrix</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">1.0 = perfectly correlated · High correlation during war = co-movement</div>', unsafe_allow_html=True)
        if "norm" in comp_df.columns:
            pivot = comp_df.pivot_table(index="date", columns="label", values="close")
            corr  = pivot.pct_change().corr().round(2)
            fig_corr = go.Figure(go.Heatmap(
                z=corr.values,
                x=corr.columns.tolist(),
                y=corr.index.tolist(),
                colorscale=[[0, "#080a0f"], [0.4, "#1e2738"], [0.7, "#7c3aed"], [1, "#e25c2e"]],
                text=corr.values,
                texttemplate="%{text:.2f}",
                textfont=dict(family="JetBrains Mono", size=11, color="#e2e8f0"),
                hovertemplate="<b>%{x} vs %{y}</b><br>Correlation: %{z:.2f}<extra></extra>",
                zmin=-1, zmax=1,
            ))
            fig_corr.update_layout(**base_layout(height=290, margin=dict(l=10, r=10, t=10, b=40)))
            st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAGE: PIPELINE
# ============================================================
def page_pipeline():
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-hdr">'
        '<div class="page-title">🔧 Pipeline Log</div>'
        '<div class="page-sub">▸ Data ingestion history · Yahoo Finance ETL · Daily refresh</div>'
        '</div>',
        unsafe_allow_html=True
    )

    if not runs.empty:
        last = runs.iloc[0]
        ok   = last["status"] == "success"
        cls  = "alert-green" if ok else "alert-red"
        ts   = pd.to_datetime(last["started_at"]).strftime("%d %b %Y %H:%M")
        st.markdown(
            f'<div class="alert-banner {cls}">'
            f'<strong>{"✅ Last run succeeded" if ok else "❌ Last run failed"}</strong>'
            f' · {ts} · {last["rows_loaded"]:,} rows loaded'
            f'</div>',
            unsafe_allow_html=True
        )

        r = runs.copy()
        r["started_at"] = pd.to_datetime(r["started_at"])
        r = r.sort_values("started_at")
        r["status_color"] = r["status"].map({"success": "#22c55e", "failed": "#ef4444", "running": "#f59e0b"})

        st.markdown('<div class="sec-head">Rows Loaded Per Run</div>', unsafe_allow_html=True)
        fig_r = go.Figure(go.Bar(
            x=r["started_at"].dt.strftime("%d %b %H:%M"),
            y=r["rows_loaded"],
            marker_color=r["status_color"].tolist(),
            text=r["rows_loaded"],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=10, color=FONT_CLR),
            hovertemplate="<b>%{x}</b><br>Rows: %{y:,}<extra></extra>"
        ))
        fig_r.update_layout(**base_layout(height=250, yaxis_title="Rows loaded"))
        st.plotly_chart(fig_r, use_container_width=True)

    st.markdown('<div class="sec-head">Full Run History</div>', unsafe_allow_html=True)
    if not runs.empty:
        def color_status(val):
            if val == "success": return "color:#22c55e;font-weight:600"
            if val == "failed":  return "color:#ef4444;font-weight:600"
            return ""
        disp = runs[["started_at", "finished_at", "status", "rows_loaded", "error_message"]].copy()
        st.dataframe(
            disp.style.map(color_status, subset=["status"]),
            use_container_width=True, hide_index=True
        )
    else:
        st.info("No pipeline runs recorded yet.")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ROUTER
# ============================================================
pg = st.session_state.page
if   pg == "Overview":             page_overview()
elif pg == "Price Analysis":       page_price_analysis()
elif pg == "Event Intelligence":   page_event_intelligence()
elif pg == "Commodity Comparison": page_commodity_comparison()
elif pg == "Pipeline":             page_pipeline()