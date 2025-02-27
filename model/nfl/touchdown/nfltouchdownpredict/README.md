# NFL Touchdown predict

## Setup

```sh
# If using pyenv
~/.pyenv/versions/3.10.7/bin/python3 -m venv ~/venv/nfltouchdownpredict
# If using a single python install
python3 -m venv ~/venv/nfltouchdownpredict
source ~/venv/nfltouchdownpredict/bin/activate
```

## Install dependencies

```sh
# Using remote virtual repo
gcloud auth login
gcloud auth application-default login
poetry lock && poetry install --no-root
```

## Running a local predict service

```sh
fastapi run predict.py --port 8080
```

## Testing the service

Open up the Swagger docs [http://localhost:8080/docs#](http://localhost:8080/docs#), and use the **Try it out** for the predict endpoint.

## Build and publish

First authenticate you `gcloud` cli.

```sh
gcloud auth login
```

Execute the `gcloud` statement in the `cloudbuild.sh` script.
