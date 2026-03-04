#eventbridge.tf

resource "aws_cloudwatch_event_rule" "daily" {
  name                = "daily-stock-ingest"
  schedule_expression = "cron(0 0 * * ? *)"  # runs every day at midnight UTC
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily.name
  target_id = "stockLambda"
  arn       = aws_lambda_function.stock_ingest.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.stock_ingest.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily.arn
}