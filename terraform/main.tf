provider "aws"{
	region = var.region
}

resource "aws_key_pair" "weatherforecast_key" {
	key_name = "weatherforecast_key"
	public_key = file(var.weather_key)
}

resource "aws_instance" "app-ec2" {
	ami = var.aws_instance
	instance_type = var.instance_type
	key_name = aws_key_pair.weatherforecast_key.key_name
	vpc_security_group_ids = [aws_security_group.app-sg.id]
	tags = {
		Name = "WeatherForecast-ec2"
		Environment = "Production"
	}
	user_data = <<-EOF
	#!/bin/bash
		sudo yum update -y
		sudo yum install git docker -y

		sudo systemctl start docker
		sudo systemctl enable docker

		usermod -aG docker ec2-user

		curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
		chmod +x /usr/local/bin/docker-compose
		EOF
}

resource "aws_security_group" "app-sg" {
	name = "WeatherForecast-sg"
	description = "App firewall"

	ingress {
		from_port = 22
		to_port = 22
		protocol = "tcp"  
		cidr_blocks = ["0.0.0.0/0"]
	}

	ingress {
        from_port = 8080
        to_port = 8080
		protocol = "tcp"  
        cidr_blocks = ["0.0.0.0/0"]
	}	

	egress {
        from_port = 0
        to_port = 0
		protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
	}
}


