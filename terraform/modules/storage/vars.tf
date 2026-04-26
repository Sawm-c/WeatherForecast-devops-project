variable "bucket_name" {
  type        = string
  description = "Name of the S3 bucket"
}

variable "common_tags" {
  type        = map(string)
  description = "Common tags to apply to all resources"
}

