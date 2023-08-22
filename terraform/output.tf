output "redshift_password" {
    description = "Database password"
    value = var.db_password
    sensitive = true
  
}

output "redshift_username" {
    description = "Redshift username"
    value = aws_redshiftserverless_namespace.Redshift.admin_username
    sensitive = true
  
}

output "aws_region" {
    description = "Region set for AWS"
    value = var.aws_region

}

output "s3_bucket_name" {
    description = "Region set for AWS"
    value = var.s3_bucket
    sensitive = true
}

