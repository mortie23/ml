# GCP Cloud Function IP Checker

A GCP Cloud Function that checks the public IP address the Cloud Function uses.

## Usage

### Dev

Install all packages on a local _venv_.
Create the _venv_.

```sh
python3 -m venv ~/venv/fn_misc_ipchecker
source ~/venv/fn_misc_ipchecker/bin/activate
pip install poetry
```

Use poetry to install everything else.

```sh
poetry lock && poetry install --no-root
python3 -m ipykernel install --user --name fn_misc_ipchecker
```

Ensure you are authenticated

```sh
gcloud atuh application-default login
```

Open the Python script (in this case in VScode), and ensure the active kernel is the _venv_.

Run the script in interactive.

If you have updated any packages in the `pytproject.toml` then export to the requirements file.

```sh
poetry export --without-hashes --format=requirements.txt > ./src/requirements.txt
```

## Deploy

To deploy the funciton run the deploy script passing the target environment.

```sh
./deploy.sh --env dev
```

## Calling

To test calling the Cloud Function we can use a basic curl. Ensure you are logged in as a user that has invoke permissions.

```sh
curl https://australia-southeast1-prj-xyz-dev-misc-ip-1.cloudfunctions.net/fn-misc-ipchecker-0 -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```

## Testing

To run the unit tests during development we can run this:

```sh
pytest ./tests/test_fn-misc-ipchecker.py::test_ip_checker
```

```log
====================== test session starts ===========================
platform linux -- Python 3.10.7, pytest-8.3.3, pluggy-1.5.0
rootdir: /mnt/c/git/github/mortie23/ml/eng/misc/fn-misc-ipchecker
configfile: pytest.ini
plugins: env-1.1.5, hydra-core-1.3.2
collected 1 item

tests/test_fn-misc-ipchecker.py .                               [100%]

====================== 1 passed in 2.72s =============================
```
