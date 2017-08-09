"""Main module to get stock quotes"""
import sys
import os
import os.path
from datastore import datacontext
from reader import quandl_reader, etf_reader

if len(sys.argv) > 1:
    command = sys.argv[1]
    if command == "help":
        print("create, historical, daily, help")
    elif command == "create":
        create()
    elif command == "historical":
        historical()
    elif command == "daily":
        daily()
    else:
        print("Unknown command {command}".format(command = command))

def create():
    # grab etf symbols
    etf_items = etf_reader.get_etf()

    # grab the historical zip file from quandl
    quandl_reader.set_api_key("qSUzVYsyx4v7xVe9VdD3")

    if os.path.exists("historical.zip"):
        os.remove("historical.zip")    

    quandl_reader.bulk_download("historical.zip")

    # delete existing database
    if os.path.exists("stock.db"):
        os.remove("stock.db")

    # create new database

    # load symbols
    pass

def historical():
    # load historical data
    # grab the etf symbols and get historical data
    pass

def daily():
    # get etf symbols and grab the daily data based on last run
    # get daily quandl using the diff file
    pass