# lambda_ingestion.tf

resource "aws_lambda_function" "stock_ingest" {
  function_name = "stock-ingest-lambda"
  role          = aws_iam_role.lambda_ingestion_role.arn
  handler       = "ingestion_handler.lambda_handler"
  runtime       = "python3.11"
  filename      = "../lambda/ingestion/lambda_ingestion.zip"
  source_code_hash = filebase64sha256("../lambda/ingestion/lambda_ingestion.zip")
  timeout = 45

  environment {
    variables = {
      MASSIVE_API_KEY = var.massive_api_key
      TABLE_NAME      = var.table_name
    }
  }
}