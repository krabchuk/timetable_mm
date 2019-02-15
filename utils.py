import functools
import pandas as pd
import numpy as np
from os.path import isfile
from database import tt_storage
from database import db


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

    @staticmethod
    def group_branch(group):
        group = int(str(group)[1:])
        if 0 < group < 7:
            return 1
        if 6 < group < 13:
            return 2
        if 20 < group < 27:
            return 3
        if 30 < group < 34:
            return 4
        return None

    def group_data(self, group):
        course = group // 100
        branch = self.group_branch(group)
        return self.timetable_data[course][branch][group]


class TeachersCoursersStorage:
    def __init__(self):
        self.teachers = set()
        self.courses = set()

        for group in range(100, 700):
            if group_valid(group):
                for week in range(2):
                    data = get_data_for_group(group, week)
                    for para, day in zip(range(5), range(7)):
                        row = day * 15 + para * 3
                        self.courses.add(str(data[row]))
                        self.teachers.add(str(data[row + 1]))

    def print(self):
        print(self.courses)
        print(self.teachers)


class OwnTimetableStorage:
    def __init__(self, user_id, group):
        self.id = user_id
        self.actual_group = group
        self.actual_tt = [None] * 2
        self.file_prefix = './user_timetables/'

        self.update_actual_tt()
        self.backup_actual_tt()

    def get_tt(self, week):
        return self.actual_tt[week]

    def get_filepath(self, week):
        return self.file_prefix + str(self.id) + '_' + str(self.actual_group) + '_' + str(week) + '.txt'

    def update_actual_tt(self):
        for week in range(2):
            if isfile(self.get_filepath(week)):
                self.actual_tt[week] = pd.read_csv(self.get_filepath(week), header=None)[0]
            else:
                self.actual_tt[week] = get_data_for_group(self.actual_group, week)
        for i in range(90):
            print(self.actual_tt[1][i])

    def backup_actual_tt(self):
        for week in range(2):
            self.actual_tt[week].to_csv(self.get_filepath(week), index=False, header=False)

    def change_actual_group(self, group):
        if self.actual_group == group:
            pass
        self.actual_group = group
        self.update_actual_tt()
        self.backup_actual_tt()

    # Field type: 0 for course name
    #             1 for teacher name
    #             2 for class name
    def change_actual_tt(self, week, day, para, field_type, data):
        self.actual_tt[week][day * 5 + para * 3 + field_type] = data
        self.backup_actual_tt()


timetable_up = TimetableData('osen_2018_up.xls')
timetable_down = TimetableData('vesna_2019_down.xls')


get_log = [0]


def group_valid(group):
    if 100 < group < 113 or 120 < group < 127 or \
            200 < group < 213 or 220 < group < 227 or \
            300 < group < 313 or 320 < group < 327 or 330 < group < 334 or \
            400 < group < 413 or 420 < group < 427 or 430 < group < 434 or \
            500 < group < 512 or 520 < group < 527 or 530 < group < 533 or \
            600 < group < 612 or 620 < group < 627 or 630 < group < 633:
        return True
    else:
        return False


def is_nan(x):
    return x != x


def bold(text, html=True):
    return '<b>{}</b>'.format(text) if html else '*{}*'.format(text)


def code(text, html=True):
    return '<code>{}</code>'.format(text) if html else '`{}`'.format(text)


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
    timetable_data = timetable_up if week == 0 else timetable_down
    return timetable_data.group_data(group)


def get_actual_para_name(user_id, day, para_num, week):
    data = tt_storage.get_student_tt(user_id).get_tt(week)
    return get_para_name_from_data(data, day, para_num)


def get_para_name(group, day, para_num, week):
    data = get_data_for_group(group, week)
    return get_para_name_from_data(data, day, para_num)


def get_para_name_from_data(data, day, para_num):
    row = day * 15 + para_num * 3
    para_name = ''
    if data is None:
        return para_name
    if str(data[row]) == 'Физическое воспитание':
        para_name = "└ 🏃 Физическое воспитание"
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


def get_actual_timetable(user_id, manual_day=None):
    week, day = get_week_and_day()
    if manual_day is not None:
        day = manual_day
    if day == 6:
        return "Сегодня воскресенье, какие пары?"
    text = ''
    for para_num in range(5):
        text += '{} пара\n'.format(para_num + 1) + \
                '└ ⏰ ' + '{}\n'.format(get_para_time(para_num, db.get_users_group(user_id)))
        text += get_actual_para_name(user_id, day, para_num, week)
        text += '\n\n'
    return text


def get_timetable(group, day, week):
    text = ''
    for para_num in range(5):
        text += '{} пара\n'.format(para_num + 1) + '└ ⏰ ' + '{}\n'.format(get_para_time(para_num, group))
        text += get_para_name(group, day, para_num, week)
        text += '\n\n'
    return text


def check_user_exist(storage):
    from main import bot

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


def get_week_and_day():
    from datetime import datetime
    from dateutil import tz
    msk = tz.gettz('UTC+3')
    now = datetime.now(msk)
    week = now.isocalendar()[1] % 2
    day = now.weekday()
    # новая неделя начинается в субботу
    if day == 6:
        week = (week + 1) % 2
    return week, day


def get_msk_time():
    from datetime import datetime
    from dateutil import tz
    msk = tz.gettz('UTC+3')
    return datetime.now(msk)


def get_log_filename():
    now = get_msk_time()
    return '{0}_{1}_{2}_commands_log.txt'.format(str(now.year), str(now.month), str(now.day))


def logger(func):
    @functools.wraps(func)
    def wrapped(message):
        from database import db
        user_id = message.chat.id
        group = db.get_users_group(message.chat.id)
        with open('./logs/' + get_log_filename(), 'a') as file:
            print(get_msk_time(), user_id, group, message.text, file=file)
        return func(message)

    return wrapped
