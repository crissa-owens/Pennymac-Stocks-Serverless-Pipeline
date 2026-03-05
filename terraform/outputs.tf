output "api_url" {
  value = aws_api_gateway_deployment.stocks_api_deployment.invoke_url
}

output "s3_url" {
  value = "http://crissa-stock-dashboard.s3-website-us-east-1.amazonaws.com"
}