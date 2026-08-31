import numpy as np
import pandas as pd

from afl_ladder.config import ROUND_DISPLAY_NAMES, TEAM_METADATA


def smooth_step(t: np.ndarray) -> np.ndarray:
    """Cubic smoothstep easing function: 3t^2 - 2t^3 for smooth transitions."""
    return t * t * (3.0 - 2.0 * t)


def cosine_ease(t: np.ndarray) -> np.ndarray:
    """Cosine easing: 0.5 * (1 - cos(pi * t)) for ultra-smooth easing."""
    return 0.5 * (1.0 - np.cos(np.pi * t))


def prepare_ladder_time_series(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure standard types, calculate round progression and rank shifts."""
    df = df.copy()
    df["round_display"] = (
        df["round_name"].map(ROUND_DISPLAY_NAMES).fillna(df["round_name"])
    )

    # Calculate rank delta per team between rounds
    df = df.sort_values(["round_index", "position"]).reset_index(drop=True)

    # Previous position
    prev_pos = {}
    rank_deltas = []

    for _, row in df.iterrows():
        team = row["team"]
        curr_pos = row["position"]
        if team in prev_pos:
            delta = (
                prev_pos[team] - curr_pos
            )  # Positive means moved up (e.g. 5 -> 3 is +2)
        else:
            delta = 0
        rank_deltas.append(delta)
        prev_pos[team] = curr_pos

    df["rank_delta"] = rank_deltas
    return df


def generate_race_frames(
    df: pd.DataFrame,
    steps_per_round: int = 24,
    hold_start_frames: int = 30,
    hold_end_frames: int = 90,
    easing: str = "cosine",
) -> list[pd.DataFrame]:
    """
    Generate interpolated frame dataframes for animation.

    Each frame contains 18 team records with smooth y_pos, points, and percentage.
    Rank 1 is given the top y-coordinate (17), and Rank 18 is given 0.
    """
    df = prepare_ladder_time_series(df)
    unique_rounds = sorted(df["round_index"].unique())
    num_rounds = len(unique_rounds)

    round_dfs = {r: df[df["round_index"] == r].set_index("team") for r in unique_rounds}
    teams = list(TEAM_METADATA.keys())

    frames: list[pd.DataFrame] = []
    frame_idx = 0

    ease_func = cosine_ease if easing == "cosine" else smooth_step

    for r_idx in range(num_rounds):
        curr_r = unique_rounds[r_idx]
        curr_df = round_dfs[curr_r]
        round_name = curr_df["round_name"].iloc[0]
        round_display = curr_df["round_display"].iloc[0]

        # Determine steps for this round
        if r_idx == 0:
            # Initial hold on Round 0 / Opening Round
            total_steps = hold_start_frames
            is_transition = False
            next_df = curr_df
        elif r_idx == num_rounds - 1:
            # Transition from previous round, then final hold
            total_steps = steps_per_round
            is_transition = True
            prev_df = round_dfs[unique_rounds[r_idx - 1]]
        else:
            # Standard round transition
            total_steps = steps_per_round
            is_transition = True
            prev_df = round_dfs[unique_rounds[r_idx - 1]]

        if not is_transition:
            # Static hold frame (Opening Round)
            for _ in range(total_steps):
                frame_rows = []
                for team in teams:
                    if team not in curr_df.index:
                        continue
                    row = curr_df.loc[team]
                    pos = int(row["position"])
                    y_pos = 18 - pos  # Rank 1 -> y=17, Rank 18 -> y=0
                    frame_rows.append(
                        {
                            "frame_idx": frame_idx,
                            "round_index": curr_r,
                            "round_name": round_name,
                            "round_display": round_display,
                            "team": team,
                            "position": pos,
                            "y_pos": float(y_pos),
                            "points": float(row["points"]),
                            "percentage": float(row["percentage"]),
                            "played": int(row["played"]),
                            "wins": int(row["wins"]),
                            "losses": int(row["losses"]),
                            "draws": int(row["draws"]),
                            "rank_delta": int(row["rank_delta"]),
                            "is_top8": pos <= 8,
                        }
                    )
                frames.append(pd.DataFrame(frame_rows))
                frame_idx += 1
        else:
            # Interpolated frames from prev_df to curr_df
            t_values = np.linspace(0.0, 1.0, total_steps, endpoint=True)
            eased_t = ease_func(t_values)

            for step_i, factor in enumerate(eased_t):
                frame_rows = []
                for team in teams:
                    p_row = (
                        prev_df.loc[team]
                        if team in prev_df.index
                        else curr_df.loc[team]
                    )
                    c_row = (
                        curr_df.loc[team]
                        if team in curr_df.index
                        else prev_df.loc[team]
                    )

                    p_pos = int(p_row["position"])
                    c_pos = int(c_row["position"])

                    p_y = 18 - p_pos
                    c_y = 18 - c_pos

                    # Interpolate y_pos, points, percentage
                    interp_y = p_y + (c_y - p_y) * factor
                    interp_pts = (
                        float(p_row["points"])
                        + (float(c_row["points"]) - float(p_row["points"])) * factor
                    )
                    interp_pct = (
                        float(p_row["percentage"])
                        + (float(c_row["percentage"]) - float(p_row["percentage"]))
                        * factor
                    )

                    # Categorical stats switch when factor >= 0.5
                    active_row = c_row if factor >= 0.5 else p_row

                    frame_rows.append(
                        {
                            "frame_idx": frame_idx,
                            "round_index": curr_r,
                            "round_name": round_name,
                            "round_display": round_display,
                            "team": team,
                            "position": int(active_row["position"]),
                            "y_pos": float(interp_y),
                            "points": float(interp_pts),
                            "percentage": float(interp_pct),
                            "played": int(active_row["played"]),
                            "wins": int(active_row["wins"]),
                            "losses": int(active_row["losses"]),
                            "draws": int(active_row["draws"]),
                            "rank_delta": int(c_row["rank_delta"]),
                            "is_top8": int(c_row["position"]) <= 8,
                        }
                    )
                frames.append(pd.DataFrame(frame_rows))
                frame_idx += 1

    # Final hold frames on the completed Round 24 ladder
    final_df = round_dfs[unique_rounds[-1]]
    final_round_name = final_df["round_name"].iloc[0]
    final_round_display = final_df["round_display"].iloc[0]

    for _ in range(hold_end_frames):
        frame_rows = []
        for team in teams:
            row = final_df.loc[team]
            pos = int(row["position"])
            y_pos = 18 - pos
            frame_rows.append(
                {
                    "frame_idx": frame_idx,
                    "round_index": unique_rounds[-1],
                    "round_name": final_round_name,
                    "round_display": final_round_display,
                    "team": team,
                    "position": pos,
                    "y_pos": float(y_pos),
                    "points": float(row["points"]),
                    "percentage": float(row["percentage"]),
                    "played": int(row["played"]),
                    "wins": int(row["wins"]),
                    "losses": int(row["losses"]),
                    "draws": int(row["draws"]),
                    "rank_delta": int(row["rank_delta"]),
                    "is_top8": pos <= 8,
                }
            )
        frames.append(pd.DataFrame(frame_rows))
        frame_idx += 1

    return frames
