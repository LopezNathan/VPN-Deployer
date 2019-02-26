#!/usr/bin/env python
# VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 0.5.3

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
        curl -o /root/vpn-installer.sh https://raw.githubusercontent.com/LopezNathan/vpn-deployer/development/vpn-installer.sh
        chmod +x /root/vpn-installer.sh && bash /root/vpn-installer.sh""",
                                    backups=True)

        droplet.create()

vpn = Deploy()
vpn.create_vpn(args.ip, args.email)
