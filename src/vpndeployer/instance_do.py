#!/usr/bin/env python3
import requests
import digitalocean
import tenacity
import ansible_runner
from vpndeployer import ansible_data


def create_instance(api_token, ip, name, region, image, email, sshkey):
    instance = digitalocean.Droplet(
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

    return instance.create()


class InstanceNotFound(Exception):
    """Droplet cannot be found."""


class IPNotFound(Exception):
    """Droplet Public IP cannot be found."""


@tenacity.retry(stop=tenacity.stop_after_attempt(10), wait=tenacity.wait_fixed(2), reraise=True)
def get_ip(name, api_token):
    instance_list = requests.get(f"https://api.digitalocean.com/v2/droplets", headers={
                                 "Authorization": "Bearer %s" % api_token, "Content-Type": "application/json"})
    for item in instance_list.json()['droplets']:
        if item['name'] == name:
            instance = item
            break
    else:
        raise InstanceNotFound('Instance Not Found')

    for item in instance['networks']['v4']:
        if item['type'] == 'public':
            ip = item['ip_address']
            break
    else:
        raise IPNotFound('Instance IP Not Found')

    return ip


def add_key(api_token):
    data_path = ansible_data.playbook_path()
    public_key = open(data_path + '/env/ssh_key.pub').read()
    key = digitalocean.SSHKey(
        token=api_token, name='VPN-Deployer', public_key=public_key)
    key.create()

    with open(data_path + '/env/ssh_key.id', 'w+') as f:
        f.write(str(key.id))

    return key.id


def test_instance_connection():
    data_path = ansible_data.playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='connection_test.yml',
                                host_pattern='VPN-*', quiet=True)

    # TODO - Return something proper
    return runner.status
