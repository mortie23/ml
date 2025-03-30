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
class ModelInputItem(BaseModel):
    game_team_id: int = Field(..., example=411)
    total_first_downs: int = Field(..., example=26)
    total_yards: int = Field(..., example=419)
    interceptions: int = Field(..., example=0)
    punts: int = Field(..., example=4)


class VertexPredictionRequest(BaseModel):
    instances: List[ModelInputItem] = Field(
        ...,
        example=[
            {
                "game_team_id": 411,
                "total_first_downs": 26,
                "total_yards": 419,
                "interceptions": 0,
                "punts": 4,
            }
        ],
    )

with open("model.joblib", "wb") as model_f:
    client.download_blob_to_file(
        f"{os.environ['AIP_STORAGE_URI']}/model.joblib", model_f
    )

_model = joblib.load("model.joblib")


@app.get(os.environ["AIP_HEALTH_ROUTE"], status_code=200)
def health():
    return {"status": "healthy"}


@app.post("/")
async def predict_root(
    input_data: ModelInputItem,
) -> dict[str, Any]:
    """
    Root endpoint for single prediction requests.

    Args:
        input_data: Single game stats for prediction

    Returns:
        dict[str, Any]: Prediction result with game_team_id
    """
    # Convert input to feature array
    features = np.array(
        [
            [
                input_data.total_first_downs,
                input_data.total_yards,
                input_data.interceptions,
                input_data.punts,
            ]
        ]
    )

    # Generate prediction
    prediction: np.ndarray = _model.predict(features)

    return {"game_team_id": input_data.game_team_id, "prediction": prediction[0]}


@app.post(os.environ["AIP_PREDICT_ROUTE"])
async def predict_vertex(
    input_data: VertexPredictionRequest,
) -> dict[str, Any]:
    """
    Vertex AI endpoint for batch predictions.

    Args:
        input_data: Batch of game stats for prediction

    Returns:
        dict[str, Any]: Batch prediction results
    """
    # Convert input data to feature arrays
    features = np.array(
        [
            [
                instance.total_first_downs,
                instance.total_yards,
                instance.interceptions,
                instance.punts,
            ]
            for instance in input_data.instances
        ]
    )

    # Generate predictions
    predictions: np.ndarray = _model.predict(features)

    # Pair predictions with game_team_ids
    results = [
        {"game_team_id": instance.game_team_id, "prediction": pred}
        for instance, pred in zip(input_data.instances, predictions)
    ]

    return {"predictions": results}
