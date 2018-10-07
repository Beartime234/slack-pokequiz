#!/usr/bin/env bash
set -e

if [ -z "$1" ]
  then
    echo "Argument stage is required"
    exit 1
fi

# Aws Variables
STAGE=$1
ACCOUNT_ID="934679804324"  # Your AWS account id
REGION="us-east-1"  # The AWS region you are building in e.g. ap-southeast-2
AWS_PROFILE="beartimeworks"  # Your AWS profile that you have set up
BUCKET="${ACCOUNT_ID}-${REGION}-lambda-code-storage"  # An S3 bucket that can store lambda code in

# Stack Variables
SECRETS_NAME="pokequiz-secrets"  # The name of the secret in secrets manager that stores
SERVICE="pokequiz"  # The name of the service e.g. MySuperCoolSlackApp
API_STACK_NAME="${STAGE}-${SERVICE}-api"  # The name of the stack. You could just but ${SERVICE} here

# File Pathing
TEMPLATE_FOLDER="templates"  # The folder which your template lives in
API_TEMPLATE_FILE="api.yml"  # the file that in your template folder it lives in
DIST_FOLDER="dist"  # A folder that the distribution files live in. Just leave this
SAM_DIST_FOLDER="sam-build"

# Export our set Aws Profile
export AWS_PROFILE=${AWS_PROFILE}

# Comment it out if your tests suck :)
bash ./scripts/test.sh

echo "Removing Old Deployment Template"
mkdir -p ${DIST_FOLDER}/${SAM_DIST_FOLDER}
rm -f ${DIST_FOLDER}/${SAM_DIST_FOLDER}/${STAGE}-packaged-template.yml

bash ./scripts/build.sh

echo "CloudFormation packaging..."

aws cloudformation package \
    --region ${REGION} \
    --template-file ${TEMPLATE_FOLDER}/${API_TEMPLATE_FILE} \
    --output-template-file ${DIST_FOLDER}/${SAM_DIST_FOLDER}/${STAGE}-packaged-template.yml \
    --s3-bucket ${BUCKET} \
    --s3-prefix sam/${SERVICE}

echo "CloudFormation deploying..."

aws cloudformation deploy  \
    --region ${REGION} \
    --template-file ${DIST_FOLDER}/${SAM_DIST_FOLDER}/${STAGE}-packaged-template.yml \
    --stack-name ${API_STACK_NAME} \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-override Stage=${STAGE} SecretsName=${SECRETS_NAME} ServiceName=${SERVICE} || true

echo "CloudFormation outputs..."
aws cloudformation describe-stacks \
    --stack-name ${API_STACK_NAME} \
    --query 'Stacks[].Outputs' \
    --region ${REGION}