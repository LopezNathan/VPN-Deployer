#!/bin/bash
# Cloud VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 1.1.1

# Update and Install WGET
yum -y update && yum -y upgrade
yum -y install wget

# Download & Run OpenVPN Installer
curl -o /root/openvpn-install.sh  https://raw.githubusercontent.com/LopezNathan/openvpn-install/master/openvpn-install.sh
chmod +x /root/openvpn-install.sh
export AUTO_INSTALL=y
bash /root/openvpn-install.sh

# Define Server IP
SERVER_IP="$(hostname -I | cut -d' ' -f1)"

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
rm -f /usr/share/nginx/html/client.ovpn /root/vpn-installer.sh /root/openvpn-install.sh /root/client.ovpn /root/email.txt
