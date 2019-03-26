# VPN Deployer

## Simple OpenVPN Deploy Script to DigitalOcean Cloud

This script will install OpenVPN utilizing the [OpenVPN Installer by Angristan](https://github.com/Angristan/OpenVPN-install) on a DigitalOcean Droplet.
Once OpenVPN has been installed, NGINX is installed and a link is provided to download the OpenVPN Client file. This link will only be available for 5 minutes before NGINX is removed.

**This is only intended for short-term/one-time use, as currently no major security protection is added to the base server.**

## Installation

This package requires Python 3.7

```bash
$ pip3 install git+https://github.com/LopezNathan/vpn-deployer
```

You will now have access to the `vpndeployer` command.

## Usage

```bash
$ vpndeployer --help

usage: vpndeployer [-h] [--email EMAIL] [--name NAME] [--region REGION] ip

VPN Deploy Script with DigitalOcean

positional arguments:
  ip               Your IP Address

optional arguments:
  -h, --help       show this help message and exit
  --email EMAIL    Email Address for OpenVPN download link
  --name NAME      Droplet Name
  --region REGION  Droplet Region
```

### Example

> vpndeployer 123.123.123.123

- You will be prompted for your [DigitalOcean API Token](https://www.digitalocean.com/docs/api/create-personal-access-token/). This is only passed through `getpass` to the DigitalOcean API during the creation of the droplet and obtaining the droplet IP.
- Your IP Address is needed to restrict port `80` for the OpenVPN download link.

Once the installer script has completed, it will output the OpenVPN download link. This link automatically expires in 5 minutes.

## Legacy Deploy Options

#### DigitalOcean - API

- Copy the API request Code:

  ```bash
  curl -X POST "https://api.digitalocean.com/v2/droplets" \
        -d'{"name":"VPN-Deployer.local","region":"nyc3","size":"512mb","image":"centos-7-x64","user_data":
  "#!/bin/bash
  export EMAIL='EMAIL'
  export IP='IP'
  bash
  curl -o /root/vpn-installer.sh https://raw.githubusercontent.com/LopezNathan/VPN-Deployer/master/OpenVPN-Deploy.sh
  chmod +x /root/vpn-installer.sh && bash /root/vpn-installer.sh"}' \
        -H "Authorization: Bearer API-TOKEN" \
        -H "Content-Type: application/json"
  ```

- Edit IP, EMAIL and API-Token

  - IP - Your local IP address
  - Email - Where the download link will be sent
  - API-Token - Your DigitalOcean API token

#### DigitalOcean - Control Panel

- Create [New DigitalOcean Droplet](https://cloud.digitalocean.com/droplets/new) with Options:
  - Choose an image: CentOS
  - Choose a size: 512 MB
  - Choose a datacenter region: Any
  - Select additional options: Check "User Data" & Paste the [Script](https://raw.githubusercontent.com/LopezNathan/VPN-Deployer/master/OpenVPN-Deploy.sh)
  - Edit $IP & $EMAIL in the "User Data" Script
    - IP - Your local IP address
    - Email - Where the download link will be sent