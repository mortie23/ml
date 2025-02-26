# Enterprise resource
## Custom build images
resource "google_artifact_registry_repository" "repo_bld_dkr" {
  project       = google_project.rep_0.project_id
  repository_id = "rpo-bld-dkr-0"
  format        = "DOCKER"
  location      = var.region
  description   = "Docker repository for containers used in build"

  depends_on = [
    google_project.rep_0,
    google_project_service.rep_artifact_registry,
  ]
}

## Remote cache of PyPI packages
resource "google_artifact_registry_repository" "repo_pypi" {
  project       = google_project.rep_0.project_id
  repository_id = "rpo-pypi-0"
  description   = "Python PyPI remote repository"
  format        = "PYTHON"
  location      = var.region
  mode          = "REMOTE_REPOSITORY"

  remote_repository_config {
    description = "PyPI"
    python_repository {
      public_repository = "PYPI"
    }
  }

  depends_on = [
    google_project.rep_0,
    google_project_service.rep_artifact_registry,
  ]
}

## Custom internal Python packages
resource "google_artifact_registry_repository" "repo_py" {
  project       = google_project.rep_0.project_id
  repository_id = "rpo-py-0"
  format        = "PYTHON"
  location      = var.region
  description   = "Python package repository for custom packages"
}

## Virtual repository linked to both internal and remote cache
resource "google_artifact_registry_repository" "repo_vpy" {
  project       = google_project.rep_0.project_id
  repository_id = "rpo-vpy-0"
  description   = "Python PyPI virtual repository"
  format        = "PYTHON"
  location      = var.region
  mode          = "VIRTUAL_REPOSITORY"

  virtual_repository_config {
    upstream_policies {
      id         = "custom"
      repository = google_artifact_registry_repository.repo_py.id
      priority   = 100
    }
    upstream_policies {
      id         = "remote"
      repository = google_artifact_registry_repository.repo_pypi.id
      priority   = 50
    }
  }

  depends_on = [
    google_artifact_registry_repository.repo_pypi,
    google_artifact_registry_repository.repo_py
  ]
}