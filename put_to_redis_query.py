#!/usr/bin/python3
import redis
import sys


if __name__ == '__main__':
    try:
        CHANNEL = 'zabbix'
        MESSAGE = sys.argv[1]
        redis_client = redis.Redis(host='localhost', port=6379, db=0, password='oozee4ad')
        redis_client.publish(CHANNEL, MESSAGE)
    except IndexError:
        print("\nNot enough args")
