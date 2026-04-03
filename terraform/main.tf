provider "aws" {
  region = var.region
}

resource "aws_key_pair" "weatherforecast_key" {
  key_name   = "weatherforecast_key"
  public_key = file(var.weather_key)
}

resource "aws_instance" "weather_app" {
  ami                    = var.aws_instance
  instance_type          = var.instance_type
  key_name               = aws_key_pair.weatherforecast_key.key_name
  vpc_security_group_ids = [aws_security_group.weather-sg.id]

  tags = {
    Name        = "WeatherForecast-ec2"
    Environment = "Production"
  }

  user_data = <<-EOF
#!/bin/bash
sudo yum update -y

sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker ec2-user

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
EOF
}

resource "aws_eip" "app-eip" {
  instance = aws_instance.weather_app.id
  domain   = "vpc"
}

output "public_ip" {
  value = aws_eip.app-eip.public_ip
}

resource "aws_security_group" "weather-sg" {
  name        = "WeatherForecast-sg"
  description = "App firewall"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
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