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

def run_bot(baseAsset_latest_price, debug=True):
    potential_baseAssets = aljson.load(POTENTIAL_SYMBOLS_PATH)
    baseAssets = [key for key in potential_baseAssets.keys()]
    # try:
    if True:
        t_0 = time.time()
        for baseAsset in baseAssets:
            # now = time.time()
            # if now - baseAsset_latest_scan[baseAsset] < 5 * 60: continue #5 minutes
            latest_price = -1
            if True:
                data_list = binance_listing[baseAsset]
                messages = []
                proof_data = []
                for id, data_ in enumerate(data_list):
                    momentum_signal = MOMENTUM_SIGNAL(baseAsset=data_['baseAsset'], quoteAsset=data_['quoteAsset'],
                                                      lot_size=data_['lot_size'], change_threshold=3., debug=debug)
                    message = momentum_signal.update_info()
                    proof_data.append(momentum_signal.proof_data)

                    #check if the price change is not significant
                    if id == 0:
                        latest_price = momentum_signal.latest_price
                        price_change = max(baseAsset_latest_price[baseAsset], latest_price) / \
                                       min(baseAsset_latest_price[baseAsset], latest_price)
                        if price_change > 0 and price_change < 1.015:
                            messages = []
                            break

                    #check if there is a significant change
                    if message is not None:
                        messages.append(message)
                    else:
                        messages = []
                        break

                if len(messages) > 0:
                    for message in messages:
                        send_to_telegram(message)
                        print (message)

                        if debug:
                            proof_file = open("{}{}_{}.csv".format(DATA_PATH, baseAsset, proof_data[0][-1][0]), 'w')
                            proof_file.write("Datetime")
                            for data_ in data_list:
                                proof_file.write(", {}".format(data_['quoteAsset']))
                            proof_file.write('\n')
                            for line_id in range(len(proof_data[0])):
                                proof_file.write("{}, {}".format(proof_data[0][line_id][0], proof_data[0][line_id][1]))
                                for quote_id in range(1, len(proof_data)):
                                    proof_file.write(", {}".format(proof_data[quote_id][line_id][1]))
                                proof_file.write('\n')

                    baseAsset_latest_price[baseAsset] = latest_price

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
    baseAsset_latest_price = defaultdict(lambda: -1)
    while True:
        t_0 = time.time()
        try:
            run_bot(baseAsset_latest_price, debug=True)
        except BaseException as error:
            print(error)
            time.sleep(0.5)
            continue


