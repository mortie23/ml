resource "google_secret_manager_secret" "sct_devops_ssh" {
  project   = google_project.nfl_0.project_id
  secret_id = "sct-dataform-ssh-key"
  replication {
    user_managed {
      replicas {
        location = "australia-southeast1"
      }
    }
  }
  depends_on = [google_project_service.secretmanager]
}