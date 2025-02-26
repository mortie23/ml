from nfltouchdown.io import get_data, upload_to_gcs, download_from_gcs


def test_get_data():
    project_id = "prj-xyz-dev-nfl-0"
    dataset_name = "cur"
    table_name = "game_stats"
    df = get_data(
        project_id=project_id,
        dataset_name=dataset_name,
        table_name=table_name,
    )
