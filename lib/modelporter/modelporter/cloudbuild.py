from google.cloud.devtools import cloudbuild_v1
import google.auth
from google.oauth2 import service_account
from pathlib import Path
from omegaconf import DictConfig, OmegaConf
import yaml
import os
import sys
import logging
import conman.setenv as se


def trigger_build(
    env: str,
    cfg: DictConfig,
    model_project: str,
    model_name: str,
    phase: str,
):
    credentials, project_id = google.auth.default()
    client = cloudbuild_v1.services.cloud_build.CloudBuildClient(
        credentials=credentials,
        client_options={
            "api_endpoint": f"{cfg.location}-cloudbuild.googleapis.com:443"
        },
    )

    build_config = cloudbuild_v1.Build()
    cloudbuild_config = (
        Path()
        / model_project
        / model_name
        / f"{model_project}{model_name}{phase}"
        / "cloudbuild.yaml"
    )
    with open(cloudbuild_config, "r") as f:
        build_config_dict = yaml.safe_load(f)
    build_config = cloudbuild_v1.Build(build_config_dict)

    build_config.service_account = cfg.build_service_account
    build_config.logs_bucket = cfg.build_logs_bucket
    build_config.substitutions.update({"_ENV": env})

    handler = logging.StreamHandler(sys.stdout)

    # Set up the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)  # Add the handler to the root logger

    logging.getLogger("google.auth").setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    logging.getLogger("google.cloud.build").setLevel(logging.DEBUG)
    logging.getLogger("google.api_core.grpc_helpers").setLevel(logging.DEBUG)

    # ? NOTE: This became too complex.
    # ? The Python SDK for Cloud Build does not automatically zip the Dockerfile etc to Cloud storage
    # ? gcloud does
    # Creating temporary archive of 14 file(s) totalling 13.9 MiB before compression.
    # Uploading tarball of [.] to [gs://prj-xyz-dev-nfl-0_cloudbuild/source/<guid-hash>.tgz]
    # ? For now, just use the gcloud cli through the shell script in each directory

    operation = client.create_build(
        project_id=cfg.project_id,
        build=build_config,
    )
    print(f"Cloud Build triggered. Operation: {operation.operation.name}")
    result = operation.result()
