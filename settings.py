#! /usr/bin/python3
from telegram.ext import Updater
import telegram
# telegram token here
TELEGRAM_TOKEN = '198842159:AAGe1r7PUlnKmhFb9CBPvH5GyGXIQhzeDZs'
bot = telegram.Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher
face_api_key = 'a9c890353dbb41a4a34f8315ab593eee'
