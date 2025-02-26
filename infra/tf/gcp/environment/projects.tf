terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("~/.config/gcloud/application_default_credentials.json")
  region      = var.region
}

resource "google_project" "misc_ip_1" {
  name            = "prj-xyz-${var.env}-misc-ip-1"
  project_id      = "prj-xyz-${var.env}-misc-ip-1"
  billing_account = var.billing_account
}

resource "google_project" "nfl_0" {
  name            = "prj-xyz-${var.env}-nfl-0"
  project_id      = "prj-xyz-${var.env}-nfl-0"
  billing_account = var.billing_account
}