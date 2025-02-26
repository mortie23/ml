# Bucket for terraform state files
## ! Create outside terraform. Here for reference
/*
resource "google_storage_bucket" "bkt_ops_tfstate_0" {
  name     = "bkt-xyz-ops-tfstate-0"
  location = var.region
  project  = google_project.ops_0.project_id

  # Optional: Define storage class, versioning, etc.
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}
*/