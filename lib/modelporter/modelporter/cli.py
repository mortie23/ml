"""Deploy a custom model

Usage:
    # This was when building containers locally
    ## Predict first, as the training job requires the configuration to point to the prediction container
    modelporter serve --model nfl.touchdown
    ## Then train
    modelporter server --model nfl.touchdown

TODO:
    Add the deploy to endpoint
"""

import os
from pathlib import Path
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

from hydra import compose, initialize_config_dir
from omegaconf import DictConfig, OmegaConf

console = Console()

import conman.setenv as se
from modelporter import docker, serve, vertex, cloudbuild


@click.group()
@click.argument("model")
@click.option(
    "--env",
    "-e",
    type=str,
    required=True,
    help="The environment <dev|ppd|prd>",
)
@click.pass_context
def cli(
    ctx: dict,
    model: str,
    env: str,
):
    """ModelPorter CLI - A tool for deploying ML models.

    Args:
        MODEL (str): The name of the program and model <program>.<model> e.g. nfl.touchdown
    """
    ctx.ensure_object(dict)
    # Store globally accessible values
    ctx.obj["model"] = model
    ctx.obj["env"] = env


@click.command(name="build")
@click.option(
    "--phase",
    default="train",
    type=str,
    required=True,
    help="The model phase [train/predict]",
)
@click.option(
    "--builder",
    default="cloudbuild",
    type=str,
    required=True,
    help="The target method used to build the container [cloudbuild/docker]",
)
@click.pass_context
def build_command(
    ctx: dict,
    phase: str,
    builder: str,
):
    """Build a Docker container for the model.

    Args:
        phase (str): The model phase [train/predict]
        builder (str): The target method used to build the container [cloudbuild/docker]

    example:
        modelporter --env=dev nfl.touchdown build --phase=predict --builder=cloudbuild
    """
    model = ctx.obj["model"]
    env = ctx.obj["env"]

    model_project, model_name = model.split(".", 1)
    # Configs are relative to current working directory (not internal package directory)
    config_dir = os.path.join(os.getcwd(), model_project, model_name)
    initialize_config_dir(version_base=None, config_dir=config_dir)
    cfg = compose(config_name=model_name)

    # Replacing environment within configuration
    se.replace_env_values(cfg, env)

    with Progress(
        SpinnerColumn(),
        TextColumn(
            "[bold magenta]Build Docker container {task.description}.[/bold magenta]"
        ),
    ) as progress:
        task = progress.add_task(
            f"[green]Phase {phase}...[/green]",
            total=None,
        )
        if builder == "cloudbuild":
            cloudbuild.trigger_build(
                env=env,
                cfg=cfg,
                model_project=model_project,
                model_name=model_name,
                phase=phase,
            )
        elif builder == "docker":
            docker.build_and_push(
                env=env,
                cfg=cfg,
                context=f"./{model_project}/{model_name}/{phase}",
                phase=phase,
            )
        progress.remove_task(task)

    console.print


@click.command(name="train")
@click.option(
    "--service",
    default="vertex",
    type=str,
    required=True,
    help="The target service to run training [vertex]",
)
@click.pass_context
def train_command(
    ctx: dict,
    service: str,
):
    """Train a model on Vertex AI.

    Args:
        MODEL (str): The name of the program and model <program>.<model> e.g. nfl.touchdown
        service (str): The service to use to train [vertex]

    example:
        modelporter --env=dev nfl.touchdown train --service=vertex
    """
    model = ctx.obj["model"]
    env = ctx.obj["env"]

    model_project, model_name = model.split(".", 1)
    # Configs are relative to current working directory (not internal package directory)
    config_dir = os.path.join(os.getcwd(), model_project, model_name)
    initialize_config_dir(version_base=None, config_dir=config_dir)
    cfg = compose(config_name=model_name)

    # Replacing environment within configuration
    se.replace_env_values(cfg, env)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold magenta]Training model {task.description}.[/bold magenta]"),
    ) as progress:
        task = progress.add_task(
            f"[cyan]{model} is training on {service}...[/cyan]",
            total=None,
        )
        vertex.train(
            cfg,
            model_project,
            model_name,
        )
        progress.remove_task(task)


@click.command(name="serve")
@click.pass_context
@click.option(
    "--service",
    default="cloudrun",
    type=str,
    required=True,
    help="The target service to serve [vertex|cloudrun]",
)
def serve_command(
    ctx: dict,
    service: str,
):
    """Serving a model as API (Cloud Run or Vertex AI online prediction).

    Args:
        MODEL (str): The name of the program and model <program>.<model> e.g. nfl.touchdown
        service (str): The target service to serve [vertex|cloudrun] (only cloudrun implemented)
    """
    model = ctx.obj["model"]
    env = ctx.obj["env"]

    model_project, model_name = model.split(".", 1)
    # Configs are relative to current working directory (not internal package directory)
    config_dir = os.path.join(os.getcwd(), model_project, model_name)
    initialize_config_dir(version_base=None, config_dir=config_dir)
    cfg = compose(config_name=model_name)

    # Replacing environment within configuration
    se.replace_env_values(cfg, env)

    with Progress(
        SpinnerColumn(),
        TextColumn(
            "[bold magenta]Serving a model as API {task.description}.[/bold magenta]"
        ),
    ) as progress:
        task = progress.add_task(
            f"[cyan]Deploying the {service} prediction hosting infra for {model}...[/cyan]",
            total=None,
        )
        serve.cloud_run(
            cfg,
            model_project,
            model_name,
            env,
        )
        progress.remove_task(task)


cli.add_command(build_command)
cli.add_command(train_command)
cli.add_command(serve_command)

if __name__ == "__main__":
    cli()  # Runs the CLI
