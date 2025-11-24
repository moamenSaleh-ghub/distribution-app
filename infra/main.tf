terraform {
  required_version = ">= 1.10.0"
}

# DynamoDB Table
resource "aws_dynamodb_table" "main" {
  name           = "${var.app_name}-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "pk"
  range_key      = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  attribute {
    name = "entityType"
    type = "S"
  }

  attribute {
    name = "name"
    type = "S"
  }

  # Optional GSI for listing products/customers by entityType
  global_secondary_index {
    name            = "EntityTypeIndex"
    hash_key        = "entityType"
    range_key       = "name"
    projection_type = "ALL"
  }

  tags = {
    Name        = "${var.app_name}-${var.environment}"
    Environment = var.environment
  }
}

# S3 Bucket for product images
resource "aws_s3_bucket" "product_images" {
  bucket = "${var.app_name}-product-images-${var.environment}"

  tags = {
    Name        = "${var.app_name}-product-images-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "product_images" {
  bucket = aws_s3_bucket.product_images.id
  versioning_configuration {
    status = "Disabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "product_images" {
  bucket = aws_s3_bucket.product_images.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "product_images" {
  bucket = aws_s3_bucket.product_images.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets  = true
}

# IAM Role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "${var.app_name}-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.app_name}-lambda-role-${var.environment}"
    Environment = var.environment
  }
}

# IAM Policy for Lambda to access DynamoDB and S3
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.app_name}-lambda-policy-${var.environment}"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.main.arn,
          "${aws_dynamodb_table.main.arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.product_images.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.product_images.arn
      }
    ]
  })
}

# API Gateway HTTP API
resource "aws_apigatewayv2_api" "main" {
  name          = "${var.app_name}-api-${var.environment}"
  protocol_type = "HTTP"
  description   = "Distribution App API"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
    allow_headers = ["content-type", "authorization"]
  }

  tags = {
    Name        = "${var.app_name}-api-${var.environment}"
    Environment = var.environment
  }
}

# API Gateway Stage
resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "$default"
  auto_deploy = true
}
