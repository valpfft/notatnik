import sqlite3
import datetime
import sys
import re
from create_database import create_table


def fun(database, argv):
    for_slice = [item for item in argv.split(' ')
                 if item != u'Ja' and item != u'?']
    cmd = for_slice.pop(0)
    predicate = for_slice
    if cmd in (u'co', u'kto', u'jak', u'gdzie'):
        return predicate_history(database, 0, predicate)
    elif cmd2 in (u'ile', u'oblicz'):
        return predicate_stats(database, 0, predicate)
    else:
        predicate, num = cmd, extract_number(object)
        return remember(database, 0, predicate, object, num)


def remember(database, user_id, predicate, object, num):
    database.execute(
        'INSERT INTO memory (user_id, predicate, object, num, finished) '
        'VALUES (?, ?, ?, ?, ?)',
        (user_id, str(predicate), str(object),
         num, datetime.datetime.utcnow())
    )
    database.commit()
    return u"Okey"


def predicate_history(database, user_id, predicate):
    database.execute('''SELECT finished,
                    predicate, object FROM memory  WHERE predicate = ? ''',
                     (predicate))
    data = database.fetchall()
    print(data)


def predicate_stats(database, user_id, predicate):
    database.execute('''SELECT count(predicate), avg(predicate),
                     object FROM memory WHERE predicate = ? ''', (predicate))
    data = database.fetchall()
    print(data)


def extract_number(argument):
    str_argument = str(argument)
    num = re.sub("[^0-9.]", " ", str_argument)
    if re.search("\.", num):
        return int(num)
    else:
        if re.search("[0-9]", num) is None:
            return None
        return int(num)
create_table()

with sqlite3.connect('base.db',
                     detect_types=sqlite3.PARSE_DECLTYPES) as database:
    if len(sys.argv) > 1:
        print(fun(database, ' '.join(sys.argv[1:])))
