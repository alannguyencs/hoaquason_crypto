import requests
import json
import datetime

#reference: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
BINANE_URL = 'https://api.binance.com/api/v1/klines'
symbol = 'BTCUSDT'
interval = '1d'
url = BINANE_URL + '?symbol=' + symbol + '&interval=' + interval
#data: unix_time, open, high, low, close
data = json.loads(requests.get(url).text) #ignore the first day, maybe noisy
print (data)
for data_ in data:
    print (data_)
    dt = datetime.datetime.fromtimestamp(data_[0] / 1000)
    print ('dt', dt)


