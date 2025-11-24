#!/bin/bash
# Script to deploy frontend to S3 and invalidate CloudFront cache

set -e

cd "$(dirname "$0")"

# Get bucket name and distribution ID from Terraform outputs
cd ../infra
BUCKET_NAME=$(terraform output -raw frontend_s3_bucket_name)
DISTRIBUTION_ID=$(terraform output -raw cloudfront_distribution_id)
FRONTEND_URL=$(terraform output -raw frontend_url)
cd ..

echo "Building frontend..."
cd frontend
npm run build

echo "Uploading to S3 bucket: $BUCKET_NAME"
aws s3 sync dist s3://$BUCKET_NAME --delete --profile distribution-app

echo "Invalidating CloudFront cache..."
aws cloudfront create-invalidation \
  --distribution-id $DISTRIBUTION_ID \
  --paths "/*" \
  --profile distribution-app > /dev/null

echo ""
echo "✅ Frontend deployed successfully!"
echo "🌐 Frontend URL: $FRONTEND_URL"
echo ""
echo "Note: CloudFront cache invalidation may take a few minutes to complete."

