# %% [markdown]
# # Train a model to predict a players number of touchdowns from stats
#
# Using statistics for each player such as First downs, yards gained and punts.

# %%
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from google.cloud import bigquery
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from google.cloud import storage
from sklearn.pipeline import Pipeline, make_pipeline
from dotenv import load_dotenv

from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

# Internal helpers
from nfltouchdown.io import get_data, upload_to_gcs, download_from_gcs

# initialize(version_base=None, config_path="../../conf")
# cfg = compose(config_name="config")
initialize(version_base=None, config_path=".")
cfg = compose(config_name="train")

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)
env = os.getenv("env")

for k, v in cfg.items():
    cfg[k] = v.replace("<env>", env)


# %%
def split_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataframe into features and target

    Args:
        data (pd.DataFrame): input dataframe

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: X, y as features and target
    """
    input_features = ["total_first_downs", "total_yards", "interceptions", "punts"]
    X = df[input_features]
    y = df["total_td"]
    return X, y


# %%
def train_model(
    x_train: pd.DataFrame,
    y_train: pd.Series,
) -> Pipeline:
    """Train a Radom forest regressor on NFL players

    Args:
        x_train (pd.DataFrame): Features
        y_train (pd.Series): Target

    Returns:
        Pipeline: Sklearn pipeline
    """
    model = RandomForestRegressor()
    pipe = make_pipeline(model)
    pipe.fit(x_train, y_train)
    return pipe


# %%
def save_model_artifact(
    pipe: Pipeline,
) -> None:
    """Save the pipeline artifact to bucket storage

    Args:
        pipe (Pipeline): Sklearn pipeline
    """

    artifact_filename = "model.joblib"

    # Save model artifact to local filesystem (doesn't persist)
    local_path = artifact_filename
    joblib.dump(pipe, local_path)

    # Upload model artifact to Cloud Storage
    # gs://bkt-xyz-dev-nfl-vertex-0/aiplatform-custom-training-yyyy-mm-dd-hh:mm:ss.ms/model
    model_directory = os.environ["AIP_MODEL_DIR"]
    print("AIP_MODEL_DIR: ", model_directory)
    storage_path = os.path.join(model_directory, artifact_filename)
    blob = storage.blob.Blob.from_string(storage_path, client=storage.Client())
    blob.upload_from_filename(local_path)


# %%
def main():
    # Run the training
    df = get_data(
        project_id=os.environ["CLOUD_ML_PROJECT_ID"],
        dataset_name=cfg.source_dataset,
        table_name=cfg.source_table,
    )
    X, y = split_data(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    pipe = train_model(X_train, y_train)
    y_pred = pipe.predict(X_test)
    save_model_artifact(pipe)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("RMSE:", rmse)


# %%
if __name__ == "__main__":
    main()

# %%
