#! /usr/bin/python3
import telegram.ext
import create_table
from flask import Flask, g, request
from settings import bot, TELEGRAM_TOKEN

HOST = '0.0.0.0'
# FQDN or ip address of the server (should be same as used when generating
# SSL certificate)
PORT = 5000
CERT = 'ssl/webhook_cert.crt'
CERT_KEY = 'ssl/webhook_cert.key'


app = Flask(__name__)
context = (CERT, CERT_KEY)


@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True))
    bot.sendMessage(chat_id=update.message.chat_id, text='HALO TO JA')

    return u'ok'


def set_webhook():
    bot.setWebhook(webhook_url='https://%s:%s/%s' %
                   (HOST, PORT, TELEGRAM_TOKEN),
                   certificate=open(CERT, 'rb'))

    if __name__ == '__main__':
        setWebhook()

        app.run(host='0.0.0.0',
                port=PORT,
                ssl_context=context,
                debug=True)
