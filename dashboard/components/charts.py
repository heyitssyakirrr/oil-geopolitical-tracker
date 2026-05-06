"""
Reusable Plotly chart helpers.
All chart functions return a go.Figure ready for st.plotly_chart().
"""

import plotly.graph_objects as go
import pandas as pd

from .constants import (
    PLOT_BG, GRID_CLR, FONT_CLR,
    SEV_COLORS, COMMODITY_META, label_map, color_map,
)


def base_layout(**kwargs) -> dict:
    """Default dark-theme layout dict; merge extra kwargs on top."""
    d = dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PLOT_BG,
        font=dict(family="DM Sans", color=FONT_CLR, size=11),
        xaxis=dict(showgrid=True, gridcolor=GRID_CLR, color=FONT_CLR, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=GRID_CLR, color=FONT_CLR, zeroline=False),
        hovermode="x unified",
        margin=dict(l=50, r=20, t=30, b=40),
    )
    d.update(kwargs)
    return d


def price_history_chart(
    filtered: pd.DataFrame,
    events: pd.DataFrame,
    meta: dict,
    start_dt,
    end_dt,
    show_ma: bool = True,
    show_ev: bool = True,
    height: int = 430,
) -> go.Figure:
    """Area line chart with optional moving averages and event vlines."""
    accent = meta.get("color", "#e25c2e")
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered["date"],
        y=filtered["close"],
        customdata=filtered["close"],
        name=f"{meta.get('label', '')} ({meta.get('unit_short', '')})",
        fill="tozeroy",
        fillcolor="rgba(226,92,46,0.07)",
        line=dict(color=accent, width=2),
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            "<b>$%{customdata:.2f}</b> / " + meta.get("unit_short", "") +
            "<extra></extra>"
        ),
    ))

    if show_ma:
        fig.add_trace(go.Scatter(
            x=filtered["date"],
            y=filtered["rolling_7d_avg"],
            customdata=filtered["rolling_7d_avg"],
            name="7-day MA",
            line=dict(color="#6b7280", width=1.2, dash="dash"),
            hovertemplate="7d MA: $%{customdata:.2f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=filtered["date"],
            y=filtered["rolling_30d_avg"],
            customdata=filtered["rolling_30d_avg"],
            name="30-day MA",
            line=dict(color="#9ba3b5", width=1.5, dash="dot"),
            hovertemplate="30d MA: $%{customdata:.2f}<extra></extra>",
        ))

    if show_ev and events is not None:
        added_sevs = set()
        for _, e in events.iterrows():
            if start_dt <= e["date"] <= end_dt:
                c  = SEV_COLORS.get(e["severity"], "#888")
                dm = int(pd.Timestamp(e["date"]).timestamp() * 1000)
                fig.add_vline(x=dm, line_dash="dot", line_color=c, line_width=1.2)
                if e["severity"] not in added_sevs:
                    fig.add_trace(go.Scatter(
                        x=[None], y=[None], mode="markers",
                        marker=dict(color=c, size=9, symbol="line-ns-open", line=dict(width=2, color=c)),
                        name=f"Event: {e['severity'].title()}",
                        showlegend=True,
                    ))
                    added_sevs.add(e["severity"])

    fig.update_layout(**base_layout(
        height=height,
        yaxis_title=f"Price ({meta.get('unit_short', 'USD')})",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.01,
            font=dict(family="IBM Plex Mono", size=10, color=FONT_CLR),
            bgcolor="rgba(0,0,0,0)", title_text="",
        ),
    ))
    return fig


def candlestick_chart(filtered: pd.DataFrame, meta: dict, show_ma: bool = True, height: int = 420) -> go.Figure:
    """OHLC candlestick with optional moving average overlays."""
    candle_hover = [
        (
            f"<b>{d:%d %b %Y}</b><br>"
            f"Open:  ${o:.2f}<br>"
            f"High:  ${h:.2f}<br>"
            f"Low:   ${l:.2f}<br>"
            f"Close: ${c:.2f}"
        )
        for d, o, h, l, c in zip(
            filtered["date"],
            filtered["open"],
            filtered["high"],
            filtered["low"],
            filtered["close"],
        )
    ]

    fig = go.Figure(data=go.Candlestick(
        x=filtered["date"],
        open=filtered["open"],
        high=filtered["high"],
        low=filtered["low"],
        close=filtered["close"],
        increasing_line_color="#22c55e",
        decreasing_line_color="#ef4444",
        increasing_fillcolor="rgba(34,197,94,0.25)",
        decreasing_fillcolor="rgba(239,68,68,0.25)",
        hovertext=candle_hover,
        hoverinfo="text",
    ))

    if show_ma:
        fig.add_trace(go.Scatter(
            x=filtered["date"], y=filtered["rolling_7d_avg"],
            customdata=filtered["rolling_7d_avg"], name="7d MA",
            line=dict(color="#f59e0b", width=1.3, dash="dash"),
            hovertemplate="7d MA: $%{customdata:.2f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=filtered["date"], y=filtered["rolling_30d_avg"],
            customdata=filtered["rolling_30d_avg"], name="30d MA",
            line=dict(color="#9ba3b5", width=1.5, dash="dot"),
            hovertemplate="30d MA: $%{customdata:.2f}<extra></extra>",
        ))

    fig.update_layout(**base_layout(
        height=height,
        yaxis_title=f"Price ({meta.get('unit_short', '')})",
    ))
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


def return_histogram(filtered: pd.DataFrame, accent: str, height: int = 280) -> go.Figure:
    """Histogram of daily % returns."""
    fig = go.Figure(go.Histogram(
        x=filtered["daily_return_pct"].dropna(),
        nbinsx=60,
        marker_color=accent,
        opacity=0.8,
        hovertemplate="Return: %{x:.2f}%<br>Days: %{y}<extra></extra>",
    ))
    fig.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.15)")
    fig.update_layout(**base_layout(
        height=height,
        xaxis_title="Daily return (%)",
        yaxis_title="# Trading days",
    ))
    return fig


def volatility_chart(filtered: pd.DataFrame, height: int = 280) -> go.Figure:
    """30-day rolling volatility area chart."""
    fig = go.Figure(go.Scatter(
        x=filtered["date"],
        y=filtered["volatility_30d"],
        customdata=filtered["volatility_30d"],
        fill="tozeroy",
        fillcolor="rgba(239,68,68,0.07)",
        line=dict(color="#ef4444", width=1.8),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Vol: %{customdata:.2f}<extra></extra>",
    ))
    fig.update_layout(**base_layout(height=height, yaxis_title="Volatility (30d)"))
    return fig


def monthly_range_bar(filtered: pd.DataFrame, meta: dict, height: int = 260) -> go.Figure:
    """Average monthly daily-range bar chart."""
    monthly = filtered.copy()
    monthly["ym"] = monthly["date"].dt.to_period("M").astype(str)
    mr = monthly.groupby("ym")["daily_range"].mean().reset_index()

    fig = go.Figure(go.Bar(
        x=mr["ym"],
        y=mr["daily_range"],
        marker_color=mr["daily_range"],
        marker_colorscale=[[0, "#1c2030"], [0.5, "#f59e0b"], [1, "#ef4444"]],
        text=[f"${v:.2f}" for v in mr["daily_range"]],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=9, color=FONT_CLR),
        hovertemplate="<b>%{x}</b><br>Avg daily range: $%{y:.2f}<extra></extra>",
    ))
    fig.update_layout(**base_layout(
        height=height,
        yaxis_title=f"Avg daily range ({meta.get('unit_short', '')})",
    ))
    return fig


def severity_avg_bar(impact_rows: list, height: int = 220) -> go.Figure:
    """Horizontal bar — average 30-day price impact grouped by severity."""
    import pandas as pd
    idf = pd.DataFrame(impact_rows)
    sev_avg = idf.groupby("_sev")["_pct"].mean().reset_index()
    sev_avg["color"] = sev_avg["_sev"].map(SEV_COLORS)
    sev_avg["label"] = sev_avg["_sev"].str.title()
    sev_avg = sev_avg.sort_values("_pct", ascending=True)

    fig = go.Figure(go.Bar(
        x=sev_avg["_pct"],
        y=sev_avg["label"],
        orientation="h",
        marker_color=sev_avg["color"].tolist(),
        text=[f"{v:+.1f}%" for v in sev_avg["_pct"]],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=11, color=FONT_CLR),
        hovertemplate="<b>%{y}</b><br>Avg 30d impact: %{x:+.1f}%<extra></extra>",
    ))
    fig.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.1)")
    fig.update_layout(**base_layout(
        height=height,
        xaxis_title="Avg 30-day price change (%)",
    ))
    return fig


def event_timeline_scatter(impact_rows: list, height: int = 280) -> go.Figure:
    """Scatter: each event dot coloured by direction, sized by severity."""
    import pandas as pd
    idf = pd.DataFrame(impact_rows)
    idf["dot_color"] = idf["_pct"].apply(lambda v: "#ef4444" if v > 0 else "#22c55e")
    idf["size"] = idf["_sev"].map({"critical": 20, "high": 14, "medium": 9, "low": 5}).fillna(8)

    fig = go.Figure(go.Scatter(
        x=idf["_date"],
        y=idf["_pct"],
        mode="markers",
        marker=dict(
            size=idf["size"],
            color=idf["dot_color"],
            opacity=0.85,
            line=dict(width=1, color="rgba(255,255,255,0.1)"),
        ),
        customdata=list(zip(idf["Event"], idf["_pct"], idf["_sev"])),
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            "%{customdata[0]}<br>"
            "Severity: %{customdata[2]}<br>"
            "Impact: %{customdata[1]:+.1f}%<extra></extra>"
        ),
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.1)")
    fig.update_layout(**base_layout(height=height, yaxis_title="30-day price impact (%)"))
    return fig


def normalized_comparison_chart(
    comp_df,
    events: pd.DataFrame,
    start_dt,
    end_dt,
    show_ev: bool = True,
    height: int = 420,
) -> go.Figure:
    """Multi-commodity normalized index chart."""
    fig = go.Figure()

    for com in comp_df["commodity_name"].unique():
        sub = comp_df[comp_df["commodity_name"] == com]
        m   = COMMODITY_META.get(com, {})
        fig.add_trace(go.Scatter(
            x=sub["date"],
            y=sub["norm"],
            customdata=list(zip(sub["close"], sub["norm"])),
            name=m.get("label", com),
            line=dict(color=m.get("color", "#888"), width=2),
            hovertemplate=(
                f"<b>%{{x|%d %b %Y}}</b><br>"
                f"{m.get('label', com)}: <b>${{customdata[0]:.2f}}</b>"
                f" ({m.get('unit_short', '')})<br>"
                f"Index: %{{customdata[1]:.1f}}<extra></extra>"
            ),
        ))

    fig.add_hline(
        y=100, line_dash="dash", line_color="rgba(255,255,255,0.08)",
        annotation_text="Baseline", annotation_font_size=9,
        annotation_font_color="#4b5570",
    )

    max_n = comp_df["norm"].max() if not comp_df.empty else 200
    fig.add_hrect(
        y0=130, y1=max_n * 1.02,
        fillcolor="rgba(239,68,68,0.04)", line_width=0,
        annotation_text="SYSTEMIC SHOCK ZONE (>130%)",
        annotation_font_size=8, annotation_font_color="#ef4444",
        annotation_position="top left",
    )

    if show_ev and events is not None:
        for _, e in events.iterrows():
            if start_dt <= e["date"] <= end_dt:
                c  = SEV_COLORS.get(e["severity"], "#888")
                dm = int(pd.Timestamp(e["date"]).timestamp() * 1000)
                txt = e["event"][:20] + ("…" if len(e["event"]) > 20 else "")
                fig.add_vline(
                    x=dm, line_dash="dot", line_color=c, line_width=1,
                    annotation_text=txt, annotation_position="top left",
                    annotation_font_size=7, annotation_font_color=c,
                )

    fig.update_layout(**base_layout(
        height=height,
        yaxis_title="Normalized index (100 = start)",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.01,
            font=dict(family="IBM Plex Mono", size=10, color=FONT_CLR),
            bgcolor="rgba(0,0,0,0)", title_text="",
        ),
    ))
    return fig


def volatility_ranking_bar(prices, height: int = 280) -> go.Figure:
    """Horizontal bar of current 30d volatility for all commodities."""
    import pandas as pd
    ld = prices["date"].max()
    lv = prices[prices["date"] == ld][["commodity_name", "volatility_30d"]].copy()
    lv = lv.sort_values("volatility_30d", ascending=True)
    lv["label"] = lv["commodity_name"].map(label_map).fillna(lv["commodity_name"])
    lv["color"] = lv["commodity_name"].map(color_map).fillna("#9ba3b5")

    fig = go.Figure(go.Bar(
        x=lv["volatility_30d"],
        y=lv["label"],
        orientation="h",
        marker_color=lv["color"].tolist(),
        text=[f"{v:.2f}" for v in lv["volatility_30d"]],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=11, color=FONT_CLR),
        hovertemplate="<b>%{y}</b><br>30d vol: %{x:.2f}<extra></extra>",
    ))
    fig.update_layout(**base_layout(
        height=height,
        xaxis_title="30-day Volatility",
        margin=dict(l=10, r=60, t=10, b=40),
        showlegend=False,
    ))
    return fig


def correlation_heatmap(comp_df, height: int = 320) -> go.Figure:
    """Pearson correlation heatmap of daily returns."""
    pivot = comp_df.pivot_table(index="date", columns="label", values="close")
    corr  = pivot.pct_change(fill_method=None).corr().round(2)

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale=[[0, "#0b0d11"], [0.4, "#1c2030"], [1, "#e25c2e"]],
        text=corr.values,
        texttemplate="%{text:.2f}",
        textfont=dict(family="IBM Plex Mono", size=11),
        hovertemplate="<b>%{x} vs %{y}</b><br>Correlation: %{z:.2f}<extra></extra>",
        zmin=-1, zmax=1,
    ))
    fig.update_layout(**base_layout(height=height, margin=dict(l=10, r=10, t=10, b=40)))
    return fig


def pipeline_bar(runs, height: int = 240) -> go.Figure:
    """Bar chart of rows loaded per pipeline run."""
    import pandas as pd
    r = runs.copy()
    r["started_at"] = pd.to_datetime(r["started_at"])
    r = r.sort_values("started_at")
    r["status_color"] = r["status"].map({"success": "#22c55e", "failed": "#ef4444", "running": "#f59e0b"})

    fig = go.Figure(go.Bar(
        x=r["started_at"].dt.strftime("%d %b %H:%M"),
        y=r["rows_loaded"],
        marker_color=r["status_color"].tolist(),
        text=r["rows_loaded"],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono", size=10, color=FONT_CLR),
        hovertemplate="<b>%{x}</b><br>Rows: %{y:,}<extra></extra>",
    ))
    fig.update_layout(**base_layout(height=height, yaxis_title="Rows loaded"))
    return fig