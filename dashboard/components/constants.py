"""
Shared constants: commodity metadata, colour maps, category definitions.
Single source of truth — import from here in every module.
"""

# ---------------------------------------------------------------------------
# Category definitions — controls page routing and colour coding
# ---------------------------------------------------------------------------
CATEGORIES = {
    "energy":      {"label": "Energy",      "icon": "⚡", "color": "#e25c2e", "accent": "#ff8a4c"},
    "agriculture": {"label": "Agriculture", "icon": "🌾", "color": "#84cc16", "accent": "#a3e635"},
    "livestock":   {"label": "Livestock",   "icon": "🐄", "color": "#f59e0b", "accent": "#fbbf24"},
    "macro":       {"label": "Macro",       "icon": "📊", "color": "#a78bfa", "accent": "#c4b5fd"},
}

# ---------------------------------------------------------------------------
# Per-commodity metadata
# ---------------------------------------------------------------------------
COMMODITY_META = {
    # ── ENERGY ──────────────────────────────────────────────────────────────
    "brent_crude": {
        "label": "Brent Crude",
        "category": "energy",
        "unit": "USD / barrel (159 L)",
        "unit_short": "bbl",
        "icon": "🛢️",
        "color": "#e25c2e",
        "why": "Global oil benchmark. Sets the baseline for petrol prices worldwide.",
        "war_signal": "Supply shock indicator — spikes on Middle East or Russian supply threats.",
        "ripple": ["heating_oil", "corn", "wheat", "live_cattle", "feeder_cattle", "lean_hogs"],
    },
    "wti_crude": {
        "label": "WTI Crude",
        "category": "energy",
        "unit": "USD / barrel (159 L)",
        "unit_short": "bbl",
        "icon": "⛽",
        "color": "#f97316",
        "why": "US domestic benchmark. Usually $2–5 cheaper than Brent.",
        "war_signal": "US energy independence gauge — smaller spike vs Brent = US is shielded.",
        "ripple": ["heating_oil", "corn"],
    },
    "natural_gas": {
        "label": "Natural Gas",
        "category": "energy",
        "unit": "USD / MMBtu",
        "unit_short": "MMBtu",
        "icon": "🔥",
        "color": "#3b82f6",
        "why": "Russia weaponised gas supply in 2021–22.",
        "war_signal": "Energy weaponisation indicator — used as direct political leverage.",
        "ripple": ["wheat", "corn", "soybeans"],
    },
    "heating_oil": {
        "label": "Heating Oil",
        "category": "energy",
        "unit": "USD / gallon",
        "unit_short": "gal",
        "icon": "🚢",
        "color": "#ef4444",
        "why": "Direct diesel proxy — the cost of moving everything: trucks, ships, farms.",
        "war_signal": "Transport cost transmission — when this rises, all food prices follow within 30–60 days.",
        "ripple": ["wheat", "corn", "soybeans", "sugar", "live_cattle", "feeder_cattle", "lean_hogs"],
    },
    # ── AGRICULTURE ─────────────────────────────────────────────────────────
    "wheat": {
        "label": "Wheat",
        "category": "agriculture",
        "unit": "USD / bushel (27 kg)",
        "unit_short": "bu",
        "icon": "🌾",
        "color": "#84cc16",
        "why": "Russia + Ukraine = ~30% of global exports. 2022 invasion spiked wheat 60%+.",
        "war_signal": "Food security crisis indicator — disrupted agricultural supply chains.",
        "ripple": ["live_cattle", "feeder_cattle", "lean_hogs"],
    },
    "corn": {
        "label": "Corn",
        "category": "agriculture",
        "unit": "USD / bushel (25 kg)",
        "unit_short": "bu",
        "icon": "🌽",
        "color": "#eab308",
        "why": "Primary animal feed AND biofuel input. Directly links energy prices to livestock costs.",
        "war_signal": "Livestock feed cost amplifier — corn price rises before cattle prices do.",
        "ripple": ["live_cattle", "feeder_cattle", "lean_hogs"],
    },
    "soybeans": {
        "label": "Soybeans",
        "category": "agriculture",
        "unit": "USD / bushel (27 kg)",
        "unit_short": "bu",
        "icon": "🫘",
        "color": "#a3e635",
        "why": "Global protein source and animal feed. Brazil + US = 80% of world supply.",
        "war_signal": "Supply chain disruption signal — drought, trade wars, and transport costs all hit here.",
        "ripple": ["live_cattle", "feeder_cattle", "lean_hogs"],
    },
    "sugar": {
        "label": "Sugar",
        "category": "agriculture",
        "unit": "USD / pound",
        "unit_short": "lb",
        "icon": "🍬",
        "color": "#f0abfc",
        "why": "Energy policy linkage — Brazil diverts cane to ethanol when oil is high.",
        "war_signal": "Biofuel substitution signal — rising oil often pulls sugar up as ethanol demand rises.",
        "ripple": ["corn"],
    },
    # ── LIVESTOCK ───────────────────────────────────────────────────────────
    "live_cattle": {
        "label": "Live Cattle",
        "category": "livestock",
        "unit": "USD / hundredweight (100 lbs)",
        "unit_short": "cwt",
        "icon": "🐄",
        "color": "#f59e0b",
        "why": "Finished cattle ready for slaughter. End-consumer beef price indicator.",
        "war_signal": "Consumer food cost gauge — reflects accumulated input cost shocks from energy and grain.",
        "ripple": [],
    },
    "feeder_cattle": {
        "label": "Feeder Cattle",
        "category": "livestock",
        "unit": "USD / hundredweight (100 lbs)",
        "unit_short": "cwt",
        "icon": "🐂",
        "color": "#d97706",
        "why": "Young cattle entering feedlots. Corn price is the primary cost driver.",
        "war_signal": "Feed cost transmission — corn spikes hit feeder cattle before live cattle.",
        "ripple": ["live_cattle"],
    },
    "lean_hogs": {
        "label": "Lean Hogs",
        "category": "livestock",
        "unit": "USD / hundredweight (100 lbs)",
        "unit_short": "cwt",
        "icon": "🐷",
        "color": "#fb923c",
        "why": "Pork pricing benchmark. Hogs convert grain to protein faster than cattle.",
        "war_signal": "Fast-response food cost signal — grain price impacts show up in hogs within weeks.",
        "ripple": [],
    },
    # ── MACRO ────────────────────────────────────────────────────────────────
    "gold": {
        "label": "Gold",
        "category": "macro",
        "unit": "USD / troy oz (31 g)",
        "unit_short": "oz",
        "icon": "🥇",
        "color": "#eab308",
        "why": "Safe-haven asset. Rising gold = rising fear. Investors flee here during crisis.",
        "war_signal": "Fear & flight-to-safety — gold + oil rising together = prolonged conflict priced in.",
        "ripple": [],
    },
    "copper": {
        "label": "Copper",
        "category": "macro",
        "unit": "USD / pound",
        "unit_short": "lb",
        "icon": "🔩",
        "color": "#a78bfa",
        "why": "'Dr. Copper' — the most reliable leading indicator of global economic health.",
        "war_signal": "Economic activity gauge — copper falls before recessions and rises before recoveries.",
        "ripple": [],
    },
}

# ---------------------------------------------------------------------------
# Severity colour mapping
# ---------------------------------------------------------------------------
SEV_COLORS = {
    "critical": "#ef4444",
    "high":     "#f59e0b",
    "medium":   "#3b82f6",
    "low":      "#22c55e",
}

# ---------------------------------------------------------------------------
# Page navigation
# ---------------------------------------------------------------------------
PAGES = [
    ("🏠",  "Overview"),
    ("⚡",  "Energy"),
    ("🌾",  "Agriculture"),
    ("🐄",  "Livestock"),
    ("📊",  "Macro"),
    ("🔗",  "Ripple Effects"),
    ("🔧",  "Pipeline"),
]

# ---------------------------------------------------------------------------
# Chart theme
# ---------------------------------------------------------------------------
PLOT_BG  = "rgba(0,0,0,0)"
GRID_CLR = "rgba(255,255,255,0.04)"
FONT_CLR = "#b8c4d8"

# ---------------------------------------------------------------------------
# Derived lookup maps (computed once, imported everywhere)
# ---------------------------------------------------------------------------
label_map    = {k: v["label"]    for k, v in COMMODITY_META.items()}
color_map    = {k: v["color"]    for k, v in COMMODITY_META.items()}
category_map = {k: v["category"] for k, v in COMMODITY_META.items()}

# Commodities grouped by category
CATEGORY_COMMODITIES = {}
for com, meta in COMMODITY_META.items():
    cat = meta["category"]
    CATEGORY_COMMODITIES.setdefault(cat, []).append(com)