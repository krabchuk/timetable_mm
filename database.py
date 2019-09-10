from pymongo import MongoClient
import pandas as pd


class TimeTableData:
    def __init__(self):
        client = MongoClient(port=27017)
        self.db = client.database
        self.time_table = self.db.test_timetable

        load = False

        if load:
            branch_offset = [0, 0, 8, 20, 30]

            for week_num, week in enumerate(['up', 'down']):
                xls_file = pd.ExcelFile("osen_2019_" + week + ".xls")
                for course in range(1, 7):
                    for branch in range(1, 3 + (course > 2) + 1):
                        data_xls = xls_file.parse('{}.{}'.format(course, branch))
                        data_list = list(data_xls.items())
                        for group_num in range(1, len(data_list)):
                            actual_group = course * 100 + branch_offset[branch] + group_num
                            data = data_list[group_num - 1][1]
                            for row_num in range(6 * 5):  # 6 days x 5 classes
                                day = row_num // 5
                                para_num = row_num - day * 5
                                first_data_row = row_num * 3
                                first_row = data[first_data_row]
                                if first_row != first_row:
                                    self.insert_to_timetable(week_num, actual_group, day, para_num, "", "", "")
                                    continue
                                if '\n' in str(first_row):  # parse first row
                                    parsed_row = str(first_row).split('\n')
                                    self.insert_to_timetable(week_num, actual_group, day, para_num,
                                                             parsed_row[0], parsed_row[1], parsed_row[2])
                                    continue
                                self.insert_to_timetable(week_num, actual_group, day, para_num,
                                                         data[first_row], data[first_row + 1], data[first_row + 2])

    def insert_to_timetable(self, week, group, day, para_num, class_name, teacher, room):
        self.time_table.insert_one({'week': week,
                                    'group': group,
                                    'day': day,
                                    'para_num': para_num,
                                    'class': class_name,
                                    'teacher': teacher,
                                    'room': room})

    def get_para_data(self, week, group, day, para_num):
        return self.time_table.find_one({'week': week,
                                         'group': group,
                                         'day': day,
                                         'para_num': para_num})

    def update_timetable(self, user_id, data):
        if data["admin"]:
            timetable = self.time_table
        else:
            timetable = self.db[str(user_id) + "_time_table"]

        timetable.update_one({'week': data['week'],
                              'group': users_db.get_users_group(user_id),
                              'day': data['day'],
                              'para_num': data['para_num']},
                             {'$set': {'class': data['class'],
                                       'teacher': data['teacher'],
                                       'room': data['room']}})


class DataStorage:
    def __init__(self):
        client = MongoClient(port=27017)
        self.db = client.databse

    def add_user(self, user_id, user_group):
        self.db.users.delete_many({'id': user_id})
        self.db.users.insert_one({'id': user_id, 'group': user_group})

    def user_exist(self, user_id):
        user = self.db.users.find_one({'id': user_id})
        if user:
            return True
        else:
            return False

    def get_users_group(self, user_id):
        user = self.db.users.find_one({'id': user_id})
        if user:
            return user.get('group')
        else:
            return 0


class AdminsStorage:
    def __init__(self):
        client = MongoClient(port=27017)
        self.admins = client.database.admins

    def add_admin(self, admin_id):
        self.admins.insert_one({'id': admin_id})

    def remove_admin(self, admin_id):
        self.admins.delete_many({'id': admin_id})

    def exist(self, admin_id):
        if self.admins.find_one({'id': admin_id}):
            return True
        else:
            return False

    def __iter__(self):
        admins_ids = self.admins.find({})
        for admin in admins_ids:
            yield admin.get('id')


users_db = DataStorage()
add_user_db = set()

admins_db = AdminsStorage()
add_admins_db = set()

timetable_db = TimeTableData()

change_timetable_db = dict(dict())
