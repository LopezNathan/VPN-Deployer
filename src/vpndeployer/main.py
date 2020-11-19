#!/usr/bin/env python3
import argparse
import time
import requests
import logging
from vpndeployer import auth, instance_do, openvpn, ssh

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_handler = logging.StreamHandler()
logger.addHandler(logger_handler)


def parse_args():
    parser = argparse.ArgumentParser(
        description="OpenVPN Deploy CLI Tool")

    available_distros = [
        'centos-7-x64',
        'centos-8-x64',
        'ubuntu-16-04-x64',
        'ubuntu-18-04-x64',
        'ubuntu-20-04-x64',
        'debian-9-x64',
        'debian-10-x64',
    ]

    parser.add_argument("--headless", dest="headless",
                        action='store_true',
                        help="Automated Deploy - No User Input"
                        )
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
                        default='centos-8-x64',
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

    logger.info("\nDeploy Started!")
    logger.info("This process typically takes less than 3 minutes.\n")

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
        instance_name=args.name,
        client_ip=args.ip,
        email=args.email
    )

    # TODO - Add proper checking into the deploy, tenacity should no longer be needed though.
    logger.info(f"Deploy Completed!\n Download OpenVPN File: http://{droplet_ip}/client.ovpn")

    if args.headless:
        logger.info("\nStarting download link cleanup in 5 minutes...")
        # Can this be moved to a background thread?
        time.sleep(300)
    else:
        input("\nPress Enter to proceed with download link cleanup...")

    logger.info("\nCleanup Started!")
    openvpn.cleanup(instance_name=args.name)
    logger.info("\nCleanup Completed! Don't forget to delete the instance after you're done.")
