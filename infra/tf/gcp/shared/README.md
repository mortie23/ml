# Shared resources

A separate Terraform workspace for GCP resources that are shared across environment controlled resources.

```sh
terraform init -backend-config="vars/backend.hcl" -reconfigure
```
