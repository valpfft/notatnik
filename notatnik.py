#! /usr/bin/python3

import logging
import datetime
import re
from create_database import *
from settings import *


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')


def fun(database, bot, update):
    msg = update.message.text
    for_slice = [item.lower() for item in msg.split(' ')
                 if item.lower() != u'ja' and item.lower() != u'?']
    cmd = for_slice.pop(0)
    done = ' '.join(for_slice)
    predicate = for_slice.pop(0)

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if cmd == u'co' and done == u'robiłem':
        bot.sendMessage(chat_id, prediacte_list(
            database, user_id))
    elif cmd in (u'co', u'kto', u'jak', u'gdzie',
                 u'przypomni', u'działanie'):
        bot.sendMessage(chat_id,
                        predicate_history(database,
                                          user_id,
                                          predicate))
    elif cmd in (u'ile', u'oblicz'):
        bot.sendMessage(chat_id,
                        predicate_stats(database,
                                        user_id,
                                        predicate))
        bot.sendPhoto(chat_id, get_google_chart(
            database, user_id, predicate))
    else:
        predicate, num = cmd, extract_number(done)
        done = re.sub("\d+", "", done)
        bot.sendMessage(
            chat_id,
            remember(database, user_id, predicate,
                     done, num))


def remember(database, user_id, predicate, done, num):
    database.execute(
        'INSERT INTO memory (user_id, predicate, done, num, finished) '
        'VALUES (?, ?, ?, ?, ?)',
        (user_id, str(predicate), str(done),
         num, datetime.datetime.utcnow())
    )
    database.commit()
    return u"Okey"


def prediacte_list(database, user_id):
    c = database.cursor()
    c.execute('''SELECT finished, predicate FROM memory''')
    data = '\n'.join([str(elem[0]) + str("\t") + elem[1]
                      for elem in c.fetchall()])
    if data:
        return data
    else:
        return u"Nic nie robiłem =("


def predicate_history(database, user_id, predicate):
    c = database.cursor()
    c.execute('''SELECT finished,
                    done FROM memory  WHERE predicate = ? ''',
              (predicate,))
    data = '\n'.join([str(elem[0]) + str("\t") + elem[1]
                      for elem in c.fetchall()])
    if data:
        return data
    else:
        return u'Nic nie %s =(' % (predicate)


def predicate_stats(database, user_id, predicate):
    c = database.cursor()
    c.execute('''SELECT count(predicate), avg(num), min(num), max(num),
                     done FROM memory WHERE predicate = ?''', (predicate,))
    data = '\n'.join([u"Liczba zapisów:\t" + str(predicate) + '\t' +
                      str(elem[0]) +
                      str(u"\traz\nśrednia:\t") +
                      str(elem[1]) + str(elem[4]) +
                      u"\nOd\t%s do %s" % (str(elem[2]), str(elem[3])) +
                      str(elem[4])
                      for elem in c.fetchall()])
    return data


def get_google_chart(database, user_id, predicate):
    data = database.execute('''SELECT num, finished FROM memory
                            WHERE user_id=? AND predicate=?
                            ORDER BY finished DESC LIMIT 30''',
                            (user_id, predicate)).fetchall()
    if(len(data)) > 4:
        max_num = max(data, key=lambda m: m[0])[0]
        v, k = zip(*[('%d' % (100.0 * num / max_num),
                      date.strftime('%m.%d')) for num,
                     date in data])
        return 'http://chart.googleapis.com/chart?' \
            'cht=bvg&chs=750x250&chd=t:%s&chxl=0:|%s' \
            '&chxt=x,y&chxr=1,0,%d' % (','.join(v), '|'.join(k), max_num)
    else:
        return 'https://cdn.meme.am/instances/500x/62608723.jpg'


def extract_number(argument):
    str_argument = str(argument)
    num = re.sub("[^0-9.]", " ", str_argument)
    if re.search("\.", num):
        return int(num)
    else:
        if re.search("[0-9]", num) is None:
            return None
        return int(num)

with conn:
    last_update_id = bot.getUpdates()[-1].update_id
    while True:
        for update in bot.getUpdates(offset=last_update_id, timeout=10):
            if last_update_id < update.update_id:
                if update.message.text:
                    fun(conn, bot, update)
                    last_update_id = update.update_id
