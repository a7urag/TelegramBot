#coder :- Salman Faris

import sys
import os
import time
import telepot
import datetime
from subprocess import PIPE, Popen

DOWNLOADS_PATH = '/Downloads'

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def gitCommandHandler(command):
    params = command.split(' ')[1:]
    if params[0] == 'update':
        path = os.path.dirname(os.path.realpath(__file__))
        os.system('cd %s; git pull;' % path)
        return True
    return False


def torrentCommandHandler(command):
    params = command.split(' ')[1:]
    if params[0] == 'add':
        os.system('deluge console "add {} -p = {}; exit"'.format(params[1], DOWNLOADS_PATH))
        return True
    elif params[0] == 'show':
        files = [f for f in os.listdir(DOWNLOADS_PATH) if os.path.isfile(os.path.join(DOWNLOADS_PATH, f))]
        return files
    elif params[0] == 'current':
        return cmdline('deluge-console "info -v; exit;"')
    return False


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)
    bot.sendMessage(chat_id, "Acknowledged %s" %command)
    result = False
    if command.startswith('/'):
        if command.startswith('/git'):
            result = gitCommandHandler(command)
        elif command.startswith('/torrent'):
            result = torrentCommandHandler(command)
    if result:
        bot.sendMessage(chat_id, result)
    else:
        bot.sendMessage(chat_id, "Not a valid command")
token = os.getenv("TELEGRAM_TOKEN")
if token:
    bot = telepot.Bot(token)
    bot.message_loop(handle)
    print('Bot initiated at ', datetime.datetime.now())
else:
    print("Set TELEGRAM_TOKEN in env")
    exit()

while 1:
    try:
        time.sleep(10)
    
    except KeyboardInterrupt:
        print('\n Program interrupted')
        exit()
    
    except:
        print('Other error or exception occured!')
