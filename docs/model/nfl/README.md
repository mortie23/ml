# Deploying ML Models on Cloud Run: From Placeholder to Production

This guide walks through deploying a machine learning model on Google Cloud Run, using a two-phase deployment strategy: placeholder service followed by model deployment.

## Phase 1: Placeholder Service

First, we deploy a minimal nginx container that serves a simple status endpoint. This helps us establish our infrastructure and permissions before deploying the actual model.

### Placeholder Container Structure

```
devops/serve/placeholder/
├── Dockerfile
├── nginx.conf
└── status.json
```

Our placeholder service uses nginx to serve a static JSON response:

```nginx
server {
    listen 8080;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        try_files /status.json =404;
        default_type application/json;
    }
}
```

### Initial Deployment

The placeholder is deployed via Terraform:

```hcl
resource "google_cloud_run_service" "cr_nfl_predict" {
  name     = "nfl-touchdown"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/placeholder:latest"
        // ...configuration...
      }
    }
  }
}
```

![Placeholder service running in Cloud Run console]()

## Phase 2: Model Training and Deployment

### Training on Vertex AI

Using our custom `modelporter` CLI tool:

```bash
modelporter --env=dev nfl.touchdown train --service=vertex
```

This command:

1. Initiates a training job on Vertex AI
2. Saves the trained model to GCS bucket
3. Registers the model in Vertex AI registry

![Vertex AI training job progress]()

### Deploying the Model Service

Once training is complete, we deploy our FastAPI prediction service:

```bash
modelporter --env=dev nfl.touchdown serve
```

Behind the scenes, `modelporter`:

1. Locates the latest trained model in Vertex AI
2. Updates the Cloud Run service with our prediction container
3. Configures environment variables to point to the model in GCS

```python
# Key environment variables set during deployment
env = [
    {"name": "AIP_STORAGE_URI", "value": model.uri},
    {"name": "AIP_PREDICT_ROUTE", "value": "/predict"},
    {"name": "PROJECT_ID", "value": project_id}
]
```

![Cloud Run service updated with prediction container]()

## Architecture Overview

The final architecture connects these components:

1. Cloud Run service running our prediction container
2. Model artifacts stored in Cloud Storage
3. BigQuery for making predictions via remote functions

![Architecture diagram showing component interactions]()

## Testing the Deployment

You can verify the deployment using:

```bash
# Test health check
curl https://nfl-touchdown-<hash>.a.run.app/ping

# Make a prediction
curl -X POST https://nfl-touchdown-<hash>.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"instances": [...]}'
```

## Infrastructure as Code

All components are managed via Terraform:

- Cloud Run service configuration
- IAM permissions
- BigQuery connections
- Storage buckets

This ensures consistent deployments across environments and makes it easy to replicate the setup.

![Terraform plan showing resource creation]()

The complete solution demonstrates a production-ready ML serving infrastructure that's both scalable and maintainable.

> TODO:

# Deploy a model

## Training

```sh
modelporter --env=dev nfl.touchdown train --service=vertex
No existing model found with display name 'nfl-touchdown'. Creating a new model.
⠴ Training model nfl.touchdown is training on vertex....Training Output directory:
gs://bkt-xyz-dev-nfl-vertex-0/aiplatform-custom-training-2025-02-28-16:29:02.387
⠼ Training model nfl.touchdown is training on vertex....View Training:
https://console.cloud.google.com/ai/platform/locations/australia-southeast1/training/<training-job-id>?project=<project-number>
⠸ Training model nfl.touchdown is training on vertex....CustomContainerTrainingJob projects/<project-number>/locations/australia-southeast1/trainingPipelines/<training-job-id> current state:
PipelineState.PIPELINE_STATE_RUNNING
View backing custom job:
https://console.cloud.google.com/ai/platform/locations/australia-southeast1/training/<id>?project=<project-number>
⠴ Training model nfl.touchdown is training on vertex....CustomContainerTrainingJob projects/<project-number>/locations/australia-southeast1/trainingPipelines/<training-job-id> current state:
PipelineState.PIPELINE_STATE_RUNNING
⠙ Training model nfl.touchdown is training on vertex....CustomContainerTrainingJob run completed. Resource name: projects/<project-number>/locations/australia-southeast1/trainingPipelines/<training-job-id>
⠴ Training model nfl.touchdown is training on vertex....Model available at projects/<project-number>/locations/australia-southeast1/models/<model-id>
```

## Prediction service

```sh
modelporter --env=dev nfl.touchdown serve
```

```log
Waiting for operation to complete...
Cloud Run service updated. URL: https://nfl-touchdown-<>.a.run.app
```
