import requests
import json
import datetime
from binance.client import Client
import config
import time

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
start_time = int(time.time() * 1000 - 1000 * 300)
print ('start_time', start_time)
url = BINANE_URL + '?symbol=' + symbol + '&interval=' + interval + f'&startTime={start_time}'
#data: unix_time, open, high, low, close
data = json.loads(requests.get(url).text) #ignore the first day, maybe noisy
print (data)
for data_ in data[-1:]:
    print (data_[4])
    dt = datetime.datetime.fromtimestamp(data_[0] / 1000)
    print ('dt', dt)


client = Client(config.apiKey, config.apiSecurity)
btc_info = client.get_symbol_ticker(symbol='BTCBUSD')
print(btc_info)