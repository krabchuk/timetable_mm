import database


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


def get_actual_timetable(user_id, manual_day=None):
    group = database.users_db.get_users_group(user_id)
    week, day = get_week_and_day()
    if manual_day is not None:
        day = manual_day
    if day == 6:
        return "Сегодня воскресенье, какие пары?"
    text = ''
    for para_num in range(5):
        text += '{} пара\n'.format(para_num + 1) + \
                '└ ⏰ ' + '{}\n'.format(get_para_time(para_num, group))
        text += get_actual_para_name(user_id, week, group, day, para_num)
        text += '\n\n'
    return text


def get_actual_para_name(user_id, week, group, day, para_num):
    para_data = database.timetable_db.get_para_data(week, group, day, para_num)

    if len(para_data) == 0:
        return '└ 😴🌭🎮'
    if para_data['class'] == 'Физическое воспитание':
        return "└ 🏃 Физическое воспитание"

    para_name = ''
    para_name += '└ 📚 ' + para_data['class'] + '\n'
    para_name += '└ 👨‍🏫 ' + para_data['teacher'] + '\n'
    para_name += '└ 🏫 ' + para_data['room']
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
