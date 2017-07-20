"""Module to read quote data from Quandl"""
import quandl

def set_api_key(key):
    """Set the Quandl api key before making any calls"""
    quandl.ApiConfig.api_key = key

# zip file is a csv
# ["Date", "Open", "High", "Low", "Close", "Volume", "Ex-Dividend", "Split Ratio", "Adj. Open", "Adj. High", "Adj. Low", "Adj. Close", "Adj. Volume"]
def bulk_download(file):
    """Download a csv zip file to the given file location"""
    quandl.Database('WIKI').bulk_download_to_file(file)

# api to download delta file
# https://www.quandl.com/api/v3/datatables/WIKI/PRICES/delta.json?api_key=qSUzVYsyx4v7xVe9VdD3

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
