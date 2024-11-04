#!/usr/bin/bash
#
# Deploys as a GCP Cloud Function
# 
# Arguments:
#   env: a GCP project environment
#
# Usage
#    ./deploy.sh --env <dev/prd>
# Example
#   ./deploy.sh --env dev

source ../../../lib/shelpers/argon.sh

# Parse arguments
parse_args "$@"

# Ensure the argument existed when the script was called
if [[ -z ${env} ]]; then
    error_code=1
    echo "ERROR" "environment was not provided"
    exit ${error_code}
fi

gcloud functions deploy fn-misc-ipchecker-0 \
    --project prj-xyz-${env}-misc-ip-1 \
    --gen2 \
    --runtime python310 \
    --memory=512M \
    --timeout=600 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point fn_misc_ipchecker \
    --region australia-southeast1 \
    --stage-bucket bkt-xyz-${env}-misc-ip-fn-0 \
    --run-service-account gsvc-xyz-${env}-misc-ip-cf@prj-xyz-${env}-misc-ip-1.iam.gserviceaccount.com \
    --build-service-account projects/prj-xyz-${env}-misc-ip-1/serviceAccounts/gsvc-xyz-${env}-misc-ip-cf@prj-xyz-${env}-misc-ip-1.iam.gserviceaccount.com \
    --source ./src/ \
    --set-env-vars env=${env}