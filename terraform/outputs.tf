output "api_url" {
  value = aws_api_gateway_deployment.stocks_api_deployment.invoke_url
}

output "frontend_url" {
  value = "https://crissa-stocks-terraform-state.s3-website-us-east-1.amazonaws.com"
}