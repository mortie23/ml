# Mono repo with Python Poetry

Testing

[Source](https://medium.com/opendoor-labs/our-python-monorepo-d34028f2b6fa)

## Fresh venv

```sh
mkdir ~/venv
cd ~/venv
python3 -m venv poetry
source poetry/bin/activate
```

Clone this Git repo

```sh

```

## Getting started with Poetry

Install requirements (just poetry) the rest poetry will handle.

```sh
pip install -r requirements.txt
```

## Using Poetry to install Python packages

Now using poetry to install the packages (including the internal one)

```sh
cd flask-app-1/flask-app-1
poetry lock && poetry install
```

```log
Updating dependencies
Resolving dependencies... (1.8s)

Writing lock file
Installing dependencies from lock file

...
```

Run the app with poetry. This app sources from the internal package in dev mode, so changes made to the source files are reflected as they change.

```sh
poetry run python3 app.py
```

```sh
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
127.0.0.1 - - [15/Feb/2023 19:33:46] "GET / HTTP/1.1" 200 -
```

![](docs/browser-poetry-flask.png)

## Testing internal package for EDA

```sh
cd eda/eda-project-1/
poetry lock && poetry install
```

```log
Updating dependencies
Resolving dependencies... (1.8s)

Writing lock file
Installing dependencies from lock file

...
```

Register the ipykernel

```sh
python3 -m ipykernel install --user --name=poetry
```

![](docs/vscode-jupyter-interactive.png)

## Internal package dependency

Since we are using poetry to manage the internal package as a dependency in the mono repo, it works in development mode on own local client machine, however the Docker container will not have access to the internal package.

We can either:
- deploy the package to an internal package server
- copy the internal package from the mono repo temporarily for the building of the docker image
There are probably other options, but the simplest for this small example was the second option. the build step does this.

## Build the docker container

```sh
cd tools/build/
chmod +x build.sh
./build.sh flask-app-1
```

```log
flask-app-1
sending incremental file list
created directory ../../flask-app-1/flask-app-1/lib
./
helloworld/
helloworld/README.md
helloworld/pyproject.toml
helloworld/helloworld/
helloworld/helloworld/__init__.py
helloworld/helloworld/helloworld.py
helloworld/helloworld/__pycache__/
helloworld/helloworld/__pycache__/__init__.cpython-39.pyc
helloworld/helloworld/__pycache__/helloworld.cpython-39.pyc
helloworld/tests/
helloworld/tests/__init__.py
helloworld/tests/sayhello_tests.py

sent 2,025 bytes  received 247 bytes  4,544.00 bytes/sec
total size is 1,216  speedup is 0.54
Sending build context to Docker daemon  37.89kB
Step 1/11 : FROM python:3.8-buster
3.8-buster: Pulling from library/python
b2404786f3fe: Pull complete 
e97ef50ee5a8: Pull complete 
dfb1477a1a0e: Pull complete 
838447eff6a7: Pull complete 
61f659024e30: Pull complete 
0a27566d127a: Pull complete 
93e0efd44924: Pull complete 
3ecf63890d25: Pull complete 
d9a83bb06b35: Pull complete 
Digest: sha256:25d2f418db3891aa88df92fd974875f326188f816a5a64e0b99a2095dd9f01a1
Status: Downloaded newer image for python:3.8-buster
 ---> d98cbcebcd8b
Step 2/11 : ARG YOUR_ENV
 ---> Running in 2553d52e23a0
Removing intermediate container 2553d52e23a0
 ---> 8935d9af192d
Step 3/11 : ENV YOUR_ENV=DEV   POETRY_VERSION=1.3.2
 ---> Running in 8124c84a8579
Removing intermediate container 8124c84a8579
 ---> 1eba5f10906f
Step 4/11 : RUN pip install "poetry==$POETRY_VERSION"
 ---> Running in 711f4aa8d500
Collecting poetry==1.3.2
  Downloading poetry-1.3.2-py3-none-any.whl (218 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 218.9/218.9 KB 1.6 MB/s eta 0:00:00
Collecting cleo<3.0.0,>=2.0.0
  Downloading cleo-2.0.1-py3-none-any.whl (77 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 77.3/77.3 KB 519.8 kB/s eta 0:00:00
Collecting trove-classifiers>=2022.5.19
  Downloading trove_classifiers-2023.2.8-py3-none-any.whl (13 kB)
Collecting tomlkit!=0.11.2,!=0.11.3,<1.0.0,>=0.11.1
  Downloading tomlkit-0.11.6-py3-none-any.whl (35 kB)
Collecting crashtest<0.5.0,>=0.4.1
  Downloading crashtest-0.4.1-py3-none-any.whl (7.6 kB)
Collecting poetry-core==1.4.0
  Downloading poetry_core-1.4.0-py3-none-any.whl (546 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 546.4/546.4 KB 4.7 MB/s eta 0:00:00
Collecting pkginfo<2.0,>=1.5
  Downloading pkginfo-1.9.6-py3-none-any.whl (30 kB)
Collecting requests-toolbelt<0.11.0,>=0.9.1
  Downloading requests_toolbelt-0.10.1-py2.py3-none-any.whl (54 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 54.5/54.5 KB 2.6 MB/s eta 0:00:00
Collecting dulwich<0.21.0,>=0.20.46
  Downloading dulwich-0.20.50-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (502 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 502.2/502.2 KB 5.1 MB/s eta 0:00:00
Collecting tomli<3.0.0,>=2.0.1
  Downloading tomli-2.0.1-py3-none-any.whl (12 kB)
Collecting virtualenv!=20.4.5,!=20.4.6,<21.0.0,>=20.4.3
  Downloading virtualenv-20.19.0-py3-none-any.whl (8.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.7/8.7 MB 812.6 kB/s eta 0:00:00
Collecting packaging>=20.4
  Downloading packaging-23.0-py3-none-any.whl (42 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42.7/42.7 KB 287.2 kB/s eta 0:00:00
Collecting urllib3<2.0.0,>=1.26.0
  Downloading urllib3-1.26.14-py2.py3-none-any.whl (140 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 140.6/140.6 KB 339.7 kB/s eta 0:00:00
Collecting poetry-plugin-export<2.0.0,>=1.2.0
  Downloading poetry_plugin_export-1.3.0-py3-none-any.whl (10 kB)
Collecting cachecontrol[filecache]<0.13.0,>=0.12.9
  Downloading CacheControl-0.12.11-py2.py3-none-any.whl (21 kB)
Collecting importlib-metadata<5.0,>=4.4
  Downloading importlib_metadata-4.13.0-py3-none-any.whl (23 kB)
Collecting requests<3.0,>=2.18
  Downloading requests-2.28.2-py3-none-any.whl (62 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.8/62.8 KB 448.2 kB/s eta 0:00:00
Collecting shellingham<2.0,>=1.5
  Downloading shellingham-1.5.0.post1-py2.py3-none-any.whl (9.4 kB)
Collecting lockfile<0.13.0,>=0.12.2
  Downloading lockfile-0.12.2-py2.py3-none-any.whl (13 kB)
Collecting pexpect<5.0.0,>=4.7.0
  Downloading pexpect-4.8.0-py2.py3-none-any.whl (59 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 59.0/59.0 KB 274.5 kB/s eta 0:00:00
Collecting keyring<24.0.0,>=23.9.0
  Downloading keyring-23.13.1-py3-none-any.whl (37 kB)
Collecting platformdirs<3.0.0,>=2.5.2
  Downloading platformdirs-2.6.2-py3-none-any.whl (14 kB)
Collecting jsonschema<5.0.0,>=4.10.0
  Downloading jsonschema-4.17.3-py3-none-any.whl (90 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 90.4/90.4 KB 698.4 kB/s eta 0:00:00
Collecting html5lib<2.0,>=1.0
  Downloading html5lib-1.1-py2.py3-none-any.whl (112 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 112.2/112.2 KB 676.0 kB/s eta 0:00:00
Collecting filelock<4.0.0,>=3.8.0
  Downloading filelock-3.9.0-py3-none-any.whl (9.7 kB)
Collecting msgpack>=0.5.2
  Downloading msgpack-1.0.4-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (322 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 322.5/322.5 KB 695.9 kB/s eta 0:00:00
Collecting rapidfuzz<3.0.0,>=2.2.0
  Downloading rapidfuzz-2.13.7-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.2/2.2 MB 1.0 MB/s eta 0:00:00
Collecting webencodings
  Downloading webencodings-0.5.1-py2.py3-none-any.whl (11 kB)
Collecting six>=1.9
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Collecting zipp>=0.5
  Downloading zipp-3.13.0-py3-none-any.whl (6.7 kB)
Collecting importlib-resources>=1.4.0
  Downloading importlib_resources-5.10.2-py3-none-any.whl (34 kB)
Collecting pkgutil-resolve-name>=1.3.10
  Downloading pkgutil_resolve_name-1.3.10-py3-none-any.whl (4.7 kB)
Collecting attrs>=17.4.0
  Downloading attrs-22.2.0-py3-none-any.whl (60 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.0/60.0 KB 545.6 kB/s eta 0:00:00
Collecting pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0
  Downloading pyrsistent-0.19.3-py3-none-any.whl (57 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.5/57.5 KB 781.8 kB/s eta 0:00:00
Collecting jeepney>=0.4.2
  Downloading jeepney-0.8.0-py3-none-any.whl (48 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 48.4/48.4 KB 847.9 kB/s eta 0:00:00
Collecting SecretStorage>=3.2
  Downloading SecretStorage-3.3.3-py3-none-any.whl (15 kB)
Collecting jaraco.classes
  Downloading jaraco.classes-3.2.3-py3-none-any.whl (6.0 kB)
Collecting ptyprocess>=0.5
  Downloading ptyprocess-0.7.0-py2.py3-none-any.whl (13 kB)
Collecting idna<4,>=2.5
  Downloading idna-3.4-py3-none-any.whl (61 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.5/61.5 KB 568.3 kB/s eta 0:00:00
Collecting charset-normalizer<4,>=2
  Downloading charset_normalizer-3.0.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (195 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 195.4/195.4 KB 602.6 kB/s eta 0:00:00
Collecting certifi>=2017.4.17
  Downloading certifi-2022.12.7-py3-none-any.whl (155 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 155.3/155.3 KB 429.6 kB/s eta 0:00:00
Collecting distlib<1,>=0.3.6
  Downloading distlib-0.3.6-py2.py3-none-any.whl (468 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 468.5/468.5 KB 640.6 kB/s eta 0:00:00
Collecting cryptography>=2.0
  Downloading cryptography-39.0.1-cp36-abi3-manylinux_2_28_x86_64.whl (4.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 756.0 kB/s eta 0:00:00
Collecting more-itertools
  Downloading more_itertools-9.0.0-py3-none-any.whl (52 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 52.8/52.8 KB 574.5 kB/s eta 0:00:00
Collecting cffi>=1.12
  Downloading cffi-1.15.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (442 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 442.7/442.7 KB 850.5 kB/s eta 0:00:00
Collecting pycparser
  Downloading pycparser-2.21-py2.py3-none-any.whl (118 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 118.7/118.7 KB 892.6 kB/s eta 0:00:00
Installing collected packages: webencodings, trove-classifiers, ptyprocess, msgpack, lockfile, distlib, charset-normalizer, zipp, urllib3, tomlkit, tomli, six, shellingham, rapidfuzz, pyrsistent, pycparser, poetry-core, platformdirs, pkgutil-resolve-name, pkginfo, pexpect, packaging, more-itertools, jeepney, idna, filelock, crashtest, certifi, attrs, virtualenv, requests, jaraco.classes, importlib-resources, importlib-metadata, html5lib, dulwich, cleo, cffi, requests-toolbelt, jsonschema, cryptography, cachecontrol, SecretStorage, keyring, poetry-plugin-export, poetry
Successfully installed SecretStorage-3.3.3 attrs-22.2.0 cachecontrol-0.12.11 certifi-2022.12.7 cffi-1.15.1 charset-normalizer-3.0.1 cleo-2.0.1 crashtest-0.4.1 cryptography-39.0.1 distlib-0.3.6 dulwich-0.20.50 filelock-3.9.0 html5lib-1.1 idna-3.4 importlib-metadata-4.13.0 importlib-resources-5.10.2 jaraco.classes-3.2.3 jeepney-0.8.0 jsonschema-4.17.3 keyring-23.13.1 lockfile-0.12.2 more-itertools-9.0.0 msgpack-1.0.4 packaging-23.0 pexpect-4.8.0 pkginfo-1.9.6 pkgutil-resolve-name-1.3.10 platformdirs-2.6.2 poetry-1.3.2 poetry-core-1.4.0 poetry-plugin-export-1.3.0 ptyprocess-0.7.0 pycparser-2.21 pyrsistent-0.19.3 rapidfuzz-2.13.7 requests-2.28.2 requests-toolbelt-0.10.1 shellingham-1.5.0.post1 six-1.16.0 tomli-2.0.1 tomlkit-0.11.6 trove-classifiers-2023.2.8 urllib3-1.26.14 virtualenv-20.19.0 webencodings-0.5.1 zipp-3.13.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
WARNING: You are using pip version 22.0.4; however, version 23.0 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.
Removing intermediate container 711f4aa8d500
 ---> b55dd2ac8444
Step 5/11 : WORKDIR /
 ---> Running in 190ca7ab7da4
Removing intermediate container 190ca7ab7da4
 ---> a1ea4ebf4d5b
Step 6/11 : COPY poetry.lock pyproject.toml app.py /
 ---> 67c34e3ae487
Step 7/11 : COPY lib lib/
 ---> f144c79aa622
Step 8/11 : COPY templates templates/
 ---> f9063d8d4bfc
Step 9/11 : RUN poetry config virtualenvs.create false   && poetry install --no-dev
 ---> Running in e99b5e3b4ed3
Skipping virtualenv creation, as specified in config file.
The `--no-dev` option is deprecated, use the `--only main` notation instead.
Installing dependencies from lock file
Warning: poetry.lock is not consistent with pyproject.toml. You may be getting improper dependencies. Run `poetry lock [--no-update]` to fix it.

Package operations: 5 installs, 0 updates, 0 removals

  • Installing exceptiongroup (1.1.0)
  • Installing iniconfig (2.0.0)
  • Installing pluggy (1.0.0)
  • Installing pytest (7.2.1)
  • Installing helloworld (0.1.0 /lib/helloworld)
Removing intermediate container e99b5e3b4ed3
 ---> 2291a75f5a9b
Step 10/11 : EXPOSE 5000
 ---> Running in d85287acfd44
Removing intermediate container d85287acfd44
 ---> 370bde06b217
Step 11/11 : CMD ["gunicorn", "-b 0.0.0.0:5000", "app:app"]
 ---> Running in 9fd5742ba6d3
Removing intermediate container 9fd5742ba6d3
 ---> df8a8803fd96
Successfully built df8a8803fd96
Successfully tagged mortimerxyz/flaskapp1:0.0.1
```

## Run the docker container

```sh
docker run -p 5000:5000 mortimerxyz/flaskapp1:0.0.1
```

```log
[2023-02-15 08:59:29 +0000] [1] [INFO] Starting gunicorn 20.1.0
[2023-02-15 08:59:29 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2023-02-15 08:59:29 +0000] [1] [INFO] Using worker: sync
[2023-02-15 08:59:29 +0000] [8] [INFO] Booting worker with pid: 8
```

![](docs/browser-docker-flask.png)