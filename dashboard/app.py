import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title = "Oil & Geopolitical Impact Tracker",
    page_icon  = "🛢️",
    layout     = "wide"
)

# ---------------------------------------------------------------------------
# Database connection
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


# ---------------------------------------------------------------------------
# Data loaders — cached so the dashboard doesn't re-query on every interaction
# ---------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_prices() -> pd.DataFrame:
    engine = get_engine()
    df = pd.read_sql(
        "SELECT * FROM commodity_prices ORDER BY date ASC",
        engine
    )
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(ttl=3600)
def load_events() -> pd.DataFrame:
    engine = get_engine()
    df = pd.read_sql(
        "SELECT * FROM geopolitical_events ORDER BY date ASC",
        engine
    )
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(ttl=3600)
def load_pipeline_runs() -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(
        "SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT 10",
        engine
    )


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
prices = load_prices()
events = load_events()
runs   = load_pipeline_runs()

# ---------------------------------------------------------------------------
# Sidebar — filters
# ---------------------------------------------------------------------------
st.sidebar.title("🛢️ Oil Tracker")
st.sidebar.markdown("---")

all_commodities = sorted(prices["commodity_name"].unique())
selected_commodity = st.sidebar.selectbox(
    "Select Commodity",
    all_commodities,
    index = all_commodities.index("brent_crude") if "brent_crude" in all_commodities else 0
)

min_date = prices["date"].min().date()
max_date = prices["date"].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value = [min_date, max_date],
    min_value = min_date,
    max_value = max_date
)

show_events = st.sidebar.checkbox("Show Geopolitical Events", value=True)
show_ma     = st.sidebar.checkbox("Show Moving Averages",     value=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"Last pipeline run: {runs['started_at'].iloc[0].strftime('%Y-%m-%d %H:%M') if not runs.empty else 'Never'}")
st.sidebar.caption(f"Last status: {runs['status'].iloc[0] if not runs.empty else 'N/A'}")

# ---------------------------------------------------------------------------
# Filter data by selected commodity and date range
# ---------------------------------------------------------------------------
filtered = prices[
    (prices["commodity_name"] == selected_commodity) &
    (prices["date"] >= pd.to_datetime(date_range[0])) &
    (prices["date"] <= pd.to_datetime(date_range[1]))
].copy()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🛢️ Oil Price & Geopolitical Impact Tracker")
st.caption(
    "Tracks how Middle East conflict events affect global commodity prices. "
    "Data sourced from Yahoo Finance · Updated daily."
)
st.markdown("---")

# ---------------------------------------------------------------------------
# KPI cards — top row
# ---------------------------------------------------------------------------
if not filtered.empty:
    latest       = filtered.iloc[-1]
    prev         = filtered.iloc[-2] if len(filtered) > 1 else latest
    price_delta  = latest["close"] - prev["close"]

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        label = "Current Price (USD)",
        value = f"${latest['close']:.2f}",
        delta = f"{price_delta:+.2f} vs yesterday"
    )
    col2.metric(
        label = "7-Day Average",
        value = f"${latest['rolling_7d_avg']:.2f}"
    )
    col3.metric(
        label = "30-Day Average",
        value = f"${latest['rolling_30d_avg']:.2f}"
    )
    col4.metric(
        label = "vs 30-Day Avg",
        value = f"{latest['price_vs_30d_avg_pct']:+.1f}%"
    )
    col5.metric(
        label = "30-Day Volatility",
        value = f"{latest['volatility_30d']:.2f}"
    )

st.markdown("---")

# ---------------------------------------------------------------------------
# Main price chart with event markers
# ---------------------------------------------------------------------------
st.subheader(f"📈 {selected_commodity.replace('_', ' ').title()} — Price History")

fig = go.Figure()

# Close price line
fig.add_trace(go.Scatter(
    x    = filtered["date"],
    y    = filtered["close"],
    name = "Close Price",
    line = dict(color="#2196F3", width=2)
))

# Moving averages
if show_ma:
    fig.add_trace(go.Scatter(
        x    = filtered["date"],
        y    = filtered["rolling_7d_avg"],
        name = "7-Day MA",
        line = dict(color="#FF9800", width=1, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x    = filtered["date"],
        y    = filtered["rolling_30d_avg"],
        name = "30-Day MA",
        line = dict(color="#4CAF50", width=1, dash="dot")
    ))

# Geopolitical event markers
if show_events:
    for _, event in events.iterrows():
        if pd.to_datetime(date_range[0]) <= event["date"] <= pd.to_datetime(date_range[1]):
            color = "#F44336" if event["severity"] == "critical" else "#FF9800"
            fig.add_vline(
                x                  = event["date"],
                line_dash          = "dot",
                line_color         = color,
                line_width         = 1.5,
                annotation_text    = event["event"][:35],
                annotation_position= "top left",
                annotation_font_size= 9,
                annotation_font_color= color
            )

fig.update_layout(
    height     = 500,
    hovermode  = "x unified",
    xaxis_title= "Date",
    yaxis_title= "Price (USD)",
    legend     = dict(orientation="h", yanchor="bottom", y=1.02),
    margin     = dict(l=40, r=40, t=60, b=40)
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Event impact table
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("💥 Geopolitical Event Impact Analysis")
st.caption("Price change in the 30 days following each event for the selected commodity")

impact_rows = []
for _, event in events.iterrows():
    event_date    = event["date"]
    date_plus_30  = event_date + pd.Timedelta(days=30)

    price_on_event = filtered[filtered["date"] == event_date]["close"]
    price_after_30 = filtered[filtered["date"] <= date_plus_30]["close"]

    if not price_on_event.empty and not price_after_30.empty:
        p_before = price_on_event.iloc[0]
        p_after  = price_after_30.iloc[-1]
        pct_change = (p_after - p_before) / p_before * 100

        impact_rows.append({
            "Date"           : event_date.strftime("%Y-%m-%d"),
            "Event"          : event["event"],
            "Severity"       : event["severity"].upper(),
            "Price at Event" : f"${p_before:.2f}",
            "Price +30 Days" : f"${p_after:.2f}",
            "Change (%)"     : f"{pct_change:+.1f}%"
        })

if impact_rows:
    impact_df = pd.DataFrame(impact_rows)
    st.dataframe(impact_df, use_container_width=True, hide_index=True)
else:
    st.info("No event impact data available for the selected date range.")

# ---------------------------------------------------------------------------
# Commodity comparison chart — all commodities normalized to 100
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("📊 Commodity Comparison (Normalized to 100)")
st.caption("Shows relative price movement across all commodities from the selected start date — removes the effect of different price scales")

comparison_df = prices[
    (prices["date"] >= pd.to_datetime(date_range[0])) &
    (prices["date"] <= pd.to_datetime(date_range[1]))
].copy()

# Normalize each commodity to 100 at the start date
def normalize(group):
    first_valid = group["close"].iloc[0]
    group["normalized"] = group["close"] / first_valid * 100
    return group

comparison_df = (
    comparison_df
    .groupby("commodity_name", group_keys=False)
    .apply(normalize)
)

fig2 = px.line(
    comparison_df,
    x     = "date",
    y     = "normalized",
    color = "commodity_name",
    title = "All Commodities — Normalized Price Index"
)

fig2.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.5)
fig2.update_layout(
    height      = 400,
    hovermode   = "x unified",
    yaxis_title = "Normalized Price (base = 100)",
    xaxis_title = "Date",
    legend_title= "Commodity"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Volatility ranking
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("⚡ Current Volatility Ranking")
st.caption("30-day rolling volatility — higher means more price instability right now")

latest_date    = prices["date"].max()
latest_vol     = prices[prices["date"] == latest_date][["commodity_name", "volatility_30d"]].copy()
latest_vol     = latest_vol.sort_values("volatility_30d", ascending=True)

fig3 = px.bar(
    latest_vol,
    x           = "volatility_30d",
    y           = "commodity_name",
    orientation = "h",
    color       = "volatility_30d",
    color_continuous_scale = "Reds",
    title       = f"Volatility as of {latest_date.strftime('%Y-%m-%d')}"
)
fig3.update_layout(height=300, showlegend=False, coloraxis_showscale=False)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------
# Pipeline run history
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("🔧 Pipeline Run History")
st.caption("Last 10 pipeline executions")

if not runs.empty:
    st.dataframe(
        runs[["started_at", "finished_at", "status", "rows_loaded", "error_message"]],
        use_container_width = True,
        hide_index          = True
    )
else:
    st.info("No pipeline runs recorded yet.")