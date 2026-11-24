variable "region" {
  type    = string
  default = "ap-southeast-2"
}

variable "project" {
  type    = string
  default = "cloud-devops"
}

variable "vpc_cidr" {
  type    = string
  default = "10.1.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.1.1.0/24"
}

variable "private_subnet_cidr" {
  type    = string
  default = "10.1.2.0/24"
}

variable "key_name" {
  type    = string
  default = "cloud-devops-key"
}

variable "my_ip" {
  type        = string
  description = "Your public IP in CIDR form, for SSH access"
}
