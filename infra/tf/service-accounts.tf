# Misc
## Cloud functions
resource "google_service_account" "gsvc_misc_ip_cf" {
  project      = google_project.misc_ip_1.project_id
  account_id   = "gsvc-xyz-${var.env}-misc-ip-cf"
  display_name = "Cloud Function Service Account"
}