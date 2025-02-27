import docker
from typing import Tuple, Union

from omegaconf import DictConfig, OmegaConf


def docker_client():
    try:
        client = docker.from_env()
        return client
    except docker.errors.DockerException as e:
        return e


def build_and_push(
    env: str,
    cfg: DictConfig,
    context: str,
    phase: str,
) -> Tuple[bool, Union[str, docker.models.images.Image]]:
    """
    Build and push a Docker image.

    Args:
        env (str): The environment
        image_name (str): The name of the Docker image to build and push.
        tag (str): The tag to assign to the Docker image.
        context (str): The path to the build context directory.

    Returns:
        Tuple[bool, Union[str, docker.models.images.Image]]:
            A tuple containing a success flag and either the built image object
            (on success) or an error message (on failure).
    """
    client = docker_client()

    # Construct the full image name
    image_name = getattr(cfg, f"{phase}_container_image", None)
    docker_image_name = f"{cfg.location}-docker.pkg.dev/{cfg.project_id}/{cfg.artifact_registry_repository}/{image_name}"

    try:
        # Build the Docker image
        build_output = []
        for line in client.api.build(
            path=context,
            tag=docker_image_name,
            buildargs={
                "env": env,
                "project_id": cfg.project_id,
            },
            rm=True,  # Removes intermediate containers
            decode=True,
        ):
            build_output.append(line)
            if "stream" in line:
                print(line["stream"].strip())  # Print real-time output

        # Push the Docker image
        push_output = []
        for line in client.images.push(docker_image_name, stream=True, decode=True):
            push_output.append(line)
            print(line)
        print(f"Successfully pushed {docker_image_name}")

        # Return success and the image object
        return True, image_name

    except docker.errors.DockerException as e:
        error_message = f"Error during Docker operation: {e}"
        print(error_message)

        # Return failure and the error message
        return False, error_message
