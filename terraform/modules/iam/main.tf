resource "aws_iam_role" "weather_iam_role" {
  name = "weather-iam-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
  tags = var.common_tags
}

resource "aws_iam_policy" "weather_iam_policy" {
  name        = "weather-iam-policy"
  description = "Cho phép EC2 đọc file từ bucket Weather"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Effect   = "Allow"
        Resource = ["${var.bucket_arn}", "${var.bucket_arn}/*"]
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "weather_iam_policy_attachment" {
  role       = aws_iam_role.weather_iam_role.name
  policy_arn = aws_iam_policy.weather_iam_policy.arn
}

resource "aws_iam_instance_profile" "weather_instance_profile" {
  name = "weather_instance_profile"
  role = aws_iam_role.weather_iam_role.name
}
