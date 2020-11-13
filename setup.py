#!/usr/bin/env python3
from setuptools import find_packages, setup
from os import path

with open(path.join('src/vpndeployer/', '__version__')) as version_file:
    version = version_file.read().strip()

setup(
    name='vpndeployer',
    version=version,
    author='Nathan Lopez',
    author_email='contact@lopeznathan.com',
    description='OpenVPN Deploy CLI Tool',
    url='https://github.com/LopezNathan/vpn-deployer',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['python-digitalocean', 'requests', 'tenacity', 'ansible==2.8.0a1', 'ansible-runner', 'paramiko'],
    entry_points={
        'console_scripts': [
            'vpndeployer=vpndeployer.main:main'
        ]
    }
)
