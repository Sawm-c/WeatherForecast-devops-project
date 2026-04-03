variable "aws_instance" {
    type = string
    default = "ami-04d7457c43c292911"
}

variable "weather_key" {
    type = string
    default = "D:/Project/weatherforecast-key/wf-keypairs.pub"
}

variable "region" {
    type = string
    default = "ap-southeast-1"
}

variable "instance_type" {
    type = string
    default = "t3.micro"
}