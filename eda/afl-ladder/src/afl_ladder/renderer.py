from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import patches
from matplotlib.animation import FFMpegWriter

from afl_ladder.config import (
    TEAM_METADATA,
    THEME,
)


def get_rank_badge_color(rank: int) -> tuple[str, str]:
    """Return (background_color, text_color) for a ladder rank position."""
    if rank == 1:
        return "#FFD700", "#111111"  # 1st: Gold
    elif rank == 2:
        return "#D1D5DB", "#111111"  # 2nd: Silver
    elif rank == 3:
        return "#CD7F32", "#FFFFFF"  # 3rd: Bronze
    elif rank <= 4:
        return "#1F6FEB", "#FFFFFF"  # Top 4: Double Chance Blue
    elif rank <= 8:
        return "#238636", "#FFFFFF"  # Top 8: Finals Green
    else:
        return "#21262D", "#8B949E"  # 9-18: Non-finals Gray


def draw_frame_landscape(
    ax: plt.Axes,
    frame_df: pd.DataFrame,
    max_pts_limit: float,
    round_display: str,
    season_year: int = 2026,
):
    """Draw a single high-polish 16:9 landscape frame."""
    ax.clear()
    fig = ax.figure
    fig.texts.clear()
    ax.set_facecolor(THEME["background"])

    # X-axis limits & grid
    ax.set_xlim(-6.5, max_pts_limit)
    ax.set_ylim(-0.9, 18.2)

    # Gridlines
    ax.xaxis.grid(True, linestyle="--", alpha=0.15, color=THEME["grid_color"])
    ax.set_axisbelow(True)

    # Top 4 Qualifier boundary line (between rank 4 and 5 -> y=13.5)
    ax.axhline(
        y=13.5,
        color="#388BFD",
        linestyle=":",
        linewidth=1.2,
        alpha=0.6,
        xmin=0.08,
        xmax=0.98,
    )
    ax.text(
        max_pts_limit * 0.98,
        13.6,
        "TOP 4 • DOUBLE CHANCE",
        color="#58A6FF",
        fontsize=8.5,
        fontweight="bold",
        ha="right",
        va="bottom",
        alpha=0.75,
    )

    # Top 8 Finals Cutoff line (between rank 8 and 9 -> y=9.5)
    ax.axhline(
        y=9.5,
        color=THEME["finals_line"],
        linestyle="--",
        linewidth=1.8,
        alpha=0.85,
        xmin=0.08,
        xmax=0.98,
    )
    ax.text(
        max_pts_limit * 0.98,
        9.6,
        "TOP 8 • FINALS QUALIFIER CUTOFF",
        color=THEME["finals_label"],
        fontsize=9,
        fontweight="bold",
        ha="right",
        va="bottom",
        alpha=0.9,
    )

    sorted_frame = frame_df.sort_values("y_pos", ascending=True)

    for _, row in sorted_frame.iterrows():
        team_name = row["team"]
        y = float(row["y_pos"])
        pts = float(row["points"])
        pct = float(row["percentage"])
        pos = int(row["position"])
        delta = int(row["rank_delta"])
        played = int(row["played"])
        wins = int(row["wins"])
        losses = int(row["losses"])
        draws = int(row["draws"])

        meta = TEAM_METADATA.get(
            team_name,
            {
                "short_name": team_name,
                "primary_color": "#444444",
                "secondary_color": "#888888",
                "accent_color": "#FFFFFF",
                "text_color": "#FFFFFF",
            },
        )

        bar_height = 0.72

        # 1. Background bar track
        track_box = patches.FancyBboxPatch(
            (0, y - bar_height / 2),
            max_pts_limit * 0.96,
            bar_height,
            boxstyle="round,pad=0.0,rounding_size=0.15",
            facecolor="#12161F",
            edgecolor="#1E2330",
            linewidth=0.8,
            zorder=1,
        )
        ax.add_patch(track_box)

        # 2. Main Team Bar
        bar_width = max(pts, 0.4)
        bar_patch = patches.FancyBboxPatch(
            (0, y - bar_height / 2),
            bar_width,
            bar_height,
            boxstyle="round,pad=0.0,rounding_size=0.15",
            facecolor=meta["primary_color"],
            edgecolor=meta.get("accent_color", "#FFFFFF"),
            linewidth=0.8,
            zorder=2,
        )
        ax.add_patch(bar_patch)

        # 3. Left Brand Stripe
        stripe_width = min(0.6, bar_width)
        stripe_patch = patches.FancyBboxPatch(
            (0, y - bar_height / 2),
            stripe_width,
            bar_height,
            boxstyle="round,pad=0.0,rounding_size=0.12",
            facecolor=meta.get("secondary_color", "#FFFFFF"),
            edgecolor="none",
            zorder=3,
        )
        ax.add_patch(stripe_patch)

        # 4. Rank Badge
        bg_col, txt_col = get_rank_badge_color(pos)
        rank_circle = patches.Circle(
            (-4.8, y),
            radius=0.38,
            facecolor=bg_col,
            edgecolor="none",
            zorder=4,
        )
        ax.add_patch(rank_circle)
        ax.text(
            -4.8,
            y,
            str(pos),
            color=txt_col,
            fontsize=10,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )

        # 5. Rank Delta (Shift indicator)
        if delta > 0:
            delta_str = f"+{delta}"
            delta_col = "#3FB950"
        elif delta < 0:
            delta_str = f"{delta}"
            delta_col = "#F85149"
        else:
            delta_str = "—"
            delta_col = "#6E7681"

        ax.text(
            -3.7,
            y,
            delta_str,
            color=delta_col,
            fontsize=8.5,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )

        # 6. Team Name & Record Text
        record_str = f"({wins}-{losses}-{draws})" if played > 0 else "(0-0-0)"
        team_display = f"{meta.get('short_name', team_name)}"

        # Scale text threshold based on max_pts_limit
        in_bar_threshold = max_pts_limit * 0.16

        if pts >= in_bar_threshold:
            # Inside bar
            ax.text(
                1.2,
                y + 0.02,
                team_display,
                color="#FFFFFF",
                fontsize=10.5,
                fontweight="bold",
                ha="left",
                va="center",
                zorder=5,
            )
            ax.text(
                1.2 + len(team_display) * (max_pts_limit * 0.0055) + 0.6,
                y + 0.02,
                record_str,
                color="#D0D7DE",
                fontsize=8.5,
                ha="left",
                va="center",
                alpha=0.85,
                zorder=5,
            )
        else:
            # Outside bar
            ax.text(
                max(pts + 0.6, 1.2),
                y + 0.02,
                f"{team_display} {record_str}",
                color="#FFFFFF",
                fontsize=9.5,
                fontweight="bold",
                ha="left",
                va="center",
                zorder=5,
            )

        # 7. End of Bar Stats Label (Points & Percentage)
        stat_x = pts + 0.8
        min_stat_x = (
            in_bar_threshold + len(team_display) * (max_pts_limit * 0.0055) + 4.0
        )
        if pts < in_bar_threshold:
            stat_x = max(stat_x + len(team_display) * 0.5 + 4.0, min_stat_x)

        pts_label = f"{int(round(pts))} pts"
        pct_label = f"{pct:.1f}%"

        ax.text(
            stat_x,
            y + 0.02,
            pts_label,
            color="#FFFFFF",
            fontsize=10,
            fontweight="bold",
            ha="left",
            va="center",
            zorder=5,
        )
        ax.text(
            stat_x + max_pts_limit * 0.045,
            y + 0.02,
            pct_label,
            color="#8B949E",
            fontsize=8.5,
            ha="left",
            va="center",
            zorder=5,
        )

    # 8. Axes Styling
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#30363D")
    ax.spines["bottom"].set_linewidth(1.2)

    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.tick_params(axis="x", colors="#8B949E", labelsize=9)
    ax.set_xlabel("Premiership Points", color="#8B949E", fontsize=10, labelpad=8)

    # Header Card
    fig = ax.figure
    fig.text(
        0.08,
        0.955,
        f"AFL {season_year} PREMIERSHIP LADDER",
        color="#F0F6FC",
        fontsize=18,
        fontweight="bold",
        ha="left",
        va="top",
    )
    fig.text(
        0.08,
        0.92,
        "Official Standings • Finals Race",
        color="#8B949E",
        fontsize=10,
        ha="left",
        va="top",
    )

    # Current Round Banner
    fig.text(
        0.92,
        0.955,
        round_display.upper(),
        color="#FFD200",
        fontsize=18,
        fontweight="bold",
        ha="right",
        va="top",
    )

    # Leader callout
    top_team = frame_df.sort_values("y_pos", ascending=False).iloc[0]
    leader_name = top_team["team"]
    leader_pts = int(round(top_team["points"]))
    fig.text(
        0.92,
        0.92,
        f"Ladder Leader: {leader_name} ({leader_pts} pts)",
        color="#58A6FF",
        fontsize=10,
        ha="right",
        va="top",
    )

    # Footer
    fig.text(
        0.08,
        0.025,
        "Source: footyforecaster.com | Managed with uv",
        color="#484F58",
        fontsize=8.5,
        ha="left",
        va="bottom",
    )
    fig.text(
        0.92,
        0.025,
        "Sort Order: 1. Points  2. Percentage (%)",
        color="#484F58",
        fontsize=8.5,
        ha="right",
        va="bottom",
    )


def draw_frame_portrait(
    ax: plt.Axes,
    frame_df: pd.DataFrame,
    max_pts_limit: float,
    round_display: str,
    season_year: int = 2026,
):
    """Draw a single 9:16 portrait frame optimized for mobile/Shorts."""
    ax.clear()
    fig = ax.figure
    fig.texts.clear()
    ax.set_facecolor(THEME["background"])

    ax.set_xlim(-5.0, max_pts_limit)
    ax.set_ylim(-0.9, 18.2)

    ax.xaxis.grid(True, linestyle="--", alpha=0.15, color=THEME["grid_color"])
    ax.set_axisbelow(True)

    # Top 8 Cutoff
    ax.axhline(
        y=9.5, color=THEME["finals_line"], linestyle="--", linewidth=1.5, alpha=0.85
    )

    sorted_frame = frame_df.sort_values("y_pos", ascending=True)

    for _, row in sorted_frame.iterrows():
        team_name = row["team"]
        y = float(row["y_pos"])
        pts = float(row["points"])
        pct = float(row["percentage"])
        pos = int(row["position"])
        delta = int(row["rank_delta"])

        meta = TEAM_METADATA.get(
            team_name,
            {
                "short_name": team_name,
                "primary_color": "#444444",
                "secondary_color": "#888888",
                "accent_color": "#FFFFFF",
            },
        )

        bar_height = 0.72
        bar_width = max(pts, 0.4)

        # Track
        ax.add_patch(
            patches.FancyBboxPatch(
                (0, y - bar_height / 2),
                max_pts_limit * 0.95,
                bar_height,
                boxstyle="round,pad=0.0,rounding_size=0.15",
                facecolor="#12161F",
                edgecolor="#1E2330",
                linewidth=0.8,
                zorder=1,
            )
        )

        # Main Bar
        ax.add_patch(
            patches.FancyBboxPatch(
                (0, y - bar_height / 2),
                bar_width,
                bar_height,
                boxstyle="round,pad=0.0,rounding_size=0.15",
                facecolor=meta["primary_color"],
                edgecolor=meta.get("accent_color", "#FFFFFF"),
                linewidth=0.8,
                zorder=2,
            )
        )

        # Rank badge
        bg_col, txt_col = get_rank_badge_color(pos)
        ax.add_patch(
            patches.Circle(
                (-3.8, y), radius=0.42, facecolor=bg_col, edgecolor="none", zorder=4
            )
        )
        ax.text(
            -3.8,
            y,
            str(pos),
            color=txt_col,
            fontsize=10,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )

        # Team name
        team_short = meta.get("code", meta.get("short_name", team_name)[:3].upper())
        ax.text(
            -2.0,
            y,
            team_short,
            color="#FFFFFF",
            fontsize=9.5,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=5,
        )

        # Stats
        pts_label = f"{int(round(pts))}p"
        pct_label = f"{pct:.0f}%"
        ax.text(
            max(pts + 0.6, 1.0),
            y,
            f"{pts_label} ({pct_label})",
            color="#FFFFFF",
            fontsize=9,
            fontweight="bold",
            ha="left",
            va="center",
            zorder=5,
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#30363D")
    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.tick_params(axis="x", colors="#8B949E", labelsize=8)

    fig = ax.figure
    fig.text(
        0.5,
        0.965,
        f"AFL {season_year} LADDER RACE",
        color="#F0F6FC",
        fontsize=16,
        fontweight="bold",
        ha="center",
        va="top",
    )
    fig.text(
        0.5,
        0.935,
        round_display.upper(),
        color="#FFD200",
        fontsize=14,
        fontweight="bold",
        ha="center",
        va="top",
    )


def render_preview_image(
    frame_df: pd.DataFrame,
    output_path: Path,
    orientation: str = "landscape",
    dynamic_scale: bool = True,
    season_year: int = 2026,
    dpi: int = 100,
):
    """Render a single frame as a PNG image for preview."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    round_display = frame_df["round_display"].iloc[0]

    if dynamic_scale:
        curr_max = frame_df["points"].max()
        max_pts = max(16.0, curr_max * 1.18)
    else:
        max_pts = 85.0

    if orientation == "portrait":
        fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=dpi)
        fig.patch.set_facecolor(THEME["background"])
        fig.subplots_adjust(left=0.08, right=0.94, top=0.91, bottom=0.06)
        draw_frame_portrait(ax, frame_df, max_pts, round_display, season_year)
    else:
        fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=dpi)
        fig.patch.set_facecolor(THEME["background"])
        fig.subplots_adjust(left=0.08, right=0.94, top=0.88, bottom=0.08)
        draw_frame_landscape(ax, frame_df, max_pts, round_display, season_year)

    plt.savefig(output_path, facecolor=THEME["background"], edgecolor="none")
    plt.close(fig)


def render_race_video(
    frames: list[pd.DataFrame],
    output_path: Path,
    fps: int = 30,
    orientation: str = "landscape",
    dynamic_scale: bool = True,
    season_year: int = 2026,
    dpi: int = 100,
    progress_callback: Callable[[int, int], None] | None = None,
):
    """Render the full sequence of interpolated frames into an MP4 video."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if orientation == "portrait":
        fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=dpi)
        fig.subplots_adjust(left=0.08, right=0.94, top=0.91, bottom=0.06)
        draw_fn = draw_frame_portrait
    else:
        fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=dpi)
        fig.subplots_adjust(left=0.08, right=0.94, top=0.88, bottom=0.08)
        draw_fn = draw_frame_landscape

    fig.patch.set_facecolor(THEME["background"])
    total_frames = len(frames)

    global_max_pts = max(frame["points"].max() for frame in frames)
    fixed_max_limit = max(global_max_pts * 1.15, 20.0)

    writer = FFMpegWriter(
        fps=fps,
        codec="libx264",
        extra_args=["-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p"],
    )

    with writer.saving(fig, str(output_path), dpi=dpi):
        for idx, frame_df in enumerate(frames):
            round_display = frame_df["round_display"].iloc[0]

            if dynamic_scale:
                curr_max = frame_df["points"].max()
                max_pts = max(16.0, curr_max * 1.18)
            else:
                max_pts = fixed_max_limit

            draw_fn(ax, frame_df, max_pts, round_display, season_year)
            writer.grab_frame()

            if progress_callback:
                progress_callback(idx + 1, total_frames)

    plt.close(fig)
