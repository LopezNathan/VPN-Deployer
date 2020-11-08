#!/usr/bin/env python3
import requests
import digitalocean
import tenacity
from vpndeployer import ansible


class DropletNotFound(Exception):
    """Droplet cannot be found."""


class IPNotFound(Exception):
    """Droplet Public IP cannot be found."""


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


@tenacity.retry(stop=tenacity.stop_after_attempt(10), wait=tenacity.wait_fixed(2), reraise=True)
def get_droplet_ip(name, api_token):
    droplet_list = requests.get(f"https://api.digitalocean.com/v2/droplets", headers={
                                "Authorization": "Bearer %s" % api_token, "Content-Type": "application/json"})
    for item in droplet_list.json()['droplets']:
        if item['name'] == name:
            droplet_vpn = item
            break
    else:
        raise DropletNotFound('Droplet Not Found')

    for item in droplet_vpn['networks']['v4']:
        if item['type'] == 'public':
            droplet_ip = item['ip_address']
            break
    else:
        raise IPNotFound('Droplet IP Not Found')

    return droplet_ip


def add_sshkey(api_token):
    data_path = ansible.playbook_path()
    public_key = open(data_path + '/env/ssh_key.pub').read()
    addkey = digitalocean.SSHKey(
        token=api_token, name='VPN-Deployer', public_key=public_key)
    addkey.create()

    with open(data_path + '/env/ssh_key.id', 'w+') as f:
        f.write(str(addkey.id))

    return addkey.id
