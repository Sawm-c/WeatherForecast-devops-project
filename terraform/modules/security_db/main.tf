resource "aws_security_group" "database-sg" {
  name        = "database-sg"
  description = "database security group"
  vpc_id      = var.vpc_id
  tags        = var.common_tags

  ingress {
    description     = "PostgreSql from be"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [var.backend_sg_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
