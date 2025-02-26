# NFL
## Custom train and predict model images
resource "google_artifact_registry_repository" "repo_nfl_dkr" {
  project       = google_project.nfl_0.project_id
  repository_id = "rpo-xyz-${var.env}-nfl-dkr-0"
  format        = "DOCKER"
  location      = var.region
  description   = "Docker repository for NFL"
}