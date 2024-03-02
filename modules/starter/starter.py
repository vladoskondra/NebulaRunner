import git
from telethon import TelegramClient
from modules.utils.files import *


# repo = git.Repo("./.git", search_parent_directories=True)
# status = repo.git.status()
# print(status)
# for x in repo.index.diff("HEAD"):
#     # Just print
#     print(x)
print('UPDATED')
# if len(diff) != 0:
#     print('Обнаружена новая версия скрипта, обновляю!')
# git.Repo('.git').remote().pull()
# repo.git.stash('drop')
#     input('Скрипт обновлен, перезапусти скрипт... ')
# else:
#     print('Скрипт последней версии')

hero = read_file('hero')

const = {
    "last_action": '',
    "msg_status": None,
    "orig_msg_status": '',
    "game": 'OrionNebulaBot',
    "day_or_night": 'day',
    "fish_timer": False,
    "peh_list": [],
    "pin_point": ''
}

config = read_file('config')
while config['api_id'] == 0 or config['api_hash'] == '':
    if config['api_id'] == 0:
        inp = input('Введи App api_id: ')
        config['api_id'] = int(inp)
    if config['api_hash'] == '':
        inp = input('Введи App api_hash: ')
        config['api_hash'] = inp
    update_file('config', config)
if config['api_id'] != 0 or config['api_hash'] != '':
    if config['password'] == '-':
        pw_inp = input('На аккаунте установлен пароль? (Y/n) ')
        while pw_inp not in ['Y', 'n']:
            pw_inp = input('Неверный синтаксис! Отправь "Y" — если установлен пароль, либо "n" — если пароля нет.\nОтвет: (Y/n) ')
        if pw_inp == 'n':
            config['password'] = None
        elif pw_inp == 'Y':
            inp = input('Укажи пароль (он будет храниться локально только у тебя): ')
            config['password'] = inp
        update_file('config', config)
    client = TelegramClient('NebulaBot', config["api_id"], config["api_hash"], system_version="4.16.30-vxCUSTOM")


