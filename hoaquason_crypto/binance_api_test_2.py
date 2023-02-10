import requests
import json
import datetime
from binance.client import Client
import config
import time
from constants import *
import aljson
"""
this is to check which method is faster:
method 1: from kline-candlestick-data
method 2: with user token
"""
#this is to check which method is faster
#reference: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
BINANE_URL = 'https://api.binance.com/api/v1/klines'
symbol = 'BTCBUSD'
interval = '1s'

# print ('start_time', start_time)

#data: unix_time, open, high, low, close

binance_listing = aljson.load(BINANCE_LISTING_PATH)
symbols = [key for key in binance_listing.keys()]

for num_second in range(300, 1, -10):
    t_0 = time.time()
    for symbol in symbols:
        start_time = int(time.time() * 1000 - 1000 * num_second)
        url = BINANE_URL + '?symbol=' + symbol + '&interval=' + interval + f'&startTime={start_time}'
        data = json.loads(requests.get(url).text)
    t_1 = time.time()
    print ("num_second = {}: Average scanning time = {:.4f}".format(num_second, (t_1 - t_0) / len(symbols)))