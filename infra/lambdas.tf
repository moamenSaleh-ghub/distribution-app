# Lambda function for products
resource "aws_lambda_function" "create_product" {
  filename         = "${path.module}/../backend/deploy/create_product.zip"
  function_name    = "${var.app_name}-create-product-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.create_product.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/create_product.zip")
}

resource "aws_lambda_function" "get_products" {
  filename         = "${path.module}/../backend/deploy/get_products.zip"
  function_name    = "${var.app_name}-get-products-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.get_products.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/get_products.zip")
}

resource "aws_lambda_function" "get_product" {
  filename         = "${path.module}/../backend/deploy/get_product.zip"
  function_name    = "${var.app_name}-get-product-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.get_product.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/get_product.zip")
}

resource "aws_lambda_function" "update_product" {
  filename         = "${path.module}/../backend/deploy/update_product.zip"
  function_name    = "${var.app_name}-update-product-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.update_product.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/update_product.zip")
}

# Lambda functions for customers
resource "aws_lambda_function" "create_customer" {
  filename         = "${path.module}/../backend/deploy/create_customer.zip"
  function_name    = "${var.app_name}-create-customer-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.create_customer.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/create_customer.zip")
}

resource "aws_lambda_function" "get_customers" {
  filename         = "${path.module}/../backend/deploy/get_customers.zip"
  function_name    = "${var.app_name}-get-customers-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.get_customers.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/get_customers.zip")
}

resource "aws_lambda_function" "get_customer_detail" {
  filename         = "${path.module}/../backend/deploy/get_customer_detail.zip"
  function_name    = "${var.app_name}-get-customer-detail-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.get_customer_detail.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/get_customer_detail.zip")
}

# Lambda functions for orders
resource "aws_lambda_function" "create_order" {
  filename         = "${path.module}/../backend/deploy/create_order.zip"
  function_name    = "${var.app_name}-create-order-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.create_order.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/create_order.zip")
}

resource "aws_lambda_function" "get_customer_orders" {
  filename         = "${path.module}/../backend/deploy/get_customer_orders.zip"
  function_name    = "${var.app_name}-get-customer-orders-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.get_customer_orders.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/get_customer_orders.zip")
}

# Lambda function for debt adjustments
resource "aws_lambda_function" "adjust_customer_debt" {
  filename         = "${path.module}/../backend/deploy/adjust_customer_debt.zip"
  function_name    = "${var.app_name}-adjust-customer-debt-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.handlers.adjust_customer_debt.handler"
  runtime         = "python3.12"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.main.name
    }
  }

  source_code_hash = filebase64sha256("${path.module}/../backend/deploy/adjust_customer_debt.zip")
}

