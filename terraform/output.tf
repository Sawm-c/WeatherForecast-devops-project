output "weather_be_url" {
  description = "Địa chỉ truy cập Website Backend"
  value       = "http://${module.be.weather_be_ip}"
}

output "weather_be_ip" {
  value = module.be.weather_be_ip
}

output "database_host" {
  description = "RDS endpoint hostname (dùng làm DB_HOST)"
  value       = module.database.db_address
}

output "frontend_url" {
  description = "Link truy cập Website Frontend (HTTPS)"
  value       = "https://${module.fe.cloudfront_domain_name}"
}

output "fe_bucket_name" {
  value = module.fe.fe_bucket_name
}

output "cloudfront_distribution_id" {
  value = module.fe.cloudfront_distribution_id
}
