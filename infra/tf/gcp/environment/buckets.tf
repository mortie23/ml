# Misc
## Cloud function
resource "google_storage_bucket" "bkt_misc_ip_misc_ip_fn_0" {
  name     = "bkt-xyz-${var.env}-misc-ip-fn-0"
  location = var.region
  project  = google_project.misc_ip_1.project_id

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}

# NFL
## Raw source data
resource "google_storage_bucket" "bkt_nfl_raw_0" {
  name     = "bkt-xyz-${var.env}-nfl-raw-0"
  location = var.region
  project  = google_project.nfl_0.project_id

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}
## For Vertex registered models
resource "google_storage_bucket" "bkt_nfl_vertex_0" {
  name     = "bkt-xyz-${var.env}-nfl-vertex-0"
  location = var.region
  project  = google_project.nfl_0.project_id

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}

## For Cloud Build logs
resource "google_storage_bucket" "bkt_nfl_cblog_0" {
  name     = "bkt-xyz-${var.env}-nfl-cblog-0"
  location = var.region
  project  = google_project.nfl_0.project_id

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}