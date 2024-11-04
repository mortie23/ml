# Misc
# Service account permissions for cloud functions
resource "google_project_iam_binding" "service_account_misc_ip_cf_run_admin" {
  project = google_project.misc_ip_1.project_id
  role    = "roles/run.admin"
  members = ["serviceAccount:${google_service_account.gsvc_misc_ip_cf.email}"]
}

resource "google_project_iam_binding" "service_account_misc_ip_cf_logging_logwriter" {
  project = google_project.misc_ip_1.project_id
  role    = "roles/logging.logWriter"
  members = ["serviceAccount:${google_service_account.gsvc_misc_ip_cf.email}"]
}

resource "google_project_iam_binding" "service_account_misc_ip_cf_artifactregistry_writer" {
  project = google_project.misc_ip_1.project_id
  role    = "roles/artifactregistry.writer"
  members = ["serviceAccount:${google_service_account.gsvc_misc_ip_cf.email}"]
}

resource "google_project_iam_binding" "service_account_misc_ip_cf_storage_objectadmin" {
  project = google_project.misc_ip_1.project_id
  role    = "roles/storage.objectAdmin"
  members = ["serviceAccount:${google_service_account.gsvc_misc_ip_cf.email}"]
}

resource "google_project_iam_binding" "service_account_misc_ip_cf_cloudbuild_builder" {
  project = google_project.misc_ip_1.project_id
  role    = "roles/cloudbuild.builds.builder"
  members = ["serviceAccount:${google_service_account.gsvc_misc_ip_cf.email}"]
}

resource "google_project_iam_member" "service_account_misc_ip_cf_bigquery_dataeditor" {
  project = google_project.misc_ip_1.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.gsvc_misc_ip_cf.email}"
}

resource "google_project_iam_member" "service_account_misc_ip_cf_bigquery_jobuser" {
  project = google_project.misc_ip_1.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.gsvc_misc_ip_cf.email}"
}