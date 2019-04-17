#!/usr/bin/env python3
import ansible_runner
from pathlib import Path, PurePath
import os

###
# TODO -
# Install Ansible-Runner
# Execute SSHKeyGen Playbook on Localhost
# Configure Inventory based on Droplet Created
# Execute Prep Playbook on Remote Host
# If Cleanup Flag Provided, Run Cleanup Playbook on Remote Host
###

def playbook_path():
    cwd = Path(__file__).resolve().parent
    path = str(cwd) + '/playbooks'

    return path

def gen_sshkey():
    data_path = playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='local-sshkeygen.yml', host_pattern='localhost', quiet=True)

    with open('/tmp/.VPN-Deployer', 'r') as file:
        sshkey = file.read()
        file.close

    with open(data_path + "/env/ssh_key", "w+") as file:
        file.writelines(sshkey)
        os.chmod(str(file.name), 0o600)
        file.close

    return runner.status