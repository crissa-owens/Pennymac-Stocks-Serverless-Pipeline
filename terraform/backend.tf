#backend.tf

terraform {
  backend "s3" {
    bucket         = "..."
    key            = "stocks-pipeline/terraform.tfstate"
    region         = var.aws_region
    dynamodb_table = "..."
    encrypt        = true
  }
}