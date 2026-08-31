# AFL 2026 Ladder Bar Chart Race

A modern, high-polish Python tool for generating dynamic bar chart race videos of AFL premiership ladder standings across the 2026 season. Built with **Matplotlib**, **FFmpeg**, and managed with **`uv`**.

---

## ✨ Features

- **Automated Scraping & Caching**: Scrapes round-by-round ladder data (Opening Round through Round 24) from FootyForecaster with local disk caching to prevent unnecessary network requests.
- **Smooth Easing & Transitions**: Cubic / Cosine interpolation for seamless bar movement when teams swap ladder positions.
- **Official AFL Club Branding**: Accurate club primary, secondary, and accent colors for all 18 clubs.
- **Broadcast-Style Visuals**:
  - Dark sleek broadcast HUD theme.
  - Ranked position badges (#1 Gold, #2 Silver, #3 Bronze, Top 4 Blue, Top 8 Green).
  - Prominent **Top 8 Finals Qualifier Cutoff** and **Top 4 Double Chance** boundary lines.
  - Team records `(W-L-D)`, ladder points, and percentage indicators.
  - Rank shift indicators ($\uparrow +2$, $\downarrow -1$, $-$).
  - Dynamic x-axis scaling that naturally expands as the season advances.
- **Aspect Ratio Support**:
  - **16:9 Landscape** (`1920x1080`) for YouTube and desktop viewing.
  - **9:16 Portrait** (`1080x1920`) for Instagram Reels, YouTube Shorts, and TikTok.

---

## 🚀 Quickstart

### 1. Requirements
Ensure you have `uv` and `ffmpeg` installed:
```bash
# On Linux / macOS
which uv ffmpeg
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Generate Video in One Command
```bash
uv run afl-ladder all
```
The rendered video will be saved to `output/afl_2026_ladder_race_landscape.mp4`.

---

## 🛠️ CLI Commands

### 1. Scrape Ladder Data
Scrape all 2026 rounds into `data/processed/ladder_2026.csv`:
```bash
uv run afl-ladder scrape
```
Use `--force` / `-f` to bypass local HTML cache and re-download fresh tables.

### 2. Generate a Preview Image
Quickly generate a single static frame to inspect visual styling:
```bash
# Preview Round 24 in Landscape (16:9)
uv run afl-ladder preview --round 24 --orientation landscape

# Preview Round 4 in Portrait (9:16)
uv run afl-ladder preview --round 4 --orientation portrait
```

### 3. Render Animation Video
Render the full sequence with customizable options:
```bash
# Standard 16:9 Landscape video (30 FPS)
uv run afl-ladder render --orientation landscape --fps 30

# 9:16 Portrait for Shorts / TikTok
uv run afl-ladder render --orientation portrait --fps 30 --output output/afl_2026_ladder_shorts.mp4

# High Frame Rate 60 FPS
uv run afl-ladder render --fps 60 --steps 30
```

#### Render Options:
| Option | Default | Description |
| :--- | :--- | :--- |
| `--year` | `2026` | Season year |
| `--fps` | `30` | Output video frames per second |
| `--steps` | `24` | Number of interpolation frames per round |
| `--hold-start` | `30` | Hold frames on Opening Round (e.g. 1s at 30fps) |
| `--hold-end` | `90` | Hold frames on the final ladder (e.g. 3s at 30fps) |
| `--orientation` | `landscape` | Video orientation (`landscape` or `portrait`) |
| `--dynamic-scale / --fixed-scale` | `True` | Smoothly expand points axis as season advances |
| `--output` | `output/...` | Output file path (`.mp4`) |

---

## 📁 Project Structure

```text
afl-ladder/
├── data/
│   ├── raw/                  # Cached raw HTML files per round
│   └── processed/            # Compiled ladder CSV datasets
├── output/                   # Rendered MP4 videos and preview PNGs
├── src/
│   └── afl_ladder/
│       ├── __init__.py       # Package entrypoint
│       ├── cli.py            # Typer & Rich CLI interface
│       ├── config.py         # AFL club metadata, colors, and theme styling
│       ├── processor.py      # Easing, interpolation & rank calculations
│       ├── renderer.py       # Matplotlib & FFmpeg rendering pipeline
│       └── scraper.py        # FootyForecaster scraping & parser
├── pyproject.toml            # uv project configuration
└── README.md
```
