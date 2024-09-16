# AFL Teams web scraping

```sh
gcloud services enable iam.googleapis.com
gcloud services enable run.googleapis.com --project=prj-xyz-dev-fruit-0
```

## Creation of BigQuery dataset for Horizon Scanning

```sh
bq mk --location=australia-southeast1 --project_id=prj-xyz-dev-fruit-0 afl
```

## Setup of the Cloud Build things

Create a custom bucket for the source code

```sh
gcloud storage buckets create --location=australia-southeast1 --project=prj-xyz-dev-fruit-0 gs://bkt-xyz-dev-afl-fn-0
```

## Create service accounts for Cloud Functions and Cloud Build

```sh
# Create a service account
gcloud iam service-accounts create sa-xyz-dev-fruit-cf --display-name "Cloud Function Service Account"
# Allow gcp-developers to act as the Cloud Function service account for deployment
gcloud iam service-accounts add-iam-policy-binding sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com --member='group:gcp-developers@tremendousdomain.xyz' --role='roles/iam.serviceAccountUser'
# Allow developers to invoke functions
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member='group:gcp-developers@tremendousdomain.xyz' --role='roles/run.invoker'
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="group:gcp-developers@tremendousdomain.xyz" --role="roles/cloudfunctions.invoker"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="group:gcp-developers@tremendousdomain.xyz" --role="roles/cloudfunctions.developer"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="group:gcp-developers@tremendousdomain.xyz" --role="roles/cloudfunctions.viewer"
# Give service account permissions to all the things needed (might be too many permissions)
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/cloudfunctions.invoker"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/cloudfunctions.developer"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/cloudfunctions.viewer"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/logging.logWriter"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/artifactregistry.writer"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/storage.objectAdmin"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/cloudbuild.builds.builder"
# Added this one after getting error below. Cloud Functions use Cloud Run it seems
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/run.admin"
# Needed for the BigQuery part after getting bigquery/client.py errors
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/bigquery.dataEditor"
gcloud projects add-iam-policy-binding prj-xyz-dev-fruit-0 --member="serviceAccount:sa-xyz-dev-fruit-cf@prj-xyz-dev-fruit-0.iam.gserviceaccount.com" --role="roles/bigquery.jobUser"
```

## Error:

```log
Preparing function...done.
✓ Deploying function...
  ✓ [Build] Logs are available at [https://console.cloud.google.com/cloud-build/builds;region=australia-southeast1/xyz]
  ✓ [Service]
  . [ArtifactRegistry]
  . [Healthcheck]
  . [Triggercheck]
Done.
ERROR: (gcloud.functions.deploy) ResponseError:
  status=[403],
  code=[Ok],
  message=[Permission 'run.services.setIamPolicy' denied on resource 'projects/prj-xyz-dev-fruit-0/locations/australia-southeast1/services/fn-afl-teams-0' (or resource may not exist).]
```

## Calling

```sh
# This will work
curl https://australia-southeast1-prj-xyz-dev-fruit-0.cloudfunctions.net/fn-afl-teams-0 -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```
