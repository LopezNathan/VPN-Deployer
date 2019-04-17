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

cwd = Path(__file__).resolve().parent
playbook_path = str(cwd) + '/playbooks'

def gen_sshkey():
    runner = ansible_runner.run(private_data_dir=playbook_path, playbook='local-sshkeygen.yml', host_pattern='localhost', quiet=True)

    with open('/tmp/VPN-Test', 'r') as file:
        sshkey = file.read()
        file.close

    with open(playbook_path + "/env/ssh_key", "w+") as file:
        file.writelines(sshkey)
        os.chmod(str(file.name), 0o600)
        file.close

gen_sshkey()

# def testcmd():
#     runner = ansible_runner.run(private_data_dir=playbook_path, host_pattern='droplets', module='ping')

# testcmd()