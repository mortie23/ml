# Poetry Cloud build container for Docker images

> This planned to be a generic container that could be used for Cloud Build to build anything that uses poetry.
> However, building and publishing a Python package was failing.

```log
ERROR    InvalidDistribution: Metadata is missing required fields: Name,
         Version.
         Make sure the distribution includes the files where those fields are
         specified, and is using a supported Metadata-Version: 1.0, 1.1, 1.2,
         2.0, 2.1, 2.2.
```

It was failing due to the version of poetry being >= 2.0 which creates package Metadata-Version of 2.3.
[https://github.com/pypi/warehouse/issues/15611](https://github.com/pypi/warehouse/issues/15611)
The assumption was that the version of pkginfo and twine that is used by the Cloud Build `artifacts/pythonPackage` cannot publish.

A core shared container.

## Build and push

Currently build and publish once. No need for a new build and publish each environment as they are shared.

```sh
docker build -t australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/poetry-dkr .
docker push australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/poetry-dkr
```
