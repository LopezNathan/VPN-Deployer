#!/usr/bin/env python3
import requests
import digitalocean


def create_droplet(api_token, ip, name, region, image, email):
    droplet = digitalocean.Droplet(
        token=f'{api_token}',
        name=f'{name}',
        region=f'{region}',
        image=f'{image}',
        size_slug='512mb',
        user_data=f"""#!/bin/bash
    if [[ -e /etc/debian_version ]]; then
        apt-get -y update
        apt-get -y install ansible
    else
        yum -y update
        yum -y install ansible
    fi
    curl -o /root/openvpn-install.yml https://raw.githubusercontent.com/LopezNathan/vpn-deployer/development/openvpn-install.yml
    ansible-playbook /root/openvpn-install.yml --extra-vars "IP={ip} EMAIL={email}" > /var/log/ansible.log 2>&1
    """,
    )

    return droplet.create()


def get_droplet_ip(name, api_token):
    droplet_list = requests.get(f"https://api.digitalocean.com/v2/droplets", headers={"Authorization": "Bearer %s" % api_token, "Content-Type": "application/json"})
    for item in droplet_list.json()['droplets']:
        if item['name'] == name:
            droplet_vpn = item

    for item in droplet_vpn['networks']['v4']:
        # TODO - Grab first IP from json array without a break
        droplet_ip = item['ip_address']
        break

    return droplet_ip
