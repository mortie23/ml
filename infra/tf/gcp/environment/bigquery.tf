# Misc
## 
resource "google_bigquery_dataset" "demo" {
  dataset_id = "demo"
  project    = google_project.misc_ip_1.project_id
  location   = var.region
  lifecycle {
    ignore_changes = [
      max_time_travel_hours,
    ]
  }
  depends_on = [google_project.misc_ip_1, google_project_service.misc_ip_bigquery]
}

## NFL
resource "google_bigquery_dataset" "cur" {
  dataset_id = "cur"
  project    = google_project.nfl_0.project_id
  location   = var.region
  lifecycle {
    ignore_changes = [
      max_time_travel_hours,
    ]
  }
  depends_on = [google_project.nfl_0, google_project_service.nfl_bigquery]
}

resource "google_bigquery_dataset" "mdl" {
  dataset_id = "mdl"
  project    = google_project.nfl_0.project_id
  location   = var.region
  lifecycle {
    ignore_changes = [
      max_time_travel_hours,
    ]
  }
  depends_on = [google_project.nfl_0, google_project_service.nfl_bigquery]
}

# BigQuery Connection Resources
## Used for Vertex
resource "google_bigquery_connection" "vertex_connection" {
  connection_id = "vertex"
  location      = var.region
  project       = google_project.nfl_0.project_id

  cloud_resource {}
  friendly_name = "Vertex AI Connection"
  description   = "Connection to Vertex AI for BigQuery ML"
}

## Used for Cloud Run
resource "google_bigquery_connection" "cloudrun_connection" {
  connection_id = "cloudrun"
  location      = var.region
  project       = google_project.nfl_0.project_id

  cloud_resource {}
  friendly_name = "Cloud Run Connection"
  description   = "Connection to Cloud Run for remote functions"
}

# Define the SQL for creating the BigQuery model
locals {
  sql_create_model_scripts = {
    nfltouchdown_cloudrun = "${path.module}/bigquery-sql/mdl.nfltouchdown_cloudrun.sql"
    # Add more SQL files as needed
  }
  service_url = "https://nfl-touchdown-${google_project.nfl_0.number}.${var.region}.run.app"
}

resource "random_id" "create_model_cloud_job_id" {
  byte_length = 4

  # Manually bump this version when you need to re-run the create model SQL
  keepers = {
    version = "v1.1"
  }
}

# Create the BigQuery Model using SQL
resource "google_bigquery_job" "create_model_cloud" {
  for_each = local.sql_create_model_scripts

  job_id   = "bq-job-${each.key}-${random_id.create_model_cloud_job_id.hex}"
  project  = google_project.nfl_0.project_id
  location = var.region

  query {
    query = templatefile(each.value, {
      cloud_run_url = local.service_url
    })
    use_legacy_sql = false
    # Ensure these values are blank for ML DDL statements
    create_disposition = ""
    write_disposition  = ""
  }

  depends_on = [
    google_bigquery_dataset.mdl
  ]

  lifecycle {
    ignore_changes = [
      query[0].write_disposition,
      query[0].create_disposition,
    ]
  }
}