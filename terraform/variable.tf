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
