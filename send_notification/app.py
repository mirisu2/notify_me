from os import environ
from pyrogram import Client
import pyrogram
import redis
import re
from datetime import datetime
import smtplib
from email.message import EmailMessage

try:
    print('================= Starting APP: send_notification =================')
    CHANNEL = environ.get('CHANNEL')

    REDIS_PASS = environ.get('REDIS_PASS')
    REDIS_HOST = environ.get('REDIS_HOST')
    REDIS_PORT = environ.get('REDIS_PORT')

    TELEGRAM_API_TOKEN = environ.get('TELEGRAM_API_TOKEN')
    API_ID = environ.get('API_ID')
    API_HASH = environ.get('API_HASH')

    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEBUG = int(environ.get('MAIL_DEBUG'))

    telegram = Client("notify_bot", API_ID, API_HASH, bot_token=TELEGRAM_API_TOKEN)
    telegram.start()

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASS)
    pubsub = redis_client.pubsub()
    pubsub.subscribe(CHANNEL)

    for message in pubsub.listen():
        if message['data'] != 1:
            print(datetime.now(), 'Found new message')
            match = re.search(r'(.*)1#2#3(.*)1#2#3(.*)', message["data"].decode("utf-8"))
            TYPE = match.group(1)
            DEST = match.group(2)
            MESSAGE = match.group(3)
            print('APP: send_notification; ' + 'TYPE: ' + TYPE + '; DEST: ' + DEST + '; MESSAGE: ' + MESSAGE)

            if TYPE == 'telegram':
                try:
                    telegram.send_message(int(DEST), MESSAGE)
                except KeyError as e:
                    print('APP: send_notification; ' + 'KeyError', e)
                except pyrogram.errors.exceptions.bad_request_400.MessageEmpty as e:
                    print('APP: send_notification; ' + 'bad_request_400.MessageEmpty', e)

            if TYPE == 'email':
                print('TYPE: ', TYPE)
                msg = EmailMessage()
                msg['Subject'] = 'NOTIFICATION SERVICE'
                msg['From'] = MAIL_USERNAME
                msg['To'] = DEST
                msg.set_content(MESSAGE)
                with smtplib.SMTP(host=MAIL_SERVER, port=MAIL_PORT) as smtp:
                    smtp.set_debuglevel(MAIL_DEBUG)
                    smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
                    smtp.starttls(keyfile=None, certfile=None, context=None)
                    smtp.send_message(msg)

except AttributeError as e:
    print('APP: send_notification; ', e)
