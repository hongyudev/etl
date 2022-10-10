from constant import *
import sqlite3


class SqliteLoader:
    def __init__(self):
        self.con = sqlite3.connect("test_db.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS test_table (%s PRIMARY KEY, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
            COLUMN_ID, COLUMN_USER_NAME, COLUMN_FIRST_NAME, COLUMN_LAST_NAME, COLUMN_EMAIL, COLUMN_PHONE, COLUMN_GENDER,
            COLUMN_IP_ADDRESS, COLUMN_COUNTRY, COLUMN_CC_NUMBER, COLUMN_CC_TYPE, COLUMN_FIRST_NAME+"_raw", COLUMN_LAST_NAME+"_raw",
            COLUMN_EMAIL+"_raw", COLUMN_PHONE+"_raw", COLUMN_IP_ADDRESS+"_raw", COLUMN_CC_NUMBER+"_raw"
        ))

    def insert(self, rows):
        data = [
            (row[COLUMN_ID], row[COLUMN_USER_NAME], row[COLUMN_FIRST_NAME], row[COLUMN_LAST_NAME], row[COLUMN_EMAIL],
             row[COLUMN_PHONE], row[COLUMN_GENDER], row[COLUMN_IP_ADDRESS], row[COLUMN_COUNTRY], row[COLUMN_CC_NUMBER],
             row[COLUMN_CC_TYPE], row[COLUMN_FIRST_NAME+"_raw"], row[COLUMN_LAST_NAME+"_raw"], row[COLUMN_EMAIL+"_raw"],
             row[COLUMN_PHONE+"_raw"], row[COLUMN_IP_ADDRESS+"_raw"], row[COLUMN_CC_NUMBER+"_raw"]) for row in rows
        ]
        self.cur.executemany("INSERT INTO test_table VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        self.con.commit()
