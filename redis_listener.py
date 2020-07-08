#!/usr/bin/python3
from pyrogram import Client
import redis

TELEGRAM_API_TOKEN = 'blablablabla'
API_HASH = 'blablabla'
API_ID = 34534523
CHAT_ID = -345345234234234
CHANNEL = 'zabbix'

app = Client("notify_bot", API_ID, API_HASH, bot_token=TELEGRAM_API_TOKEN)
app.start()

redis_client = redis.Redis(host='localhost', port=6379, db=0, password='oozee4ad')
pubsub = redis_client.pubsub()
pubsub.subscribe(CHANNEL)
for message in pubsub.listen():
    if message['data'] != 1:
        app.send_message(CHAT_ID, message["data"].decode("utf-8"))
