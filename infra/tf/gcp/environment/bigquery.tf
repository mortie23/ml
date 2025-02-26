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