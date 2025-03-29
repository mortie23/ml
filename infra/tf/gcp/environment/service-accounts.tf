# Misc
## Cloud functions
resource "google_service_account" "gsvc_misc_ip_cf" {
  project      = google_project.misc_ip_1.project_id
  account_id   = "gsvc-xyz-${var.env}-misc-ip-cf"
  display_name = "Cloud Function Service Account"
}

# NFL
## Dataform
resource "google_service_account" "gsvc_nfl_df" {
  project      = google_project.nfl_0.project_id
  account_id   = "gsvc-xyz-${var.env}-nfl-df"
  display_name = "Dataform Service Account for NFL"
}
## Cloud Build
resource "google_service_account" "gsvc_nfl_cb" {
  project      = google_project.nfl_0.project_id
  account_id   = "gsvc-xyz-${var.env}-nfl-cb"
  display_name = "Cloud Build Service Account for NFL"
}
## Vertex AI
resource "google_service_account" "gsvc_nfl_vt" {
  project      = google_project.nfl_0.project_id
  account_id   = "gsvc-xyz-${var.env}-nfl-vt"
  display_name = "Vertex AI Service Account for NFL"
}