# VPN Deployer
### Simple OpenVPN Deploy Script to DigitalOcean Cloud

This script will install OpenVPN utilizing the [OpenVPN Installer by Angristan](https://github.com/Angristan/OpenVPN-install).
Once OpenVPN has been installed, NGINX & Sendmail are installed and an email is sent with a link to download the .ovpn client file (most likely in spam folder). This link will only be available for 5 minutes before NGINX is removed.

**This is only intended for short-term/one-time use, as currently no extra security is added to the base server.**

#### Todo
- [ ] Improve Link Download
- [ ] Add Sever Security for Long-term Use

----

###  Instructions

Currently two methods are available to build the server and deploy OpenVPN. The first method utilizes DigitalOcean API, running a cURL request to configure, build, and install everything. The second method requires logging into the DigitalOcean Control Panel to configure and build the server.

Once the installer script has completed, you will receive an email with a link to download the .ovpn client file. This link automatically expires in 5 minutes. Make sure to check your spam folder, as the email is not authenticated in anyway.

#### DigitalOcean - API

* Copy the API request Code:

  ```bash
  curl -X POST "https://api.digitalocean.com/v2/droplets" \
        -d'{"name":"VPN-Deployer.local","region":"nyc3","size":"512mb","image":"centos-7-x64","user_data":
  "#!/bin/bash
  export EMAIL='EMAIL'
  export IP='IP'
  bash
  yum -y update && yum -y upgrade
  yum -y install wget
  wget -O /root/openvpn-deploy.sh https://raw.githubusercontent.com/LopezNathan/VPN-Deployer/master/OpenVPN-Deploy.sh
  chmod +x /root/openvpn-deploy.sh && bash /root/openvpn-deploy.sh"}' \
        -H "Authorization: Bearer API-TOKEN" \
        -H "Content-Type: application/json"
  ```

* Edit IP, EMAIL and API-Token
  * IP - Your local IP address
  * Email - Where the download link will be sent
  * API-Token - Your DigitalOcean API token

#### DigitalOcean - Control Panel

* Create [New DigitalOcean Droplet](https://cloud.digitalocean.com/droplets/new) with Options:
  * Choose an image: CentOS
  * Choose a size: 512 MB
  * Choose a datacenter region: Any
  * Select additional options: Check "User Data" & Paste the [Script](https://raw.githubusercontent.com/NathanZepol/VPN-Deployer/master/user-data.txt)
  * Edit YOUR-IP & YOUR-EMAIL in the "User Data" Script
