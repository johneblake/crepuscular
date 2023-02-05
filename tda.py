'''Class to access the TDAmeritrade API.'''
import requests
import os
import time

# define class to access the TDAmeritrade API through the restful API
class TDClient:
    # define access and refresh token variables
    access_token = None
    refresh_token = None
    api_key = 'JAYBEEJA3'
    client_id = api_key + '@AMER.OAUTH_AP'

    # define the init function
    def __init__(self):
        # load the refresh token
        self.load_token()
        # get the access token
        self.get_access_token()
        # get a new access token every 25 minutes
        self.timer = time.time() + 1500

    # define a function check if the access token is expired
    def check_token(self):
        # check if the timer is expired
        if time.time() > self.timer:
            # get a new access token
            self.get_access_token()
            # reset the timer
            self.timer = time.time() + 1500

    # use the refresh token to get a new refresh token
    def request_refresh_token(self):
        # define the url
        url = 'https://api.tdameritrade.com/v1/oauth2/token'
        # define the headers
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # define the payload
        payload = {'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'access_type': 'offline',
                'client_id': self.client_id}
        # post the token to the url
        response = requests.post(url, headers=headers, data=payload)
        # assign the refresh token from the response
        self.refresh_token = response.json()['refresh_token']       

    # create a function to load the refresh token from a file name token.txt
    def load_token(self):
        # check if the last modified time of the file is > 80 days
        if (time.time() - os.path.getmtime('token.txt')) > 6912000:
            # request a new refresh token
            self.request_refresh_token()
            self.save_token()
        # otherwise
        else:
            # open the file
            with open('token.txt', 'r') as f:
                # read the lines
                lines = f.readlines()
                # assign the refresh token
                self.refresh_token = lines[0].strip()
    
    # create a function to save the refresh token to a file name token.txt
    def save_token(self):
        # open the file
        with open('token.txt', 'w') as f:
            # write the refresh token
            f.write(self.refresh_token + '\n')

    # get access token to https://api.tdameritrade.com/v1/oauth2/token
    # and return the response
    def get_access_token(self):
        # define the url
        url = 'https://api.tdameritrade.com/v1/oauth2/token'
        # define the headers
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # define the payload
        payload = {'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': self.client_id}
        # post the token to the url
        response = requests.post(url, headers=headers, data=payload)

        # assign the access token from the response
        self.access_token = response.json()['access_token']




