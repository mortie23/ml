# Deploying infrastructure

```sh
terraform init -reconfigure -var-file="env-dev.tfvars"
```

Format and validate any changes:

```sh
terraform fmt
terraform validate
```

Plan

```sh
terraform plan -var-file="env-dev.tfvars"
```

Apply

```sh
terraform apply -var-file="env-dev.tfvars"
```
