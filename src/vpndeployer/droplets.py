#!/usr/bin/env python3
import requests
import digitalocean

# TODO - Move this to method in __init__.py


def api_authentication(DO_API_TOKEN):
    api_authentication.DO_API_TOKEN = DO_API_TOKEN
    

def create_droplet(ip, name, region, email):
    droplet = digitalocean.Droplet(
        token=f'{api_authentication.DO_API_TOKEN}',
        name=f'{name}',
        region=f'{region}',
        image='centos-7-x64',
        size_slug='512mb',
        user_data=f"""#!/bin/bash
    export IP="{ip}"
    export EMAIL="{email}"
    if [[ $EMAIL == "None" ]]; then
        unset EMAIL
    fi
    curl -o /root/openvpn-install-prep.sh https://raw.githubusercontent.com/LopezNathan/vpn-deployer/master/openvpn-install-prep.sh
    chmod +x /root/openvpn-install-prep.sh && bash /root/openvpn-install-prep.sh""",
    )

    return droplet.create()


def get_droplet_ip(name):
    droplet_list = requests.get(f"https://api.digitalocean.com/v2/droplets", headers={"Authorization": "Bearer %s" % api_authentication.DO_API_TOKEN, "Content-Type": "application/json"})
    for item in droplet_list.json()['droplets']:
        if item['name'] == name:
            droplet_vpn = item

    for item in droplet_vpn['networks']['v4']:
        droplet_ip = item['ip_address']

    return droplet_ip
