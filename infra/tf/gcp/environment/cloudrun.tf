# NFL
## Model prediction service
resource "google_cloud_run_service" "cr_nfl_predict" {
  project  = google_project.nfl_0.project_id
  name     = "nfl-predict"
  location = var.region

  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "0"
        "autoscaling.knative.dev/maxScale" = "10"
      }
    }
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/placeholder:latest"
        resources {
          limits = {
            memory = "8Gi"
            cpu    = "2"
          }
        }
        env {
          name  = "PROJECT_ID"
          value = google_project.nfl_0.project_id
        }
        env {
          name  = "AIP_STORAGE_URI"
          value = "gs://${google_storage_bucket.bkt_nfl_vertex_0.name}/model"
        }
        env {
          name  = "AIP_HEALTH_ROUTE"
          value = "/ping"
        }
        env {
          name  = "AIP_PREDICT_ROUTE"
          value = "/predict"
        }
      }
      timeout_seconds      = 180
      service_account_name = google_service_account.gsvc_nfl_vt.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true

  lifecycle {
    ignore_changes = [
      template[0].metadata[0].annotations["run.googleapis.com/client-name"],
      template[0].metadata[0].annotations["run.googleapis.com/client-version"],
      template[0].metadata[0].annotations["run.googleapis.com/cpu-throttling"],
      template[0].metadata[0].annotations["run.googleapis.com/sessionAffinity"],
      template[0].spec[0].containers[0].image,
      template[0].spec[0].containers[0].env,
      traffic,
      autogenerate_revision_name
    ]
  }
}