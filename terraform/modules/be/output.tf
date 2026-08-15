output "weather_be_ip" {
  value = aws_eip.weather_be_ip.public_ip
}
output "weather_be_public_dns" {
  value = aws_eip.weather_be_ip.public_dns
}
