'''Read data from TD Ameritrade API'''
import requests
import datetime
import time
from tda import TDClient

# create a class to read data from TD Ameritrade API
class TDReader:
    # add variable to track the number of requests
    requests = 0
    # add variable to track start time of first request in second
    start_time = 0

    # define the init function
    def __init__(self):
        # create a new tda client
        self.client = TDClient()

    # define a function to prevent 120 requests per 60 seconds
    def check_requests(self):
        # check if the number of requests is 120
        if self.requests == 120:
            # check if the time since the first request is less than 60 seconds
            if time.time() - self.start_time < 60:
                # wait until the time is up
                time.sleep(60 - (time.time() - self.start_time))
            # reset the number of requests
            self.requests = 0
        # check if the number of requests is 0
        if self.requests == 0:
            # set the start time
            self.start_time = time.time()
        # increment the number of requests
        self.requests += 1

    # define a function to get all stock symbols
    def get_all_symbols(self):
        symbols = []
        # verify the access token
        self.client.check_token()
        # define the url
        url = 'https://api.tdameritrade.com/v1/instruments'

        # for each capital letter
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            # define the payload
            payload = {'apikey': self.client.api_key,
                        'symbol': letter+".*",
                        'projection': 'symbol-regex'}
            self.check_requests()
            # request the data from the url
            response = requests.get(url, params=payload)

            # check if the response is ok
            if response.ok:
                # add the symbols to the list
                symbols += [symbol['symbol'] for symbol in response.json()]
        # return the list of symbols
        return symbols

    # define a function to get all stocks with weekly options with total open interest over 1000
    def get_all_stocks_with_weekly_options(self):
        optionsSymbols = []

        # verify the access token
        self.client.check_token()
        # define the url
        url = 'https://api.tdameritrade.com/v1/marketdata/chains'

        # get all the symbols
        symbols = self.get_all_symbols()

        # get today's date
        today = datetime.date.today()

        # for each symbol see if it has weekly options with open interest above 1000
        for symbol in symbols:
            # define the payload to determine if the symbol has weekly options
            payload = {'apikey': self.client.api_key,
                        'symbol': symbol,
                        'contractType': 'ALL',
                        'strikeCount': '1',
                        'includeQuotes': 'FALSE',
                        'strategy': 'SINGLE',
                        'fromDate': today.strftime('%Y-%m-%d'),
                        'optionType': 'ALL',
            }
            self.check_requests()
            # request the data from the url
            response = requests.get(url, params=payload)
            # check if the response is ok
            if response.ok:
                # check if the symbol has weekly options
                if 'weekly' in response.json()['callExpDateMap']:
                    # add the symbol to the list
                    optionsSymbols.append(symbol)
        # return the list of symbols
        return optionsSymbols             

    def get_historical_stock_data(self, symbol, periodType='year', period=20, frequencyType='daily', frequency=1):
        # verify the access token
        self.client.check_token()
        # define the url
        url = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(symbol)

        # define the payload
        payload = {'apikey': self.client.api_key,
                    'periodType': periodType,
                    'period': period,
                    'frequencyType': frequencyType,
                    'frequency': frequency,
                    'needExtendedHoursData': 'false'
        }
        self.check_requests()
        # request the data from the url
        response = requests.get(url, params=payload)

        # check if the response is ok
        if response.ok:
            # return the data
            return response.json()
