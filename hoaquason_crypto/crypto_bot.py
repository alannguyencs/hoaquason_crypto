"""
reference: https://help.nethunt.com/en/articles/6467726-how-to-create-a-telegram-bot-and-use-it-to-post-in-telegram-channels
API (bot) token: 5620146081:AAHaBTB3l-WK9La2398cDYeMfyQejIGIT-c
API ID: 20203502
API hash: ec118c1ece2ed133a869d5f079611aa8

To find user_id: https://www.alphr.com/telegram-find-user-id/
channel id: -1001861452010
"""
from constants import *
import time
from momentum_signal import MOMENTUM_SIGNAL
import requests
import aljson
from multiprocessing import Pool
import config
from collections import defaultdict
NUM_PROCESSES = 8

def send_to_telegram(message):
    apiToken = config.apiToken
    chatID = config.chatID
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message}) #'parse_mode': 'html'
        # print(response.text)
    except Exception as e:
        print(e)

binance_listing = aljson.load(BINANCE_LISTING_PATH)

def run_bot(symbol_latest_scan):
    potential_symbols = aljson.load(POTENTIAL_SYMBOLS_PATH)
    symbols = [key for key in potential_symbols.keys()]
    # try:
    if True:
        t_0 = time.time()
        for symbol in symbols:
            now = time.time()
            if now - symbol_latest_scan[symbol] < 5 * 60: continue #5 minutes

            if True:
                data_ = binance_listing[symbol]
                momentum_signal = MOMENTUM_SIGNAL(baseAsset=data_['baseAsset'], quoteAsset=data_['quoteAsset'],
                                                  lot_size=data_['lot_size'], change_threshold=3.)
                message = momentum_signal.update_info()
                if message is not None:
                    # print(message)
                    # in case of script ran first time it will
                # ask either to input token or otp sent to
                # number or sent or your telegram id3
                    send_to_telegram(message)
                    symbol_latest_scan[symbol] = now

            # except BaseException as error_:
            #     print (symbol, error_)
            #     continue

        t_1 = time.time()
        if t_1 - t_0 > 0.5: print ("running time = {:.2f} seconds".format((t_1 - t_0)))
    # time.sleep(5 * 60)
    # except BaseException as error:
    #     print (error)
    #     pass


if __name__ == '__main__':
    symbol_latest_scan = defaultdict(lambda: 0)
    while True:
        t_0 = time.time()
        try:
            run_bot(symbol_latest_scan)
        except BaseException as error:
            print(error)
            time.sleep(0.5)
            continue


