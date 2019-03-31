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
    # import getpass
    import time
    import requests
    import getpass
    from vpndeployer import ApiAuth
    from vpndeployer import droplets

    args = parse_args()

    DO_API_TOKEN = getpass.getpass('DigitalOcean API Token: ')
    DO_API_TOKEN = ApiAuth(DO_API_TOKEN).get_api_token()

    if args.ip is None:
        args.ip = requests.get("https://ifconfig.co/ip")
        args.ip = args.ip.text.strip('\n')

    if args.name == "VPN":
        args.name = args.name + "-" + str(time.time())

    print("\nDeploy Started!")
    print("This process typically takes less than 5 minutes.\n")

    droplets.create_droplet(ip=args.ip, name=args.name, region=args.region, email=args.email, api_token=DO_API_TOKEN)
    time.sleep(10)
    droplet_ip = droplets.get_droplet_ip(name=args.name, api_token=DO_API_TOKEN)

    # TODO - Use tenacity
    while True:
        try:
            check_deploy = requests.get(f"http://{droplet_ip}/client.ovpn")
            print(f"\nDeploy Completed!\nDownload OpenVPN File: http://{droplet_ip}/client.ovpn")
            break
        except:
            print("Deploy In-Progress...")
            time.sleep(60)
