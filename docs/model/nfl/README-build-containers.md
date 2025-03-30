# Building Google Cloud ML containers

### Building the prediction container

```sh
./cloudbuild.sh --env dev
```

```sh
env = dev
Creating temporary archive of 12 file(s) totalling 2.6 MiB before compression.
Uploading tarball of [.] to [gs://prj-xyz-dev-nfl-0_cloudbuild/source/1743302186.833702-a51b48965f16497a92eedafd71769f52.tgz]
Created [https://cloudbuild.googleapis.com/v1/projects/prj-xyz-dev-nfl-0/locations/global/builds/eb326c2b-23b3-417b-8751-1270d1eb90f4].
Logs are available at [ https://console.cloud.google.com/cloud-build/builds/eb326c2b-23b3-417b-8751-1270d1eb90f4?project=346990393894 ].
Waiting for build to complete. Polling interval: 1 second(s).
----------------------------------------------------------------------------- REMOTE BUILD OUTPUT -----------------------------------------------------------------------------
starting build "eb326c2b-23b3-417b-8751-1270d1eb90f4"

FETCHSOURCE
Fetching storage object: gs://prj-xyz-dev-nfl-0_cloudbuild/source/1743302186.833702-a51b48965f16497a92eedafd71769f52.tgz#1743302189684909
Copying gs://prj-xyz-dev-nfl-0_cloudbuild/source/1743302186.833702-a51b48965f16497a92eedafd71769f52.tgz#1743302189684909...
/ [1 files][431.6 KiB/431.6 KiB]
Operation completed over 1 objects/431.6 KiB.
BUILD
Already have image (with digest): gcr.io/cloud-builders/docker
Sending build context to Docker daemon  2.779MB
Step 1/20 : FROM australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/poetry-dkr AS base
latest: Pulling from prj-xyz-shr-rep-0/rpo-bld-dkr-0/poetry-dkr
485ca86a58f8: Pulling fs layer
...
e451f55144f6: Waiting
...
1e36295709cc: Verifying Checksum
1e36295709cc: Download complete
...
2a975e0129db: Pull complete
Digest: sha256:707c6a7e669b42fdd7eb2f4ed53560ef746a266b487e20098bea82e767c4a442
Status: Downloaded newer image for australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/poetry-dkr:latest
 ---> 5adbce776000
Step 2/20 : WORKDIR /build
 ---> Running in f81d85329379
Removing intermediate container f81d85329379
 ---> c1448906e27b
Step 3/20 : ENV PYTHONUNBUFFERED=1
 ---> Running in 20df6ff26526
Removing intermediate container 20df6ff26526
 ---> dc2bf1e2a914
Step 4/20 : ENV POETRY_VIRTUALENVS_IN_PROJECT=true
 ---> Running in cd7ad5ba4fcc
Removing intermediate container cd7ad5ba4fcc
 ---> 518d765e3792
Step 5/20 : ENV POETRY_NO_INTERACTION=1
 ---> Running in f75045d3fb6e
Removing intermediate container f75045d3fb6e
 ---> 86a99ebd3318
Step 6/20 : COPY ./ ./
 ---> af54703630e8
Step 7/20 : RUN poetry install
 ---> Running in 9fc4f0004a9a
Creating virtualenv nfltouchdownpredict in /build/.venv
Installing dependencies from lock file

Package operations: 113 installs, 0 updates, 0 removals

  - Installing pyasn1 (0.6.1)
  - Installing cachetools (5.5.2)
...
  - Installing nfltouchdown (0.1.6)

Installing /build/.venv/bin/fastapi over existing file
  - Installing scikit-learn (1.6.1)

Installing the current project: nfltouchdownpredict (0.1.0)
Removing intermediate container 9fc4f0004a9a
 ---> 17e1f98b0801
Step 8/20 : FROM base AS model
 ---> 17e1f98b0801
Step 9/20 : ARG env=nil
 ---> Running in 7b5ad87d8517
Removing intermediate container 7b5ad87d8517
 ---> 12b9ffc003ba
Step 10/20 : ENV env=$env
 ---> Running in 35b6a9634c64
Removing intermediate container 35b6a9634c64
 ---> 464561be9756
Step 11/20 : ARG project_id=nil
 ---> Running in 2abc82e96e60
Removing intermediate container 2abc82e96e60
 ---> dd17efff10ba
Step 12/20 : ENV project_id=$project_id
 ---> Running in 201584ed2b43
Removing intermediate container 201584ed2b43
 ---> 713ab2f22efd
Step 13/20 : ENV NLTK_DATA=/usr/share/nltk_data
 ---> Running in 4c9a780a9359
Removing intermediate container 4c9a780a9359
 ---> a95012f3de0a
Step 14/20 : COPY --from=base /build /build
 ---> 8cfc05d43758
Step 15/20 : WORKDIR /model
 ---> Running in dbeddc5a77bf
Removing intermediate container dbeddc5a77bf
 ---> 919a377c8542
Step 16/20 : COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
 ---> 26b327cd6782
Step 17/20 : RUN chmod +x ./docker-entrypoint.sh
 ---> Running in 3e996a4b7571
Removing intermediate container 3e996a4b7571
 ---> 166b11f988cb
Step 18/20 : COPY predict.py ./
 ---> ee152a8918b6
Step 19/20 : COPY predict.yaml ./
 ---> f011262e7f78
Step 20/20 : ENTRYPOINT ["./docker-entrypoint.sh"]
 ---> Running in efc78c780408
Removing intermediate container efc78c780408
 ---> cebd0c197735
Successfully built cebd0c197735
Successfully tagged australia-southeast1-docker.pkg.dev/prj-xyz-dev-nfl-0/rpo-xyz-dev-nfl-dkr-0/predict/nfl-touchdown:latest
PUSH
Pushing australia-southeast1-docker.pkg.dev/prj-xyz-dev-nfl-0/rpo-xyz-dev-nfl-dkr-0/predict/nfl-touchdown:latest
The push refers to repository [australia-southeast1-docker.pkg.dev/prj-xyz-dev-nfl-0/rpo-xyz-dev-nfl-dkr-0/predict/nfl-touchdown]
322dd8785490: Preparing
...
1d665e87fffc: Waiting
...
08103cbc1b09: Pushed
...
latest: digest: sha256:90cec7ffbeb8293b7b42d8d35af36d74425370f56eccb41bd1bd6da7f756773a size: 4309
DONE
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ID                                    CREATE_TIME                DURATION  SOURCE                                                                                           IMAGES                                                                                                       STATUS
eb326c2b-23b3-417b-8751-1270d1eb90f4  2025-03-30T02:36:30+00:00  5M19S     gs://prj-xyz-dev-nfl-0_cloudbuild/source/1743302186.833702-a51b48965f16497a92eedafd71769f52.tgz  australia-southeast1-docker.pkg.dev/prj-xyz-dev-nfl-0/rpo-xyz-dev-nfl-dkr-0/predict/nfl-touchdown (+1 more)  SUCCESS
```
