#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='vpndeployer',
    version='0.10.1',
    author='Nathan Lopez',
    author_email='contact@lopeznathan.com',
    description='Fully Install OpenVPN on DigitalOcean Automatically',
    url='https://github.com/LopezNathan/vpn-deployer',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'vpndeployer=vpndeployer.main:main'
        ]
    }
)
