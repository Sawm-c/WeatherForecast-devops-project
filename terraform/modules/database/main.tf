resource "aws_db_subnet_group" "weather_db_subnet_group" {
  name       = "weather-db-subnet-group"
  subnet_ids = var.subnet_ids # ← Truyền danh sách Private Subnets
  tags       = merge(var.common_tags, { Name = "weather-db-subnet-group" })
}

resource "aws_db_instance" "weather_db" {
  identifier             = "weather-db"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.weather_db_subnet_group.name
  vpc_security_group_ids = [var.database_sg_id]

  backup_retention_period = 1
  skip_final_snapshot     = true

  tags = merge(var.common_tags, { Name = "weather-db" })
}
