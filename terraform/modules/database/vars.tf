variable "common_tags" {
  type = map(string)
}

variable "subnet_ids" {
  type        = list(string)
  description = "Danh sách private subnet IDs cho RDS subnet group (cần >= 2 AZ)"
}

variable "database_sg_id" {
  type = string
}

variable "db_name" {
  type        = string
  description = "Tên database khởi tạo trong RDS"
}

variable "db_username" {
  type        = string
  description = "Username đăng nhập RDS"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Password đăng nhập RDS"
}
