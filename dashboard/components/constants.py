"""
Shared constants: commodity metadata, colour maps, chart defaults.
Import from here instead of re-defining in every page module.
"""

COMMODITY_META = {
    "brent_crude": {
        "label": "Brent Crude",
        "unit": "USD / barrel (159 L)",
        "unit_short": "bbl",
        "icon": "🛢️",
        "color": "#e25c2e",
        "why": "Global oil benchmark, priced per barrel (159 litres). Sets baseline for petrol prices worldwide.",
        "war_signal": "Supply shock indicator — rises when Middle East or Russian supply is threatened.",
    },
    "wti_crude": {
        "label": "WTI Crude",
        "unit": "USD / barrel (159 L)",
        "unit_short": "bbl",
        "icon": "⛽",
        "color": "#f59e0b",
        "why": "US domestic benchmark. Usually $2–5 below Brent. Gap widening = US shielded from global shock.",
        "war_signal": "US energy independence gauge — smaller spike vs. Brent means US is shielded.",
    },
    "natural_gas": {
        "label": "Natural Gas",
        "unit": "USD / MMBtu",
        "unit_short": "MMBtu",
        "icon": "🔥",
        "color": "#3b82f6",
        "why": "Russia weaponised gas supply in 2021–22. Priced per million BTU.",
        "war_signal": "Energy weaponisation indicator — Russia used gas as political leverage.",
    },
    "gold": {
        "label": "Gold",
        "unit": "USD / troy oz (31g)",
        "unit_short": "oz",
        "icon": "🥇",
        "color": "#eab308",
        "why": "Safe-haven asset. Rising gold = rising fear. Investors flee to it during war and economic collapse.",
        "war_signal": "Fear & flight-to-safety indicator — gold and oil rising together = prolonged conflict priced in.",
    },
    "wheat": {
        "label": "Wheat",
        "unit": "USD / bushel (27 kg)",
        "unit_short": "bu",
        "icon": "🌾",
        "color": "#84cc16",
        "why": "Russia + Ukraine = ~30% of global wheat exports. 2022 invasion spiked wheat 60%+ in weeks.",
        "war_signal": "Food security crisis indicator — wheat spikes signal disrupted agricultural supply chains.",
    },
}

SEV_COLORS = {
    "critical": "#ef4444",
    "high": "#f59e0b",
    "medium": "#3b82f6",
    "low": "#22c55e",
}

PAGES = [
    ("🏠", "Overview"),
    ("📈", "Price Analysis"),
    ("💥", "Event Intelligence"),
    ("📊", "Commodity Comparison"),
    ("🔧", "Pipeline"),
]

# Chart theme
PLOT_BG  = "rgba(0,0,0,0)"
GRID_CLR = "rgba(255,255,255,0.04)"
FONT_CLR = "#9ba3b5"

# Derived maps (computed once here, imported everywhere)
label_map = {k: v["label"] for k, v in COMMODITY_META.items()}
color_map = {k: v["color"] for k, v in COMMODITY_META.items()}