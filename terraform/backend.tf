#backend.tf

terraform {
  backend "s3" {
    bucket = "crissa-stocks-terraform-state"
    key    = "global/s3/terraform.tfstate"
    region = "us-east-1"
  }
}
