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

# NFL
# Dataform permissions
resource "google_service_account_iam_member" "service_account_df_user_binding" {
  service_account_id = google_service_account.gsvc_nfl_df.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:service-${google_project.nfl_0.number}@gcp-sa-dataform.iam.gserviceaccount.com"
}

resource "google_service_account_iam_member" "service_account_df_token_creator_binding" {
  service_account_id = google_service_account.gsvc_nfl_df.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:service-${google_project.nfl_0.number}@gcp-sa-dataform.iam.gserviceaccount.com"
}

# Grant the Secret Manager access role at the project level
resource "google_project_iam_member" "service_account_dfdefault_secret_accessor" {
  project = google_project.nfl_0.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:service-${google_project.nfl_0.number}@gcp-sa-dataform.iam.gserviceaccount.com"
}

# Grant roles to the Dataform service account
resource "google_project_iam_member" "service_account_df_bigquery_data_editor" {
  project = google_project.nfl_0.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_df.email}"
}

resource "google_project_iam_member" "service_account_df_bigquery_data_viewer" {
  project = google_project.nfl_0.project_id
  role    = "roles/bigquery.dataViewer"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_df.email}"
}

resource "google_project_iam_member" "service_account_df_bigquery_job_user" {
  project = google_project.nfl_0.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_df.email}"
}

resource "google_project_iam_member" "service_account_df_bigquery_data_owner" {
  project = google_project.nfl_0.project_id
  role    = "roles/bigquery.dataOwner"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_df.email}"
}

resource "google_project_iam_member" "service_account_df_bigquery_user" {
  project = google_project.nfl_0.project_id
  role    = "roles/bigquery.user"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_df.email}"
}

resource "google_project_iam_member" "service_account_df_storage_viewer_hs" {
  project = google_project.nfl_0.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_df.email}"
}

resource "google_project_iam_member" "service_account_df_run_invoker_hs" {
  project = google_project.nfl_0.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_df.email}"
}

### Custom Role for BigQuery connection
resource "google_project_iam_custom_role" "role_bigquery_connection_user" {
  role_id     = "custom_rl_bigquery_conusr"
  title       = "BigQuery Connection User"
  description = "Custom role to use BigQuery connections"
  project     = google_project.nfl_0.project_id
  permissions = [
    "bigquery.connections.use",
  ]
}

resource "google_project_iam_member" "custom_role_binding" {
  project = google_project.nfl_0.project_id
  role    = "projects/${google_project.nfl_0.project_id}/roles/custom_rl_bigquery_conusr"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_df.email}"
}

## Cloud Build
resource "google_project_iam_member" "service_account_nfl_cb_storage_objectadmin" {
  project = google_project.nfl_0.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_cb.email}"
}
resource "google_project_iam_member" "service_account_nfl_cb_nfl_artifactregistry_writer" {
  project = google_project.nfl_0.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_cb.email}"
}
resource "google_project_iam_member" "service_account_cb_logging_logwriter" {
  project = google_project.nfl_0.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_cb.email}"
}
resource "google_project_iam_member" "service_account_nfl_cb_cloudbuild_builder" {
  project = google_project.nfl_0.project_id
  role    = "roles/cloudbuild.builds.builder"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_cb.email}"
}
### Cloud build SA needs to read and write to and from the shared Artifact Registry
resource "google_project_iam_member" "service_account_nfl_cb_rep_artifactregistry_reader" {
  project = "prj-xyz-shr-rep-0"
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_cb.email}"
}
resource "google_project_iam_member" "service_account_nfl_cb_rep_artifactregistry_writer" {
  project = "prj-xyz-shr-rep-0"
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_cb.email}"
}

## Vertex AI
resource "google_project_iam_member" "service_account_nfl_vt_aiplatform_user" {
  project = google_project.nfl_0.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_vt.email}"
}
resource "google_project_iam_member" "service_account_nfl_vt_artifactregistry_reader" {
  project = google_project.nfl_0.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_vt.email}"
}
resource "google_project_iam_member" "service_account_nfl_vt_storage_objectviewer" {
  project = google_project.nfl_0.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_vt.email}"
}
# Allow Vertex service account to read from shared repository
resource "google_project_iam_member" "service_account_nfl_vt_rep_artifactregistry_reader" {
  project = "prj-xyz-shr-rep-0"
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.gsvc_nfl_vt.email}"
}

# Allow Cloud Run Service Agent to read from shared repository
resource "google_project_iam_member" "service_account_nfl_cr_rep_artifactregistry_reader" {
  project = "prj-xyz-shr-rep-0"
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:service-${google_project.nfl_0.number}@serverless-robot-prod.iam.gserviceaccount.com"
}
