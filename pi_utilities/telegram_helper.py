#This script is independet of lib or python version (tested on python 2.7 and 3.5)

import telegram

from hello_settings import SECRETS_DICT
#token that can be generated talking with @BotFather on telegram
my_token = SECRETS_DICT['TELEGRAM_TOKEN']


def send_telegram(msg, chat_id, token=my_token):
	"""
	Send a mensage to a telegram user specified on chatId
	chat_id must be a number!
	"""
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)


def telegram_log(msg):
	chat_id='643117986'
	send_telegram(msg=msg, chat_id=chat_id)


if __name__ == '__main__':
    send_telegram('++ hi this is test message', chat_id='643117986')