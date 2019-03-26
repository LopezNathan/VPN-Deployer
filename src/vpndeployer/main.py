import argparse


## TODO
# droplet_ip variable broken?
# email, vpn, region arguments being ignored.

def create_parser():
    parser = argparse.ArgumentParser(description="VPN Deploy Script with DigitalOcean")
    
    parser.add_argument("ip", help="Your IP Address")
    parser.add_argument("--email", dest="email", help="Email Address for OpenVPN download link")
    parser.add_argument("--name", default='VPN', dest="name", help="Droplet Name")
    parser.add_argument("--region", default='nyc1', dest="region", help="Droplet Region")

    return parser

def main():
    import getpass
    import time
    import requests
    from vpndeployer import droplets

    # TODO - check api token auth before proceeding
    DO_API_TOKEN = getpass.getpass('DigitalOcean API Token: ')
    droplets.api_authentication(DO_API_TOKEN)

    args = create_parser().parse_args()

    print("\nDeploy Started!")
    print("This process typically takes less than 5 minutes.\n")

    droplets.create_droplet(args.ip, args.name, args.region, args.email)
    time.sleep(10)
    droplets.get_droplet_ip(args.name)

    # TODO - Use something else instead of a while loop to check the actual progress.
    # can we move it into the class and check the progress on a class method easier?
    while True:
        try:
            check_deploy = requests.get(f"http://{droplet_ip}/client.ovpn")
            print(f"\nDeploy Completed!\nDownload OpenVPN File: http://{droplet_ip}/client.ovpn")
            break
        except:
            print("Deploy In-Progress...")
            time.sleep(60)