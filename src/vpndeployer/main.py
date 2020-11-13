#!/usr/bin/env python3
import argparse
import time
import requests
from vpndeployer import auth, instance_do, openvpn, ssh


def parse_args():
    parser = argparse.ArgumentParser(
        description="VPN Deploy Script with DigitalOcean")

    available_distros = [
        'centos-7-x64',
    ]

    parser.add_argument("--ip", dest="ip", help="Your IP Address")
    parser.add_argument("--email", dest="email",
                        help="Email Address for OpenVPN download link")
    parser.add_argument("--name", default='VPN',
                        dest="name", help="Droplet Name")
    parser.add_argument("--region", default='nyc1',
                        dest="region", help="Droplet Region")
    parser.add_argument("--image", default='centos-7-x64', dest="image", choices=available_distros,
                        help="Droplet Distribution Image")

    return parser.parse_args()


def main():

    args = parse_args()

    DO_API_TOKEN = auth.ApiAuth.get_api_token()

    if args.ip is None:
        args.ip = requests.get("https://ipv4.icanhazip.com").text.strip('\n')

    if args.name == "VPN":
        args.name = args.name + "-" + str(time.time())

    sshkey = ssh.generate_key(DO_API_TOKEN)

    print("\nDeploy Started!")
    print("This process typically takes less than 5 minutes.\n")

    instance_do.create_instance(ip=args.ip, name=args.name, region=args.region,
                                image=args.image, email=args.email, sshkey=sshkey, api_token=DO_API_TOKEN)

    droplet_ip = instance_do.get_ip(
        name=args.name, api_token=DO_API_TOKEN)

    instance_do.test_instance_connection()

    openvpn.deploy(ip=args.ip, email=args.email)

    # TODO - Add proper checking into the deploy, tenacity should no longer be needed though.
    print(
        f"Deploy Completed!\n Download OpenVPN File: http://{droplet_ip}/client.ovpn")

    print("\nStarting the cleanup in 5 minutes...")
    # Better way to pause after the deploy?
    time.sleep(300)
    openvpn.cleanup()
    print("Cleanup completed! Don't forget to delete the droplet after you're done.")
