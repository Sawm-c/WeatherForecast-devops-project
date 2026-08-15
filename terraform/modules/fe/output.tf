output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.fe_distribution.domain_name
}

output "fe_bucket_name" {
  value = aws_s3_bucket.fe_bucket.id
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.fe_distribution.id
}
