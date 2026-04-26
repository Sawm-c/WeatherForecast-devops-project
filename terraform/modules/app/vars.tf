variable "aws_instance" {
  type = string
}

variable "weather_key_name" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "common_tags" {
  type = map(string)
}


variable "iam_instance_profile_name" {
  type = string
}


variable "security_group_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "bucket_id" {
  type = string
}
