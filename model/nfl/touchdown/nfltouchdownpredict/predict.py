# %% [markdown]
# # Predict a players number of touchdowns from stats
#
# Using statistics for each player such as First downs, yards gained and punts.

"""
Environment variables when running in Vertex:
    AIP_HTTP_PORT=8080
    AIP_HEALTH_ROUTE=/health
    AIP_PREDICT_ROUTE=/predict
    AIP_STORAGE_URI={BUCKET_URI}/{MODEL_ARTIFACT_DIR}
Example response from Vertex call:
    {
        "predictions": [
            2.01,
            4.51
        ],
        "deployedModelId": "<18-digit-integer>",
        "model": "projects/<project-number>/locations/australia-southeast1/models/<19-digit-integer>",
        "modelDisplayName": "nfl-touchdown",
        "modelVersionId": "1"
    }
"""

# %%
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing import Any, List

import joblib
import json
import numpy as np
import pickle
import os
from pathlib import Path
from dotenv import load_dotenv

from google.cloud import storage

from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

initialize(version_base=None, config_path=".")
cfg = compose(config_name="predict")

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)
env = os.getenv("env")

for k, v in cfg.items():
    cfg[k] = v.replace("<env>", env)

app = FastAPI()
client = storage.Client(os.environ["project_id"])


# Define a model input schema with example data
class ModelInput(BaseModel):
    # Example input for Swagger UI
    instances: List[List[float]] = Field(
        ...,
        description="A list of feature arrays to predict outcomes for.",
        examples=[
            [[23.0, 150.0, 1.0, 20.0], [33.0, 400.0, 1.0, 2.0]],
        ],  # Directly the field value, not wrapped in another object
    )


with open("model.joblib", "wb") as model_f:
    client.download_blob_to_file(
        f"{os.environ['AIP_STORAGE_URI']}/model.joblib", model_f
    )

_model = joblib.load("model.joblib")


@app.get(os.environ["AIP_HEALTH_ROUTE"], status_code=200)
def health():
    return {"status": "healthy"}


@app.post(os.environ["AIP_PREDICT_ROUTE"])
async def predict(
    input_data: ModelInput,
) -> dict[str, Any]:
    """
    Accepts input data in JSON format, runs predictions using a pre-trained
    sklearn model, and returns predictions as a JSON response.

    Args:
        request (Request): JSON input containing a list of instances.

    Returns:
        dict[str, Any]: JSON object containing predictions.
    """
    # Convert input data to numpy array
    data: np.ndarray = np.array(input_data.instances)

    # Generate predictions
    predictions: np.ndarray = _model.predict(data)

    # Convert numpy array to JSON-serializable list
    response: List[int] = predictions.tolist()

    return {"predictions": response}
