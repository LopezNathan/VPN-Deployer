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

    with open(data_path + "/env/ssh_key", "w+") as file:
        file.writelines(sshkey)
        os.chmod(str(file.name), 0o600)

    # TODO - Return something proper, the key?
    return runner.status
