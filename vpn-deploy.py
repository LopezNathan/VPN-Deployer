#!/usr/bin/env python
# VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 0.4

import os
#import fileinput
import argparse
#import requests
import digitalocean

DO_API_TOKEN=os.environ["DO_API_TOKEN"]

parser = argparse.ArgumentParser(description="VPN Deploy Script")
parser.add_argument("ip", help="Your IP Address")
parser.add_argument("email", help="Your Email Address")
args = parser.parse_args()

#TODO (user-data): CHANGE WGET TO CURL (installed by default?) AND REMOVE YUM (already in-use within bash script)

droplet = digitalocean.Droplet(token=f"{DO_API_TOKEN}",
                               name='test',
                               region='nyc1',
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

# with fileinput.FileInput('/tmp/user-data.txt', inplace=True, backup='.bak') as file:
#     for line in file:
#         print(line.replace('YOUR-IP', args.ip), end='')

# with fileinput.FileInput('/tmp/user-data.txt', inplace=True, backup='.bak') as file:
#     for line in file:
#         print(line.replace('YOUR-EMAIL', args.email), end='')

# with open('/tmp/user-data.txt', 'r') as myfile:
#     user_data=myfile.read()
# myfile.close()
    
#payload = {'name': 'test', 'region': 'nyc3', 'size': '512mb', 'image': 'centos-7-x64', 'user_data': user_data}
#create = requests.post("https://api.digitalocean.com/v2/droplets", params=payload, headers={"Authorization": "Bearer %s" % DO_API_TOKEN, "Content-Type": "application/json"})

droplet.create()

# for i in create:
#     print(i)