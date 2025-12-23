#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 -e <env_prefix>" >&2
  exit 1
}

ENV_PREFIX=""
while getopts "e:h" opt; do
  case "$opt" in
    e) ENV_PREFIX="$OPTARG" ;;
    h) usage ;;
    *) usage ;;
  esac
done

[ -n "$ENV_PREFIX" ] || usage
case "$ENV_PREFIX" in
  dev|prod) ;;
  *) echo "Environment prefix must be one of: dev, prod" >&2; exit 1 ;;
esac

command -v awslocal >/dev/null 2>&1 || { echo "awslocal is required but not installed" >&2; exit 1; }

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TEMPLATE_FILE="$SCRIPT_DIR/template.yaml"
[ -f "$TEMPLATE_FILE" ] || { echo "template.yaml not found next to deploy.sh" >&2; exit 1; }

export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
STACK_NAME="photo-bucket-${ENV_PREFIX}"

echo "Deploying stack $STACK_NAME to LocalStack (env: $ENV_PREFIX)..."
awslocal cloudformation deploy \
  --stack-name "$STACK_NAME" \
  --template-file "$TEMPLATE_FILE" \
  --parameter-overrides "EnvironmentName=$ENV_PREFIX" \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-fail-on-empty-changeset

echo "Deployment complete."
