output "Datanode_dns_address" {
    value = aws_instance.Datanode.*.public_dns
}

output "Namenode_dns_address" {
    value = aws_instance.Namenode.*.public_dns
}