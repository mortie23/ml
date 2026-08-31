from pathlib import Path
from typing import Dict, Any

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"

# Season Config
SEASON_YEAR = 2026
ROUND_NAMES = ["Opening_Round"] + [f"Round_{i}" for i in range(1, 25)]

ROUND_DISPLAY_NAMES = {
    "Opening_Round": "Opening Round",
    **{f"Round_{i}": f"Round {i}" for i in range(1, 25)},
}

# Footyforecaster Name to Standard Name Mapping
TEAM_NAME_MAP = {
    "Adelaide": "Adelaide",
    "Brisbane": "Brisbane Lions",
    "Carlton": "Carlton",
    "Collingwood": "Collingwood",
    "Essendon": "Essendon",
    "Fremantle": "Fremantle",
    "GW Sydney": "GWS Giants",
    "Geelong": "Geelong Cats",
    "Gold Coast": "Gold Coast Suns",
    "Hawthorn": "Hawthorn",
    "Melbourne": "Melbourne",
    "Nth Melbourne": "North Melbourne",
    "Port Adelaide": "Port Adelaide",
    "Richmond": "Richmond",
    "St Kilda": "St Kilda",
    "Sydney": "Sydney Swans",
    "West Coast": "West Coast Eagles",
    "Wstn Bulldogs": "Western Bulldogs",
}

# AFL Team Branding & Colors
TEAM_METADATA: Dict[str, Dict[str, Any]] = {
    "Adelaide": {
        "short_name": "Adelaide",
        "code": "ADE",
        "primary_color": "#002B5C",     # Navy
        "secondary_color": "#E21E31",   # Red
        "accent_color": "#FFD200",      # Gold
        "text_color": "#FFFFFF",
    },
    "Brisbane Lions": {
        "short_name": "Brisbane",
        "code": "BRL",
        "primary_color": "#7A003C",     # Maroon
        "secondary_color": "#FDBE11",   # Gold
        "accent_color": "#0055A5",      # Blue
        "text_color": "#FFFFFF",
    },
    "Carlton": {
        "short_name": "Carlton",
        "code": "CAR",
        "primary_color": "#0E1E2D",     # Navy
        "secondary_color": "#FFFFFF",   # White
        "accent_color": "#0091DA",      # Cyan highlight
        "text_color": "#FFFFFF",
    },
    "Collingwood": {
        "short_name": "Collingwood",
        "code": "COL",
        "primary_color": "#111111",     # Black
        "secondary_color": "#FFFFFF",   # White
        "accent_color": "#9E9E9E",      # Silver
        "text_color": "#FFFFFF",
    },
    "Essendon": {
        "short_name": "Essendon",
        "code": "ESS",
        "primary_color": "#CC2031",     # Red
        "secondary_color": "#1A1A1A",   # Black
        "accent_color": "#E53935",      # Bright Red
        "text_color": "#FFFFFF",
    },
    "Fremantle": {
        "short_name": "Fremantle",
        "code": "FRE",
        "primary_color": "#2A1A5E",     # Purple
        "secondary_color": "#FFFFFF",   # White
        "accent_color": "#9C27B0",      # Lavender
        "text_color": "#FFFFFF",
    },
    "GWS Giants": {
        "short_name": "GWS Giants",
        "code": "GWS",
        "primary_color": "#F15C22",     # Orange
        "secondary_color": "#373A36",   # Charcoal
        "accent_color": "#FFFFFF",      # White
        "text_color": "#FFFFFF",
    },
    "Geelong Cats": {
        "short_name": "Geelong",
        "code": "GEE",
        "primary_color": "#001C58",     # Navy
        "secondary_color": "#FFFFFF",   # White
        "accent_color": "#4A90E2",      # Blue accent
        "text_color": "#FFFFFF",
    },
    "Gold Coast Suns": {
        "short_name": "Gold Coast",
        "code": "GCS",
        "primary_color": "#E11B22",     # Red
        "secondary_color": "#FFDE00",   # Gold
        "accent_color": "#007AC2",      # Sky Blue
        "text_color": "#FFFFFF",
    },
    "Hawthorn": {
        "short_name": "Hawthorn",
        "code": "HAW",
        "primary_color": "#4D2004",     # Brown
        "secondary_color": "#FBB814",   # Gold
        "accent_color": "#FDB813",      # Yellow
        "text_color": "#FFFFFF",
    },
    "Melbourne": {
        "short_name": "Melbourne",
        "code": "MEL",
        "primary_color": "#0F192D",     # Navy
        "secondary_color": "#CC2031",   # Red
        "accent_color": "#E53935",      # Bright Red
        "text_color": "#FFFFFF",
    },
    "North Melbourne": {
        "short_name": "Nth Melbourne",
        "code": "NM",
        "primary_color": "#003B7B",     # Royal Blue
        "secondary_color": "#FFFFFF",   # White
        "accent_color": "#4FC3F7",      # Light Blue
        "text_color": "#FFFFFF",
    },
    "Port Adelaide": {
        "short_name": "Port Adelaide",
        "code": "PA",
        "primary_color": "#008A97",     # Teal
        "secondary_color": "#111111",   # Black
        "accent_color": "#FFFFFF",      # White
        "text_color": "#FFFFFF",
    },
    "Richmond": {
        "short_name": "Richmond",
        "code": "RIC",
        "primary_color": "#111111",     # Black
        "secondary_color": "#FED100",   # Yellow
        "accent_color": "#FFEB3B",      # Bright Yellow
        "text_color": "#FFFFFF",
    },
    "St Kilda": {
        "short_name": "St Kilda",
        "code": "STK",
        "primary_color": "#ED1B2F",     # Red
        "secondary_color": "#111111",   # Black
        "accent_color": "#FFFFFF",      # White
        "text_color": "#FFFFFF",
    },
    "Sydney Swans": {
        "short_name": "Sydney",
        "code": "SYD",
        "primary_color": "#ED171F",     # Blood Red
        "secondary_color": "#FFFFFF",   # White
        "accent_color": "#FFCDD2",      # Light Red
        "text_color": "#FFFFFF",
    },
    "West Coast Eagles": {
        "short_name": "West Coast",
        "code": "WCE",
        "primary_color": "#002C88",     # Royal Blue
        "secondary_color": "#F2A900",   # Gold
        "accent_color": "#FFC72C",      # Yellow
        "text_color": "#FFFFFF",
    },
    "Western Bulldogs": {
        "short_name": "Western Bulldogs",
        "code": "WB",
        "primary_color": "#014896",     # Royal Blue
        "secondary_color": "#C7012F",   # Red
        "accent_color": "#FFFFFF",      # White
        "text_color": "#FFFFFF",
    },
}

# Theme Colors for Broadcast Styling
THEME = {
    "background": "#0B0E14",         # Very deep slate/obsidian
    "card_bg": "#151922",            # Card container
    "text_main": "#F0F6FC",          # High-contrast white
    "text_muted": "#8B949E",         # Soft gray
    "grid_color": "#1F2430",         # Grid line
    "finals_line": "#238636",        # Finals threshold divider
    "finals_label": "#3FB950",       # Finals qualifier label
    "accent_gold": "#E3B341",        # Champion gold
    "bar_edge": "#30363D",           # Border for bars
}
