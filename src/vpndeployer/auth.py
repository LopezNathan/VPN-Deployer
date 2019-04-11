#!/usr/bin/env python3


class ApiAuth:

    def __init__(self, API_TOKEN):
        self.API_TOKEN = API_TOKEN

    def get_api_token(self):
        return self.API_TOKEN
