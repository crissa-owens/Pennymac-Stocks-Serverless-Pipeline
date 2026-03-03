resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"  # allows Lambda to write to DynamoDB
}

resource "aws_lambda_function" "stock_ingest" {
  function_name = "stock-ingest-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.11"
  filename      = "../lambda/ingestion/lambda.zip"
  source_code_hash = filebase64sha256("../lambda/ingestion/lambda.zip")
  

  environment {
    variables = {
      MASSIVE_API_KEY = var.massive_api_key
      TABLE_NAME      = aws_dynamodb_table.stock_movers.name
    }
  }
}