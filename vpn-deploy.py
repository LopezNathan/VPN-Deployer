#!/usr/bin/env python
# VPN Deploy Script
# Fully Install OpenVPN on DigitalOcean Automatically
# Utilizes OpenVPN-Install by Angristan (https://github.com/Angristan/OpenVPN-install)
# Version 0.2

import os
import fileinput
import argparse
import requests

DO_API_TOKEN=os.environ["DO_API_TOKEN"]

parser = argparse.ArgumentParser(description="VPN Deploy Script")
parser.add_argument("ip", help="Your IP Address")
parser.add_argument("email", help="Your Email Address")
args = parser.parse_args()

with fileinput.FileInput('/tmp/user-data.txt', inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace('YOUR-IP', args.ip), end='')

with fileinput.FileInput('/tmp/user-data.txt', inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace('YOUR-EMAIL', args.email), end='')

with open('/tmp/user-data.txt', 'r') as myfile:
    user_data=myfile.read()
myfile.close()
    
payload = {'name': 'test', 'region': 'nyc3', 'size': '512mb', 'image': 'centos-7-x64', 'user_data': user_data}
create = requests.post("https://api.digitalocean.com/v2/droplets", params=payload, headers={"Authorization": "Bearer %s" % DO_API_TOKEN, "Content-Type": "application/json"})

for i in create:
    print(i)