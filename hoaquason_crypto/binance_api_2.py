import requests
import json
from collections import OrderedDict, defaultdict
import aljson
import math
from constants import *

BINANE_URL = 'https://api.binance.com/api/v1/'
exchange_url = BINANE_URL + 'exchangeInfo'

data = json.loads(requests.get(exchange_url).text)


listing = defaultdict(lambda: {})
for data_ in data['symbols']:
    print ('data_', data_)
    symbol = data_['symbol']
    baseAsset = data_['baseAsset']
    if baseAsset[-2:] == 'UP' or baseAsset[-4:] == 'DOWN': continue
    quoteAsset = data_['quoteAsset']
    lot_size = int(-math.log10(float(data_['filters'][0]['minPrice'])))
    status = data_['status']
    if status == 'TRADING':
        data_ = {
            'baseAsset': baseAsset,
            'quoteAsset': quoteAsset,
            'lot_size': lot_size,
        }
        listing[baseAsset][quoteAsset] = data_

#re-organize USDT, BUSD, BTC
for baseAsset, data_dict in listing.items():
    data_list = []
    for quoteAsset in ['USDT', 'BUSD', 'BTC']:
        if quoteAsset in data_dict:
            data_list.append(data_dict[quoteAsset])
    listing[baseAsset] = data_list

print ('#baseAsset = {}'.format(len(listing)))
aljson.save(listing, BINANCE_LISTING_PATH)

#1394 symbols in total