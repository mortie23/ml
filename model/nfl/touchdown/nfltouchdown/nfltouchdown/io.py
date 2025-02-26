import numpy as np
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage

def get_data(
    project_id: str,
    dataset_name: str,
    table_name: str,
) -> pd.DataFrame:
    """From a given dataset and table name return a dataframe of the table

    Args:
        project_id (str): The 12 digit project number to connect the BigQuery client to
        dataset_name (str): The name of a dataset in BigQuery
        table_name (str): The name of a table in BigQuery

    Returns:
        pd.DataFrame: A dataframe of the whole table

    """
    client = bigquery.Client(
        project=project_id,
    )

    sql = f"""
    select
      *
    from
      {dataset_name}.{table_name}
    ;
    """
    return client.query(sql).to_dataframe()


def upload_to_gcs(
    local_file_path: str,
    bucket_name: str,
    destination_blob_name: str,
) -> str:
    """Uploads a file to Google Cloud Storage.

    Args:
        local_file_path (str): Path to the local file to upload.
        bucket_name (str): Name of the GCS bucket.
        destination_blob_name (str): Destination path in the GCS bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    return f"File {local_file_path} uploaded to {bucket_name}/{destination_blob_name}."


def download_from_gcs(
    bucket_name: str,
    source_blob_name: str,
    destination_file_name: str,
):
    """Downloads a file from Google Cloud Storage.

    Args:
        bucket_name (str): Name of the GCS bucket.
        source_blob_name (str): Path in the bucket to the file.
        destination_file_name (str): Local path to save the downloaded file.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    return f"File {source_blob_name} downloaded to {destination_file_name}."
