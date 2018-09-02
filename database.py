import sqlite3

table_sql = 'CREATE TABLE IF NOT EXISTS users (id integer, group_num integer)'

insert_sql = 'INSERT INTO users VALUES (?,?)'

get_data_by_id_sql = 'SELECT * FROM users WHERE id=?'

delete_by_id_sql = 'DELETE FROM users WHERE id=?'

db_file = './database_users'


class DataStorage:
    def __init__(self, db_file, table_sql):
        self.db = sqlite3.connect(db_file, isolation_level=None)
        self.db.cursor().execute(table_sql)

    def __del__(self):
        self.db.close()

    def add_user(self, user_id, user_group):
        c = self.db.cursor()
        c.execute(delete_by_id_sql, (user_id,))
        c.execute(insert_sql, (user_id, user_group))

    def user_exist(self, user_id):
        c = self.db.cursor()
        c.execute(get_data_by_id_sql, (user_id,))
        res = c.fetchall()
        if len(res) > 0:
            return True
        else:
            return False

    def get_users_group(self, user_id):
        c = self.db.cursor()
        c.execute(get_data_by_id_sql, (user_id,))
        if c.rowcount == 0:
            return 0
        else:
            data = c.fetchall()
            return data[0][1]


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


db = DataStorage(db_file, table_sql)
add_user_db = SmallStorage()
