#!/usr/bin/env python
# VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 0.6.0

import os
import argparse
import digitalocean
import time
import requests
import sys

#TODO - Accept user input for this securely
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

time.sleep(10)
print("Deploy Started!")
print("This process typically takes less than 10 minutes.\n")

droplet_list = requests.get(f"https://api.digitalocean.com/v2/droplets", headers={"Authorization": "Bearer %s" % DO_API_TOKEN, "Content-Type": "application/json"})

# TODO - Clean this mess up...
for item in droplet_list.json()['droplets']:
    #TODO - Convert "VPN" into args.name
    if item['name'] == 'VPN':
        droplet_vpn = item

for item in droplet_vpn['networks']['v4']:
    droplet_ip = item['ip_address']

# TODO - Use something else instead of a while loop to check the actual progress.
while True:
    try:
        check_deploy = requests.get(f"http://{droplet_ip}/client.ovpn")
        print(f"""
        \nDeploy Completed!
        Download OpenVPN File: http://{droplet_ip}/client.ovpn"
        """)
        sys.exit() # dirtyyyyy...
    except:
        print("Deploy In-Progress...")
        time.sleep(120)