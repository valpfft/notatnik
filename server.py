#! usr/bin/python3
from os import environ
from flask import Flask, g, request, url_for
import notatnik
from settings import bot, updater, dispatcher
from database import create_table, conn, cursor
from face_detection import face_detection

app = Flask(__name__)

with conn:
    try:
        last_update_id = bot.getUpdates()[0].update_id
    except IndexError:
        last_update_id = 0
    while True:
        for update in bot.getUpdates(offset=last_update_id, timeout=10):
            if last_update_id < update.update_id:
                if update.message.text:
                    notatnik.fun(cursor, bot, update)
                    last_update_id = update.update_id
                elif update.message.photo:
                    chat_id = update.message.chat_id
                    user_id = update.message.from_user.id
                    photo_url = update.message.photo[-1].file_id
                    file = bot.get_file(photo_url)
                    bot.sendMessage(chat_id, face_detection(file.file_path))
                    last_update_id = update.update_id


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = create_table()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is None:
        db.close()


@app.route('/setup', methods=['GET', 'POST'])
def set_webhook():
    webhook_url = url_for('receive_update',
                          _external=False)
    return 'ok' if bot.setWebhook(webhook_url) else 'failure'
if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=environ.get('PORT', 5000),
            debug=False,
            process=2,
            server='gunicorn')
