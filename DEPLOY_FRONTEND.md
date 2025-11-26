# Frontend Deployment Instructions

## Prerequisites
- AWS CLI configured with credentials
- Frontend built (`npm run build` in `frontend/` directory)

## Deployment Steps

1. **Build the frontend** (if not already built):
```bash
cd frontend
npm run build
cd ..
```

2. **Get the S3 bucket name**:
```bash
cd infra
terraform output frontend_s3_bucket_name
```

3. **Upload to S3**:
```bash
aws s3 sync frontend/dist/ s3://$(cd infra && terraform output -raw frontend_s3_bucket_name) --delete
```

4. **Get the CloudFront distribution ID**:
```bash
cd infra
terraform output cloudfront_distribution_id
```

5. **Invalidate CloudFront cache**:
```bash
aws cloudfront create-invalidation \
  --distribution-id $(cd infra && terraform output -raw cloudfront_distribution_id) \
  --paths "/*"
```

6. **Get the frontend URL**:
```bash
cd infra
terraform output frontend_url
```

## Quick Deploy Script

You can also run this one-liner (from project root):

```bash
cd frontend && npm run build && cd .. && \
aws s3 sync frontend/dist/ s3://$(cd infra && terraform output -raw frontend_s3_bucket_name) --delete && \
aws cloudfront create-invalidation --distribution-id $(cd infra && terraform output -raw cloudfront_distribution_id) --paths "/*" && \
echo "Frontend deployed! URL: $(cd infra && terraform output -raw frontend_url)"
```

## Current Deployment Info

- **S3 Bucket**: `distribution-app-frontend-dev`
- **CloudFront Distribution ID**: `E2ECVN5BX6Z3IN`
- **Frontend URL**: `https://ddcgt2y78p790.cloudfront.net`

## Troubleshooting

If you get "Unable to locate credentials":
1. Configure AWS CLI: `aws configure`
2. Or set environment variables:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION` (e.g., `eu-central-1`)

