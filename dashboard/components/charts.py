"""
Reusable Plotly chart helpers for Commodity Pulse.
All functions return go.Figure ready for st.plotly_chart().
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from .constants import (
    PLOT_BG, GRID_CLR, FONT_CLR,
    SEV_COLORS, COMMODITY_META, CATEGORIES,
    label_map, color_map, category_map,
)

MONO = "IBM Plex Mono"
SANS = "DM Sans"


# ─────────────────────────────────────────────────────────────────────────────
# Base layout
# ─────────────────────────────────────────────────────────────────────────────

def base_layout(**kwargs) -> dict:
    """Dark-theme base layout dict. Merge extra kwargs on top."""
    d = dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PLOT_BG,
        font=dict(family=SANS, color=FONT_CLR, size=11),
        xaxis=dict(showgrid=True, gridcolor=GRID_CLR, color=FONT_CLR, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=GRID_CLR, color=FONT_CLR, zeroline=False),
        hovermode="x unified",
        margin=dict(l=50, r=20, t=30, b=40),
    )
    d.update(kwargs)
    return d


# ─────────────────────────────────────────────────────────────────────────────
# Shared helper — add event vlines to an existing figure
# ─────────────────────────────────────────────────────────────────────────────

def _add_event_vlines(fig: go.Figure, events: pd.DataFrame, start_dt, end_dt) -> None:
    added = set()
    if events is None or events.empty:
        return
    for _, e in events.iterrows():
        if start_dt <= e["date"] <= end_dt:
            c  = SEV_COLORS.get(e["severity"], "#888")
            dm = int(pd.Timestamp(e["date"]).timestamp() * 1000)
            fig.add_vline(x=dm, line_dash="dot", line_color=c, line_width=1)
            if e["severity"] not in added:
                fig.add_trace(go.Scatter(
                    x=[None], y=[None], mode="markers",
                    marker=dict(color=c, size=9, symbol="line-ns-open",
                                line=dict(width=2, color=c)),
                    name=f"Event · {e['severity'].title()}",
                    showlegend=True,
                ))
                added.add(e["severity"])


# ─────────────────────────────────────────────────────────────────────────────
# Price history — area line + optional MAs + events
# ─────────────────────────────────────────────────────────────────────────────

def price_history_chart(
    filtered: pd.DataFrame,
    events: pd.DataFrame,
    meta: dict,
    start_dt,
    end_dt,
    show_ma: bool = True,
    show_ev: bool = True,
    height: int = 420,
) -> go.Figure:
    accent = meta.get("color", "#ff8a4c")
    fig = go.Figure()

    # Fill area
    fig.add_trace(go.Scatter(
        x=filtered["date"],
        y=filtered["close"],
        customdata=filtered["close"],
        name=f"{meta.get('label','')} ({meta.get('unit_short','')})",
        fill="tozeroy",
        fillcolor=f"rgba({_hex_to_rgb(accent)},0.06)",
        line=dict(color=accent, width=2),
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            "<b>$%{customdata:.2f}</b> / " + meta.get("unit_short","") +
            "<extra></extra>"
        ),
    ))

    if show_ma:
        fig.add_trace(go.Scatter(
            x=filtered["date"], y=filtered["rolling_7d_avg"],
            customdata=filtered["rolling_7d_avg"], name="7-day MA",
            line=dict(color="#4b5878", width=1.2, dash="dash"),
            hovertemplate="7d MA: $%{customdata:.2f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=filtered["date"], y=filtered["rolling_30d_avg"],
            customdata=filtered["rolling_30d_avg"], name="30-day MA",
            line=dict(color="#6b7fa8", width=1.5, dash="dot"),
            hovertemplate="30d MA: $%{customdata:.2f}<extra></extra>",
        ))

    if show_ev:
        _add_event_vlines(fig, events, start_dt, end_dt)

    fig.update_layout(**base_layout(
        height=height,
        yaxis_title=f"Price ({meta.get('unit_short','USD')})",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.01,
            font=dict(family=MONO, size=10, color=FONT_CLR),
            bgcolor="rgba(0,0,0,0)", title_text="",
        ),
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Candlestick OHLC
# ─────────────────────────────────────────────────────────────────────────────

def candlestick_chart(
    filtered: pd.DataFrame,
    meta: dict,
    show_ma: bool = True,
    height: int = 400,
) -> go.Figure:
    hover = [
        (f"<b>{d:%d %b %Y}</b><br>O ${o:.2f}  H ${h:.2f}  L ${l:.2f}  C ${c:.2f}")
        for d, o, h, l, c in zip(
            filtered["date"], filtered["open"], filtered["high"],
            filtered["low"], filtered["close"],
        )
    ]
    fig = go.Figure(go.Candlestick(
        x=filtered["date"],
        open=filtered["open"], high=filtered["high"],
        low=filtered["low"],   close=filtered["close"],
        increasing_line_color="#22c55e", decreasing_line_color="#ef4444",
        increasing_fillcolor="rgba(34,197,94,0.2)",
        decreasing_fillcolor="rgba(239,68,68,0.2)",
        hovertext=hover, hoverinfo="text",
    ))
    if show_ma:
        fig.add_trace(go.Scatter(
            x=filtered["date"], y=filtered["rolling_7d_avg"],
            customdata=filtered["rolling_7d_avg"], name="7d MA",
            line=dict(color="#f59e0b", width=1.2, dash="dash"),
            hovertemplate="7d MA: $%{customdata:.2f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=filtered["date"], y=filtered["rolling_30d_avg"],
            customdata=filtered["rolling_30d_avg"], name="30d MA",
            line=dict(color="#6b7fa8", width=1.5, dash="dot"),
            hovertemplate="30d MA: $%{customdata:.2f}<extra></extra>",
        ))
    fig.update_layout(**base_layout(
        height=height,
        yaxis_title=f"Price ({meta.get('unit_short','')})",
    ))
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Return histogram
# ─────────────────────────────────────────────────────────────────────────────

def return_histogram(filtered: pd.DataFrame, accent: str, height: int = 260) -> go.Figure:
    data = filtered["daily_return_pct"].dropna()
    fig = go.Figure(go.Histogram(
        x=data, nbinsx=60,
        marker_color=accent, opacity=0.8,
        hovertemplate="Return: %{x:.2f}%<br>Days: %{y}<extra></extra>",
    ))
    # Add mean line
    mean_val = data.mean()
    fig.add_vline(x=0,        line_dash="dash", line_color="rgba(255,255,255,0.1)")
    fig.add_vline(x=mean_val, line_dash="dot",  line_color=accent, line_width=1,
                  annotation_text=f"μ={mean_val:.2f}%",
                  annotation_font_size=9, annotation_font_color=accent,
                  annotation_position="top right")
    fig.update_layout(**base_layout(
        height=height,
        xaxis_title="Daily return (%)",
        yaxis_title="# Trading days",
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Volatility timeline
# ─────────────────────────────────────────────────────────────────────────────

def volatility_chart(filtered: pd.DataFrame, height: int = 260) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=filtered["date"], y=filtered["volatility_30d"],
        customdata=filtered["volatility_30d"],
        fill="tozeroy",
        fillcolor="rgba(239,68,68,0.06)",
        line=dict(color="#ef4444", width=1.8),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Vol: %{customdata:.2f}<extra></extra>",
    ))
    # Mean vol reference
    mean_vol = filtered["volatility_30d"].mean()
    if not np.isnan(mean_vol):
        fig.add_hline(y=mean_vol, line_dash="dash", line_color="rgba(255,255,255,0.1)",
                      annotation_text=f"avg {mean_vol:.2f}",
                      annotation_font_size=9, annotation_font_color="#4a5878")
    fig.update_layout(**base_layout(height=height, yaxis_title="Volatility (30d std)"))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Monthly range bar
# ─────────────────────────────────────────────────────────────────────────────

def monthly_range_bar(filtered: pd.DataFrame, meta: dict, height: int = 250) -> go.Figure:
    m = filtered.copy()
    m["ym"] = m["date"].dt.to_period("M").astype(str)
    mr = m.groupby("ym")["daily_range"].mean().reset_index()

    fig = go.Figure(go.Bar(
        x=mr["ym"], y=mr["daily_range"],
        marker_color=mr["daily_range"],
        marker_colorscale=[[0, "#0c0f18"], [0.5, "#f59e0b"], [1, "#ef4444"]],
        text=[f"${v:.2f}" for v in mr["daily_range"]],
        textposition="outside",
        textfont=dict(family=MONO, size=9, color=FONT_CLR),
        hovertemplate="<b>%{x}</b><br>Avg daily range: $%{y:.2f}<extra></extra>",
    ))
    fig.update_layout(**base_layout(
        height=height,
        yaxis_title=f"Avg daily range ({meta.get('unit_short','')})",
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Category overview — multi-commodity price history on one chart
# ─────────────────────────────────────────────────────────────────────────────

def category_price_chart(
    cat_df: pd.DataFrame,
    events: pd.DataFrame,
    start_dt,
    end_dt,
    show_ev: bool = True,
    height: int = 380,
) -> go.Figure:
    """Normalized index chart for all commodities in one category."""
    fig = go.Figure()

    for com in cat_df["commodity_name"].unique():
        sub  = cat_df[cat_df["commodity_name"] == com].copy()
        meta = COMMODITY_META.get(com, {})
        base = sub["close"].iloc[0]
        if base == 0:
            continue
        sub["norm"] = sub["close"] / base * 100

        fig.add_trace(go.Scatter(
            x=sub["date"],
            y=sub["norm"],
            customdata=list(zip(sub["close"], sub["norm"])),
            name=meta.get("label", com),
            line=dict(color=meta.get("color", "#888"), width=2),
            hovertemplate=(
                f"<b>%{{x|%d %b %Y}}</b><br>"
                f"{meta.get('label',com)}: ${{customdata[0]:.2f}}"
                f" ({meta.get('unit_short','')})<br>"
                f"Index: %{{customdata[1]:.1f}}<extra></extra>"
            ),
        ))

    fig.add_hline(y=100, line_dash="dash", line_color="rgba(255,255,255,0.06)",
                  annotation_text="Baseline", annotation_font_size=9,
                  annotation_font_color="#2a3350")

    if show_ev:
        _add_event_vlines(fig, events, start_dt, end_dt)

    fig.update_layout(**base_layout(
        height=height,
        yaxis_title="Normalized index (100 = period start)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.01,
            font=dict(family=MONO, size=10, color=FONT_CLR),
            bgcolor="rgba(0,0,0,0)", title_text="",
        ),
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Volatility ranking bar (horizontal)
# ─────────────────────────────────────────────────────────────────────────────

def volatility_ranking_bar(prices: pd.DataFrame, commodity_list: list = None, height: int = 280) -> go.Figure:
    ld = prices["date"].max()
    lv = prices[prices["date"] == ld][["commodity_name", "volatility_30d"]].copy()
    if commodity_list:
        lv = lv[lv["commodity_name"].isin(commodity_list)]
    lv = lv.sort_values("volatility_30d", ascending=True)
    lv["label"] = lv["commodity_name"].map(label_map).fillna(lv["commodity_name"])
    lv["color"] = lv["commodity_name"].map(color_map).fillna("#6b7fa8")

    fig = go.Figure(go.Bar(
        x=lv["volatility_30d"], y=lv["label"],
        orientation="h",
        marker_color=lv["color"].tolist(),
        text=[f"{v:.2f}" for v in lv["volatility_30d"]],
        textposition="outside",
        textfont=dict(family=MONO, size=10, color=FONT_CLR),
        hovertemplate="<b>%{y}</b><br>30d vol: %{x:.2f}<extra></extra>",
    ))
    fig.update_layout(**base_layout(
        height=height,
        xaxis_title="30-day Volatility (std dev)",
        margin=dict(l=10, r=60, t=10, b=40),
        showlegend=False,
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Correlation heatmap
# ─────────────────────────────────────────────────────────────────────────────

def correlation_heatmap(comp_df: pd.DataFrame, height: int = 320) -> go.Figure:
    pivot = comp_df.pivot_table(index="date", columns="label", values="close")
    corr  = pivot.pct_change(fill_method=None).corr().round(2)

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale=[[0, "#080a0f"], [0.5, "#1a2035"], [1, "#ff8a4c"]],
        text=corr.values,
        texttemplate="%{text:.2f}",
        textfont=dict(family=MONO, size=10),
        hovertemplate="<b>%{x} vs %{y}</b><br>Correlation: %{z:.2f}<extra></extra>",
        zmin=-1, zmax=1,
    ))
    fig.update_layout(**base_layout(height=height, margin=dict(l=10, r=10, t=10, b=40)))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Event impact — severity average bar
# ─────────────────────────────────────────────────────────────────────────────

def severity_avg_bar(impact_rows: list, height: int = 220) -> go.Figure:
    idf     = pd.DataFrame(impact_rows)
    sev_avg = idf.groupby("_sev")["_pct"].mean().reset_index()
    sev_avg["color"] = sev_avg["_sev"].map(SEV_COLORS)
    sev_avg["label"] = sev_avg["_sev"].str.title()
    sev_avg = sev_avg.sort_values("_pct", ascending=True)

    fig = go.Figure(go.Bar(
        x=sev_avg["_pct"], y=sev_avg["label"],
        orientation="h",
        marker_color=sev_avg["color"].tolist(),
        text=[f"{v:+.1f}%" for v in sev_avg["_pct"]],
        textposition="outside",
        textfont=dict(family=MONO, size=11, color=FONT_CLR),
        hovertemplate="<b>%{y}</b><br>Avg 30d impact: %{x:+.1f}%<extra></extra>",
    ))
    fig.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.07)")
    fig.update_layout(**base_layout(
        height=height,
        xaxis_title="Avg 30-day price change (%)",
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Event timeline scatter
# ─────────────────────────────────────────────────────────────────────────────

def event_timeline_scatter(impact_rows: list, height: int = 280) -> go.Figure:
    idf = pd.DataFrame(impact_rows)
    idf["dot_color"] = idf["_pct"].apply(lambda v: "#ef4444" if v > 0 else "#22c55e")
    idf["size"]      = idf["_sev"].map({"critical": 20, "high": 14, "medium": 9, "low": 5}).fillna(8)

    fig = go.Figure(go.Scatter(
        x=idf["_date"], y=idf["_pct"],
        mode="markers",
        marker=dict(
            size=idf["size"],
            color=idf["dot_color"],
            opacity=0.85,
            line=dict(width=1, color="rgba(255,255,255,0.08)"),
        ),
        customdata=list(zip(idf["Event"], idf["_pct"], idf["_sev"])),
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            "%{customdata[0]}<br>"
            "Severity: %{customdata[2]}<br>"
            "30d Impact: %{customdata[1]:+.1f}%<extra></extra>"
        ),
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.07)")
    fig.update_layout(**base_layout(height=height, yaxis_title="30-day price impact (%)"))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Ripple effects — lead/lag scatter
# ─────────────────────────────────────────────────────────────────────────────

def ripple_scatter(
    prices: pd.DataFrame,
    source_com: str,
    target_com: str,
    lag_days: int = 30,
    height: int = 300,
) -> go.Figure:
    """
    Scatter of source commodity return (x) vs target return lagged by lag_days (y).
    Shows how price shocks in the source transmit to the target.
    """
    src = prices[prices["commodity_name"] == source_com][["date", "close"]].copy()
    tgt = prices[prices["commodity_name"] == target_com][["date", "close"]].copy()

    src = src.sort_values("date").set_index("date")
    tgt = tgt.sort_values("date").set_index("date")

    src["ret"] = src["close"].pct_change(lag_days) * 100
    tgt["ret"] = tgt["close"].pct_change(lag_days) * 100

    merged = src[["ret"]].join(tgt[["ret"]], lsuffix="_src", rsuffix="_tgt").dropna()
    corr   = merged["ret_src"].corr(merged["ret_tgt"])

    src_meta = COMMODITY_META.get(source_com, {})
    tgt_meta = COMMODITY_META.get(target_com, {})

    fig = go.Figure(go.Scatter(
        x=merged["ret_src"],
        y=merged["ret_tgt"],
        mode="markers",
        marker=dict(
            size=5,
            color=tgt_meta.get("color", "#888"),
            opacity=0.6,
            line=dict(width=0.5, color="rgba(255,255,255,0.05)"),
        ),
        hovertemplate=(
            f"{src_meta.get('label','Source')}: %{{x:.1f}}%<br>"
            f"{tgt_meta.get('label','Target')}: %{{y:.1f}}%<extra></extra>"
        ),
    ))

    # Trend line
    if len(merged) > 5:
        z  = np.polyfit(merged["ret_src"], merged["ret_tgt"], 1)
        xr = np.linspace(merged["ret_src"].min(), merged["ret_src"].max(), 100)
        fig.add_trace(go.Scatter(
            x=xr, y=np.polyval(z, xr),
            mode="lines",
            line=dict(color="rgba(255,138,76,0.5)", width=1.5, dash="dash"),
            name=f"trend (r={corr:.2f})",
        ))

    fig.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.05)")
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.05)")

    fig.update_layout(**base_layout(
        height=height,
        xaxis_title=f"{src_meta.get('label','Source')} {lag_days}d return (%)",
        yaxis_title=f"{tgt_meta.get('label','Target')} {lag_days}d return (%)",
        title=dict(
            text=f"Pearson r = {corr:.3f}",
            font=dict(family=MONO, size=11, color="#6b7fa8"),
            x=0.99, xanchor="right",
        ),
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Ripple effects — cross-commodity lag correlation bar
# ─────────────────────────────────────────────────────────────────────────────

def ripple_lag_bar(
    prices: pd.DataFrame,
    source_com: str,
    target_commodities: list,
    lag_days: int = 30,
    height: int = 300,
) -> go.Figure:
    """
    Horizontal bar: Pearson correlation of source vs each target at lag_days.
    """
    src = prices[prices["commodity_name"] == source_com][["date", "close"]].copy()
    src = src.sort_values("date").set_index("date")
    src["ret"] = src["close"].pct_change(lag_days) * 100

    rows = []
    for tgt_com in target_commodities:
        tgt = prices[prices["commodity_name"] == tgt_com][["date", "close"]].copy()
        tgt = tgt.sort_values("date").set_index("date")
        tgt["ret"] = tgt["close"].pct_change(lag_days) * 100
        merged = src[["ret"]].join(tgt[["ret"]], lsuffix="_s", rsuffix="_t").dropna()
        if len(merged) > 10:
            corr = merged["ret_s"].corr(merged["ret_t"])
            rows.append({"commodity": tgt_com, "corr": corr})

    if not rows:
        return go.Figure()

    df = pd.DataFrame(rows).sort_values("corr", ascending=True)
    df["label"] = df["commodity"].map(label_map).fillna(df["commodity"])
    df["color"] = df["commodity"].map(color_map).fillna("#6b7fa8")

    src_meta = COMMODITY_META.get(source_com, {})

    fig = go.Figure(go.Bar(
        x=df["corr"], y=df["label"],
        orientation="h",
        marker_color=df["color"].tolist(),
        text=[f"{v:+.2f}" for v in df["corr"]],
        textposition="outside",
        textfont=dict(family=MONO, size=10, color=FONT_CLR),
        hovertemplate="<b>%{y}</b><br>Correlation: %{x:.3f}<extra></extra>",
    ))
    fig.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.07)")
    fig.update_layout(**base_layout(
        height=height,
        xaxis_title=f"Pearson r with {src_meta.get('label','source')} ({lag_days}d lag)",
        margin=dict(l=10, r=70, t=10, b=40),
        showlegend=False,
        xaxis=dict(range=[-1, 1], showgrid=True, gridcolor=GRID_CLR, color=FONT_CLR, zeroline=False),
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline bar
# ─────────────────────────────────────────────────────────────────────────────

def pipeline_bar(runs: pd.DataFrame, height: int = 230) -> go.Figure:
    r = runs.copy()
    r["started_at"]   = pd.to_datetime(r["started_at"])
    r = r.sort_values("started_at")
    r["status_color"] = r["status"].map({
        "success": "#22c55e",
        "failed":  "#ef4444",
        "running": "#f59e0b",
    })
    fig = go.Figure(go.Bar(
        x=r["started_at"].dt.strftime("%d %b %H:%M"),
        y=r["rows_loaded"],
        marker_color=r["status_color"].tolist(),
        text=r["rows_loaded"],
        textposition="outside",
        textfont=dict(family=MONO, size=10, color=FONT_CLR),
        hovertemplate="<b>%{x}</b><br>Rows: %{y:,}<extra></extra>",
    ))
    fig.update_layout(**base_layout(height=height, yaxis_title="Rows loaded"))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Overview — full cross-category normalized chart
# ─────────────────────────────────────────────────────────────────────────────

def overview_normalized_chart(
    prices: pd.DataFrame,
    events: pd.DataFrame,
    start_dt,
    end_dt,
    show_ev: bool = True,
    height: int = 420,
) -> go.Figure:
    """All 13 commodities normalized on one chart, coloured by commodity."""
    fig = go.Figure()

    for com in prices["commodity_name"].unique():
        sub  = prices[
            (prices["commodity_name"] == com)
            & (prices["date"] >= start_dt)
            & (prices["date"] <= end_dt)
        ].copy()
        if sub.empty:
            continue
        meta  = COMMODITY_META.get(com, {})
        base  = sub["close"].iloc[0]
        if base == 0:
            continue
        sub["norm"] = sub["close"] / base * 100

        fig.add_trace(go.Scatter(
            x=sub["date"],
            y=sub["norm"],
            customdata=list(zip(sub["close"], sub["norm"])),
            name=meta.get("label", com),
            line=dict(color=meta.get("color", "#888"), width=1.5),
            hovertemplate=(
                f"<b>%{{x|%d %b %Y}}</b><br>"
                f"{meta.get('label',com)}: ${{customdata[0]:.2f}}<br>"
                f"Index: %{{customdata[1]:.1f}}<extra></extra>"
            ),
        ))

    fig.add_hline(y=100, line_dash="dash", line_color="rgba(255,255,255,0.05)")

    if show_ev:
        _add_event_vlines(fig, events, start_dt, end_dt)

    fig.update_layout(**base_layout(
        height=height,
        yaxis_title="Normalized index (100 = start)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.01,
            font=dict(family=MONO, size=9, color=FONT_CLR),
            bgcolor="rgba(0,0,0,0)", title_text="",
        ),
    ))
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Utility
# ─────────────────────────────────────────────────────────────────────────────

def _hex_to_rgb(hex_color: str) -> str:
    """Convert #rrggbb to 'r,g,b' string for rgba()."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}"