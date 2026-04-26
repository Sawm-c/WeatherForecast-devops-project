variable "azs" {
  type = list(any)
}

variable "cidr_blocks" {
  type = string
}

variable "common_tags" {
  type = map(string)
}

variable "region" {
  type        = string
  description = "AWS region"
}
