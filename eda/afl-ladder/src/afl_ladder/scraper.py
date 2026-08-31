import time
from typing import Any

import httpx
import pandas as pd
from bs4 import BeautifulSoup

from afl_ladder.config import (
    DATA_PROCESSED_DIR,
    DATA_RAW_DIR,
    ROUND_NAMES,
    SEASON_YEAR,
    TEAM_NAME_MAP,
)


def fetch_round_html(
    round_name: str,
    year: int = SEASON_YEAR,
    force: bool = False,
    client: httpx.Client | None = None,
) -> str:
    """Fetch raw HTML for a specific round ladder with local disk caching."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = DATA_RAW_DIR / f"{year}_{round_name}.html"

    if cache_path.exists() and not force:
        return cache_path.read_text(encoding="utf-8")

    url = f"https://footyforecaster.com/AFL/Ladder/{year}_{round_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    if client:
        resp = client.get(url, headers=headers, follow_redirects=True)
    else:
        with httpx.Client() as c:
            resp = c.get(url, headers=headers, follow_redirects=True)

    resp.raise_for_status()
    html = resp.text
    cache_path.write_text(html, encoding="utf-8")
    return html


def parse_ladder_html(
    html: str,
    round_name: str,
    round_index: int,
) -> list[dict[str, Any]]:
    """Parse ladder table from FootyForecaster HTML."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="bigpadding")
    if not table:
        raise ValueError(f"Could not find ladder table in HTML for {round_name}")

    tbody = table.find("tbody") or table
    rows = tbody.find_all("tr")
    records = []

    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cols or len(cols) < 10:
            continue

        # Header or invalid row check
        if cols[0].lower() in ("position", "pos", ""):
            continue

        try:
            position = int(cols[0])
            raw_team = cols[1]
            played = int(cols[2])
            wins = int(cols[3])
            draws = int(cols[4])
            losses = int(cols[5])
            pts_for = int(cols[6])
            pts_agst = int(cols[7])
            percentage = float(cols[8].replace("%", "").strip())
            points = int(cols[9])

            canonical_team = TEAM_NAME_MAP.get(raw_team, raw_team)

            records.append(
                {
                    "round_index": round_index,
                    "round_name": round_name,
                    "position": position,
                    "raw_team": raw_team,
                    "team": canonical_team,
                    "played": played,
                    "wins": wins,
                    "draws": draws,
                    "losses": losses,
                    "points_for": pts_for,
                    "points_against": pts_agst,
                    "percentage": percentage,
                    "points": points,
                }
            )
        except (ValueError, IndexError):
            continue

    return records


def scrape_season_ladders(
    year: int = SEASON_YEAR,
    force: bool = False,
    delay_sec: float = 0.2,
) -> pd.DataFrame:
    """Scrape and compile ladder data across all rounds for a given season."""
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    all_records: list[dict[str, Any]] = []

    with httpx.Client() as client:
        for idx, round_name in enumerate(ROUND_NAMES):
            try:
                html = fetch_round_html(
                    round_name, year=year, force=force, client=client
                )
                records = parse_ladder_html(
                    html, round_name=round_name, round_index=idx
                )
                all_records.extend(records)
                time.sleep(delay_sec)
            except Exception as e:
                print(f"Warning: Failed to fetch/parse {round_name}: {e}")

    df = pd.DataFrame(all_records)
    output_path = DATA_PROCESSED_DIR / f"ladder_{year}.csv"
    df.to_csv(output_path, index=False)
    return df
