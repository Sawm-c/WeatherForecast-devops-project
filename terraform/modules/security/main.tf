resource "aws_security_group" "weather-sg" {
  name        = "WeatherForecast-sg"
  description = "Gatekeeper firewall (Allow SSH and Web only)"
  vpc_id      = var.vpc_id
  tags = var.common_tags

  ingress {
    description = "SSH for management"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Public Web Traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
