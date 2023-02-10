from constants import *
from momentum_signal import MOMENTUM_SIGNAL
from collections import OrderedDict
import aljson
import time

def rank_tokens(num_selections):
    binance_listing = aljson.load(BINANCE_LISTING_PATH)
    symbols = [key for key in binance_listing.keys()]
    rank_tokens = []
    for symbol in symbols:
        data_ = binance_listing[symbol]
        if data_['quoteAsset'] not in ['BUSD', 'USDT', 'BTC']: continue
        momentum_signal = MOMENTUM_SIGNAL(baseAsset=data_['baseAsset'], quoteAsset=data_['quoteAsset'],
                                          lot_size=data_['lot_size'], change_threshold=3.)
        percentage_change = momentum_signal.get_percentage_change()
        rank_tokens.append((percentage_change, symbol))

    rank_tokens.sort(reverse=True)
    print ("\n\n")
    for percentage_change, symbol in rank_tokens[:num_selections]:
        print (symbol, percentage_change)
    potential_symbols = OrderedDict([
        (symbol, percentage_change) for percentage_change, symbol in rank_tokens[:num_selections]
    ])
    aljson.save(potential_symbols, POTENTIAL_SYMBOLS_PATH)

if __name__ == '__main__':
    while True:
        try:
            rank_tokens(num_selections=30)
        except BaseException as error:
            print(error)
            time.sleep(0.5)
            continue


