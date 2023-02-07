"""
reference: https://www.geeksforgeeks.org/send-message-to-telegram-user-using-python/
API (bot) token: 5620146081:AAHaBTB3l-WK9La2398cDYeMfyQejIGIT-c
API ID: 20203502
API hash: ec118c1ece2ed133a869d5f079611aa8

To find user_id: https://www.alphr.com/telegram-find-user-id/
"""
import time
from momentum_signal import MOMENTUM_SIGNAL
import requests
import aljson
from multiprocessing import Pool
NUM_PROCESSES = 8

def send_to_telegram(message):
    apiToken = '5956793173:AAEJbf1VkyhTVYOlSjbh6cFrzEaIQX5ebHI'
    chatID = '2051192236'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message}) #'parse_mode': 'html'
        # print(response.text)
    except Exception as e:
        print(e)

binance_listing = aljson.load('binance_listing.json')

def run_bot(pid):
    symbols = [key for key in binance_listing.keys()]
    fold_length = len(symbols) // NUM_PROCESSES
    fold_start = fold_length * pid
    fold_end = fold_length * (pid + 1) if pid < NUM_PROCESSES - 1 else len(symbols)
    symbols_pid = symbols[fold_start : fold_end]
    print (pid, fold_start, fold_end, len(symbols))
    while True:
        t_0 = time.time()
        for symbol in symbols_pid:
            data_ = binance_listing[symbol]
            momentum_signal = MOMENTUM_SIGNAL(symbol=symbol, quoteAsset=data_['quoteAsset'], change_threshold=2.)
            message = momentum_signal.update_info()
            if message is not None:
                # print(message)
                # in case of script ran first time it will
            # ask either to input token or otp sent to
            # number or sent or your telegram id
                send_to_telegram(message)
        t_1 = time.time()
        print ("pid = {}, running time = {:.0f} seconds".format(pid, (t_1 - t_0)))
        # time.sleep(5 * 60)
    return pid

if __name__ == '__main__':
    with Pool(NUM_PROCESSES) as p: #processes is the number of worker processes to use
        p.map(run_bot, [i for i in range(NUM_PROCESSES)])