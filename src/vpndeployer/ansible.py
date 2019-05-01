#!/usr/bin/env python3
import ansible_runner
from pathlib import Path
import os


def playbook_path():
    cwd = Path(__file__).resolve().parent
    path = str(cwd) + '/playbooks'

    return path


def gen_sshkey():
    data_path = playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='local-sshkeygen.yml', host_pattern='localhost', quiet=True)

    with open('/tmp/.VPN-Deployer', 'r') as file:
        sshkey = file.read()

    if not os.path.exists(data_path + "/env"):
        os.makedirs(data_path + "/env")

    with open(data_path + "/env/ssh_key", "w+") as file:
        file.writelines(sshkey)
        os.chmod(str(file.name), 0o600)

    # TODO - Return something proper, the key?
    return runner.status


def deploy_openvpn(ip, email):
    data_path = playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='openvpn-install.yml', extravars={"IP": ip, "EMAIL": email}, quiet=False)

    # TODO - Return something proper, the key?
    return runner.status


# TODO - Update this to be dynamic, this is a bad way of accomplishing this.
def inventory_keypath_update():
    data_path = playbook_path()

    with open(data_path + '/inventory', 'r') as f:
        data = f.read().replace('KEYPATH', data_path + '/env/ssh_key')

    with open(data_path + '/inventory', 'w') as f:
        f.write(data)


# TODO - Update this to be dynamic, this is a bad way of accomplishing this.
def inventory_ip_update(ip_address):
    data_path = playbook_path()

    with open(data_path + '/inventory', 'r') as f:
        data = f.read().replace('IP', ip_address)

    with open(data_path + '/inventory', 'w') as f:
        f.write(data)

    inventory_keypath_update()
