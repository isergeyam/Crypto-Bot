from telegram.ext import Updater, CommandHandler
import CryptoParser
import logging

with open('help.txt', 'r') as cur_file:
    help_text = cur_file.read()


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=help_text)


def bot_crate(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=CryptoParser.crate(*update.message.text.split()[1:]))


def bot_history(bot, update):
    CryptoParser.history(*update.message.text.split()[1:])
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
