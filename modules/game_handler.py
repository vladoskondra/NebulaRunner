import asyncio
from _datetime import datetime
from random import randint
from telethon import events
from modules.starter.starter import hero, const
from modules.utils import time_handler
from modules.game.movement import do_move
from modules.utils.files import *
from modules.game.captcha import solve_captcha
from modules.game.grind import mob_farm
from modules.game.dungeon import dungeon_handler
from modules.game.energy_update import energy_full, energy_plus
from modules.peh.peh import peh_runner


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
        if '🧬 Cимуляция №: ' in text:
            hero['name'] = text.split('📝 Имя: ')[1].split('\n')[0]
            hero['cur_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[0])
            hero['max_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[1].split('\n')[0])
            hero['lvl'] = int(text.split('🏅 Уровень: ')[1].split(' 💠 ')[0])
            hero['energy'] = int(text.split('⚡️ Энергия: ')[1].split('/')[0])
            update_file('hero', hero)
        # INTOX REFRESH
        if 'Интоксикация восстановлена!' in text and hero['intox'] is True:
            hero['intox'] = False
        # ENERGY UPDATE
        elif any(fel in text for fel in full_energy_list):
            await energy_full(text)
        elif '⚡️ +1 к энергии' in text:
            await energy_plus(text)
        # GRIND MODE
        if hero['mode'] == 'farm' or hero['mode'] == 'boost':
            await mob_farm(event)
        # PEH MODE
        elif hero['mode'] == 'peh':
            await peh_runner(text)
        # DUNGEON MODE || UNDER CONSTRUCT ||
        elif hero['mode'] == 'dg':
            await dungeon_handler(event)
