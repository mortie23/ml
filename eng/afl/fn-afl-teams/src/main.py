# %%
import requests
from bs4 import BeautifulSoup
from google.cloud import bigquery
import requests
import pandas as pd
import json
import pprint
import re
import os
import sys
from pathlib import Path
from typing import Tuple
from dotenv import load_dotenv

from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

# initialize(version_base=None, config_path="../../conf")
# cfg = compose(config_name="config")
initialize(version_base=None, config_path=".")
cfg = compose(config_name="afl")

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)
env = os.getenv("env")

for k, v in cfg.items():
    cfg[k] = v.replace("<env>", env)


# %%
def scrape_data() -> pd.DataFrame:
    """Scraoe the data and standardise the format of column names and types

    Returns:
        pd.DataFrame: _description_
    """
    reqUrl = "https://api.squiggle.com.au/"

    # Set parameters in Python variables
    params = {
        "q": "teams",
    }

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    }
    # Pass parameters using the 'params' parameter
    response = requests.get(
        reqUrl,
        params=params,
        headers=headersList,
    )

    json_data = response.json()
    # Initialise the dataframe
    columns = [
        "debut",
        "retirement",
        "abbrev",
        "id",
        "name",
        "logo",
    ]
    df = pd.DataFrame(columns=columns)

    # Parse out the data into a dataframe
    for val in json_data["teams"]:
        df = pd.concat([df, pd.DataFrame([val])], ignore_index=True)

    df["debut"] = df["debut"].astype(str)
    df["retirement"] = df["retirement"].astype(str)
    df["abbrev"] = df["abbrev"].astype(str)
    df["id"] = df["id"].astype(str)
    df["name"] = df["name"].astype(str)
    df["logo"] = df["logo"].astype(str)

    return df


# %%
def insert_into_bigquery(
    df: pd.DataFrame,
) -> None:
    """Insert the scraped data into BigQuery table

    Args:
        df (pd.DataFrame): the scraped data
    """
    client = bigquery.Client(cfg.project_id)
    project_id = cfg.project_id
    dataset_name = cfg.dataset_name
    table_name = cfg.table_name
    table_id = f"{project_id}.{dataset_name}.{table_name}"

    # Define a dictionary with your data
    df["created_timestamp"] = pd.Timestamp.now()

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("debut", "STRING"),
            bigquery.SchemaField("retirement", "STRING"),
            bigquery.SchemaField("abbrev", "STRING"),
            bigquery.SchemaField("id", "STRING"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("logo", "STRING"),
            bigquery.SchemaField("created_timestamp", "TIMESTAMP"),
        ],
        write_disposition="WRITE_TRUNCATE",
    )
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config,
    )
    job.result()
    job.done()


# %%
def fn_afl_teams(request) -> Tuple[str, int]:
    """The main functions

    Returns:
        Tuple[str, int]: A status message and code
    """
    print(request)
    data = scrape_data()
    insert_into_bigquery(data)
    return "Data successfully inserted into BigQuery", 200


# %%
if __name__ == "__main__":
    fn_afl_teams(None)

# %%
