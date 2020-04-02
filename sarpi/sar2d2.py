import os
import json

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from pi_utilities.telegram_helper import telegram_log
from sarpi.servo_helper import press_button
from hello_settings import SECRETS_DICT


def handle_message(update, context):
    t = update.message.text.lower()
    if t == 'open':
        open_cmd(update, context)
    elif t == 'reboot':
        reboot(update, context)
    elif t == 'open please':
        open_cmd(update, context)
    elif t == 'restart':
        reboot(update, context)
    elif t == 'buzz':
        open_cmd(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="++ hello this is sar2d2, how can I help you?")


def open_cmd(update, context):
    telegram_log('++ someone is opening the front door')
    context.bot.send_message(chat_id=update.effective_chat.id, text="++ no problem dear, will try to open the front door now")
    try:
        press_button()
        telegram_log("++ just tried to open the door, if it didn't work, wait a few seconds and try again, or you can try sending the message reboot and then try again")
    except Exception as e:
        telegram_log('++ failed to open the door: '.format(str(e)))
        context.bot.send_message(chat_id=update.effective_chat.id, text="++ oops, something went wrong")


def write_reboot_id(t_id):
    reboot_log_file = SECRETS_DICT['REBOOT_LOG_FILE']
    with open(reboot_log_file, 'w') as r_file:
        text = json.dumps({'t_id': t_id})
        r_file.write(text)
        telegram_log('++ logged {} to reboot_file'.format(text))


def reboot(update, context):
    telegram_log('++ someone is rebooting sar2d2: {}'.format(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text="++ no problem dear, one sec... will take about a minute")
    try:
        write_reboot_id(update.effective_chat.id)
    except exception as e:
        telegram_log('++ failed to log to reboot_file: {}'.format(e.message))
        pass
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

    open_handler = CommandHandler('open', reboot)
    dispatcher.add_handler(open_handler)

    reboot_handler = CommandHandler('reboot', open_cmd)
    dispatcher.add_handler(reboot_handler)

    message_handler = MessageHandler(Filters.text, handle_message)
    dispatcher.add_handler(message_handler)

    # start polling
    telegram_log('++ starting telegram bot poller')
    updater.start_polling()


if __name__ == '__main__':
    initiate_listener()