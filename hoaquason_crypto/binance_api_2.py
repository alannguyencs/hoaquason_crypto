import requests
import json
from collections import OrderedDict
import aljson
from constants import *

BINANE_URL = 'https://api.binance.com/api/v1/'
exchange_url = BINANE_URL + 'exchangeInfo'

data = json.loads(requests.get(exchange_url).text)

listing = OrderedDict()
for data_ in data['symbols']:
    symbol = data_['symbol']
    baseAsset = data_['baseAsset']
    quoteAsset = data_['quoteAsset']
    status = data_['status']
    if status == 'TRADING':
        listing[symbol] = {
            'baseAsset': baseAsset,
            'quoteAsset': quoteAsset,
        }

aljson.save(listing, BINANCE_LISTING_PATH)

#1394 symbols in total