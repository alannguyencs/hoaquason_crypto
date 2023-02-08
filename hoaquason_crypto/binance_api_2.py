import requests
import json
from collections import OrderedDict
import aljson
import math
from constants import *

BINANE_URL = 'https://api.binance.com/api/v1/'
exchange_url = BINANE_URL + 'exchangeInfo'

data = json.loads(requests.get(exchange_url).text)

listing = OrderedDict()
for data_ in data['symbols']:
    print ('data_', data_)
    symbol = data_['symbol']
    baseAsset = data_['baseAsset']
    if baseAsset[-2:] == 'UP' or baseAsset[-4:] == 'DOWN': continue
    quoteAsset = data_['quoteAsset']
    lot_size = int(-math.log10(float(data_['filters'][0]['minPrice'])))
    status = data_['status']
    if status == 'TRADING':
        listing[symbol] = {
            'baseAsset': baseAsset,
            'quoteAsset': quoteAsset,
            'lot_size': lot_size,
        }
print ('#symbols = {}'.format(len(listing)))
aljson.save(listing, BINANCE_LISTING_PATH)

#1394 symbols in total