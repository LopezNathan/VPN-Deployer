#!/usr/bin/env python3
import os
import ansible_runner
from vpndeployer import ansible_data, instance_do


def generate_key(DO_API_TOKEN):
    data_path = ansible_data.playbook_path()

    if os.path.isfile(data_path + '/env/ssh_key') is True:
        sshkey_id = open(data_path + '/env/ssh_key.id').read()
        return [int(key) for key in [sshkey_id]]

    ansible_runner.run(
        private_data_dir=data_path,
        playbook='local_key_gen.yml',
        host_pattern='localhost',
        extravars={"PATH": data_path},
        quiet=True
    )
    sshkey_id = instance_do.add_key(DO_API_TOKEN)

    return [sshkey_id]
