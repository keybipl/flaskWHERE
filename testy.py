import sqlite3

db = sqlite3.connect('gminy.db', check_same_thread=False)
db.row_factory = sqlite3.Row
mycursor = db.cursor()

cur = db.execute('select * from gminy')
results = cur.fetchall()

print(results[0]['gmina'])