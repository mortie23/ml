from omegaconf import DictConfig, OmegaConf
from google.cloud import aiplatform
import os


def find_models_by_display_name(
    project: str,
    location: str,
    search_display_name: str,
) -> list[str]:
    """Finds a Model IDs based on a display name search.

    Args:
        project: Your GCP project ID.
        location: The region (e.g., 'australia-southeast1').
        search_display_name: The display name (or part of it) to search for.

    Returns:
        A list of Model IDs that match the display name criteria.  Returns an
        empty list if no matches are found.
    """

    aiplatform.init(
        project=project,
        location=location,
    )
    model_ids = []

    # List all models (no restrictive display_name filter initially)
    models = aiplatform.Model.list()

    for model in models:
        # Case-insensitive search (recommended)
        if search_display_name.lower() in model.display_name.lower():
            # Extract just the model ID from the resource name
            model_id = model.resource_name.split("/")[-1]  # Get the last part
            model_ids.append(model_id)

    return model_ids


def train(
    cfg: DictConfig,
    model_project: str,
    model_name: str,
) -> aiplatform.CustomContainerTrainingJob:
    """Run a training job, creating a new model or a new version.

    Args:
        cfg (DictConfig): The hydra configuration.
        model_project (str): The parent directory name (e.g., nfl).
        model_name (str): The name of the model (e.g., touchdown).

    Returns:
        aiplatform.CustomContainerTrainingJob: The training job.
    """

    aiplatform.init(
        project=cfg.project_id,
        staging_bucket=cfg.train.staging_bucket_name,
        location=cfg.location,
    )
    container_uri = f"{cfg.location}-docker.pkg.dev/{cfg.project_id}/{cfg.artifact_registry_repository}/{cfg.train_container_image}"
    model_serving_container_image_uri = f"{cfg.location}-docker.pkg.dev/{cfg.project_id}/{cfg.artifact_registry_repository}/{cfg.predict_container_image}"

    display_name = f"{model_project}-{model_name}"

    # Check for existing models with the same display name
    existing_model_ids = find_models_by_display_name(
        cfg.project_id,
        cfg.location,
        display_name,
    )

    job = aiplatform.CustomContainerTrainingJob(
        display_name=f"{display_name}-train-job",
        container_uri=container_uri,
        model_serving_container_image_uri=model_serving_container_image_uri,
        staging_bucket=cfg.train.staging_bucket_name,
    )
    if not existing_model_ids:
        # No existing model: Create a NEW model
        print(
            f"No existing model found with display name '{display_name}'. Creating a new model."
        )
        job.run(
            replica_count=1,
            model_display_name=display_name,  # Specify display name for a NEW model
            machine_type="n1-standard-4",
            sync=True,
        )
    else:
        # Existing model found: Create a NEW VERSION
        print(
            f"Existing model found with display name '{display_name}'. Creating a new version."
        )
        if len(existing_model_ids) > 1:
            raise ValueError(
                f"Multiple models found with display name '{display_name}'.  Expected only one."
            )
        model_id = existing_model_ids[0]
        model_resource_name = aiplatform.Model(model_name=model_id).resource_name

        job.run(
            replica_count=1,
            machine_type="n1-standard-4",
            sync=True,
            parent_model=model_resource_name,
            is_default_version=True,
        )

    job.wait()
    return job
