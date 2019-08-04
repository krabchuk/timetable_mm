from pymongo import MongoClient


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


class SmallStorage:
    def __init__(self):
        self.data = set()

    def add_id(self, user_id):
        self.data.add(user_id)

    def rm_id(self, user_id):
        self.data.remove(user_id)

    def exist(self, user_id):
        if user_id in self.data:
            return True
        else:
            return False


class TotalOwnTimetablesStorage:
    def __init__(self):
        self.db = {}

    def get_student_tt(self, user_id):
        # Create data if doesnt exist
        if user_id not in self.db:
            import utils
            self.db[user_id] = utils.OwnTimetableStorage(user_id, db.get_users_group(user_id))
        return self.db[user_id]


tt_storage = TotalOwnTimetablesStorage()
db = DataStorage()
add_user_db = SmallStorage()
