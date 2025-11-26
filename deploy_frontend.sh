#!/bin/bash
# Frontend Deployment Script

set -e

# Use distribution-app profile if it exists, otherwise use default
if aws configure list --profile distribution-app &>/dev/null; then
    AWS_PROFILE="distribution-app"
    export AWS_PROFILE
    echo "✅ Using AWS profile: distribution-app"
else
    AWS_PROFILE="default"
    export AWS_PROFILE
    echo "✅ Using AWS profile: default"
fi

echo "🚀 Deploying frontend to AWS..."

# Check AWS credentials
if ! aws sts get-caller-identity &>/dev/null; then
    echo "❌ AWS credentials not configured!"
    echo "Please run: aws configure --profile distribution-app"
    echo "Or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables"
    exit 1
fi

# Get bucket name and distribution ID from Terraform
cd infra
BUCKET=$(terraform output -raw frontend_s3_bucket_name)
DIST_ID=$(terraform output -raw cloudfront_distribution_id)
FRONTEND_URL=$(terraform output -raw frontend_url)
cd ..

echo "📦 Uploading to S3 bucket: $BUCKET"
aws s3 sync frontend/dist/ s3://$BUCKET --delete

echo "🔄 Invalidating CloudFront cache..."
INVALIDATION_ID=$(aws cloudfront create-invalidation \
    --distribution-id $DIST_ID \
    --paths "/*" \
    --query 'Invalidation.Id' \
    --output text)

echo "✅ Deployment complete!"
echo "🌐 Frontend URL: $FRONTEND_URL"
echo "📝 Invalidation ID: $INVALIDATION_ID"
echo ""
echo "Note: CloudFront cache invalidation may take a few minutes to propagate."
