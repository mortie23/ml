#!/usr/bin/bash
#
# Deploys as a Python package to Artifact Registry with Cloud Build
# 
# Arguments:
#   env: a GCP project environment
#
# Usage
#    ./cloudbuild.sh --env <dev/ppd/prd>
# Example
#   ./cloudbuild.sh --env dev

source ../../../../lib/shellpers/argon.sh

# Parse arguments
parse_args "$@"
# Ensure the argument existed when the script was called
if [[ -z ${env} ]]; then
    error_code=1
    echo "ERROR" "environment was not provided"
    exit ${error_code}
fi

# parse config yaml in src directory for parameters
eval $(parse_config ../touchdown.yaml ${env})

gcloud builds submit \
    --project=${project_id} \
    --region=${region} \
    --service-account projects/prj-xyz-${env}-nfl-0/serviceAccounts/gsvc-xyz-${env}-nfl-cb@prj-xyz-${env}-nfl-0.iam.gserviceaccount.com \
    --gcs-log-dir gs://bkt-xyz-${env}-nfl-cblog-0 \
    --config cloudbuild.yaml