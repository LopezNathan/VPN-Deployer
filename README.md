# VPN Deployer

## Simple OpenVPN Deploy Script to DigitalOcean Cloud

This script will install OpenVPN utilizing the [OpenVPN Installer by Angristan](https://github.com/Angristan/OpenVPN-install) on a DigitalOcean Droplet.
Once OpenVPN has been installed, NGINX & Sendmail are installed and an email is sent with a link to download the .ovpn client file (most likely in spam folder). This link will only be available for 5 minutes before NGINX is removed.

**This is only intended for short-term/one-time use, as currently no extra security is added to the base server.**

#### Todo

- [ ] Improve Link Download
- [ ] Add Sever Security for Long-term Use

## Usage

```bash
usage: vpn-deploy.py [-h] [--name NAME] [--region REGION] ip email

VPN Deploy Script with DigitalOcean

positional arguments:
  ip               Your IP Address
  email            Your Email Address

optional arguments:
  -h, --help       show this help message and exit
  --name NAME      Droplet Name
  --region REGION  Droplet Region
```

### Example

> python vpn-deploy.py 123.123.123.123 email@email.com 

- Your IP Address is needed to restrict port `80`.
- Your email is needed to send a notification when the deploy is completed.

Once the installer script has completed, you will receive an email with a link to download the .ovpn client file. This link automatically expires in 5 minutes. Make sure to check your spam folder, as the email is not authenticated in anyway.

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