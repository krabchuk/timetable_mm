import time

import telebot
from telebot import apihelper, types

import database
import tokens
import utils
import wrappers

bot = telebot.TeleBot(tokens.token, threaded=False)


@bot.message_handler(commands=['admin'])
@wrappers.logger
def admin_panel(message):
    user_id = message.chat.id

    if database.admins_db.exist(user_id):
        bot.send_message(chat_id=user_id, text='WIP')
    else:
        database.add_admins_db.add(user_id)
        bot.send_message(chat_id=user_id, text='Send admin\'s password.')


@bot.message_handler(func=lambda message: message.chat.id in database.add_admins_db)
@wrappers.logger
def add_admin(message):
    user_id = message.chat.id

    database.add_admins_db.discard(user_id)
    if message.text == tokens.add_admin_password:
        database.admins_db.add_admin(user_id)
        bot.send_message(chat_id=user_id, text='Successfully added.')
    else:
        bot.send_message(chat_id=user_id, text='Wrong password. This accident will be reported.')
        for admin_id in database.admins_db:
            bot.send_message(chat_id=admin_id, text='Login attempt from @{}'.format(message.from_user.username))


@bot.message_handler(commands=['today'])
@wrappers.logger
@wrappers.check_user_exist(database.users_db)
def send_today(message):
    text_timetable = utils.get_actual_timetable(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=text_timetable)


@bot.message_handler(commands=['info'])
@wrappers.logger
def send_info(message):
    info_text = """
Timetable MM bot: v1.2
Благодарности:
Яне Нагорных за подготовку аватара, дизайн,
Рамзану Бекбулатову за исправления моего быдлокода,
Елене Болотиной за тестирование и моральную поддержку

Лучшая благодарность от Вас - звездочка на гитхабе!
https://github.com/krabchuk/timetable_mm

Отзывы, пожелания по работе бота, баги и несоответствия в расписании присылайте на @krabchuk"""
    bot.send_message(chat_id=message.chat.id, text=info_text)


@bot.message_handler(commands=['help'])
@wrappers.logger
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text='Test message')


@bot.message_handler(commands=['timetable'])
@wrappers.logger
def chose_course(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
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
@wrappers.logger
def add_group_begin(message):
    database.add_user_db.add(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='Отправьте номер группы:')


@bot.message_handler(func=lambda message: message.chat.id in database.add_user_db)
@wrappers.logger
def add_group_end(message):
    if not str(message.text).isdigit():
        bot.send_message(chat_id=message.chat.id, text='Номер группы внезапно является числом, попробуй ещё раз')
        return
    group = int(message.text)
    if not utils.group_valid(group):
        bot.send_message(chat_id=message.chat.id, text='Такой группы не существует, попробуй ещё раз')
        return
    database.add_user_db.discard(message.chat.id)
    database.users_db.add_user(message.chat.id, int(message.text))
    database.tt_storage.get_student_tt(message.chat.id).change_actual_group(int(message.text))
    bot.send_message(chat_id=message.chat.id, text='Теперь номер твоей группы {}'.format(int(message.text)))


@bot.message_handler(commands=['check'])
@wrappers.logger
@wrappers.check_user_exist(database.users_db)
def check_user_id(message):
    group = database.users_db.get_users_group(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='Ваша основная группа {}'.format(group))


@bot.message_handler(content_types=['text'])
@wrappers.logger
@wrappers.check_user_exist(database.users_db)
def send_timetable(message):
    user_id = message.chat.id

    if message.text.lower() == 'сегодня':
        text_timetable = utils.get_actual_timetable(user_id)
    else:
        day = utils.text_to_weekday(message.text)
        text_timetable = utils.get_actual_timetable(user_id, day) if day is not None else 'Фича в разработке'

    bot.send_message(chat_id=message.chat.id, text=text_timetable, parse_mode='HTML')


if __name__ == '__main__':
    debug = True

    if debug:
        #_ = utils.OwnTimetableStorage(0, 101)
        #apihelper.proxy = {'https': 'socks5://' + str(tokens.proxy)}
        bot.polling(none_stop=True)
    else:
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception:
                print('Connection error, restart in 1 sec')
                time.sleep(1)
