#!/usr/bin/env bash

SECRETS_NAME="pokequiz-secrets"  # The name of the secret in secrets manager that stores
AWS_PROFILE="beartimeworks"  # Your AWS profile that you have set up
REGION="us-east-1"

# Fix for pytest wont be able to import applications
export PYTHONPATH=pokequiz

# Env variables
export SECRETS_NAME=${SECRETS_NAME}  # The name of secrets
export STAGE="local-dev"
export QUIZ_STORAGE_TABLE="dev-quizdata-storage"  # The name of the storage table
export AWS_PROFILE=${AWS_PROFILE}
export AWS_DEFAULT_REGION=${REGION}
export QUIZ_ID="pokequiz"

echo "Running Tests"
pipenv run python -m pytest tests/ -vv