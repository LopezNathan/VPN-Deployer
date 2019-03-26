import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="VPN Deploy Script with DigitalOcean")
    
    parser.add_argument("ip", help="Your IP Address")
    parser.add_argument("--email", dest="email", help="Email Address for OpenVPN download link")
    parser.add_argument("--name", default='VPN', dest="name", help="Droplet Name")
    parser.add_argument("--region", default='nyc1', dest="region", help="Droplet Region")

    return parser

def main():
    args = create_parser().parse_args()