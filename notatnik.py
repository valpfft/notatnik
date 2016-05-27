#! /usr/bin/python3

import logging
import datetime
import re
from create_database import *
from settings import bot


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')


def fun(database, bot, update):
    msg = update.message.text
    for_slice = [item for item in msg.split(' ')
                 if item != u'ja' and item != u'?']
    cmd = for_slice.pop(0)
    predicate = ' '.join(for_slice)
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    if cmd == u'co' and object == u'robiłem':
        bot.sendMessage(chat_id, prediacte_list(
            database, user_id))
    if cmd in (u'co', u'kto', u'jak', u'gdzie',
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
    else:
        predicate, num = cmd, extract_number(object)
        bot.sendMessage(
            chat_id,
            remember(database, user_id, predicate,
                     object, num))


def remember(database, user_id, predicate, object, num):
    database.execute(
        'INSERT INTO memory (user_id, predicate, object, num, finished) '
        'VALUES (?, ?, ?, ?, ?)',
        (user_id, str(predicate,), str(object),
         num, datetime.datetime.utcnow())
    )
    database.commit()
    return u"Okey"


def prediacte_list(database, user_id, predicate):
    c = database.cursor()
    c.execute('''SELECT predicate FROM memory''')
    return c.fetchall()


def predicate_history(database, user_id, predicate):
    c = database.cursor()
    c.execute('''SELECT finished,
                    predicate, object FROM memory  WHERE predicate = ? ''',
              (predicate,))
    return c.fetchall()


def predicate_stats(database, user_id, predicate):
    c = database.cursor()
    c.execute('''SELECT count(predicate), avg(predicate),
                     object FROM memory WHERE predicate = ?
                     GROUP BY object''', (predicate,))
    return c.fetchall()


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
        for update in bot.getUpdates(offset=last_update_id, timeout=5):
            if last_update_id < update.update_id:
                if update.message.text:
                    fun(conn, bot, update)
                    last_update_id = update.update_id
