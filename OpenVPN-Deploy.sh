#!/bin/bash
# Cloud VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)

# Update and Install WGET
yum -y update && yum -y upgrade
yum -y install wget

# Download OpenVPN Installer
cd /root/
wget https://raw.githubusercontent.com/Angristan/OpenVPN-install/master/openvpn-install.sh
chmod +x openvpn-install.sh

# Define Server IP
SERVER_IP="$(hostname -I | cut -d' ' -f1)"

# Create OpenVPN Installer Options File
echo "$SERVER_IP
n
1
1
3
n
n

client
1" > /root/openvpn-install-options.txt

# Start OpenVPN Installer
bash /root/openvpn-install.sh < /root/openvpn-install-options.txt

# Install NGINX & Sendmail
yum -y install nginx sendmail
service nginx start

# Restrict Traffic to Specified IP
iptables -I INPUT \! --src $IP -m tcp -p tcp --dport 80 -j DROP

# Move OpenVPN Client File to NGINX Root
cp /root/client.ovpn /usr/share/nginx/html/

# Send Email About File Download
echo "Subject: VPN Client Download

Download Link: http://$SERVER_IP/client.ovpn" > /root/email.txt
sendmail $EMAIL < /root/email.txt

# Wait 5 Minutes for Download before Cleanup
sleep 300

# Start Cleanup
yum -y remove nginx sendmail && yum clean all
rm -f /usr/share/nginx/html/client.ovpn /root/openvpn-deploy.sh /root/openvpn-install.sh /root/openvpn-install-options.txt /root/client.ovpn /root/email.txt
