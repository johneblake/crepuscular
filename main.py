"""Main module to get stock quotes"""
import csv
import os
import os.path
import sys
from datetime import datetime
import pandas_datareader as pdr
from datastore.datacontext import DataContext
from datastore.tabledef import Ticker, Quote

from reader import quandl_reader, etf_reader

def create():
    """
        Deletes existing database and creates a new one
    """
    if os.path.exists("historical.zip"):
        os.remove("historical.zip")

    # delete existing database
    if os.path.exists("ticker.db"):
        os.remove("ticker.db")

    # delete existing etf.csv
    if os.path.exists("etf.csv"):
        os.remove("etf.csv")

    # create new database
    datacontext = DataContext()
    datacontext.create()


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
    tickers = [Ticker(i[0], "etf", i[1]) for i in etf_items]
    context.add_tickers(tickers)
    etf_list = [i[0] for i in etf_items]

    symbols = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        current_symbol = ""
        for row in reader:
            if current_symbol != row[0]:
                current_symbol = row[0]
                if current_symbol not in etf_list:
                    symbols.append(current_symbol)
    context.add_tickers([Ticker(item[0], "stock", "") for item in symbols])
    context.delete_duplicate_tickers()

def addhistoricalfromcsv(csv_file):
    """Given a csv file add the data to the database"""
    context = DataContext()
    addhistorical(context, csv_file)

def addsymbolsfromcsv(csv_file):
    """helper for add symbols"""
    context = DataContext()
    addsymbols(context, csv_file)

def addhistorical(context, csv_file):
    """
    Use pandas to read etf historical data
    Read the historical data from the csv_file
    """
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        current_symbol = ""
        quote_list = []
        count = 0
        data = dict()
        for quote in reader:
            if current_symbol != quote[0]:
                if current_symbol != "":
                    print(current_symbol)
                    data[current_symbol] = quote_list
                    quote_list = []
                    count += 1
                    if count % 200 == 0:
                        context.add_quotes(data)
                        data = {}
                current_symbol = quote[0]
            quote_list.append(Quote(-1, quote[1], quote[10], quote[11], quote[9], quote[12], quote[13]))
        # add last symbol data
        if data:
            context.add_quotes(data)

    tickers = context.get_etfs()

    for ticker in tickers:
        quote_list = []
        quote_reader = pdr.get_data_yahoo(ticker, start=datetime(1995, 1, 1), end=datetime.now())
        for i in range(len(quote_reader)):
            adjusted = quote_reader.iloc[i]["Adj Close"] / quote_reader.iloc[i]["Close"]
            quote_list.append(Quote(-1, quote_reader.iloc[i].name,
                                quote_reader.iloc[i]["Open"] * adjusted,
                                quote_reader.iloc[i]["High"] * adjusted,
                                quote_reader.iloc[i]["Low"] * adjusted,
                                quote_reader.iloc[i]["Adj Close"], quote_reader.iloc[i]["Volume"]))
        context.add_quotes({ticker, quote_list})

def stocks():
    """list all stocks in the database"""
    context = DataContext()
    [print(i) for i in context.get_stocks()]

def quotes(ticker):
    """list quotes for stock"""
    context = DataContext()
    [print(q.Ticker.ticker, q.Close) for q in context.get_quotes(ticker)]

addsymbolsfromcsv("WIKI_20170908.csv")

if len(sys.argv) > 1:
    command = sys.argv[1]
    if command == "help":
        print("create, historical, daily, help")
    elif command == "create":
        create()
    elif command == "historical":
        historical()
    elif command == "historicalcsv":
        addhistoricalfromcsv(sys.argv[2])
    elif command == "daily":
        daily()
    elif command == "stocks":
        stocks()
    else:
        print("Unknown command {command}".format(command=command))
