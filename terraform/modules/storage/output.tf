output "bucket_id" {
  value = aws_s3_bucket.weather_storage_bucket.id
}

output "bucket_arn" {
  value = aws_s3_bucket.weather_storage_bucket.arn
}

