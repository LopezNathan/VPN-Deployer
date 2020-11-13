#!/usr/bin/env python3
import ansible_runner
from vpndeployer import ansible_data


def deploy_openvpn(ip, email):
    data_path = ansible_data.playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='openvpn-install.yml',
                                host_pattern='VPN-*', extravars={"IP": ip, "EMAIL": email}, quiet=True)

    # TODO - Return something proper
    return runner.status


def cleanup_openvpn():
    data_path = ansible_data.playbook_path()
    runner = ansible_runner.run(private_data_dir=data_path, playbook='openvpn-install-cleanup.yml',
                                host_pattern='VPN-*', quiet=True)

    # TODO - Return something proper
    return runner.status
