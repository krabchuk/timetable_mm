from pymongo import MongoClient
import pandas as pd


class TimeTableData:
    def __init__(self):
        client = MongoClient(port=27017)
        db = client.database
        self.time_table = db.test_timetable

        load = False

        if load:
            branch_offset = [0, 0, 8, 20, 30]
            row_name = ["class", "teacher", "room"]

            for week_num, week in enumerate(['up', 'down']):
                xls_file = pd.ExcelFile("osen_2018_" + week + ".xls")
                for course in range(1, 7):
                    for branch in range(1, 3 + (course > 2) + 1):
                        data = xls_file.parse('{}.{}'.format(course, branch))
                        for group_num, group in enumerate(data.items()):
                            actual_group = course * 100 + branch_offset[branch] + group_num
                            for row_num, row in enumerate(group[1]):
                                day = row_num // 15
                                local_row_num = row_num - day * 15
                                para_num = local_row_num // 3
                                row_name_num = local_row_num % 3
                                if row_name_num == 0:
                                    self.time_table.insert_one({'week': week_num,
                                                                'group': actual_group,
                                                                'day': day,
                                                                'para_num': para_num})

                                if row:
                                    self.time_table.update_one({'week': week_num,
                                                                'group': actual_group,
                                                                'day': day,
                                                                'para_num': para_num},
                                                               {'$set': {row_name[row_name_num]: str(row)}})
                                else:
                                    self.time_table.update_one({'week': week_num,
                                                                'group': actual_group,
                                                                'day': day,
                                                                'para_num': para_num},
                                                               {'$set': {row_name[row_name_num]: ""}})

    def get_para_data(self, week, group, day, para_num):
        return self.time_table.find_one({'week': week,
                                         'group': group,
                                         'day': day,
                                         'para_num': para_num})


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
