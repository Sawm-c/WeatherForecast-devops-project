output "db_address" {
  description = "Hostname của RDS endpoint (dùng làm DB_HOST)"
  value       = aws_db_instance.weather_db.address
}
