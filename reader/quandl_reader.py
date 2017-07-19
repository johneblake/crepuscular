import quandl

def set_api_key(key):
    quandl.ApiConfig.api_key = key

def get_all_data():
    return quandl.get_table('WIKI/PRICES', qopts={'eport':'true'}, paginate=True)
