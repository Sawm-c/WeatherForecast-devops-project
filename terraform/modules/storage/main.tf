resource "aws_s3_bucket" "weather_storage_bucket" {
  bucket        = var.bucket_name
  force_destroy = true
  tags          = var.common_tags
}

resource "aws_s3_object" "weather_object_bucket" {
  bucket = aws_s3_bucket.weather_storage_bucket.id
  key    = "database/init.sql"
  source = "${path.module}/../../../database/init.sql"
  etag   = filemd5("${path.module}/../../../database/init.sql")
}

