variable "common_tags" {
  type = map(string)
}

variable "subnet_id" {
  type = string
}

variable "database_sg_id" {
  type = string
}

variable "aws_instance" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "iam_instance_profile_name" {
  type = string
}

variable "bucket_id" {
  type = string
}

variable "weather_key_name" {
  type = string
}
