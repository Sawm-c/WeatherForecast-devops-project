output "weather_app_url" {
  value = "http://${module.app.weather_app_ip}:8000"
}

output "weather_app_ip" {
  value = module.app.weather_app_ip
}
