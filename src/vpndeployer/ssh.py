#!/usr/bin/env python3
import os
import tenacity
import ansible_runner
from paramiko import SSHClient, AutoAddPolicy, ssh_exception
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


class ConnectionFailure(Exception):
    """SSH Connection Failed"""


@tenacity.retry(
    stop=tenacity.stop_after_attempt(4),
    wait=tenacity.wait_fixed(20),
    reraise=True
)
def test_connection(instance_ip):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    private_key = ansible_data.playbook_path() + '/env/ssh_key'
    try:
        ssh.connect(
            instance_ip,
            port=22,
            username='root',
            key_filename=private_key
        )
        return True
    except (ConnectionRefusedError, TimeoutError, ssh_exception.NoValidConnectionsError):
        raise ConnectionFailure
