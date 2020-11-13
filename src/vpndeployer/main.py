#!/usr/bin/env python3
import argparse
import time
import requests
from vpndeployer import auth, instance_do, openvpn, ssh


def parse_args():
    parser = argparse.ArgumentParser(
        description="OpenVPN Deploy CLI Tool")

    available_distros = [
        'centos-7-x64',
    ]

    parser.add_argument("--ip", dest="ip",
                        help="Your IP Address"
                        )
    parser.add_argument("--email", dest="email",
                        help="Email Address for OpenVPN download link"
                        )
    parser.add_argument("--name", dest="name",
                        default='VPN',
                        help="Instance Name"
                        )
    parser.add_argument("--region", dest="region",
                        default='nyc1',
                        help="Instance Region"
                        )
    parser.add_argument("--image", dest="image",
                        choices=available_distros,
                        default='centos-7-x64',
                        help="Instance Distribution Image"
                        )

    return parser.parse_args()


def main():

    args = parse_args()

    DO_API_TOKEN = auth.ApiAuth.get_api_token()

    if args.ip is None:
        args.ip = requests.get("https://ipv4.icanhazip.com").text.strip('\n')

    if args.name == "VPN":
        args.name = args.name + "-" + str(time.time())

    ssh_key = ssh.generate_key(DO_API_TOKEN)

    print("\nDeploy Started!")
    print("This process typically takes less than 5 minutes.\n")

    instance_do.create_instance(
        ip=args.ip,
        name=args.name,
        region=args.region,
        image=args.image,
        email=args.email,
        sshkey=ssh_key,
        api_token=DO_API_TOKEN
    )

    droplet_ip = instance_do.get_ip(
        name=args.name,
        api_token=DO_API_TOKEN
    )

    ssh.test_connection(droplet_ip)

    openvpn.deploy(
        ip=args.ip,
        email=args.email
    )

    # TODO - Add proper checking into the deploy, tenacity should no longer be needed though.
    print(f"Deploy Completed!\n Download OpenVPN File: http://{droplet_ip}/client.ovpn")

    input("\nPress Enter to proceed with download link cleanup...")

    print("\nCleanup Started!")
    openvpn.cleanup()
    print("\nCleanup Completed! Don't forget to delete the instance after you're done.")
