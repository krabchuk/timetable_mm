import functools

import pandas as pd

from main import bot


class TimetableData:
    def __init__(self, xls_filename):
        self.xls_file = pd.ExcelFile(xls_filename)

        self.timetable_data = {}
        self.read()

    def read(self):
        for course in range(1, 6 + 1):
            self.timetable_data[course] = {}
            for branch in range(1, 3 + (course > 2) + 1):
                self.timetable_data[course][branch] = self.xls_file.parse('{}.{}'.format(course, branch))

    def __getitem__(self, item):
        return self.timetable_data[item]


timetable_up = TimetableData('osen_2018_up.xls')
timetable_down = TimetableData('osen_2018_down.xls')

get_log = [0]


def group_valid(group):
    if 100 < group < 113 or 120 < group < 127 or \
            200 < group < 213 or 220 < group < 227 or \
            300 < group < 313 or 320 < group < 327 or 330 < group < 334 or \
            400 < group < 413 or 420 < group < 427 or 430 < group < 434 or \
            500 < group < 513 or 520 < group < 527 or 530 < group < 534 or \
            600 < group < 613 or 620 < group < 627 or 630 < group < 634:
        return True
    else:
        return False


def is_nan(x):
    return x != x


def bold(text, html=True):
    return '<b>{}</b>'.format(text) if html else '*{}*'.format(text)


def code(text, html=True):
    return '<code>{}</code>'.format(text) if html else'`{}`'.format(text)


def text_to_weekday(text):
    if text.lower() in ['понедельник', 'пн']:
        return 0
    if text.lower() in ['вторник', 'вт']:
        return 1
    if text.lower() in ['среда', 'ср']:
        return 2
    if text.lower() in ['четверг', 'чт']:
        return 3
    if text.lower() in ['пятница', 'пт']:
        return 4
    if text.lower() in ['суббота', 'сб']:
        return 5
    if text.lower() in ['воскресенье', 'вс']:
        return 6
    return None


def get_data_for_group(group, week):
    course = group // 100
    h = 100 * course

    timetable_data = timetable_up if week == 0 else timetable_down

    if h < group < h + 7:
        return timetable_data[course][0][group]
    if h + 6 < group < h + 13:
        return timetable_data[course][1][group]
    if h + 20 < group < h + 27:
        return timetable_data[course][2][group]
    if h + 30 < group < h + 34:
        return timetable_data[course][3][group]


def get_para_name(group, day, para_num, week):
    data = get_data_for_group(group, week)
    row = day * 15 + para_num * 3
    para_name = ''
    if data is None:
        return para_name
    if str(data[row]) == 'Физическое воспитание':
        para_name = '└ 🏃 Физическое воспитание'
        return para_name
    if not is_nan(data[row]):
        para_name += '└ 📚 ' + str(data[row]) + '\n'
    if not is_nan(data[row + 1]):
        para_name += '└ 👨‍🏫 ' + str(data[row + 1]) + '\n'
    if not is_nan(data[row + 2]):
        para_name += '└ 🏫 ' + str(data[row + 2])
    if len(para_name) == 0:
        para_name = '└ 😴🌭🎮'
    return para_name


def get_para_time(para_num, group):
    course = group // 100
    if para_num == 0:
        return '09:00 — 10:35'
    if para_num == 1:
        return '10:45 — 12:20'
    if course < 3:
        if para_num == 2:
            return '13:15 — 14:50'
    else:
        if para_num == 2:
            return '12:30 — 14:05'
    if para_num == 3:
        return '15:00 — 16:35'
    if para_num == 4:
        return '16:45 — 18:20'


def get_timetable(group, day, week):
    get_log[0] += 1
    if get_log[0] % 100 == 0:
        print(get_log[0])
    text = ''
    for para_num in range(5):
        text += bold('{} пара\n'.format(para_num + 1)) + '└ ⏰ ' + code('{}\n'.format(get_para_time(para_num, group)))
        text += get_para_name(group, day, para_num, week)
        text += '\n\n'
    return text


def check_user_exist(storage):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(message):
            if not storage.user_exist(message.chat.id):
                bot.send_message(chat_id=message.chat.id,
                                 text='✨ Вас нет в базе данных, нажмите /start для регистрации')
                return

            return func(message)

        return wrapped

    return decorator
