import json
import time
from collections import OrderedDict
import requests
import datetime

#reference: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
BINANE_URL = 'https://api.binance.com/api/v1/klines'
UP_EMOJI = '\U00002705' #\U000026C4   U+2B06
DOWN_EMOJI = '\U0001F53B'

class MOMENTUM_SIGNAL:
    def __init__(self, baseAsset='BTC', quoteAsset='USDT', interval='1m',
                 timezone_change=-1., change_threshold=3.):
        self.symbol = baseAsset + quoteAsset
        self.baseAsset = baseAsset
        self.quoteAsset = quoteAsset
        self.interval = interval
        self.url = BINANE_URL + '?symbol=' + self.symbol + '&interval=' + interval
        self.timezone_change = timezone_change
        self.change_threshold = change_threshold
        self.round_up = 0 if quoteAsset in ['BUSD', 'USDT'] else 6

    def update_info(self):
        # print (requests.get(self.url).text)
        time.sleep(0.1)
        data = json.loads(requests.get(self.url).text)
        current_data = data[-5:]
        total_volume = 0
        buy_volume = 0
        for current_data_ in current_data:
            total_volume += round(float(current_data_[7]), self.round_up)
            buy_volume += round(float(current_data_[10]), self.round_up)

        sell_volume = total_volume - buy_volume
        gap_volume = round(abs(sell_volume - buy_volume), self.round_up)
        signal = 'SELL' if sell_volume > buy_volume else 'BUY'
        emoji = DOWN_EMOJI if sell_volume > buy_volume > 1 else UP_EMOJI

        price_change = float(current_data[-1][4]) / float(current_data[-5][1])
        price_change_percentage = round(100 * (price_change - 1), 2) if price_change > 1\
                                    else round(100 * (1 / price_change - 1), 2)
        # print (signal, price_change_percentage)

        if price_change_percentage < self.change_threshold: return None
        message = ""
        # message += "{}\n".format(datatime_)
        message += "{:<15}: {} {}%\n".format(self.baseAsset + '/' + self.quoteAsset, emoji, price_change_percentage)
        message += "{:<20}: {:,.6f}\n".format('Last', float(current_data[-1][4]))
        message += "{:<15}: {:,} {}\n".format('Vol total ' + '5m', total_volume, self.quoteAsset)
        message += "{:<15}: {:,} {}\n".format('Vol gap ' + '5m',
                                                 gap_volume, self.quoteAsset)
        return message

    def get_datetime(self, data_):
        return datetime.datetime.fromtimestamp(data_[0] / 1000)

# momentum_signal = MOMENTUM_SIGNAL(symbol='BTCUSDT', change_threshold=0.1)
# message = momentum_signal.update_info()
# if message is not None:
#     print (message)




