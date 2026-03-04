#backend.tf

terraform {
  backend "s3" {
    bucket         = "crissa-stocks-terraform-state"
    key            = "stocks-pipeline/terraform.tfstate"
    region         = var.aws_region
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
