resource "aws_instance" "weather_db" {
  ami                    = var.aws_instance
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.database_sg_id]
  tags                   = merge(var.common_tags, { Name = "weather-db" })
  iam_instance_profile   = var.iam_instance_profile_name
  key_name               = var.weather_key_name

  user_data = <<-EOF
        #!/bin/bash
        sudo yum update -y
        sudo yum install postgresql15-server -y
    
        # init db
        sudo postgresql-setup --initdb
        sudo systemctl start postgresql15
        sudo systemctl enable postgresql15

        # Đặt mật khẩu cho user postgres khớp với biến DB_PASSW
        sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"

        # Kéo init.sql từ S3 về và chạy khởi tạo bảng
        aws s3 cp s3://${var.bucket_id}/database/init.sql /tmp/init.sql
        sudo -u postgres psql -f /tmp/init.sql
  EOF

  user_data_replace_on_change = true
}

