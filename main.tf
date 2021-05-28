locals {
    #  Directories start with "C:..." on Windows; All other OSs use "/" for root.
    is_windows = substr(pathexpand("~"), 0, 1) == "/" ? false : true
}


provider "aws" {
    region      = var.region
    access_key  = var.access_key
    secret_key  = var.secret_key
    token       = var.token
}

resource "aws_security_group" "Hadoop_cluster_sc" {
    name = "Hadoop_cluster_sc"

    # inbound internet access
    ingress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # outbound internet access
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    lifecycle {
        create_before_destroy = true
    }
}



/*
 *  Namenode (Master)
 */
resource "aws_instance" "Namenode" {
    subnet_id = var.subnet_id
    count = var.namenode_count
    ami = var.ami_image
    instance_type = var.instance_type
    key_name = var.aws_key_name
    tags = {
        Name = lookup(var.namenode_hostnames, count.index)
    }
    private_ip = lookup(var.namenode_ips, count.index)
    vpc_security_group_ids = [aws_security_group.Hadoop_cluster_sc.id]

    /* Passing file to master */

    /* App */
    provisioner "file" {
        source      = var.local_configuration_script_path
        destination = var.remote_configuration_script_path

        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }
    }

    provisioner "file" {
        source      = var.local_app_path
        destination = var.remote_app_path
    
        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }
    }

    provisioner "file" {
        source      = var.local_configuration_files_path
        destination = var.remote_configuration_files_path

        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }
    }

    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name}.pub | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/authorized_keys'"
    }
    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name}.pub | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa.pub'"
    }
    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name} | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa'"
    }

    # execute the configuration script
    provisioner "remote-exec" {
        inline = [
            "chmod +x ${var.remote_configuration_script_path}",
            "/bin/bash ${var.remote_configuration_script_path}",
            "/opt/hadoop-2.7.7/bin/hadoop namenode -format"
        ]
        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }

    }
}


# datanode (slaves)
resource "aws_instance" "Datanode" {
    subnet_id = var.subnet_id
    count = var.datanode_count
    ami = var.ami_image
    instance_type = var.instance_type
    key_name = var.aws_key_name
    tags = {
        Name = lookup(var.datanodes_hostnames, count.index)
    }
    private_ip = lookup(var.datanodes_ips, count.index)
    vpc_security_group_ids = [aws_security_group.Hadoop_cluster_sc.id]

    # copy the initialization script to the remote machines
    provisioner "file" {
        source      = var.local_configuration_script_path
        destination = var.remote_configuration_script_path

        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }
    }

    # copy the configurations file to the remote machine
    provisioner "file" {
        source      = var.local_configuration_files_path
        destination = var.remote_configuration_files_path

        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }
    }

    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name}.pub | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/authorized_keys'"
    }
    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name}.pub | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa.pub'"
    }
    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name} | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa'"
    }

    # execute the configuration script
    provisioner "remote-exec" {
        inline = [
            "chmod +x ${var.remote_configuration_script_path}",
            "/bin/bash ${var.remote_configuration_script_path}",
        ]
        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }

    }
}