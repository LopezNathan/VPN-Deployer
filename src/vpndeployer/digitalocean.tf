# export DIGITALOCEAN_TOKEN

provider "digitalocean" {
  # token = var.do_token
}

resource "digitalocean_ssh_key" "default" {
  name       = "vpn-deployer"
  public_key = file("/Users/nathan/.ssh/vpndeployer.pub")
}

resource "digitalocean_droplet" "vpn" {
    image = "ubuntu-18-04-x64"
    name = "vpn-deployer"
    region = "nyc1"
    size = "512mb"
    ssh_keys = [digitalocean_ssh_key.default.fingerprint]
  provisioner "remote-exec" {
    inline = [
      "apt-get update -y",
      "apt-get upgrade -y",
      "apt-get install nginx -y",
      "service nginx start",
      "curl -o /root/openvpn-install.sh https://raw.githubusercontent.com/LopezNathan/vpn-deployer/master/src/vpndeployer/playbooks/openvpn-install.sh",
      "export AUTO_INSTALL=y",
      "export CONTINUE=y",
      "/bin/bash /root/openvpn-install.sh",
      "cp /root/client.ovpn /var/www/client.ovpn"
    ]
  }
  connection {
    private_key = file("/Users/nathan/.ssh/vpndeployer")
    host = digitalocean_droplet.vpn.ipv4_address
  }
}

output "instance_ip" {
  value = digitalocean_droplet.vpn.ipv4_address
}

output "ovpn_download_link" {
  value = "http://${digitalocean_droplet.vpn.ipv4_address}/client.ovpn"
  description = "OpenVPN Client Profile Download Link"
}