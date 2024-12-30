packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.1"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

variable "aws_region" {
  default = "us-east-1"
}

variable "source_ami" {
  default = "ami-0ca9fb66e076a6e32"
}

variable "instance_type" {
  default = "t2.micro"
}

source "amazon-ebs" "example" {
  region                  = var.aws_region
  source_ami             = var.source_ami
  instance_type          = var.instance_type
  ssh_username           = "admin"
  ami_name               = "csye6225-custom-ami"
  ami_description        = "Custom Debian 12 AMI for CSYE6225 Assignment"
  associate_public_ip_address = true

  tags = {
    Name = "csye6225-custom-ami"
  }
}

build {
  sources = ["source.amazon-ebs.example"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y mysql-server",
      "sudo systemctl enable mysql",
      "sudo systemctl start mysql"
    ]
  }

  provisioner "file" {
    source      = "webapp.zip"
    destination = "/tmp/webapp.zip"
  }

  provisioner "shell" {
    inline = [
      "unzip /tmp/webapp.zip -d /var/www/application",
      "sudo systemctl restart apache2"
    ]
  }
}
