#!/bin/bash
# Cloud VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 1.5.0

# Update System
# yum -y update && yum -y upgrade
yum -y install yum-plugin-security
yum --security update

# Download & Run OpenVPN Installer
curl -o /root/openvpn-install.sh  https://raw.githubusercontent.com/LopezNathan/vpn-deployer/development/openvpn-install.sh
chmod +x /root/openvpn-install.sh
export AUTO_INSTALL=y
bash /root/openvpn-install.sh

# Check if EMAIL Variable Exists
if [ "$EMAIL" ]; then
    # Install NGINX & Sendmail
    yum -y install nginx sendmail
    service nginx start
    # Send Email About File Download
    echo "Subject: VPN Client Download

    Download Link: http://"$(hostname -I | cut -d' ' -f1)"/client.ovpn" > /root/email.txt
    sendmail $EMAIL < /root/email.txt
else
    # Install NGINX
    yum -y install nginx
    service nginx start
fi

# Restrict Traffic to Specified IP
iptables -I INPUT \! --src $IP -m tcp -p tcp --dport 80 -j DROP

# Move OpenVPN Client File to NGINX Root
cp /root/client.ovpn /usr/share/nginx/html/

# Wait 5 Minutes for Download before Cleanup
sleep 300

# Start Cleanup
if [ "$EMAIL" ]; then
    yum -y remove nginx sendmail && yum clean all
else
    yum -y remove nginx && yum clean all
fi
rm -f /usr/share/nginx/html/client.ovpn /root/openvpn-install-prep.sh /root/openvpn-install.sh /root/client.ovpn /root/email.txt
