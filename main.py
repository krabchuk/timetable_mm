import telebot
from telebot import apihelper
import tokens


bot = telebot.TeleBot(tokens.token, threaded=False)
apihelper.proxy = {'https': 'socks5://' + str(tokens.proxy)}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=["text"])
def repeat_message(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
