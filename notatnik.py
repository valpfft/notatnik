import sqlite3
import datetime
import sys



def fun(database, cmd):
    if cmd in (u'co', u'kto', u'jak', u'gdzie'):
        return predicate_history(database, 0, predicate)
    elif cmd in (u'ile', u'oblicz'):
        return predicate_stats(database, 0, predicate)
    else:
        predicate, num = cmd, extract_number(object)
        return remember(database, 0, predicate, object, num)

def remember(database, user_id, predicate, object, num):
    database.execute(
                     'INSERT INTO memory (user_id, predicate, object, num, finished) '
                     'VALUES (?, ?, ?, ?, ?)',
                     (user_id, predicate, object, num, datetime.datetime.utcnow())
                     )
    database.commit()
    return u"Okey"

def predicate_history(database, user_id, predicate):
    database.execute('SELECT finished, predicate, object FROM memory  WHERE predicate = ? ',
                     (predicate))
    data = database.fetchall()
    print(data)

def predicate_stats(database, user_id, predicate_arg):
    database.execute('SELECT count(predicate), avg(predicate), oject FROM memru WHERE predicate = ?',
                     (predicate))

with  sqlite3.connect('base.db', detect_types = sqlite3.PARSE_DECLTYPES) as database:
    if len(sys.argv) > 1:
        print ( fun(database, ' '.join(sys.argv[1:]).decode('utf-8')) )                                 #Problem # 1.  ( How to slice sys.argv ? cmd + predicate)
