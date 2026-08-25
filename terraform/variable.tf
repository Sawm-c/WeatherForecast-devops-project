variable "aws_instance" {
  type = string
}

variable "weather_key_name" {
  type = string
}

variable "weather_key_path" {
  type = string
}

variable "region" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "common_tags" {
  type = map(string)
}

variable "azs" {
  type = list(any)
}

variable "cidr_blocks" {
  type = string
}

variable "bucket_name" {
  type = string
}

variable "fe_bucket_name" {
  type = string
}

variable "custom_domain_name" {
  type        = string
  description = "weather domain"
}

variable "acm_certificate_arn" {
  type        = string
  description = "ACM certificate ARN"
}

variable "db_name" {
  type        = string
  description = "Tên database trong RDS"
  default     = "weatherdb"
}

variable "db_username" {
  type        = string
  description = "Username đăng nhập RDS"
  default     = "postgres"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Password đăng nhập RDS"
}

