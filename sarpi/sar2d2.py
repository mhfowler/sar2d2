import os

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from pi_utilities.telegram_helper import telegram_log
from sarpi.servo_helper import press_button
from hello_settings import SECRETS_DICT


def handle_message(update, context):
    if update.message.text == 'open':
        open(update, context)
    elif update.message.text == 'reboot':
        reboot(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="++ hello this is sar2d2, how can I help you?")


def open(update, context):
    telegram_log('++ someone is opening the front door')
    context.bot.send_message(chat_id=update.effective_chat.id, text="++ no problem dear, opening the front door now")
    try:
        press_button()
        telegram_log('++ successfully opened the door')
    except Exception as e:
        telegram_log('++ failed to open the door: '.format(str(e)))
        context.bot.send_message(chat_id=update.effective_chat.id, text="++ oops, something went wrong")


def reboot(update, context):
    telegram_log('++ someone is rebooting sar2d2: {}'.format(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text="++ no problem dear, rebooting now... will take about a minute")
    os.system('/usr/bin/sudo /sbin/reboot')


def initiate_listener():
    telegram_token = SECRETS_DICT['TELEGRAM_TOKEN']
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    import logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # attach handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    open_handler = CommandHandler('open', open)
    dispatcher.add_handler(open_handler)

    message_handler = MessageHandler(Filters.text, handle_message)
    dispatcher.add_handler(message_handler)

    # start polling
    telegram_log('++ starting telegram bot poller')
    updater.start_polling()


if __name__ == '__main__':
    initiate_listener()