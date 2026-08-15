resource "aws_s3_bucket" "fe_bucket" {
  bucket        = var.fe_bucket_name
  tags          = var.common_tags
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "fe_public_block" {
  bucket                  = aws_s3_bucket.fe_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "fe_bucket_policy" {
  bucket = aws_s3_bucket.fe_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontReadOnly"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.fe_bucket.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.fe_distribution.arn
          }
        }

      }
    ]
  })

}

resource "aws_cloudfront_origin_access_control" "fe_oac" {
  name                              = "fe-oac"
  description                       = "OAC allows CloudFront read S3 Frontend"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "fe_distribution" {
  enabled             = true
  default_root_object = "index.html"
  tags                = var.common_tags

  origin {
    domain_name              = aws_s3_bucket.fe_bucket.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.fe_oac.id
    origin_id                = "S3-bucket-${aws_s3_bucket.fe_bucket.id}"
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    viewer_protocol_policy = "redirect-to-https"
    target_origin_id       = "S3-bucket-${aws_s3_bucket.fe_bucket.id}"
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

}

