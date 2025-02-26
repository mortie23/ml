# Shared operational services outside the software development life cycle
## For terraform state.
## ! Create outside terraform. Here for reference
/*
resource "google_project" "ops_0" {
  name            = "prj-xyz-shr-ops-0"
  project_id      = "prj-xyz-shr-ops-0"
  billing_account = var.billing_account
}
*/

## For repositories 
resource "google_project" "rep_0" {
  name            = "prj-xyz-shr-rep-0"
  project_id      = "prj-xyz-shr-rep-0"
  billing_account = var.billing_account
}