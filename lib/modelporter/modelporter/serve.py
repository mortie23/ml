from omegaconf import DictConfig, OmegaConf
from google.cloud import run_v2
from google.cloud import aiplatform
import google.auth
from datetime import datetime

from modelporter import vertex


def cloud_run(
    cfg: DictConfig,
    model_project: str,
    model_name: str,
    env: str,
):
    """Deploys (updates) a Cloud Run service with a new image.

    Args:
        docker_image_name: The full URL of the container image.
        region: The GCP region (e.g., "australia-southeast1").
        env: The environment (e.g., dev|ppd|prd).
        service_name: The name of the Cloud Run service.
    """
    model_serving_container_image_uri = f"{cfg.location}-docker.pkg.dev/{cfg.project_id}/{cfg.artifact_registry_repository}/{cfg.predict_container_image}"

    try:
        credentials, project_id = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError:
        print("Error: Could not find default credentials.")
        return

    # Get the model bucket uri
    # Vertex let's multiple models register with the same display name
    # Search through all registered models in project and return list of all with the name
    models = vertex.find_models_by_display_name(
        project=cfg.project_id,
        location=cfg.location,
        search_display_name=f"{model_project}-{model_name}",
    )
    model = aiplatform.Model(models[0])
    aip_storage_uri = model.uri

    client = run_v2.ServicesClient(credentials=credentials)
    full_service_name = client.service_path(
        cfg.project_id,
        cfg.location,
        f"{model_project}-{model_name}",
    )

    service = client.get_service(name=full_service_name)

    # Generate the formatted datetime string for the annotation
    now = datetime.now()
    revision_suffix = now.strftime("%y%m%d%H%M")  # YYMMDDHHMM

    # The properties to update are just the container image
    update_mask = {
        "paths": [
            "template.containers",
            "traffic",  # Always include traffic in the mask
            "template.annotations",  # Add annotations to the mask
        ]
    }

    # --- Update the Service ---
    request = run_v2.UpdateServiceRequest(
        service={
            "name": full_service_name,
            "template": {
                "containers": [
                    {
                        "image": model_serving_container_image_uri,
                        "resources": {
                            "limits": {
                                "cpu": "2",
                                "memory": "8Gi",
                            },
                        },
                        "env": [
                            {"name": "AIP_PREDICT_ROUTE", "value": "/predict"},
                            {"name": "BQ_PREDICT_ROUTE", "value": "/"},
                            {"name": "AIP_HEALTH_ROUTE", "value": "/ping"},
                            {"name": "PROJECT_ID", "value": cfg.project_id},
                            {"name": "AIP_STORAGE_URI", "value": aip_storage_uri},
                        ],
                    }
                ],
                "annotations": {
                    "force-new-revision": revision_suffix  # Add/update a dummy annotation
                },
            },
            "traffic": [
                {
                    "type_": run_v2.TrafficTargetAllocationType.TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST,
                    "percent": 100,
                }
            ],  # Directly to latest
        },
        update_mask=update_mask,
    )

    try:
        operation = client.update_service(request=request)
        print("Waiting for operation to complete...")
        response = operation.result()
        print(f"Cloud Run service updated. URL: {response.uri}")

    except Exception as e:
        print(f"Error updating service: {e}")
