# API Gateway REST API
resource "aws_api_gateway_rest_api" "stocks_api" {
  name        = "StocksAPI"
  description = "API for fetching top stock movers"
}

# Resource /movers
resource "aws_api_gateway_resource" "movers" {
  rest_api_id = aws_api_gateway_rest_api.stocks_api.id
  parent_id   = aws_api_gateway_rest_api.stocks_api.root_resource_id
  path_part   = "movers"
}

# GET method
resource "aws_api_gateway_method" "get_movers" {
  rest_api_id   = aws_api_gateway_rest_api.stocks_api.id
  resource_id   = aws_api_gateway_resource.movers.id
  http_method   = "GET"
  authorization = "NONE"
}

# Integration with Lambda
resource "aws_api_gateway_integration" "lambda_get_movers" {
  rest_api_id             = aws_api_gateway_rest_api.stocks_api.id
  resource_id             = aws_api_gateway_resource.movers.id
  http_method             = aws_api_gateway_method.get_movers.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.stock_api.invoke_arn
}

resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.stock_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.stocks_api.execution_arn}/*/*"
}


resource "aws_api_gateway_deployment" "stocks_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.stocks_api.id
  triggers = {
    redeployment = sha1(join("", [
      file("${path.module}/api_gateway.tf"),
      file("${path.module}/lambda_api.tf"),
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_method.get_movers,
    aws_api_gateway_integration.lambda_get_movers
  ]
}

resource "aws_api_gateway_stage" "stocks_api_stage" {
  stage_name    = "prod"
  rest_api_id   = aws_api_gateway_rest_api.stocks_api.id
  deployment_id = aws_api_gateway_deployment.stocks_api_deployment.id

  depends_on = [aws_api_gateway_deployment.stocks_api_deployment]
}

