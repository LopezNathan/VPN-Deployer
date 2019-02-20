#!/usr/bin/env python
# VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 0.5.1

import os
import argparse
import digitalocean

DO_API_TOKEN=os.environ["DO_API_TOKEN"]

parser = argparse.ArgumentParser(description="VPN Deploy Script with DigitalOcean")
parser.add_argument("ip", help="Your IP Address")
parser.add_argument("email", help="Your Email Address")
parser.add_argument("--name", default='VPN', dest="name", help="Droplet Name")
parser.add_argument("--region", default='nyc1', dest="region", help="Droplet Region")
args = parser.parse_args()

#TODO (user-data): CHANGE WGET TO CURL (installed by default?) AND REMOVE YUM (already in-use within bash script)

class Deploy:

    def create_vpn(self, ip_address, email_address):
        droplet = digitalocean.Droplet(token=f'{DO_API_TOKEN}',
                                    name=f'{args.name}',
                                    region=f'{args.region}',
                                    image='centos-7-x64',
                                    size_slug='512mb',
                                    user_data=f"""#!/bin/bash
        export IP={args.ip}
        export EMAIL={args.email}
        yum -y update && yum -y upgrade
        yum -y install wget
        wget -O /root/openvpn-deploy.sh https://raw.githubusercontent.com/LopezNathan/VPN-Deployer/master/OpenVPN-Deploy.sh
        chmod +x /root/openvpn-deploy.sh && bash /root/openvpn-deploy.sh""",
                                    backups=True)

        droplet.create()

vpn = Deploy()
vpn.create_vpn(args.ip, args.email)