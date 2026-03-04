#backend.tf

terraform {
  backend "s3" {
    bucket         = "crissa-stocks-terraform-state"
    key            = "stocks-pipeline/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
