import sqlite3 as sl
import datetime


class DB:

    def __init__(self, db_name='test_db.db'):
        self.db_name = db_name
        self.con = sl.connect(db_name)
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS parking_lot
                        (lp INTEGER,
                        entered BOOL,
                        timestamp TIMESTAMP
                        )''')

    def insert_into_table(self, table_name, columns, *values):

        values = ', '.join(str(value) for value in values)
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(table_name, columns, values)
        self.cur.execute('''{}'''.format(query))
        self.con.commit()



# current_time = datetime.datetime.now()

# ql = 'INSERT INTO parking_lot (lp, entered, timestamp) VALUES (1234567, True, \'{}\')'.format(current_time)


#      cur.execute('''{}'''.format(query))
# print('Done')
# # with con:
# #     data = con.execute("SELECT * FROM PARKING_LOT")
# #     for row in data:
# #         print(row)
# con.commit()

db_handler = DB()
