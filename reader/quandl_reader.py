"""Module to read quote data from Quandl"""
import urllib.request
import json
from io import BytesIO
from zipfile import ZipFile
import quandl

def set_api_key(key):
    """Set the Quandl api key before making any calls"""
    quandl.ApiConfig.api_key = key

# zip file is a csv
# ["Date", "Open", "High", "Low", "Close", "Volume", "Ex-Dividend", "Split Ratio", "Adj. Open", "Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"]
def bulk_download(file):
    """Download a csv zip file to the given file location"""
    quandl.Database('WIKI').bulk_download_to_file(file)

def process_changes(changes):
    """Process the delta list from quandl"""
    # need to take results of this and update our data store
    get_zip(changes["deletions"])
    get_zip(changes["insertions"])
    get_zip(changes["updates"])

def get_zip(file_url):
    """Get a zip file and return contents"""
    url = urllib.request.urlopen(file_url)
    zipfile = ZipFile(BytesIO(url.content))
    zip_names = zipfile.namelist()
    if len(zip_names) == 1:
        file_name = zip_names.pop()
        extracted_file = zipfile.open(file_name)
        return extracted_file

def process_delta_file():
    """Grab the delta file to find which files we need to get"""
    data = urllib.request.urlopen("https://www.quandl.com/api/v3/datatables/WIKI/PRICES/delta.json?api_key={key}".format(key=quandl.ApiConfig.api_key)).read().decode()
    output = json.loads(data)
    filelist = output["data"]["files"]
    for f in filelist:
        if f["to"] > runs.latest:
            process_changes(f) # process deletions, insertions and updates
            runs.latest = f["to"]
# returns
# {
# - data: {
#     - files: [
#         - {
#                from: "2016-09-01T18h32m32",
#                to: "2016-09-02T18h29m50",
#                deletions: "https://link-to-WIKI_PRICES_2016-09-02T18h29m50.zip",
#                insertions: "https://link-to-WIKI_PRICES_2016-09-02T18h29m50.zip",
#                updates: "https://link-to-WIKI_PRICES_2016-09-02T18h29m50.zip"
#            },
#         - {
#                from: "2016-09-02T18h29m50",
#                to: "2016-09-03T18h31m04",
#                deletions: "https://link-to-WIKI_PRICES_2016-09-03T18h31m04.zip",
#                insertions: "https://link-to-WIKI_PRICES_2016-09-03T18h31m04.zip",
#                updates: "https://link-to-WIKI_PRICES_2016-09-03T18h31m04.zip"
#            },
# - {
#               from: "2016-09-03T18h31m04",
#               to: "2016-09-04T18h37m34",
#               deletions: "https://link-to-WIKI_PRICES_2016-09-04T18h37m34.zip",
#               insertions: "https://link-to-WIKI_PRICES_2016-09-04T18h37m34.zip",
#               updates: "https://link-to-WIKI_PRICES_2016-09-04T18h37m34.zip"
# }
#      ],
#     - latest_full_data: {
#           full_data: "https://link-to-WIKI_PRICES_2016-09-04T18h37m34.zip",
#           to: "2016-09-04T18h37m34"
#    }
# }
# }
