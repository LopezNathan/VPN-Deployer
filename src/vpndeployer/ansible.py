#!/usr/bin/env python3
import ansible_runner
from pathlib import Path
import os
from vpndeployer import droplets


def playbook_path():
    cwd = Path(__file__).resolve().parent
    path = str(cwd) + '/playbooks'

    return path


def gen_sshkey(DO_API_TOKEN):
    data_path = playbook_path()

    if os.path.isfile(data_path + '/env/ssh_key') is True:
        sshkey_id = open(data_path + '/env/ssh_key.id').read()
        return [int(key) for key in [sshkey_id]]

    ansible_runner.run(private_data_dir=data_path, playbook='local-sshkeygen.yml',
                       host_pattern='localhost', extravars={"PATH": data_path}, quiet=True)
    sshkey_id = droplets.add_sshkey(DO_API_TOKEN)

    return [sshkey_id]


def check_droplet_connection():
    data_path = playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='droplet_connection.yml',
                                host_pattern='VPN-*', quiet=True)

    # TODO - Return something proper, the key?
    return runner.status


def deploy_openvpn(ip, email):
    data_path = playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='openvpn-install.yml',
                                host_pattern='VPN-*', extravars={"IP": ip, "EMAIL": email}, quiet=True)

    # TODO - Return something proper, the key?
    return runner.status


def cleanup_openvpn():
    data_path = playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='openvpn-install-cleanup.yml',
                                host_pattern='VPN-*', quiet=True)

    # TODO - Return something proper, the key?
    return runner.status
