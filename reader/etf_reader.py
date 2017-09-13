"""Read etf symbols from Nasdaq"""
import csv
import requests

def get_etf():
    """Download csv from nasdaq of etf or read existing file"""
    if os.path.exists("etf.csv"):
        with open("etf.csv", "rb") as csvfile:
            csv_lines = csv.reader(csvfile)
    else:
        download = requests.get("http://www.nasdaq.com/investing/etfs/etf-finder-results.aspx?download=Yes")
        with open('etf.csv','w') as file:
            file.write(download.content)
        decoded_content = download.content.decode(download.encoding)
        items = []
        csv_lines = csv.reader(decoded_content.splitlines())
    count = 0
    for line in csv_lines:
        if count > 0:
            items.append((line[0], line[1]))
            count += 1
    return items
