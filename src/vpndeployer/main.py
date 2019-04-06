#!/usr/bin/env python3
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="VPN Deploy Script with DigitalOcean")

    parser.add_argument("--ip", dest="ip", help="Your IP Address")
    parser.add_argument("--email", dest="email", help="Email Address for OpenVPN download link")
    parser.add_argument("--name", default='VPN', dest="name", help="Droplet Name")
    parser.add_argument("--region", default='nyc1', dest="region", help="Droplet Region")

    return parser.parse_args()


def main():
    import time
    import requests
    import getpass
    import tenacity
    import os
    from vpndeployer import auth
    from vpndeployer import droplets

    args = parse_args()

    if os.environ.get('DO_API_TOKEN') is not None:
        DO_API_TOKEN = os.environ.get('DO_API_TOKEN')
    else:
        DO_API_TOKEN = getpass.getpass('DigitalOcean API Token: ')
    DO_API_TOKEN = auth.ApiAuth(DO_API_TOKEN).get_api_token()

    if args.ip is None:
        args.ip = requests.get("https://ipv4.icanhazip.com")
        args.ip = args.ip.text.strip('\n')

    if args.name == "VPN":
        args.name = args.name + "-" + str(time.time())

    print("\nDeploy Started!")
    print("This process typically takes less than 5 minutes.\n")

    droplets.create_droplet(ip=args.ip, name=args.name, region=args.region, email=args.email, api_token=DO_API_TOKEN)
    time.sleep(10)
    droplet_ip = droplets.get_droplet_ip(name=args.name, api_token=DO_API_TOKEN)

    @tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_fixed(20))
    def check_deploy(droplet_ip):
        requests.get(f"http://{droplet_ip}/client.ovpn")
        print(f"Deploy Completed!\n Download OpenVPN File: http://{droplet_ip}/client.ovpn")

    check_deploy(droplet_ip=droplet_ip)
