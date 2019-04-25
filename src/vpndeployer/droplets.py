#!/usr/bin/env python3
import requests
import re
import digitalocean


def create_droplet(api_token, ip, name, region, image, email, sshkey):
    droplet = digitalocean.Droplet(
        token=f'{api_token}',
        name=f'{name}',
        region=f'{region}',
        image=f'{image}',
        ssh_keys=sshkey,
        size_slug='512mb',
        user_data=f"""#!/bin/bash
    if [[ -e /etc/debian_version ]]; then
        apt-get -y install python-minimal
    else
        yum -y install python-minimal
    fi
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


def add_sshkey(api_token):
    public_key = open('/tmp/.VPN-Deployer.pub').read()
    addkey = digitalocean.SSHKey(token=api_token, name='VPN-Deployer', public_key=public_key)

    return addkey.create()


def get_sshkey_fingerprint(api_token):
    manager = digitalocean.Manager(token=api_token)
    sshkeys = manager.get_all_sshkeys()
    fingerprint = [str(re.findall('[0-9]* VPN-Deployer', str(sshkeys)))[2:10]]

    return [int(key) for key in fingerprint]
