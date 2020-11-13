#!/usr/bin/env python3
import ansible_runner
from vpndeployer import ansible_data


def deploy(instance_name, client_ip, email):
    data_path = ansible_data.playbook_path()
    runner = ansible_runner.run(
        private_data_dir=data_path,
        playbook='deploy_openvpn.yml',
        extravars={
            "NAME": instance_name,
            "IP": client_ip,
            "EMAIL": email
        },
        quiet=True
    )

    # TODO - Return something proper
    return runner.status


def cleanup(instance_name):
    data_path = ansible_data.playbook_path()
    runner = ansible_runner.run(
        private_data_dir=data_path,
        playbook='cleanup.yml',
        extravars={"NAME": instance_name},
        quiet=True
    )

    # TODO - Return something proper
    return runner.status
