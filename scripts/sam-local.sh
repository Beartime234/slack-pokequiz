#!/usr/bin/env bash

PROFILE=beartimeworks # Your AWS profile that you have set up
REGION="us-east-1"

export AWS_PROFILE=${PROFILE}
export AWS_DEFAULT_REGION=${REGION}

bash ./scripts/build.sh
clear
sam local start-api -t templates/api.yml --env-vars templates/local-variables.json