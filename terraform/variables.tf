# variables.tf

variable "massive_api_key" {
  type = string
  description = "API key for Massive stock data"
  sensitive = true
}

variable "aws_region" {
  type = string
  description = "AWS region"
}

variable "table_name" {
  type = string
  description = "DynamoDB table name"
}