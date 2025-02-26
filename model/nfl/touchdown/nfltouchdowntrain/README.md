# NFL Touchdown training

## Setup

If you have not already, create a virtual environment.

```sh
python3 -m venv ~/venv/nfltouchdowntrain/
source ~/venv/nfltouchdowntrain/bin/activate
```

Use poetry to install all packages.

```sh
poetry lock && poetry install --no-root
```

```sh
python3 -m ipykernel install --user --name nfltouchdowntrain
```

## Build and publish

First authenticate you `gcloud` cli.

```sh
gcloud auth login
```
