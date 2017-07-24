import csv
import requests

def get_etf():
    """Download csv from nasdaq of etf"""
    download = requests.get("http://www.nasdaq.com/investing/etfs/etf-finder-results.aspx?download=Yes")
    decoded_content = download.content.decode(download.encoding)

    cr = csv.reader(decoded_content.splitlines())
    for line in cr:
        print("Symbol = {symbol}, Description = {description}".format(symbol=line[0], description=line[1]))
