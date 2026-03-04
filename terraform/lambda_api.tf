# lambda_api.tf

resource "aws_lambda_function" "api_lambda" {
  function_name = "api_lambda"
  role          = aws_iam_role.lambda_api_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  filename      = "../lambda/retrieval/lambda_api.zip"
  source_code_hash = filebase64sha256("../lambda/retrieval/lambda_api.zip")

  environment {
    variables = {
      TABLE_NAME = var.table_name
    }
  }
}