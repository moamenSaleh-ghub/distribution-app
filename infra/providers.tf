terraform {
  required_version = ">= 1.10.0"

  backend "s3" {
    bucket       = "distribution-app-tf-state-euc1-4c21b9"
    key          = "envs/dev/infra.tfstate"
    region       = "eu-central-1"       
    profile      = "distribution-app"  
    encrypt      = true                 
    use_lockfile = true                 
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "eu-central-1"
  profile = "distribution-app"
}
