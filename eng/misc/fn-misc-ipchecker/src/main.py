# %%
import flask
import requests
from google.cloud import bigquery
import pandas as pd
import time
import os
import sys
import json
from math import floor
from pathlib import Path
from typing import Tuple
from dotenv import load_dotenv

from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

initialize(version_base=None, config_path=".")
cfg = compose(config_name="misc")

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)
env = os.getenv("env")

for k, v in cfg.items():
    cfg[k] = v.replace("<env>", env)


# %%
def ip_checker() -> str:
    """Call a service that returns the calling network IP address

    Returns:
        str: The IP Address
    """
    data = requests.get(cfg.base_url)
    ip_address = json.loads(data.content.decode("utf-8"))["ip"]
    return ip_address


# %%
def insert_into_bigquery(
    ip_address: str,
) -> None:
    """Insert the response IP address into BigQuery table

    Args:
        ip_address (str): the ip address
    """
    client = bigquery.Client(cfg.project_id)
    project_id = cfg.project_id
    dataset_name = cfg.dataset_name
    table_name = cfg.table_name
    table_id = f"{project_id}.{dataset_name}.{table_name}"

    df = pd.DataFrame({"ip_address": [ip_address]})

    df["created_timestamp"] = pd.Timestamp.now()

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("ip_address", "STRING"),
            bigquery.SchemaField("created_timestamp", "TIMESTAMP"),
        ],
        write_disposition="WRITE_APPEND",
    )
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config,
    )
    job.result()
    job.done()


# %%
def fn_misc_ipchecker(request: flask.Request) -> flask.Response:
    """The main function

    Returns:
        flask.Response: A status message including IP address
    """
    ip_address = ip_checker()
    insert_into_bigquery(ip_address)
    return flask.Response(
        f"IP address {ip_address} successfully inserted into BigQuery",
        mimetype="text/plain",
    )


# %%
if __name__ == "__main__":
    fn_misc_ipchecker(None)

# %%
