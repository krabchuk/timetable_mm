import telebot
from telebot import apihelper
from telebot import types
import tokens
import database
from datetime import date
import utils

bot = telebot.TeleBot(tokens.token, threaded=False)
apihelper.proxy = {'https': 'socks5://' + str(tokens.proxy)}

@bot.message_handler(commands=['info'])
def send_info(message):
    info_text = """Timetable MM bot: v1.0

Отзывы, пожелания по работе бота, баги и несоответствия в расписании присылайте на @krabchuk"""
    bot.send_message(chat_id=message.chat.id, text=info_text)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text='Test message', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['timetable'])
def chose_course(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Сегодня')
    btn2 = types.KeyboardButton('Понедельник')
    btn3 = types.KeyboardButton('Вторник')
    btn4 = types.KeyboardButton('Среда')
    btn5 = types.KeyboardButton('Четверг')
    btn6 = types.KeyboardButton('Пятница')
    btn7 = types.KeyboardButton('Суббота')
    markup.row(btn1)
    markup.row(btn2, btn3, btn4)
    markup.row(btn5, btn6, btn7)
    bot.send_message(chat_id=message.chat.id, text='Выбери день недели:', reply_markup=markup)


@bot.message_handler(commands=['start'])
def add_group_begin(message):
    database.add_user_db.add_id(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='Отправьте номер группы:')


@bot.message_handler(func=lambda message: database.add_user_db.exist(message.chat.id))
def add_group_end(message):
    if not str(message.text).isdigit():
        bot.send_message(chat_id=message.chat.id, text='Номер группы внезапно является числом, попробуй ещё раз')
        return
    group = int(message.text)
    if not utils.group_valid(group):
        bot.send_message(chat_id=message.chat.id, text='Такой группы не существует, попробуй ещё раз')
        return
    database.add_user_db.rm_id(message.chat.id)
    database.db.add_user(message.chat.id, int(message.text))
    bot.send_message(chat_id=message.chat.id, text='Теперь номер твоей группы {}'.format(int(message.text)))


@bot.message_handler(commands=['check'])
def check_user_id(message):
    if database.db.user_exist(message.chat.id):
        group = database.db.get_users_group(message.chat.id)
        bot.send_message(chat_id=message.chat.id, text='Ваша основная группа {}'.format(group))
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы ещё не зарегистрировались. Отправьте команду /start')


@bot.message_handler(content_types=['text'])
def send_timetable(message):
    if not database.db.user_exist(message.chat.id):
        bot.send_message(chat_id=message.chat.id,
                         text='Вы ещё не зарегистрировались. Отправьте команду /start',
                         reply_markup=types.ReplyKeyboardRemove())
        return
    group = database.db.get_users_group(message.chat.id)
    # сдвигаем неделю, чтобы 0 отвечал за верхнюю
    week = (date.today().isocalendar()[1] + 1) % 2
    text_timetable = 'Фича в разработке'
    if message.text == 'Сегодня':
        day = date.today().weekday()
        if day == 6:
            text_timetable = 'Сегодня воскресенье, какие пары?'
        else:
            text_timetable = utils.get_timetable(group, day, week)
    if message.text == 'Понедельник':
        text_timetable = utils.get_timetable(group, 0, week)
    if message.text == 'Вторник':
        text_timetable = utils.get_timetable(group, 1, week)
    if message.text == 'Среда':
        text_timetable = utils.get_timetable(group, 2, week)
    if message.text == 'Четверг':
        text_timetable = utils.get_timetable(group, 3, week)
    if message.text == 'Пятница':
        text_timetable = utils.get_timetable(group, 4, week)
    bot.send_message(chat_id=message.chat.id, text=text_timetable, reply_markup=types.ReplyKeyboardRemove())


# while True:
#     try:
#         bot.polling(none_stop=True)
#     except Exception:
#         print('Connection error, restart in 1 sec')
#         time.sleep(1)

bot.polling(none_stop=True)
