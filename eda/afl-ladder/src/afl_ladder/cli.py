from pathlib import Path

import pandas as pd
import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)

from afl_ladder.config import (
    DATA_PROCESSED_DIR,
    OUTPUT_DIR,
    SEASON_YEAR,
)
from afl_ladder.processor import generate_race_frames
from afl_ladder.renderer import render_preview_image, render_race_video
from afl_ladder.scraper import scrape_season_ladders

app = typer.Typer(help="AFL Ladder Bar Chart Race Video Generator")
console = Console()


@app.command()
def scrape(
    year: int = typer.Option(SEASON_YEAR, "--year", "-y", help="Season year to scrape"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force re-download cached HTML"
    ),
):
    """Scrape round-by-round ladder data for the season from FootyForecaster."""
    console.print(f"[bold cyan]Scraping AFL {year} ladder data...[/bold cyan]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            description=f"Fetching rounds for {year}...", total=None
        )
        df = scrape_season_ladders(year=year, force=force)
        progress.update(task, completed=True)

    rounds_count = df["round_name"].nunique()
    console.print(
        f"[bold green]✓ Successfully scraped {len(df)} entries across {rounds_count} rounds![/bold green]"
    )
    console.print(f"Saved to: [bold]{DATA_PROCESSED_DIR / f'ladder_{year}.csv'}[/bold]")


@app.command()
def preview(
    year: int = typer.Option(SEASON_YEAR, "--year", "-y", help="Season year"),
    round_name: str = typer.Option(
        "Round_24",
        "--round",
        "-r",
        help="Round to preview (e.g. Round_24, Round_4, Opening_Round)",
    ),
    orientation: str = typer.Option(
        "landscape", "--orientation", "-o", help="landscape (16:9) or portrait (9:16)"
    ),
    output: Path | None = typer.Option(
        None, "--output", help="Output image file path (.png)"
    ),
):
    """Generate a single-frame preview image to verify styling."""
    ladder_file = DATA_PROCESSED_DIR / f"ladder_{year}.csv"
    if not ladder_file.exists():
        console.print("[yellow]Data file not found. Scraping now...[/yellow]")
        scrape_season_ladders(year=year)

    df = pd.read_csv(ladder_file)

    # Normalize round_name if given as a number e.g. "24" or "4"
    if round_name.isdigit():
        round_name = f"Round_{round_name}"

    if round_name not in df["round_name"].values:
        console.print(
            f"[bold red]Round '{round_name}' not found. Available rounds: {', '.join(df['round_name'].unique())}[/bold red]"
        )
        raise typer.Exit(code=1)

    frames = generate_race_frames(
        df, steps_per_round=1, hold_start_frames=1, hold_end_frames=1
    )

    # Pick matching frame
    matching_frames = [f for f in frames if f["round_name"].iloc[0] == round_name]
    if not matching_frames:
        target_frame = frames[-1]
    else:
        target_frame = matching_frames[0]

    if output is None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output = OUTPUT_DIR / f"preview_{round_name.lower()}_{orientation}.png"

    console.print(f"[cyan]Rendering preview of {round_name} ({orientation})...[/cyan]")
    render_preview_image(
        frame_df=target_frame,
        output_path=output,
        orientation=orientation,
        dynamic_scale=True,
        season_year=year,
    )
    console.print(f"[bold green]✓ Preview saved to: {output}[/bold green]")


@app.command()
def render(
    year: int = typer.Option(SEASON_YEAR, "--year", "-y", help="Season year to render"),
    fps: int = typer.Option(30, "--fps", help="Frames per second"),
    steps_per_round: int = typer.Option(
        24, "--steps", help="Interpolation frames between rounds"
    ),
    hold_start: int = typer.Option(
        30, "--hold-start", help="Initial hold frames on Opening Round"
    ),
    hold_end: int = typer.Option(
        90, "--hold-end", help="Final hold frames on Round 24"
    ),
    orientation: str = typer.Option(
        "landscape", "--orientation", "-o", help="landscape or portrait"
    ),
    dynamic_scale: bool = typer.Option(
        True,
        "--dynamic-scale/--fixed-scale",
        help="Smoothly expand max points axis as season advances",
    ),
    output: Path | None = typer.Option(None, "--output", help="Output MP4 file path"),
):
    """Render the animated bar chart race video."""
    ladder_file = DATA_PROCESSED_DIR / f"ladder_{year}.csv"
    if not ladder_file.exists():
        console.print("[yellow]Data file not found. Scraping first...[/yellow]")
        scrape_season_ladders(year=year)

    df = pd.read_csv(ladder_file)
    console.print(
        f"[cyan]Generating interpolated frames ({steps_per_round} steps/round)...[/cyan]"
    )
    frames = generate_race_frames(
        df=df,
        steps_per_round=steps_per_round,
        hold_start_frames=hold_start,
        hold_end_frames=hold_end,
    )

    total_frames = len(frames)
    duration_sec = total_frames / fps
    console.print(
        f"[bold green]Generated {total_frames} frames (Video duration: {duration_sec:.1f}s at {fps} fps)[/bold green]"
    )

    if output is None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output = OUTPUT_DIR / f"afl_{year}_ladder_race_{orientation}.mp4"

    console.print(f"[bold cyan]Rendering video to {output}...[/bold cyan]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        render_task = progress.add_task("Encoding frames...", total=total_frames)

        def on_progress(current: int, total: int):
            progress.update(render_task, completed=current)

        render_race_video(
            frames=frames,
            output_path=output,
            fps=fps,
            orientation=orientation,
            dynamic_scale=dynamic_scale,
            season_year=year,
            progress_callback=on_progress,
        )

    console.print(f"[bold green]✓ Video rendered successfully: {output}[/bold green]")


@app.command(name="all")
def run_all(
    year: int = typer.Option(SEASON_YEAR, "--year", "-y", help="Season year"),
    fps: int = typer.Option(30, "--fps", help="Frames per second"),
    orientation: str = typer.Option(
        "landscape", "--orientation", "-o", help="landscape or portrait"
    ),
    output: Path | None = typer.Option(None, "--output", help="Output MP4 file path"),
):
    """Scrape data and render the full AFL ladder race video in one pass."""
    scrape(year=year, force=False)
    render(year=year, fps=fps, orientation=orientation, output=output)


def main():
    app()


if __name__ == "__main__":
    main()
