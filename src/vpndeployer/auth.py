#!/usr/bin/env python3
import getpass
import os


class ApiAuth:

    def get_api_token():
        if os.environ.get('DO_API_TOKEN') is not None:
            DO_API_TOKEN = os.environ.get('DO_API_TOKEN')
        else:
            DO_API_TOKEN = getpass.getpass('DigitalOcean API Token: ')
            os.environ['DO_API_TOKEN'] = DO_API_TOKEN

        return DO_API_TOKEN
