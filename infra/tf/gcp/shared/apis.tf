### Enable Artifact Registry API
resource "google_project_service" "rep_artifact_registry" {
  project                    = google_project.rep_0.project_id
  service                    = "artifactregistry.googleapis.com"
  disable_on_destroy         = true
  disable_dependent_services = true
}