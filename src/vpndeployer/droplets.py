import requests
import digitalocean

def api_authentication(DO_API_TOKEN):
    api_authentication.DO_API_TOKEN = DO_API_TOKEN

def create_droplet(ip, name='VPN', region='nyc1', email=None):
    droplet = digitalocean.Droplet(token=f'{api_authentication.DO_API_TOKEN}',
                                name=f'{name}',
                                region=f'{region}',
                                image='centos-7-x64',
                                size_slug='512mb',
                                user_data=f"""#!/bin/bash
    export IP="{ip}"
    export EMAIL="{email}"
    if [[ $EMAIL == "None" ]]; then
        unset EMAIL
    fi
    curl -o /root/openvpn-install-prep.sh https://raw.githubusercontent.com/LopezNathan/vpn-deployer/development/openvpn-install-prep.sh
    chmod +x /root/openvpn-install-prep.sh && bash /root/openvpn-install-prep.sh""",
                                backups=True)

    return droplet.create()

def get_droplet_ip(name='VPN'):
    droplet_list = requests.get(f"https://api.digitalocean.com/v2/droplets", headers={"Authorization": "Bearer %s" % api_authentication.DO_API_TOKEN, "Content-Type": "application/json"})
    # TODO - Clean this mess up...
    # TODO - we should be returning something here
    # TODO - what happens if we have multiple droplets with same name?...
    for item in droplet_list.json()['droplets']:
        if item['name'] == name:
            droplet_vpn = item

    for item in droplet_vpn['networks']['v4']:
        droplet_ip = item['ip_address']