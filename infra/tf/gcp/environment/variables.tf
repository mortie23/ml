variable "env" {
  description = "The environment for this deployment (e.g. dev, ppd, prd)"
  type        = string
}

variable "billing_account" {
  description = "The GCP Billing account for the folder"
  type        = string
}

variable "region" {
  description = "The GCP region for the deployment"
  type        = string
}