import sqlite3


con = sqlite3.connect("test_db.db")
cur = con.cursor()
for row in cur.execute("SELECT * FROM test_table ORDER BY id"):
    print(row)