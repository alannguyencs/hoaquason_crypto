from constants import *
from momentum_signal import MOMENTUM_SIGNAL
from collections import OrderedDict
import aljson
import time

def rank_tokens(num_selections):
    binance_listing = aljson.load(BINANCE_LISTING_PATH)
    baseAssets = [key for key in binance_listing.keys()]
    rank_tokens = []
    for baseAsset in baseAssets:
        data_list = binance_listing[baseAsset]
        percentage_changes = []
        for data_ in data_list:
            time.sleep(0.05)
            if data_['quoteAsset']=='BTC': continue #only consider changes with stable coins
            momentum_signal = MOMENTUM_SIGNAL(baseAsset=data_['baseAsset'], quoteAsset=data_['quoteAsset'],
                                              lot_size=data_['lot_size'], change_threshold=3.)
            percentage_changes.append(momentum_signal.get_percentage_change())
        print ("#{}: {}".format(baseAsset, len(percentage_changes)))
        rank_tokens.append((sum(percentage_changes) / max(1, len(percentage_changes)), baseAsset))

    rank_tokens.sort(reverse=True)
    print ("\n\n")
    for percentage_change, baseAsset in rank_tokens[:num_selections]:
        print (baseAsset, percentage_change)
    potential_symbols = OrderedDict([
        (baseAsset, percentage_change) for percentage_change, baseAsset in rank_tokens[:num_selections]
    ])
    aljson.save(potential_symbols, POTENTIAL_SYMBOLS_PATH)

if __name__ == '__main__':
    while True:
        # try:
        if True:
            rank_tokens(num_selections=20)
        # except BaseException as error:
        #     print(error)
        #     time.sleep(0.5)
        #     continue


