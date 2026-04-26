resource "aws_instance" "weather_app" {
  ami                    = var.aws_instance
  instance_type          = var.instance_type
  key_name               = var.weather_key_name
  vpc_security_group_ids = [var.security_group_id]
  subnet_id              = var.subnet_id
  iam_instance_profile   = var.iam_instance_profile_name
  tags = {
    Name        = "WeatherForecast-ec2"
    Environment = "Production"
  }

  user_data = <<-EOF
#!/bin/bash
sudo yum update -y
sudo yum install git docker -y

sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker ec2-user

# Cài đặt Docker Compose V2 thủ công
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Tạo liên kết để lệnh 'docker compose' hoạt động
sudo mkdir -p /usr/libexec/docker/cli-plugins/
sudo ln -s /usr/local/bin/docker-compose /usr/libexec/docker/cli-plugins/docker-compose

mkdir -p home/ec2-user/database
aws s3 cp s3://${var.bucket_id}/database/init.sql home/ec2-user/database/init.sql
chown -R ec2-user:ec2-user /home/ec2-user/database
EOF

  user_data_replace_on_change = true
}

resource "aws_eip" "weather_app_ip" {
  instance = aws_instance.weather_app.id
  domain   = "vpc"
  tags = {
    Name = "weather-app-eip"
  }
}
