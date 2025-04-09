# Python applications published to Posit Connect

This is a simple Streamlit application structured as a modular project and managed using Poetry. The application is designed to be deployed to a Posit Connect server.
Reference:

- [https://github.com/streamlit/demo-face-gan/blob/master/streamlit_app.py](https://github.com/streamlit/demo-face-gan/blob/master/streamlit_app.py)
- [https://bookdown.org/**docs**/user/streamlit/](https://bookdown.org/__docs__/user/streamlit/)

## Project Structure

```
📁streamlit-posit-app
├── 📁streamlit_posit_app
│   └── 📁pages
│       └── __init__.py
│   │   └── home.py
├── 📁tests
│   └── __init__.py
├── app.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Configure Python applications on Posit Connect

Recommended installation of Python

https://docs.posit.co/resources/install-python.html

```sh
export PYTHON_VERSION="3.12.4"
curl -O https://cdn.rstudio.com/python/ubuntu-2404/pkgs/python-${PYTHON_VERSION}_1_amd64.deb
sudo apt-get update
sudo apt-get install ./python-${PYTHON_VERSION}_1_amd64.deb

# check install
/opt/python/"${PYTHON_VERSION}"/bin/python --version
```

https://docs.posit.co/connect/admin/python/

```ini
; /etc/rstudio-connect/rstudio-connect.gcfg
[Python]
Enabled = true
Executable = /opt/python/3.12.4/bin/python3
```

## Local

Setup our local development environment (WSL2 on Dell XPS Windows 11)

```sh
python3 -m venv ~/venv/posit
source ~/venv/posit/bin/activate
pip install poetry
```

All packages will be managed by poetry. We created this EDA directory with:

```sh
poetry new ./posit-connect-python
```

Then add a package with

```sh
poetry add rsconnect-python
```

But we do not do this manually if restoring from this repo:

```sh
poetry lock && poetry install --no-root
```

## Running the App

To run the Streamlit application locally, use the following command:

```sh
poetry run streamlit run app.py
# or just
streamlit run app.py
```

### Deployment

To deploy the app to a Posit Connect server, ensure you have the `rsconnect-python` package listed in your `requirements.txt`. Use the following command to deploy:

```sh
# This didn't work
rsconnect add --name vm --server http://192.168.110.133:3939 --api-key <api-key>
# This worked
rsconnect deploy streamlit --server http://192.168.110.133:3939 --api-key <api-key> --entrypoint app.py .
```

![](./img/deployed.png)
