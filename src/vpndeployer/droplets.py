#!/usr/bin/env python3
import requests
import digitalocean


def create_droplet(api_token, ip, name, region, email):
    droplet = digitalocean.Droplet(
        token=f'{api_token}',
        name=f'{name}',
        region=f'{region}',
        image='centos-7-x64',
        size_slug='512mb',
        user_data=f"""#!/bin/bash
    yum -y install ansible
    curl -o /root/openvpn-install.yml https://raw.githubusercontent.com/LopezNathan/vpn-deployer/development/openvpn-install.yml
    ansible-playbook /root/openvpn-install.yml --extra-vars "IP={ip}"
    """,
    )

    return droplet.create()


def get_droplet_ip(name, api_token):
    droplet_list = requests.get(f"https://api.digitalocean.com/v2/droplets", headers={"Authorization": "Bearer %s" % api_token, "Content-Type": "application/json"})
    for item in droplet_list.json()['droplets']:
        if item['name'] == name:
            droplet_vpn = item

    for item in droplet_vpn['networks']['v4']:
        droplet_ip = item['ip_address']

    return droplet_ip
