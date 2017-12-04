# VPN Deployer
### Simple OpenVPN Deploy Script to DigitalOcean Cloud

This script will install OpenVPN utilizing the [OpenVPN Installer by Angristan](https://github.com/Angristan/OpenVPN-install).
Once OpenVPN has been installed, NGINX & Sendmail are installed and an email is sent with a link to download the .ovpn client file (most likely in spam folder). This link will only be available for 5 minutes before NGINX is removed.

**This is only intended for short-term/one-time use, as currently no extra security is added to the base server.**

#### Todo
- [ ] Improve Link Download
- [ ] Integrate with DigitalOcean API
- [ ] Add Sever Security for Long-term Use

----

####  Instructions
* Create [New DigitalOcean Droplet](https://cloud.digitalocean.com/droplets/new) with Options:
  * Choose an image: CentOS
  * Choose a size: 512 MB
  * Choose a datacenter region: Any
  * Select additional options: Check "User Data" & Add [Script](https://raw.githubusercontent.com/NathanZepol/VPN-Deployer/master/cloudvpndeploy.sh)
  * Edit YOUR-NAME & YOUR-EMAIL in the "User Data" Script

* You will receive an email with a link to download the .ovpn client file. This link automatically expires in 5 minutes.