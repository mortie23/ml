# Misc
## Enable Org policy
resource "google_project_service" "misc_ip_org_policy" {
  project                    = google_project.misc_ip_1.project_id
  service                    = "orgpolicy.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

## Enable BigQuery API
resource "google_project_service" "misc_ip_bigquery" {
  project                    = google_project.misc_ip_1.project_id
  service                    = "bigquery.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

## Enable Cloud Functions API
resource "google_project_service" "misc_ip_cloud_functions" {
  project                    = google_project.misc_ip_1.project_id
  service                    = "cloudfunctions.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

## Enable Cloud Run API
resource "google_project_service" "misc_ip_cloud_run" {
  project                    = google_project.misc_ip_1.project_id
  service                    = "run.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

## Enable Cloud Build API
resource "google_project_service" "misc_ip_cloud_build" {
  project                    = google_project.misc_ip_1.project_id
  service                    = "cloudbuild.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}

## Enable Artifact Registry API
resource "google_project_service" "misc_ip_artifact_registry" {
  project                    = google_project.misc_ip_1.project_id
  service                    = "artifactregistry.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}