from constants import *

BINANE_URL = 'https://api.binance.com/api/v1/klines'

def get_datetime(data_, timezone_change=-1):
    return datetime.datetime.fromtimestamp(data_[0] / 1000 + timezone_change * 3600)

def investigate_token(symbol, interval='1s'):
    url = BINANE_URL + '?symbol=' + symbol + '&interval=' + interval
    data = json.loads(requests.get(url).text)
    out_file = open("{}{}.csv".format(DATA_PATH, symbol), 'w')
    for data_ in data:
        time_ = get_datetime(data_)
        price_ = data_[4]
        out_file.write("{}, {}\n".format(time_, price_))

def investigate_tokens():
    baseAsset = 'MDT'
    for quoteAsset in ['USDT', 'BUSD', 'BTC']:
        investigate_token(symbol=baseAsset+quoteAsset)

if __name__ == '__main__':
    investigate_tokens()
