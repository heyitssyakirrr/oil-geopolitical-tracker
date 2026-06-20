"""
Reusable dashboard insight helpers.

These functions keep analytical logic out of Streamlit page files so the
dashboard can grow without turning each page into a mix of UI and business
rules.
"""

from __future__ import annotations

import pandas as pd


SEVERITY_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def latest_window(prices: pd.DataFrame, days: int = 30) -> pd.DataFrame:
    """Return the latest N-day price window from a price frame."""
    if prices.empty or "date" not in prices:
        return prices.copy()

    end_date = prices["date"].max()
    start_date = end_date - pd.Timedelta(days=days)
    return prices[prices["date"].between(start_date, end_date)].copy()


def commodity_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate period return and latest volatility for each commodity."""
    required = {"commodity_name", "date", "close"}
    if prices.empty or not required.issubset(prices.columns):
        return pd.DataFrame(
            columns=[
                "commodity_name",
                "start_price",
                "end_price",
                "return_pct",
                "volatility_30d",
            ]
        )

    rows = []
    for commodity, group in prices.groupby("commodity_name"):
        group = group.sort_values("date")
        if len(group) < 2:
            continue

        start_price = group.iloc[0]["close"]
        end_price = group.iloc[-1]["close"]
        if not start_price:
            continue

        latest_volatility = (
            group.iloc[-1].get("volatility_30d", 0)
            if "volatility_30d" in group.columns
            else 0
        )

        rows.append(
            {
                "commodity_name": commodity,
                "start_price": start_price,
                "end_price": end_price,
                "return_pct": (end_price - start_price) / start_price * 100,
                "volatility_30d": latest_volatility,
            }
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "commodity_name",
                "start_price",
                "end_price",
                "return_pct",
                "volatility_30d",
            ]
        )

    return pd.DataFrame(rows).sort_values("return_pct", ascending=False)


def recent_event_summary(events: pd.DataFrame, end_dt, days: int = 60) -> dict:
    """Summarize event risk in the selected lookback window."""
    if events.empty or "date" not in events or "severity" not in events:
        return {
            "count": 0,
            "critical": 0,
            "high": 0,
            "risk_score": 0.0,
        }

    end_ts = pd.to_datetime(end_dt)
    start_ts = end_ts - pd.Timedelta(days=days)
    recent = events[events["date"].between(start_ts, end_ts)].copy()
    if recent.empty:
        return {
            "count": 0,
            "critical": 0,
            "high": 0,
            "risk_score": 0.0,
        }

    recent["severity_score"] = recent["severity"].map(SEVERITY_SCORE).fillna(0)
    return {
        "count": len(recent),
        "critical": int((recent["severity"] == "critical").sum()),
        "high": int((recent["severity"] == "high").sum()),
        "risk_score": float(recent["severity_score"].mean()),
    }


def risk_label(score: float) -> tuple[str, str]:
    """Return display label and existing CSS alert class for a risk score."""
    if score >= 3.5:
        return "Severe", "alert-red"
    if score >= 2.5:
        return "Elevated", "alert-amber"
    if score >= 1.5:
        return "Moderate", "alert-blue"
    return "Calm", "alert-green"


def important_events(events: pd.DataFrame, start_dt, end_dt, limit: int = 8) -> pd.DataFrame:
    """Return the most important recent events for briefing tables."""
    if events.empty:
        return pd.DataFrame(columns=["date", "event", "severity"])

    window = events[events["date"].between(pd.to_datetime(start_dt), pd.to_datetime(end_dt))].copy()
    if window.empty:
        return pd.DataFrame(columns=["date", "event", "severity"])

    window["severity_score"] = window["severity"].map(SEVERITY_SCORE).fillna(0)
    return (
        window.sort_values(["severity_score", "date"], ascending=[False, False])
        .head(limit)
        .drop(columns=["severity_score"])
    )