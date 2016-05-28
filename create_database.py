#! /usr/bin/python3
import sqlite3

conn = sqlite3.connect(
    'base.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
c = conn.cursor()


def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS memory(
              id integer primary key autoincrement,
              user_id integer not null,
              predicate text not null,
              done text not null,
              num real,
              finished timestamp not null);''')
conn.commit()
