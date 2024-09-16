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

source ../../../lib/shellpers/argon.sh

# Parse arguments
parse_args "$@"

# Ensure the argument existed when the script was called
if [[ -z ${env} ]]; then
    error_code=1
    echo "ERROR" "environment was not provided"
    exit ${error_code}
fi

gcloud functions deploy fn-afl-teams-0 \
    --gen2 \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point fn_afl_teams \
    --region australia-southeast1 \
    --stage-bucket bkt-xyz-${env}-afl-fn-0 \
    --run-service-account sa-xyz-${env}-fruit-cf@prj-xyz-${env}-fruit-0.iam.gserviceaccount.com \
    --build-service-account projects/prj-xyz-${env}-fruit-0/serviceAccounts/sa-xyz-${env}-fruit-cf@prj-xyz-${env}-fruit-0.iam.gserviceaccount.com \
    --source ./src/ \
    --set-env-vars env=${env}