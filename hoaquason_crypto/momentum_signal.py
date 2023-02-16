import json
import time
import requests
import datetime

#reference: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
BINANE_URL = 'https://api.binance.com/api/v1/klines'
UP_EMOJI = '\U00002705' #\U000026C4   U+2B06
DOWN_EMOJI = '\U0001F53B'

class MOMENTUM_SIGNAL:
    def __init__(self, baseAsset='BTC', quoteAsset='USDT', lot_size=5, interval='1s',
                 timezone_change=-1., change_threshold=3.):
        self.symbol = baseAsset + quoteAsset
        self.baseAsset = baseAsset
        self.quoteAsset = quoteAsset
        self.lot_size = lot_size
        self.interval = interval
        self.timezone_change = timezone_change
        self.latest_price = -1
        self.change_threshold = change_threshold
        self.round_up = 0 if quoteAsset in ['BUSD', 'USDT'] else 6

    def update_info(self):
        # print (requests.get(self.url).text)
        # time.sleep(0.2)
        start_time = int(time.time() * 1000 - 1000 * 301)
        url = BINANE_URL + '?symbol=' + self.symbol + '&interval=' + self.interval + f'&startTime={start_time}'
        data = json.loads(requests.get(url).text)

        current_price = round(float(data[-1][4]), self.lot_size)
        self.latest_price = current_price
        last_price = float(data[0][1])
        price_change = current_price / last_price
        price_change_percentage = round(100 * (price_change - 1), 2) if price_change > 1 \
            else round(100 * (1 / price_change - 1), 2)
        if price_change_percentage < self.change_threshold: return None

        total_volume = 0
        buy_volume = 0
        for current_data_ in data:
            total_volume += round(float(current_data_[7]), self.round_up)
            buy_volume += round(float(current_data_[10]), self.round_up)

        sell_volume = total_volume - buy_volume
        total_volume = round(total_volume, self.round_up)
        gap_volume = round(abs(sell_volume - buy_volume), self.round_up)
        if self.round_up==0:
            total_volume = int(total_volume)
            gap_volume = int(gap_volume)

        emoji = DOWN_EMOJI if sell_volume > buy_volume > 1 else UP_EMOJI
        datatime_ = self.get_datetime(data[-1])

        message = ""
        message += "{}\n".format(datatime_)
        message += "{:<15}: {} {}%\n".format(self.baseAsset + '/' + self.quoteAsset, emoji, price_change_percentage)
        message += "{:<20}: {}\n".format('Last', "{:.12f}".format(current_price).rstrip('0').rstrip('.'))
        message += "{:<15}: {:,} {}\n".format('Vol total ' + '5m', total_volume, self.quoteAsset)
        message += "{:<15}: {:,} {}\n".format('Vol gap ' + '5m',
                                                 gap_volume, self.quoteAsset)
        return message

    def get_percentage_change(self):
        start_time = int(time.time() * 1000 - 1000 * 301)
        url = BINANE_URL + '?symbol=' + self.symbol + '&interval=' + self.interval + f'&startTime={start_time}'
        data = json.loads(requests.get(url).text)
        # print ('data', data)
        if len(data) == 0:
            print ('{}: data is empty'.format(self.symbol))
            return 0

        current_price = round(float(data[-1][4]), self.lot_size)
        last_price = float(data[0][1])
        price_change = current_price / last_price
        price_change_percentage = round(100 * (price_change - 1), 2) if price_change > 1 \
            else round(100 * (1 / price_change - 1), 2)
        return price_change_percentage

    def get_datetime(self, data_):
        return datetime.datetime.fromtimestamp(data_[0] / 1000 + self.timezone_change * 3600)






