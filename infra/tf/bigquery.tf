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