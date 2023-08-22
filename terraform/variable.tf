variable "db_password" {
    description = "password for database"
    type = string
    default = "Greatmindk#9"
  
}

variable "s3_bucket" {
    description = "Bucket name for S3"
    type = string
    default = "redditdatabucket"
  
}

variable "aws_region" {
    description = "Region for AWS"
    type = string
    default = "us-east-1"
  
}