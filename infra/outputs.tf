output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.main.name
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket for product images"
  value       = aws_s3_bucket.product_images.id
}

output "api_gateway_url" {
  description = "API Gateway HTTP API endpoint URL"
  value       = aws_apigatewayv2_api.main.api_endpoint
}

output "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_role.arn
}

output "frontend_s3_bucket_name" {
  description = "Name of the S3 bucket for frontend"
  value       = aws_s3_bucket.frontend.id
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.frontend.id
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name"
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "frontend_url" {
  description = "Frontend URL (CloudFront)"
  value       = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}
