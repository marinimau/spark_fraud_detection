variable "region" {
    description = "The region for your instances"
    type = string
    default = "us-east-1"
}

variable "access_key" {
    description = "Your AWS access key id, don't change this variable here, use \"terraform.tfvars\" instead"
    type = string
    default = ""
}

variable "secret_key" {
    description = "Your AWS secret key, don't change this variable here, use \"terraform.tfvars\" instead"
    type = string
    default = ""
}

variable "token" {
    description = "Your AWS secret token, don't change this variable here, use \"terraform.tfvars\" instead"
    type = string
    default = null
}

variable "instance_type" {
    description = "The type for the ec2 instances"
    type = string
    default = "m5.xlarge"
}

variable "ami_image" {
    description = "The ami code for the ec2 instances, default is Ubuntu 20.04 Focal Fossa"
    type = string
    default = "ami-0885b1f6bd170450c"
}

variable "key_name" {
    description = "the name of the local key (the one generated using ssh-keygen)"
    type = string
    default = "localkey"
}

variable "key_path" {
    description = "the path for the local key (without the key name, only the directory)"
    type = string
    default = "."                       # change directory to local .ssh directory e.g. ~/.ssh/
}

variable "aws_key_name" {
    description = "the name (without extension) of the aws key (the one with .pem extension) create this key on aws: instruction in the readme"
    type = string
    default = "amzkey"
}

variable "amz_key_path" {
    description = "the path (including key name) of the aws key"
    type = string
    default = "amzkey.pem"
}

variable "subnet_id" {
    description = "the subnet id for your ec2 instances, you can find it "
    type = string
    default = "subnet-1eac9110"        # found it on the aws console using: aws ec2 describe-subnets
}


variable "namenode_count" {
    description = "the number of namenode instances"
    type = number
    default = 1                         # count = 1 = 1 aws EC2
}


variable "namenode_ips" {
    description = "the IPs for the namenode instances (each IP must be compatible with the subnet_id)"
    default = {
        "0" = "172.31.64.101"
    }
}


variable "namenode_hostnames" {
    description = "the hostnames for the namenode instances"
    default = {
        "0" = "s01"
    }
}


variable "datanode_count" {
    description = "the number of datanode instances"
    type = number
    default = 3
}


variable "datanodes_ips" {
    description = "the IPs for the datanode instances (each IP must be compatible with the subnet_id)"
    default = {
        "0" = "172.31.64.102"
        "1" = "172.31.64.103"
        "2" = "172.31.64.104"
        "3" = "172.31.64.105"
        "4" = "172.31.64.106"
        "5" = "172.31.64.107"
    }
}

variable "datanodes_hostnames" {
    description = "the datanode for the namenode instances"
    default = {
        "0" = "s02"
        "1" = "s03"
        "2" = "s04"
        "3" = "s05"
        "4" = "s06"
        "5" = "s07"
    }
}

variable "local_app_path" {
    description = "the local path of your app files"
    type = string
    default = "spark_fraud_detection/"
}


variable "remote_app_path" {
    description = "the destination path for your app files"
    type = string
    default = "/home/ubuntu/"
}


variable "local_configuration_script_path" {
    description = "the local path of the configuration_script"
    type = string
    default = "configuration_script.sh"
}


variable "remote_configuration_script_path" {
    description = "the destination path for the configuration_script"
    type = string
    default = "/tmp/configuration_script.sh"
}


variable "local_configuration_files_path" {
    description = "the local path of the files directory"
    type = string
    default = "configuration_files/"
}


variable "remote_configuration_files_path" {
    description = "the destination path for the configuration files"
    type = string
    default = "/home/ubuntu/"
}