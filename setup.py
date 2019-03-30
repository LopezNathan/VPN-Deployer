#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name='vpndeployer',
    version='1.0.1',
    author='Nathan Lopez',
    author_email='contact@lopeznathan.com',
    description='Fully Install OpenVPN on DigitalOcean Automatically',
    url='https://github.com/LopezNathan/vpn-deployer',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=['python-digitalocean', 'requests'],
    entry_points={
        'console_scripts': [
            'vpndeployer=vpndeployer.main:main'
        ]
    }
)
