terraform {
  required_version = ">= 1.2.0"

  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 4.16"
    }

  }
}

provider "aws" {
  region = var.aws_region
  profile = "hb"
}

resource "aws_iam_role" "redshift_serverless_role" {
    name = "RedshiftLoadRule"
    managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
    assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift-serverless.amazonaws.com"
        }
      },
    ]
  })
}
  


resource "aws_redshiftserverless_namespace" "Redshift" {
    namespace_name = "reddit-space-09"
    admin_username = "admin"
    db_name = "dev"
    admin_user_password = var.db_password
    iam_roles = [aws_iam_role.redshift_serverless_role.arn]
    #default_iam_role_arn = "arn:aws:iam::962066579811:role/service-role/AmazonRedshift-CommandsAccessRole-20230730T081708"

  
}

resource "aws_redshiftserverless_workgroup" "aws_workgroup" {
  namespace_name = "reddit-space-09"
  workgroup_name = "reddit-workgroup-09"
}


resource "aws_s3_bucket" "reddit_bucket" {
  bucket = var.s3_bucket
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

resource "aws_s3_bucket_ownership_controls" "name" {
  bucket = aws_s3_bucket.reddit_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }

}

resource "aws_s3_bucket_acl" "s3_reddit_bucket_acl" {
  depends_on = [ aws_s3_bucket_ownership_controls.name ]
  bucket = aws_s3_bucket.reddit_bucket.id
  acl = "private"
  
}