"""Read etf symbols from Nasdaq"""
import os
import csv
import requests

def read_lines(csv_lines):
    """read lines from csv file"""
    items = []
    count = 0
    for line in csv_lines:
        if count > 0:
            if line:
                items.append((line[0], line[1]))
        count += 1
    return items

def get_etf():
    """Download csv from nasdaq of etf or read existing file"""
    if os.path.exists("etf.csv"):
        with open("etf.csv", "r") as csvfile:
            csv_lines = csv.reader(csvfile)
            return read_lines(csv_lines)
    else:
        download = requests.get("http://www.nasdaq.com/investing/etfs/etf-finder-results.aspx?download=Yes")
        decoded_content = download.content.decode(download.encoding)
        with open('etf.csv','w') as file:
            file.write(decoded_content)
        csv_lines = csv.reader(decoded_content.splitlines())
        return read_lines(csv_lines)

