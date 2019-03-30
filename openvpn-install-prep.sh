#!/bin/bash
# Cloud VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 1.6.2

# Update System
# yum -y update && yum -y upgrade
yum -y install yum-plugin-security
yum --security update

# Download & Run OpenVPN Installer
curl -o /root/openvpn-install.sh  https://raw.githubusercontent.com/LopezNathan/vpn-deployer/master/openvpn-install.sh
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
# Loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A INPUT -d 127.0.0.0/8 -j REJECT
iptables -A OUTPUT -d 127.0.0.0/8 -j REJECT
# Established Connections
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
# Ping of Death
iptables -N PING_OF_DEATH
iptables -A PING_OF_DEATH -p icmp --icmp-type echo-request -m hashlimit --hashlimit 1/s --hashlimit-burst 10 --hashlimit-htable-expire 300000 --hashlimit-mode srcip --hashlimit-name t_PING_OF_DEATH -j RETURN
iptables -A PING_OF_DEATH -j DROP
iptables -A INPUT -p icmp --icmp-type echo-request -j PING_OF_DEATH
# Port Scanning
iptables -N PORTSCAN
iptables -A PORTSCAN -p tcp --tcp-flags ACK,FIN FIN -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags ACK,PSH PSH -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags ACK,URG URG -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags FIN,RST FIN,RST -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags SYN,FIN SYN,FIN -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags SYN,RST SYN,RST -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags ALL ALL -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags ALL NONE -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags ALL FIN,PSH,URG -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags ALL SYN,FIN,PSH,URG -j DROP
iptables -A PORTSCAN -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP
# Fragmented Packages
iptables -A INPUT -f -j DROP
# SYN Packets
iptables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP

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
