# AWS Credentials Setup

To deploy the frontend, you need to configure AWS credentials. Here are the options:

## Option 1: AWS CLI Configure (Recommended)

Run this command and follow the prompts:
```bash
aws configure
```

You'll need:
- **AWS Access Key ID**: Your AWS access key
- **AWS Secret Access Key**: Your AWS secret key
- **Default region**: `eu-central-1` (or your preferred region)
- **Default output format**: `json` (or `text`)

## Option 2: Environment Variables

Set these environment variables in your terminal:
```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_DEFAULT_REGION="eu-central-1"
```

## Option 3: AWS SSO (if using AWS SSO)

```bash
aws sso login
```

## After Configuring Credentials

Once credentials are configured, run:

```bash
cd /Users/moamens/GitHub/distribution-app
aws s3 sync frontend/dist/ s3://distribution-app-frontend-dev --delete
aws cloudfront create-invalidation --distribution-id E2ECVN5BX6Z3IN --paths "/*"
```

## Verify Configuration

Test your AWS credentials:
```bash
aws sts get-caller-identity
```

This should return your AWS account ID and user ARN.

## Deployment Info

- **S3 Bucket**: `distribution-app-frontend-dev`
- **CloudFront Distribution ID**: `E2ECVN5BX6Z3IN`
- **Frontend URL**: `https://ddcgt2y78p790.cloudfront.net`
- **API Gateway URL**: `https://jyn96fs7n5.execute-api.eu-central-1.amazonaws.com`

