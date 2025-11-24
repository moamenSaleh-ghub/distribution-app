# Lambda permissions for API Gateway
resource "aws_lambda_permission" "api_gw_products" {
  for_each = {
    create = aws_lambda_function.create_product
    list   = aws_lambda_function.get_products
    get    = aws_lambda_function.get_product
    update = aws_lambda_function.update_product
  }

  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "api_gw_customers" {
  for_each = {
    create = aws_lambda_function.create_customer
    list   = aws_lambda_function.get_customers
    detail = aws_lambda_function.get_customer_detail
  }

  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "api_gw_orders" {
  for_each = {
    create = aws_lambda_function.create_order
    list   = aws_lambda_function.get_customer_orders
  }

  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "api_gw_debt" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.adjust_customer_debt.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

# API Gateway Integrations
resource "aws_apigatewayv2_integration" "create_product" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.create_product.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "get_products" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.get_products.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "get_product" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.get_product.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "update_product" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.update_product.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "create_customer" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.create_customer.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "get_customers" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.get_customers.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "get_customer_detail" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.get_customer_detail.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "create_order" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.create_order.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "get_customer_orders" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.get_customer_orders.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "adjust_customer_debt" {
  api_id = aws_apigatewayv2_api.main.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.adjust_customer_debt.invoke_arn
  integration_method = "POST"
}

# API Gateway Routes
resource "aws_apigatewayv2_route" "create_product" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /products"
  target    = "integrations/${aws_apigatewayv2_integration.create_product.id}"
}

resource "aws_apigatewayv2_route" "get_products" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /products"
  target    = "integrations/${aws_apigatewayv2_integration.get_products.id}"
}

resource "aws_apigatewayv2_route" "get_product" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /products/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.get_product.id}"
}

resource "aws_apigatewayv2_route" "update_product" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PATCH /products/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.update_product.id}"
}

resource "aws_apigatewayv2_route" "create_customer" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /customers"
  target    = "integrations/${aws_apigatewayv2_integration.create_customer.id}"
}

resource "aws_apigatewayv2_route" "get_customers" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /customers"
  target    = "integrations/${aws_apigatewayv2_integration.get_customers.id}"
}

resource "aws_apigatewayv2_route" "get_customer_detail" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /customers/{id}"
  target    = "integrations/${aws_apigatewayv2_integration.get_customer_detail.id}"
}

resource "aws_apigatewayv2_route" "create_order" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /orders"
  target    = "integrations/${aws_apigatewayv2_integration.create_order.id}"
}

resource "aws_apigatewayv2_route" "get_customer_orders" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /customers/{id}/orders"
  target    = "integrations/${aws_apigatewayv2_integration.get_customer_orders.id}"
}

resource "aws_apigatewayv2_route" "adjust_customer_debt" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /customers/{id}/adjust-debt"
  target    = "integrations/${aws_apigatewayv2_integration.adjust_customer_debt.id}"
}

# CORS preflight
resource "aws_apigatewayv2_route" "options" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "OPTIONS /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.get_products.id}"
}

