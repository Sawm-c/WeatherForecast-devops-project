variable "fe_bucket_name" {
  type = string
}

variable "common_tags" {
  type = map(string)
}
variable "be_domain_name" {
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
