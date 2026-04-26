variable "bucket_arn" {
  type        = string
  description = "ARN of the S3 bucket"
}

variable "common_tags" {
  type        = map(string)
  description = "Common tags to apply to all resources"
}
