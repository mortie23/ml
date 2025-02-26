# API HTTP Placeholder container

This container is designed to be used when a Cloud Run container service is required.
The pattern for deployment is to create a placeholder HTTP service with Terraform and then deploy a revision to the resource as part of the application deployment phase.

A core shared container.

```sh
docker build -t australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/placeholder .
docker push australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/placeholder
```

## Local testing

```sh
docker run -p 8080:80 australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/placeholder:latest
```

Test the end point.

```sh
curl localhost:8080
```

Response

```json
{
  "status": "alive",
  "service": "placeholder"
}
```
