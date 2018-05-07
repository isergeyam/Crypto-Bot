from telegram.ext import Updater, CommandHandler
import CryptoParser
import logging
from dateutil import parser as date_parser
import time

with open('help.txt', 'r') as cur_file:
    help_text = cur_file.read()


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=help_text)


def bot_crate(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=CryptoParser.crate(*update.message.text.split()[1:]))


def bot_history(bot, update):
    mtext = update.message.text.split()
    del mtext[0]
    print(date_parser.parse(mtext[1]))
    print(date_parser.parse(mtext[2]))
    time_from = time.mktime(date_parser.parse(mtext[1]).timetuple())
    time_to = time.mktime(date_parser.parse(mtext[2]).timetuple())
    CryptoParser.history(mtext[0], int(time_from), int(time_to), *mtext[3:])
    bot.send_photo(chat_id=update.message.chat_id, photo=open('tmp_fig.png', 'rb'))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token='556522621:AAHlCktVBSe7sN2EQv3cqEqGKJJ3C_GLre4')
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    crate_handler = CommandHandler('crate', bot_crate)
    history_handler = CommandHandler('history', bot_history)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(crate_handler)
    dispatcher.add_handler(history_handler)
    updater.start_polling()
