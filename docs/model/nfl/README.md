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
