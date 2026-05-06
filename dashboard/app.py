import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Oil & Geopolitical Impact Tracker",
    page_icon="🛢️",
    layout="wide"
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .metric-card {
        background: #f8f9fa; border-radius: 10px; padding: 1rem 1.2rem;
        border: 1px solid #e9ecef;
    }
    .insight-box {
        border-radius: 8px; padding: .9rem 1rem; border: 1px solid #e9ecef;
        border-left: 4px solid; margin-bottom: .5rem;
    }
    .stDataFrame { font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DB connection
# ---------------------------------------------------------------------------
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
def load_prices() -> pd.DataFrame:
    df = pd.read_sql("SELECT * FROM commodity_prices ORDER BY date ASC", get_engine())
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data(ttl=3600)
def load_events() -> pd.DataFrame:
    df = pd.read_sql("SELECT * FROM geopolitical_events ORDER BY date ASC", get_engine())
    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data(ttl=3600)
def load_pipeline_runs() -> pd.DataFrame:
    return pd.read_sql(
        "SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT 10",
        get_engine()
    )

prices = load_prices()
events = load_events()
runs   = load_pipeline_runs()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛢️ Oil Tracker")
    st.markdown("---")

    all_commodities = sorted(prices["commodity_name"].unique())
    selected_commodity = st.selectbox(
        "Commodity",
        all_commodities,
        index=all_commodities.index("brent_crude") if "brent_crude" in all_commodities else 0
    )

    min_date = prices["date"].min().date()
    max_date = prices["date"].max().date()
    date_range = st.date_input(
        "Date range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("---")
    show_events = st.checkbox("Show event markers", value=True)
    show_ma     = st.checkbox("Show moving averages", value=True)

    st.markdown("---")
    st.caption("**Pipeline status**")
    if not runs.empty:
        last = runs.iloc[0]
        color = "🟢" if last["status"] == "success" else "🔴"
        st.caption(f"{color} {last['status']} · {last['started_at'].strftime('%Y-%m-%d %H:%M')}")
        st.caption(f"{last['rows_loaded']:,} rows loaded")

# ---------------------------------------------------------------------------
# Filter
# ---------------------------------------------------------------------------
start_dt = pd.to_datetime(date_range[0])
end_dt   = pd.to_datetime(date_range[1])

filtered = prices[
    (prices["commodity_name"] == selected_commodity) &
    (prices["date"] >= start_dt) &
    (prices["date"] <= end_dt)
].copy()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🛢️ Oil Price & Geopolitical Impact Tracker")
st.caption(
    "Tracks how Middle East conflict events affect global commodity prices. "
    "Data sourced from Yahoo Finance · Updated daily."
)

# ---------------------------------------------------------------------------
# Insight banners
# ---------------------------------------------------------------------------
if not filtered.empty:
    latest_vol = filtered["volatility_30d"].iloc[-1]
    avg_vol    = filtered["volatility_30d"].mean()
    vol_pct    = (latest_vol - avg_vol) / avg_vol * 100 if avg_vol else 0

    recent_events = events[
        (events["date"] >= end_dt - pd.Timedelta(days=60)) &
        (events["date"] <= end_dt)
    ]
    n_critical = (recent_events["severity"] == "critical").sum()

    c1, c2, c3 = st.columns(3)
    with c1:
        icon = "⚠️" if vol_pct > 15 else "✅"
        color = "#EF9F27" if vol_pct > 15 else "#639922"
        st.markdown(
            f'<div class="insight-box" style="border-left-color:{color}">'
            f'<strong>{icon} Volatility — {selected_commodity.replace("_"," ").title()}</strong><br>'
            f'<span style="font-size:13px;color:#666">30-day vol is {vol_pct:+.0f}% vs period average. '
            f'Current: {latest_vol:.2f}</span></div>',
            unsafe_allow_html=True
        )
    with c2:
        icon = "🚨" if n_critical > 0 else "📋"
        color = "#E24B4A" if n_critical > 0 else "#378ADD"
        st.markdown(
            f'<div class="insight-box" style="border-left-color:{color}">'
            f'<strong>{icon} Recent events (60d)</strong><br>'
            f'<span style="font-size:13px;color:#666">{len(recent_events)} events tracked, '
            f'{n_critical} critical severity in this window</span></div>',
            unsafe_allow_html=True
        )
    with c3:
        price_change_total = (
            (filtered["close"].iloc[-1] - filtered["close"].iloc[0])
            / filtered["close"].iloc[0] * 100
            if len(filtered) > 1 else 0
        )
        icon = "📈" if price_change_total > 0 else "📉"
        color = "#E24B4A" if price_change_total > 0 else "#639922"
        st.markdown(
            f'<div class="insight-box" style="border-left-color:{color}">'
            f'<strong>{icon} Period return</strong><br>'
            f'<span style="font-size:13px;color:#666">{selected_commodity.replace("_"," ").title()} '
            f'moved {price_change_total:+.1f}% over the selected window</span></div>',
            unsafe_allow_html=True
        )

st.markdown("---")

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
if not filtered.empty:
    latest      = filtered.iloc[-1]
    prev        = filtered.iloc[-2] if len(filtered) > 1 else latest
    price_delta = latest["close"] - prev["close"]

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Current price (USD)", f"${latest['close']:.2f}", f"{price_delta:+.2f} vs yesterday")
    k2.metric("7-day average",        f"${latest['rolling_7d_avg']:.2f}")
    k3.metric("30-day average",       f"${latest['rolling_30d_avg']:.2f}")
    k4.metric("vs 30-day avg",        f"{latest['price_vs_30d_avg_pct']:+.1f}%")
    k5.metric("30-day volatility",    f"{latest['volatility_30d']:.2f}")

st.markdown("---")

# ---------------------------------------------------------------------------
# Main price chart  — FIX: pass date as string to avoid Timestamp arithmetic
# ---------------------------------------------------------------------------
st.subheader(f"📈 {selected_commodity.replace('_', ' ').title()} — Price history")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=filtered["date"], y=filtered["close"],
    name="Close price", line=dict(color="#378ADD", width=2)
))

if show_ma:
    fig.add_trace(go.Scatter(
        x=filtered["date"], y=filtered["rolling_7d_avg"],
        name="7-day MA", line=dict(color="#EF9F27", width=1.5, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=filtered["date"], y=filtered["rolling_30d_avg"],
        name="30-day MA", line=dict(color="#639922", width=1.5, dash="dot")
    ))

# ✅ THE FIX: convert Timestamp to plain string before passing to add_vline
if show_events:
    SEV_COLORS = {
        "critical": "#E24B4A",
        "high":     "#EF9F27",
        "medium":   "#378ADD",
        "low":      "#639922",
    }
    for _, event in events.iterrows():
        if start_dt <= event["date"] <= end_dt:
            color     = SEV_COLORS.get(event["severity"], "#888")
            # Convert to string — prevents the Timestamp arithmetic crash in Plotly
            date_str  = str(event["date"].date())
            label_txt = event["event"][:30] + ("…" if len(event["event"]) > 30 else "")
            fig.add_vline(
                x                   = date_str,
                line_dash           = "dot",
                line_color          = color,
                line_width          = 1.5,
                annotation_text     = label_txt,
                annotation_position = "top left",
                annotation_font_size  = 9,
                annotation_font_color = color,
            )

fig.update_layout(
    height=480,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=40, r=40, t=60, b=40),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
    yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Event impact table + volatility ranking side by side
# ---------------------------------------------------------------------------
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("💥 Event impact analysis")
    st.caption("Price change in the 30 days following each event")

    impact_rows = []
    for _, event in events.iterrows():
        event_date   = event["date"]
        date_plus_30 = event_date + pd.Timedelta(days=30)

        price_on_event = filtered[filtered["date"] == event_date]["close"]
        price_after_30 = filtered[filtered["date"] <= date_plus_30]["close"]

        if not price_on_event.empty and not price_after_30.empty:
            p_before   = price_on_event.iloc[0]
            p_after    = price_after_30.iloc[-1]
            pct_change = (p_after - p_before) / p_before * 100

            sev_emoji = {"critical": "🔴", "high": "🟠", "medium": "🔵", "low": "🟢"}
            impact_rows.append({
                "Date"        : event_date.strftime("%Y-%m-%d"),
                "Event"       : event["event"],
                "Sev"         : sev_emoji.get(event["severity"], "") + " " + event["severity"],
                "At event"    : f"${p_before:.2f}",
                "+30 days"    : f"${p_after:.2f}",
                "Change"      : f"{pct_change:+.1f}%",
            })

    if impact_rows:
        impact_df = pd.DataFrame(impact_rows)

        def color_change(val):
            try:
                v = float(val.replace("%", "").replace("+", ""))
                color = "color: #E24B4A" if v > 0 else "color: #639922"
                return color
            except Exception:
                return ""

        st.dataframe(
            impact_df.style.map(color_change, subset=["Change"]),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No event impact data in the selected date range.")

with col_right:
    st.subheader("⚡ Volatility ranking")
    st.caption("30-day rolling volatility at the latest date")

    latest_date = prices["date"].max()
    latest_vol  = (
        prices[prices["date"] == latest_date][["commodity_name", "volatility_30d"]]
        .copy()
        .sort_values("volatility_30d", ascending=True)
    )

    fig3 = px.bar(
        latest_vol,
        x="volatility_30d",
        y="commodity_name",
        orientation="h",
        color="volatility_30d",
        color_continuous_scale=[[0, "#9FE1CB"], [0.5, "#FAC775"], [1.0, "#F09595"]],
        labels={"volatility_30d": "Volatility", "commodity_name": ""},
    )
    fig3.update_layout(
        height=320,
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=20, t=10, b=30),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------
# Normalized comparison
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("📊 Commodity comparison (normalized to 100)")
st.caption(
    "Removes the effect of different price scales — shows relative movement from the selected start date. "
    "A value of 120 means the commodity is 20% above its starting price."
)

comparison_df = prices[
    (prices["date"] >= start_dt) &
    (prices["date"] <= end_dt)
].copy()

def normalize(group):
    first_valid = group["close"].iloc[0]
    group = group.copy()
    group["normalized"] = group["close"] / first_valid * 100
    return group

comparison_df = (
    comparison_df
    .groupby("commodity_name", group_keys=False)
    .apply(normalize)
)

fig2 = px.line(
    comparison_df,
    x="date", y="normalized", color="commodity_name",
    color_discrete_sequence=["#378ADD", "#D85A30", "#1D9E75", "#BA7517", "#D4537E"]
)
fig2.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.4,
               annotation_text="baseline", annotation_font_size=10)
fig2.update_layout(
    height=380,
    hovermode="x unified",
    yaxis_title="Normalized price (base = 100)",
    xaxis_title="Date",
    legend_title="Commodity",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
    yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
    margin=dict(l=40, r=40, t=20, b=40),
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Pipeline run history
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("🔧 Pipeline run history")

if not runs.empty:
    def style_status(val):
        if val == "success":
            return "color: #639922; font-weight: 500"
        elif val == "failed":
            return "color: #E24B4A; font-weight: 500"
        return ""

    display_runs = runs[["started_at", "finished_at", "status", "rows_loaded", "error_message"]].copy()
    st.dataframe(
        display_runs.style.map(style_status, subset=["status"]),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No pipeline runs recorded yet.")