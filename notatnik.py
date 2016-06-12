#! usr/bin/python3
import logging
import datetime
import re
import telegram
from common_strings import HELP
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')


def fun(database, bot, update):
    custom_keyboard = [[u'Co robiłem', u'Pomóc']]
   #                    [u'Sprawdz wiek na zdjęciu']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,
                                                resize_keyboard=True)
    msg = update.message.text
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    print(user_id)
    print(type(user_id))
    for_slice = [item.lower() for item in msg.split(' ')
                 if item.lower() != u'ja' and item.lower() != u'?']
    if(len(for_slice)) < 2:
        if for_slice[0] in (u'pomóc', u'help', u'/help'):
            bot.sendMessage(chat_id, HELP, reply_markup=reply_markup)
     #   elif for_slice[0] in (u'image', u'/check_image'):
      #      if update.message.photo

    else:
        cmd = for_slice.pop(0)
        done = ' '.join(for_slice)
        predicate = for_slice.pop(0)
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
        'VALUES (%s, %s, %s, %s, %s)',
        (user_id, str(predicate), str(done),
         num, datetime.datetime.utcnow())
    )
    return u"Postaram się zapamiętać"


def prediacte_list(database, user_id):
    database.execute('''SELECT finished, predicate FROM memory WHERE user_id=%s
              ORDER BY finished''',
                     [int(user_id)])
    data = '\n'.join([str(elem[0]) + str("\t") + elem[1]
                      for elem in database.fetchall()])
    if data:
        return data
    else:
        return u"Nic nie robiłem =("


def predicate_history(database, user_id, predicate):
    database.execute('''SELECT finished,
                    done FROM memory  WHERE predicate = %s AND user_id=%s''',
                     [str(predicate), int(user_id)])
    data = '\n'.join([str(elem[0]) + str("\t") + elem[1]
                      for elem in database.fetchall()])
    if data:
        return data
    else:
        return u'Nic nie %s =(' % (predicate)


def predicate_stats(database, user_id, predicate):
    database.execute('''SELECT count(predicate), avg(num), min(num), max(num),
                     done FROM memory WHERE predicate = %s AND
                     user_id=%s GROUP BY done''',
                     (str(predicate), user_id))
    data = '\n'.join([u"Liczba zapisów:\t" + str(predicate) + '\t' +
                      str(elem[0]) +
                      str(u"\traz\nśrednia:\t") +
                      str(elem[1]) + u"\t" + str(elem[4]) +
                      u"\t\nOd\t%s do %s\t" % (str(elem[2]), str(elem[3])) +
                      str(elem[4])
                      for elem in database.fetchall()])
    return data


def get_google_chart(database, user_id, predicate):
    database.execute('''SELECT DISTINCT ON (finished) num,
                            finished FROM memory
                            WHERE predicate=%s AND user_id=%s''',
                     (str(predicate), user_id))
    data = database.fetchall()

    if(len(data)) > 4:
        max_num = max(data, key=lambda m: m[0])[0]
        v, k = zip(*[('%d' % (100.0 * num / max_num),
                      date.strftime('%m.%d')) for num,
                     date in data])
        return 'http://chart.googleapis.com/chart?' \
            'cht=lc&chco=0000FF&chs=500x300&chd=t:%s&chxl=0:|%s' \
            '&chxt=x,y&chxr=4,0,%d' % (','.join(v), '|'.join(k), max_num)
    else:
        return 'https://cdn.meme.am/instances/500x/62608723.jpg'


def extract_number(argument):
    str_argument = str(argument)
    num = re.sub("[^0-9.]", " ", str_argument)
    if re.search("\.", num):
        return int(num)
    else:
        if re.search("[0-9]", num) is None:
            return 0
        return int(num)
