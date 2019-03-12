#!/usr/bin/env python
# VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 0.10.1

import argparse
import digitalocean
import time
import requests
import getpass

# TODO - check api token auth before proceeding
DO_API_TOKEN = getpass.getpass('DigitalOcean API Token: ')

parser = argparse.ArgumentParser(description="VPN Deploy Script with DigitalOcean")
parser.add_argument("ip", help="Your IP Address")
parser.add_argument("--email", dest="email", help="Email Address for OpenVPN download link")
parser.add_argument("--name", default='VPN', dest="name", help="Droplet Name")
parser.add_argument("--region", default='nyc1', dest="region", help="Droplet Region")
args = parser.parse_args()

class Deploy:

    def create_droplet(self, ip_address):
        droplet = digitalocean.Droplet(token=f'{DO_API_TOKEN}',
                                    name=f'{args.name}',
                                    region=f'{args.region}',
                                    image='centos-7-x64',
                                    size_slug='512mb',
                                    user_data=f"""#!/bin/bash
        export IP="{args.ip}"
        export EMAIL="{args.email}"
        if [[ $EMAIL == "None" ]]; then
            unset EMAIL
        fi
        curl -o /root/openvpn-install-prep.sh https://raw.githubusercontent.com/LopezNathan/vpn-deployer/development/openvpn-install-prep.sh
        chmod +x /root/openvpn-install-prep.sh && bash /root/openvpn-install-prep.sh""",
                                    backups=True)

        droplet.create()
    
    def get_droplet_ip(self):
        droplet_list = requests.get(f"https://api.digitalocean.com/v2/droplets", headers={"Authorization": "Bearer %s" % DO_API_TOKEN, "Content-Type": "application/json"})
        # TODO - Clean this mess up...
        # TODO - we should be returning something here
        # TODO - what happens if we have multiple droplets with same name?...
        for item in droplet_list.json()['droplets']:
            if item['name'] == args.name:
                Deploy.droplet_vpn = item

        for item in Deploy.droplet_vpn['networks']['v4']:
            Deploy.droplet_ip = item['ip_address']

print("\nDeploy Started!")
print("This process typically takes less than 5 minutes.\n")

vpn = Deploy()

vpn.create_droplet(args.ip)
time.sleep(10)
vpn.get_droplet_ip()

# TODO - Use something else instead of a while loop to check the actual progress.
# can we move it into the class and check the progress on a class method easier?
while True:
    try:
        check_deploy = requests.get(f"http://{Deploy.droplet_ip}/client.ovpn")
        print(f"\nDeploy Completed!\nDownload OpenVPN File: http://{Deploy.droplet_ip}/client.ovpn")
        break
    except:
        print("Deploy In-Progress...")
        time.sleep(60)