output "weather_app_ip" {
  value = aws_eip.weather_app_ip.public_ip
}
