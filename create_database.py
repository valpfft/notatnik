import sqlite3

conn = sqlite3.connect('base.db')
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS memory(
              id integer primary key autoincrement,
              user_id integer not null,
              predicate text not null,
              object text not null,
              num real,
              finished timestamp not null)''')
conn.commit()
