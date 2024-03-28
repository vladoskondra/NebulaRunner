import asyncio
from _datetime import datetime
from random import randint
from telethon import events
from modules.starter.starter import hero, const
from modules.utils import time_handler
from modules.game.movement import do_move
from modules.game.captcha import solve_captcha
from modules.game.grind import mob_farm
from modules.game.dungeon import dungeon_handler
from modules.game.energy_update import energy_full, energy_plus
from modules.peh.peh import peh_runner
from modules.game.hero_handler import update_hero_from_game
from modules.cosmos.cosmos_handler import cosmos


full_energy_list = ['🌏 Сервер был перезапущен.\n\n⚡️ Энергия восполнена',
                    '⚡️ Энергия восстановлена до максимума!',
                    'Вы восполнили энергию!']


@events.register(events.NewMessage(chats=const["game"], from_users=const["game"]))
async def game_handler(event):
    message = event.message
    text = message.message
    msg_id = message.id
    now = datetime.now()
    time_handler.get_day_or_night(now)
    time_handler.is_prof_time(now)
    # print(event)
    if not text.startswith('👥 '):
        # CAPTCHA TO SOLVE
        if 'Дла этого нажмите на' in text:
            await solve_captcha(event)
        elif 'Нажмите "' in text:
            await asyncio.sleep(randint(1, 4))
            await event.click(0)
        # CAPTCHA SOLVED
        if 'Проверка прошла' in text:
            await asyncio.sleep(randint(2, 7))
            await do_move()
        # UPDATE HERO INFO
        if '🧬 Cимуляция №: ' in text or all(x in text for x in ['🧬: ', '📟: /profilesize']):
            await update_hero_from_game(text)
        # INTOX REFRESH
        if 'Интоксикация восстановлена!' in text and hero["hero"]['intox'] is True:
            hero["hero"]['intox'] = False
        # ENERGY UPDATE
        if any(fel in text for fel in full_energy_list):
            await energy_full(text)
        if '⚡️ +1 к энергии' in text:
            await energy_plus(text)
        if 'Вы прибыли ' in text:
            if 'Новый Эдем' in text:
                hero['cur_loc'] = '🌎 Новый Эдем'
            if 'Некрополис' in text:
                hero['cur_loc'] = '🏛 Некрополис'
        # GRIND MODE
        if hero['mode'] == 'farm' or hero['mode'] == 'boost':
            if hero["space"]['cosmos']:
                await cosmos(event)
            else:
                await mob_farm(event)
        # PEH MODE
        elif hero['mode'] == 'peh':
            await peh_runner(text)
        # DUNGEON MODE || UNDER CONSTRUCT ||
        elif hero['mode'] == 'dg':
            await dungeon_handler(event)
