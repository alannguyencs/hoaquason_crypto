import requests
import json
import datetime

#reference: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
BINANE_URL = 'https://api.binance.com/api/v1/klines'
symbol = 'BTCUSDT'
interval = '1d'
# url = BINANE_URL + '?symbol=' + symbol + '&interval=' + interval
#data: unix_time, open, high, low, close

# proxies = {
#   'http': 'http://10.10.1.10:3128',
#   'https': 'http://10.10.1.10:1080',
# }

url = 'https://httpbin.org/ip'
proxy_ = "190.113.42.162:999"
proxies = {
    "http": 'http://' + proxy_,
    "https": 'http://' + proxy_,
}
# response = requests.get(url=url,proxies=proxies, headers={'User-Agent': 'Chrome'})
# print(response.json())

url = BINANE_URL + '?symbol=' + symbol + '&interval=' + interval
data = json.loads(requests.get(url, proxies=proxies).text) #ignore the first day, maybe noisy
print (data)
for data_ in data:
    print (data_)
    dt = datetime.datetime.fromtimestamp(data_[0] / 1000)
    print ('dt', dt)


"""
https://premiumproxy.net/
good proxy:
190.113.42.162:999
Note: proxy makes the program running very slowly
"""