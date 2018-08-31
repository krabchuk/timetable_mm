import pandas as pd

timetable_xls = pd.ExcelFile('osen_2018.xls')
timetable_data11 = timetable_xls.parse('1.1')
timetable_data12 = timetable_xls.parse('1.2')
timetable_data13 = timetable_xls.parse('1.3')


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


def isNan(x):
    return x != x


def get_data_for_group (group):
    if 100 < group < 107:
        return timetable_data11[group]
    if 106 < group < 113:
        return timetable_data12[group]
    if 120 < group < 127:
        return timetable_data13[group]


def get_para_name(group, day, para_num):
    data = get_data_for_group(group)
    row = day * 15 + para_num * 3
    para_name = ''
    if not isNan(data[row]):
        para_name += str(data[row]) + ' '
    if not isNan(data[row + 1]):
        para_name += str(data[row + 1]) + ' '
    if not isNan(data[row + 2]):
        para_name += str(data[row + 2]) + ' '
    return para_name


def get_para_time(para_num):
    if para_num == 0:
        return '9:00-10:35'
    if para_num == 1:
        return '10:45-12:20'
    if para_num == 2:
        return '13:15-14:50'
    if para_num == 3:
        return '15:00-16:35'
    if para_num == 4:
        return '16:45-18:20'


def get_timetable(group, day):
    text = ''
    for para_num in range(5):
        text += '{} пара {}: '.format(para_num + 1, get_para_time(para_num))
        text += get_para_name(group, day, para_num)
        text += '\n\n'
    return text
