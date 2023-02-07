"""
reference: https://www.shellhacks.com/telegram-api-send-message-personal-notification-bot/
Telegram API: 5956793173:AAEJbf1VkyhTVYOlSjbh6cFrzEaIQX5ebHI
Chat ID: 2051192236
https://api.telegram.org/bot5956793173:AAEJbf1VkyhTVYOlSjbh6cFrzEaIQX5ebHI/getUpdates
"""

import requests

def send_to_telegram(message):
    apiToken = '5956793173:AAEJbf1VkyhTVYOlSjbh6cFrzEaIQX5ebHI'
    chatID = '2051192236'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

send_to_telegram("Hello from Python!")