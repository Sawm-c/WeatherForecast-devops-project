output "weather_app_url" {
  description = "Địa chỉ truy cập Website"
  value       = "http://${module.app.weather_app_ip}"
}

output "weather_app_ip" {
  value = module.app.weather_app_ip
}
