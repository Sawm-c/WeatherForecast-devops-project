provider "aws" {
  region = var.region
}

resource "aws_key_pair" "weatherforecast_key" {
  key_name   = var.weather_key_name
  public_key = file(var.weather_key_path)
}


module "network" {
  source      = "./modules/network"
  azs         = var.azs
  cidr_blocks = var.cidr_blocks
  common_tags = var.common_tags
  region      = var.region
}

module "security_be" {
  source      = "./modules/security_be"
  vpc_id      = module.network.vpc_id
  common_tags = var.common_tags
}

module "security_db" {
  source        = "./modules/security_db"
  vpc_id        = module.network.vpc_id
  common_tags   = var.common_tags
  backend_sg_id = module.security_be.backend_sg_id
}

module "database" {
  source         = "./modules/database"
  subnet_ids     = module.network.private_subnets
  common_tags    = var.common_tags
  database_sg_id = module.security_db.database_sg_id
  db_name        = var.db_name
  db_username    = var.db_username
  db_password    = var.db_password
}

module "storage" {
  source      = "./modules/storage"
  bucket_name = var.bucket_name
  common_tags = var.common_tags
}

module "iam" {
  source      = "./modules/iam"
  bucket_arn  = module.storage.bucket_arn
  common_tags = var.common_tags
}

module "be" {
  source                    = "./modules/be"
  aws_instance              = var.aws_instance
  instance_type             = var.instance_type
  common_tags               = var.common_tags
  subnet_id                 = module.network.public_subnets[0]
  iam_instance_profile_name = module.iam.iam_instance_profile_name
  weather_key_name          = aws_key_pair.weatherforecast_key.key_name
  security_group_id         = module.security_be.backend_sg_id
}

module "fe" {
  source              = "./modules/fe"
  fe_bucket_name      = var.fe_bucket_name
  common_tags         = var.common_tags
  be_domain_name      = module.be.weather_be_public_dns
  custom_domain_name  = var.custom_domain_name
  acm_certificate_arn = var.acm_certificate_arn
}










