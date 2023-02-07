"""
reference: https://www.geeksforgeeks.org/send-message-to-telegram-user-using-python/
API (bot) token: 5620146081:AAHaBTB3l-WK9La2398cDYeMfyQejIGIT-c
API ID: 20203502
API hash: ec118c1ece2ed133a869d5f079611aa8

To find user_id: https://www.alphr.com/telegram-find-user-id/
"""

import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

# get your api_id, api_hash, token
# from telegram as described above
api_id = '20203502'
api_hash = 'ec118c1ece2ed133a869d5f079611aa8'
token = '5620146081:AAHaBTB3l-WK9La2398cDYeMfyQejIGIT-c'
message = "Test Telegram bot with Huu Thanh and Huy Tung."

# your phone number
phone = '+084 975335259'

user_id_dict = {
    # 'Thanh': 2051192236,
    'Tung': 6025036895, #1859526781 1859526781 6025036895
    'Jolie': 1733763628,
}

# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)

# connecting and building the session
client.connect()

# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():
    client.send_code_request(phone)

    # signing in the client
    client.sign_in(phone, input('Enter the code: '))

try:
    # receiver user_id and access_hash, use
    # my user_id and access_hash for reference
    # receiver = InputPeerUser('user_id', 'user_hash')
    # receiver = InputPeerUser(2051192236, 0)

    receiver = InputPeerChannel(-1001805462174, 0)
    client.send_message(receiver, message, parse_mode='html')

    # sending message using telegram client
    # for user_id in user_id_dict.values():
    #     print ('user_id', user_id)
    #     receiver = InputPeerUser(user_id, 0)
    #     client.send_message(receiver, message, parse_mode='html')
except Exception as e:

    # there may be many error coming in while like peer
    # error, wrong access_hash, flood_error, etc
    print(e)

# disconnecting the telegram session
client.disconnect()