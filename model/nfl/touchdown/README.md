# Model to predict the touchdowns of a team based on other statistics

A way to implement a custom model in Vertex AI with custom Docker images.

## Getting started

Create an environment variable file.
For the development environment (running on a local development machine) we need to mock the environment for the Vertex AI service.

`.env`

Use the contents of the `.env.example` file.

## Training

We have built a custom training image ignoring the standard Google provided base image. This is because we found a lot of issues with the pre-built images that Google provides. For example trying to use:

- [us-docker.pkg.dev/vertex-ai/training/scikit-learn-cpu.0-23](us-docker.pkg.dev/vertex-ai/training/scikit-learn-cpu.0-23)

```log
InvalidArgument: 400 The image <> is not supported. Please use an image offered by Vertex AI for python package training
```

## Predicting

We also need a custom internal region prediction image. Similar reasons:

- [gcr.io/cloud-aiplatform/prediction/sklearn-cpu.1-0:latest](gcr.io/cloud-aiplatform/prediction/sklearn-cpu.1-0:latest)

These images were completely different, in fact the 1.0, when interactively looking at the Docker image seemed to be `CONTAINER_NAME=tf2-cpu/2-8`, i.e. a TensorFlow prediction image.
