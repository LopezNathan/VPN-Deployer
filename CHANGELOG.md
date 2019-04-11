# Changelog

## [2.4.4] - 2019-04-09
### Fixed
- get_droplet_ip Reporting Incorrect IP Fixed [1792720]

## [2.4.3] - 2019-04-09
### Fixed
- OpenVPN Installer Unsupported OS Prompt Fixed [163acc5]

## [2.4.2] - 2019-04-09
### Fixed
- Droplet User-Data Multi Distro Fixed [d88fff3]

## [2.4.1] - 2019-04-08
### Fixed
- Ansible Playbook Syntax Fixed [f8a0c5f]

## [2.4.0] - 2019-04-08
### Added
- Image/Distro Argument [5e5bb8f]

### Changed
- Multi Distro Support in Ansible Playbooks [b5ae89e]
- Default Image/Distro Changed [21e7845]

## [2.3.1] - 2019-04-06
### Fixed
- API Token Environment Variable Fixed [e1770ac]

## [2.3.0] - 2019-04-06
### Added
- API Token Environment Variable Check [8209cde]

## [2.2.1] - 2019-04-06
### Added
- Cleanup Ansible Playbook [cdd0812]
- Check Added to Ansible Playbook for OpenVPN Service [cb55444]

## [2.2.0] - 2019-04-06
### Changed
- ApiAuth Class (API Auth) Moved to auth.py [44c8002]

## [2.1.2] - 2019-04-06
### Fixed
- Force IPv4 in IPTables Rule [0d69915]

## Not Versioned - 2019-04-06
### Added
- Ansible Output to Log [2689ca8]

### Fixed
- Ansible Output to Log Fixed Again [90c9174]
- Ansible Output to Log Fixed [c5ccc05]

## [2.1.1] - 2019-04-06
### Fixed
- Tenacity Retry Interval Fixed [1cd250d]

## [2.1.0] - 2019-04-05
### Added
- Implemented Tenacity [1cd250d]

## [2.0.0] - 2019-04-05
### Changed
- IP Argument Made Optional [abcd2ff]
- Convert Subprocess to Requests Module [a49bd70]
- Positional Arguments Required [1934dda]
- Timestamp Added to Droplet Name [e7b28ab]
- Assign Variable to Arguments in create_droplet [c682677]
- ArgParse Function Renamed [968ab9a]
- ApiAuth Class (API Auth) Moved to __init__.py [f703d2b]
- Seperated Tasks in Ansible Playbook [1bfc6c4]
- README Updated with Optional IP Argument [0f7c653]

### Added
- Flake8 Styling Implemented [2b13133]
- Added Ansible Playbook [c33f108]
- Ansible Implemented [1706e07]
- Basic Rules Added to IPTables in Ansible Playbook [1d91512]
- Sendmail Implemented in Ansible Playbook [0a2952b]
- Version File Implemented into setup.py [fcfc4cf]

## [1.0.1] - 2019-03-26
### Changed
- Removed Development Branch References [a38b66677]
