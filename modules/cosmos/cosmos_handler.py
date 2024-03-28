import asyncio
import math
from random import randint
from modules.starter.starter import client, hero, const
from modules.game.fight_sim import fight_simulation
from telethon.tl.types import ReplyKeyboardMarkup
from modules.cosmos.galaxy_gps import galaxy_gps, get_planet_seq
from modules.cosmos.planet_seek_mob import seek_mob
from modules.cosmos.planet_seek_prof import seek_prof
from modules.cosmos.planet_seek_ship import seek_ship
from modules.game.after_fight import after_fight
from modules.utils.files import update_file
from modules.utils.script_tools import change_status

ship_modules_list = ['🛫 Взлетный Ускоритель: ', '✈️ Импульсный Двигатель: ', '☄️ Гипердвигатель: ',
                     '🏥 Система Исцеления: ', '🧿 Планетарный сканер: ', '👀 Модуль Элементального Видения: ',
                     '🪪 Имя: ', '🚀 Модель: ', '🧩 Тип: ', '🏅 Класс: ']
full_energy_list = ['🌏 Сервер был перезапущен.\n\n⚡️ Энергия восполнена',
                    '⚡️ Энергия восстановлена до максимума!',
                    'Вы восполнили энергию!']


async def cosmos(event):
    message = event.message
    text = message.text
    buttons = []
    if hasattr(message, 'reply_markup') and type(message.reply_markup) == ReplyKeyboardMarkup:
        buttons = message.reply_markup
    if any(fel in text for fel in full_energy_list):
        await asyncio.sleep(randint(1, 3))
        hero['state'] = 'map seeker'
        await client.send_message(const['game'], '🗺 Исследовать')
    if '⚠️ В импульсном двигателе нет топлива' in text:
        await asyncio.sleep(randint(1, 3))
        await client.send_message(const['game'], '🚀 Корабль')
        hero['state'] = 'ship needs impulse'
    if '🛠 Инженерный мостик.\n\n' in text:
        msg_id = message.id
        if int(text.split('🛫 Взлетный Ускоритель: ⛽️ ')[1].split('/')[0]) == 0:
            hero['state'] = 'ship needs takeoff'
        elif int(text.split('✈️ Импульсный Двигатель: 🎇 ')[1].split('/')[0]) == 0:
            hero['state'] = 'ship needs impulse'
        await event.click(text='🧯 Использовать топливо')
        await asyncio.sleep(1)
        new_msg = await client.get_messages(const['game'], ids=msg_id)
        buttons_list = []
        buttons_rows = new_msg.reply_markup.rows
        for row in buttons_rows:
            bts = row.buttons
            for b in bts:
                buttons_list.append(b.text)
        f_button = ''
        if hero['state'] == 'ship needs takeoff' and any(x.split('(')[0] == '⛽️ Взлетное топливо ' for x in buttons_list):
            f_button = next(b for b in buttons_list if b.split('(')[0] == '⛽️ Взлетное топливо ')
        elif hero['state'] == 'ship needs impulse' and any(x.split('(')[0] == '🎇 Импульсное топливо ' for x in buttons_list):
            f_button = next(b for b in buttons_list if b.split('(')[0] == '🎇 Импульсное топливо ')
        await new_msg.click(text=f_button)
        hero['state'] = 'ready to go space'
        await asyncio.sleep(randint(1, 3))
        await client.send_message(const['game'], '/buttons')
    if all(x in text for x in ship_modules_list) and hero['state'].startswith('ship needs '):
        await asyncio.sleep(randint(1, 3))
        await event.click(0)
    if hero['cur_loc'] == '🌎 Новый Эдем':
        if 'Выберите локацию' in text:
            await asyncio.sleep(randint(1, 5))
            await client.send_message(const['game'], '🚅 Воздушный Порт')
        if '🚈 Вы прибыли в воздушный порт' in text:
            await asyncio.sleep(randint(1, 3))
            await client.send_message(const['game'], '🚀 Космодром - Ω-1')
        if 'Путь А.Т.Л.А.С.-а ждет вас' in text:
            await asyncio.sleep(randint(1, 3))
            await client.send_message(const['game'], '🔥 Старт')
        if '🛰 Вы на орбите' in text:
            await asyncio.sleep(randint(1, 3))
            await event.click(text='🌌 Космос')
            hero['cur_loc'] = '🌌 Космос'
            hero["space"]['space_seq'] = 'A0'
    if hero['cur_loc'] == '🌌 Космос' and buttons:
        buttons_list = []
        buttons_rows = buttons.rows
        # print(buttons_rows)
        for row in buttons_rows:
            bts = row.buttons
            for b in bts:
                buttons_list.append(b.text)
        print(buttons_list)
        if any(x.split(' ')[0] in ['↖️', '⬆️', '↗️', '↙️', '⬇️', '↘️'] for x in buttons_list):
            await asyncio.sleep(randint(1, 3))
            path = galaxy_gps()
            if path == 'Done':
                await event.click(text='🌏 Орбита')
                hero['state'] = 'landing'
            elif len(path) > 1:
                path_dir = next(p for p in buttons_list if path[1] in p)
                await event.click(text=path_dir)
            # hero['space_seq'] = path[1]
    if text.startswith('🛰 ') and '☣️ Тип: ' in text and '🌎 Вид: ' in text and hero['state'] != 'after fight':
        planet_name = text.split('🛰 ')[1].split('\n\n')[0].split('**')[1]
        hero['cur_loc'] = planet_name
        planet_seq = get_planet_seq(planet_name)
        hero['space']['space_seq'] = planet_seq
        # hero['state'] = 'map seeker'
    if '🛰️ Вы направляетесь в сектор ' in text:
        hero["space"]['space_seq'] = text.split(' в сектор ')[1].split('.')[0]
    if '🛰 Вы на орбите планеты ' in text and hero['state'] == 'landing':
        await asyncio.sleep(randint(1, 3))
        await event.click(text='🌏 Посадка')
    if '🌏 Вы приземлились на планету ' in text:
        hero['cur_loc'] = text.split('🌏 Вы приземлились на планету ')[1].split('.')[0]
        hero['state'] = 'map seeker'
        await asyncio.sleep(randint(1, 3))
        await event.click(text='🗺 Исследовать')
    if '+1 к энергии (4/5)' in text:
        hero['state'] = 'map seeker'
        await asyncio.sleep(randint(1, 3))
        await event.click(text='🗺 Исследовать')
    if ('🌐 Защита От Вредных Факторов:\n' in text or '🌬 Система Жизнеобеспечения:\n' in text) \
            and '- Уровень заряда модуля экзоскелета достиг значения 20 или ниже. ' \
                'Используйте топливо или замените модуль, чтобы избежать ' in text:
        await asyncio.sleep(randint(1, 3))
        if '🌬 Система Жизнеобеспечения:\n' in text:
            await client.send_message(const['game'], '/fuel_oxy')
        elif '🌐 Защита От Вредных Факторов:\n' in text:
            await client.send_message(const['game'], '/fuel_def')
    if 'Вы можете пополнить заряд' in text:
        await asyncio.sleep(randint(1, 3))
        buttons_list = []
        buttons_rows = message.reply_markup.rows
        for row in buttons_rows:
            bts = row.buttons
            for b in bts:
                if ' (🎒' in b.text and int(b.text.split(' (🎒')[1].split(')')[0]) > 15:
                    buttons_list.append(b.text)
        print(f'buttons_list oxy: {buttons_list}')
        if buttons_list:
            print(f'clicking: {buttons_list[0]}')
            await event.click(text=buttons_list[0])
        else:
            hero['mode'] = 'stop'
            await client.send_message('me', '(🌬/🌐) Закончился кислород или защита. Бот поставлен на паузу.')
    if ('🌐 Защита От Вредных Факторов:\n' in text or '🌬 Система Жизнеобеспечения:\n' in text) \
            and '🚀 Система обнаружения угроз корабля ' in text \
            and 'разряжена. Шлюз не был открыт, так как в противном случае Вы умрете' in text:
        await asyncio.sleep(randint(1, 3))
        if '🌬 Система Жизнеобеспечения:\n' in text:
            await client.send_message(const['game'], '/fuel_oxy')
        elif '🌐 Защита От Вредных Факторов:\n' in text:
            await client.send_message(const['game'], '/fuel_def')
    # if '🚀 Система Исцеления корабля' in text and '- Началась регенерация здоровья' in text:
    #     hero['state'] = 'restore hp near ship'
    if '🚀 Система Исцеления корабля:\n- Регенерация здоровья завершена.' in text:
        hero["hero"]['cur_hp'] = hero["hero"]['max_hp']
        hero['state'] = 'map seeker'
        await asyncio.sleep(randint(3, 5))
        await client.send_message(const['game'], '🗺 Исследовать')
    if text.startswith('❤️ HP: ') and ' /mapSize /mType /cruiseOn' in text \
            and hero['state'] in ['map seeker', 'back to ship']:
        print(f"Got map, current status: {hero['state']}")
        await asyncio.sleep(randint(1, 3))
        if hero["space"]['planet_size'] == 0:
            await client.send_message(const['game'], '/mapSize')
            await asyncio.sleep(1)
            new_msg = await client.get_messages(const['game'], limit=1)
            buttons_list = []
            buttons_rows = new_msg[0].reply_markup.rows
            for row in buttons_rows:
                bts = row.buttons
                for b in bts:
                    buttons_list.append(b.text)
            hero["space"]['planet_size'] = int(buttons_list[1])
            await asyncio.sleep(randint(1, 3))
            await new_msg[0].click(text='✅ Завершить')
        else:
            const['space_map_msg'] = message.id
            my_pos = ((hero["space"]['planet_size'] - 1) / 2, (hero['space']['planet_size'] - 1) / 2)
            target = (math.inf, math.inf)
            if hero['state'] == 'back to ship':
                print('ready to back to ship')
                while target != my_pos:
                    new_msg = await client.get_messages(const['game'], ids=const['space_map_msg'])
                    text = new_msg.message
                    target = await seek_ship(text, target, my_pos)
            elif hero['state'] == 'map seeker':
                win_chance = await fight_simulation()
                if hero["hero"]['energy'] > 0:
                    if win_chance >= 100:
                        target = await seek_mob(text, target, my_pos)
                    else:
                        hero['state'] = 'back to ship'
                        while target != my_pos:
                            new_msg = await client.get_messages(const['game'], ids=const['space_map_msg'])
                            text = new_msg.message
                            target = await seek_ship(text, target, my_pos)
                elif hero["hero"]['energy'] == 0 and hero['mode'] == 'boost' and hero["hero"]['intox'] is False:
                    if win_chance >= 100:
                        await asyncio.sleep(randint(2, 7))
                        await client.send_message(const["game"], '/potions')
                        await asyncio.sleep(randint(2, 7))
                        target = await seek_mob(text, target, my_pos)
                    else:
                        hero['state'] = 'back to ship'
                        while target != my_pos:
                            target = await seek_ship(text, target, my_pos)
                elif hero["hero"]['energy'] == 0 and (hero['mode'] == 'farm' or hero["hero"]['intox'] is True):
                    print('going to farm prof')
                    hero['state'] = 'going to farm prof'
                    await change_status("Иду на профу")
                    await asyncio.sleep(randint(2, 5))
                    target = await seek_prof(text, target, my_pos)
            if type(target) == list and target[0] == 'No path':
                path = target[1]
                await client.send_message(const['game'], path[0])
                await asyncio.sleep(randint(3, 5))
                await client.send_message(const['game'], '🗺 Исследовать')
            elif target == my_pos and hero['state'] != 'back to ship':
                await asyncio.sleep(1)
                new_msg = await client.get_messages(const['game'], ids=const['space_map_msg'])
                text = new_msg.message

                hero['state'] = 'ready to action'
                await asyncio.sleep(1)
                await client.send_message(const['game'], '🚀⚔️🏔️')
    if '🧬 Ваше здоровье: ' in text and '🕹 Выберите действие?' in text and hero['state'] == 'ready to action':
        hero["hero"]['cur_hp'] = int(text.replace('💔', '').replace('❤️', '').split('🧬 Ваше здоровье: ')[1].split('/')[0])
        await asyncio.sleep(randint(1, 3))
        if hero["hero"]['cur_hp'] < hero['hero']['max_hp'] and hero['farm_cfg']['force_heal'] and hero['space']['cosmos']:
            hero['state'] = 'back to ship'
            await client.send_message(const['game'], '🗺 Исследовать')
        else:
            target_mob_lvl = int(text.split('Ур:')[1].split(' ')[0])
            win_chance = await fight_simulation(optional_mob=target_mob_lvl)
            if win_chance >= 100 and hero["hero"]['energy'] > 0:
                print(f'Can still fight with chance of {win_chance}')
                await change_status(f"Готов бить, шанс на успех: {win_chance}")
                hero['state'] = 'starts fight'
                await event.click(0)
            elif win_chance >= 99.5 and hero["hero"]['energy'] == 0 and hero['mode'] == 'boost' and not hero["hero"]['intox']:
                await client.send_message(const["game"], '/potions')
            else:
                hero['state'] = 'back to ship'
                await client.send_message(const['game'], '🗺 Исследовать')
    if 'Вы вступаете в бой с:' in text:
        hero['state'] = 'after fight'
        print(f'going to AFTER FARM, status cur: {hero["state"]}')
        await after_fight(text)
    if '⏱️ Размер: ' in text and '🔫 Мультитул:' in text and '👥 Пилотов:' in text:
        await asyncio.sleep(1)
        await event.click(0)
    if '⚠️ Ресурс истощен, расщепление остановлено' in text:
        print('Prof resource is empty, looking for new one')
        await asyncio.sleep(randint(1, 3))
        hero['state'] = 'map seeker'
        await client.send_message(const['game'], '🗺 Исследовать')
    if '⚠️ Произошла ошибка' in text and 'Too Many Requests: retry after' in text:
        prev_state = hero['state']
        hero['state'] = 'waiting for error'
        time_to_wait = int(text.split('Too Many Requests: retry after ')[1].split('.')[0])
        await asyncio.sleep(time_to_wait)
        hero['state'] = prev_state
        await client.send_message(const['game'], '🗺 Исследовать')

    update_file('hero', hero)
