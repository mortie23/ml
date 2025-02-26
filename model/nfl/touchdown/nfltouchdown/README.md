# NFL Touchdown

Common re use modules for the NFL Touchdown model that can be used in both train and predict

## Setup

If you have not already, create a virtual environment.

```sh
python3 -m venv ~/venv/nfltouchdown/
source ~/venv/nfltouchdown/bin/activate
```

Use poetry to install all packages.

```sh
poetry lock && poetry install --no-root
```

## Development

We will primarily use our tests for development.

```sh
# Example of development of the io
# Add a breakpoint() to the code where you want to test the new feature or bugfix
python -m pytest tests/test_io.py::test_get_data
```

## Build publish

> You may need to bump the version of the package in the `pyproject.toml` before building.

Using the `cloudbuild.sh --env dev`

## Reference: Using Poetry to add to remote cache

```sh
poetry source add --priority=primary vpy https://australia-southeast1-python.pkg.dev/prj-xyz-shr-rep-0/rpo-py-0/simple/
```

## Legacy: manual way

For reference if testing manually using poetry

```sh
# Update poetry
poetry self update
# Add Google artifact registry keyring to poetry
poetry self add keyrings.google-artifactregistry-auth
# Check the python repository on GCP
gcloud artifacts print-settings python \
    --project=prj-xyz-shr-rep-0 \
    --repository=rpo-py-0 \
    --location=australia-southeast1

# Configure a poetry repository to point to the python artifact registry
poetry config repositories.gcp-shr-0 https://australia-southeast1-python.pkg.dev/prj-xyz-shr-rep-0/rpo-py-0/
# publish the package to the repository
poetry publish --build --repository gcp-shr-0
```
