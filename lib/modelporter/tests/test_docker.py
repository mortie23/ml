import pytest
import os
import click
import docker
import deploy as dp
import conman.setenv as se

from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf


def test_docker_client():
    client = dp.docker_client()
    # Verify connection by listing containers
    containers = client.containers.list(all=True)
    # breakpoint()
    assert type(containers[0]) == docker.models.containers.Container


def test_docker_build_and_push():
    env = "dev"
    model = "fruit.bowl"
    lifecycle = "train"
    model_project, model_name = model.split(".", 1)
    config_path = os.path.join("./", model_project, model_name)

    initialize(version_base=None, config_path=config_path)
    cfg = compose(config_name=model_name)
    # Replacing environment within configuration
    se.replace_env_values(cfg, env)

    success, image = dp.docker_build_and_push(
        cfg=cfg,
        context=f"./{model_project}/{model_name}/{lifecycle}",
    )
    assert success == True
    assert type(image) == docker.models.images.Image
