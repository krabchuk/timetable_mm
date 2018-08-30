import telebot
from telebot import apihelper
from telebot import types
import tokens
import database
import time


bot = telebot.TeleBot(tokens.token, threaded=False)
apihelper.proxy = {'https': 'socks5://' + str(tokens.proxy)}


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text='Test message', reply_markup=types.ReplyKeyboardRemove())



@bot.message_handler(commands=['chose_course'])
def chose_course(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('1 курс')
    btn2 = types.KeyboardButton('2 курс')
    btn3 = types.KeyboardButton('3 курс')
    btn4 = types.KeyboardButton('4 курс')
    btn5 = types.KeyboardButton('5 курс')
    btn6 = types.KeyboardButton('6 курс')
    markup.add(btn1, btn2, btn3,
               btn4, btn5, btn6)
    bot.send_message(chat_id=message.chat.id, text='Выбери свой курс:', reply_markup=markup)


@bot.message_handler(commands=['start'])
def add_group_begin(message):
    database.small_db.add_id(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='Отправь номер группы:')


@bot.message_handler(func=lambda message: database.small_db.exist(message.chat.id))
def add_group_end(message):
    database.small_db.rm_id(message.chat.id)
    database.db.add_user(message.chat.id, int(message.text))
    bot.send_message(chat_id=message.chat.id, text='Номер {} добавлен'.format(int(message.text)))


@bot.message_handler(commands=['check'])
def check_user_id(message):
    if database.db.user_exist(message.chat.id):
        bot.send_message(chat_id=message.chat.id, text='Вы зарегистрированны')
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы ещё не зарегистрировались. Отправьте команду /start')

# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception:
#         print('Connection error, restart in 1 sec')
#         time.sleep(1)

bot.polling(none_stop=True)
