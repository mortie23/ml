# Misc
## Cloud function
resource "google_storage_bucket" "bkt_misc_ip_misc_ip_fn_0" {
  name     = "bkt-xyz-${var.env}-misc-ip-fn-0"
  location = var.region
  project  = google_project.misc_ip_1.project_id

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}