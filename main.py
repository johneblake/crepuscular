"""Main module to get stock quotes"""
import csv
import os
import os.path
import sys
import pandas_datareader as pdr
from datetime import datetime
from datastore.datacontext import DataContext
from datastore.tabledef import Ticker, Quote

from reader import quandl_reader, etf_reader

if len(sys.argv) > 1:
    COMMAND = sys.argv[1]
    if COMMAND == "help":
        print("create, historical, daily, help")
    elif COMMAND == "create":
        create()
    elif COMMAND == "historical":
        historical()
    elif COMMAND == "daily":
        daily()
    else:
        print("Unknown command {command}".format(command=COMMAND))

def create():
    """
        Deletes existing database and creates a new one
    """
    if os.path.exists("historical.zip"):
        os.remove("historical.zip")

    # delete existing database
    if os.path.exists("ticker.db"):
        os.remove("ticker.db")

    # create new database
    DataContext()


def historical():
    """
    Gets etf symbols and historical data
    Uses pandas reader to get etf historical data
    """
    context = DataContext()

    # grab the historical zip file from quandl
    quandl_reader.set_api_key("qSUzVYsyx4v7xVe9VdD3")
    csv_file = quandl_reader.bulk_download("historical.zip")

    addsymbols(context, csv_file)
    addhistorical(context, csv_file)

    if os.path.exists("historical.zip"):
        os.remove("historical.zip")

    if os.path.exists(csv_file):
        os.remove(csv_file)


def daily():
    """
    Gets daily quote data using quandl and pandas
    """
    # get etf symbols and grab the daily data based on last run
    # get daily quandl using the diff file
    pass

def addsymbols(context, csv_file):
    """
    Add symbols from the etf reader and the downloaded historical file
    """
    etf_items = etf_reader.get_etf()
    context.add_tickers([Ticker(i[0], "etf", i[1]) for i in etf_items])

    symbols = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        current_symbol = ""
        for row in reader:
            if current_symbol != row[0]:
                current_symbol = row[0]
                symbols.append(current_symbol)
    context.add_tickers([Ticker(item[0], "stock", "") for item in symbols])

def addhistorical(context, csv_file):
    """
    Use pandas to read etf historical data
    Read the historical data from the csv_file
    """
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        current_symbol = ""
        quotes = []
        for quote in reader:
            if current_symbol != quote[0]:
                if current_symbol != "":
                    context.add_quotes({current_symbol, quotes})
                    quotes = []
                current_symbol = quote[0]
            quotes.append(Quote(-1, quote[1], quote[10], quote[11], quote[9], quote[12], quote[13]))
        # add last symbol data
        context.add_quotes({current_symbol, quotes})

    tickers = context.get_etfs()        

    for ticker in tickers:
        quotes = pdr.get_data_yahoo(symbols=ticker, start=datetime(1995, 1, 1), end=datetime.now)
        ###################### needs some work ############################