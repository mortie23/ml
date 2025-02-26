# Poetry Cloud build container

This is a dedicated build container used by Cloud Build to build and publish Python packages to Artifact Registry.
The hard coded versions of `poetry` and `poetry-plugin-export` are required. See [../poetry-dkr/README.md](../poetry-dkr/README.md).

A core shared container.

## Build and push

Currently build and publish once. No need for a new build and publish each environment as they are shared.

```sh
docker build -t australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/poetry-pypkg .
docker push australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/poetry-pypkg
```
