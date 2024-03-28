import asyncio
from random import randint
from modules.starter.starter import client, hero, const
from modules.game.movement import do_move
from modules.utils.script_tools import change_status


async def energy_full(text):
    if not hero['space']['cosmos']:
        if 'Вы восполнили энергию!' in text:
            hero["hero"]['energy'] = int(text.split('Энергия: ')[1].split('/')[0])
            i_text = text.split('Интоксикация: ')[1]
            intox = int(i_text.split('/')[1]) - int(i_text.split('/')[0])
            print(intox)
            if intox <= 100:
                hero["hero"]['intox'] = True
            else:
                print('no intox, going to move')
                await change_status("Собираюсь двигаться")
                await asyncio.sleep(randint(2, 15))
                # await do_move()
        elif 'Сервер был перезапущен' in text and hero['state'] != 'none':
            hero["hero"]['energy'] = 5
            hero["hero"]['intox'] = False
            await asyncio.sleep(randint(60, 120))
            if hero['state'] == 'prof':
                hero['state'] = 'going home'
                await asyncio.sleep(randint(2, 5))
                await client.send_message(const["game"], '🔙 Назад')
                await asyncio.sleep(randint(2, 5))
                if hero["general_cfg"]['edem'] is False:
                    await client.send_message(const["game"], '🏛 Некрополис')
                else:
                    await client.send_message(const["game"], '🌎 Новый Эдем')
            else:
                await client.send_message(const["game"], const["last_action"])
        else:
            hero["hero"]['energy'] = 5
            if hero['state'] == 'prof':
                hero['state'] = 'going home'
                await asyncio.sleep(randint(2, 5))
                await client.send_message(const["game"], '🔙 Назад')
                await asyncio.sleep(randint(2, 5))
                if hero["general_cfg"]['edem'] is False:
                    await client.send_message(const["game"], '🏛 Некрополис')
                    const["last_action"] = '🏛 Некрополис'
                else:
                    await client.send_message(const["game"], '🌎 Новый Эдем')
                    const["last_action"] = '🌎 Новый Эдем'
                hero['state'] = 'to home'
                await change_status("Иду домой")
            elif hero['state'] == 'healed' and const["day_or_night"] == 'night' and (
                    hero['mode'] == 'farm' or hero['mode'] == 'boost'):
                await asyncio.sleep(randint(30, 125))
                await change_status("Ухожу из города")
                await do_move()
            elif hero['state'] == 'healed' and const["day_or_night"] == 'day' and (
                    hero['mode'] == 'farm' or hero['mode'] == 'boost'):
                await asyncio.sleep(randint(2, 15))
                await change_status("Ухожу из города")
                await do_move()


async def energy_plus(text):
    hero["hero"]['energy'] = int(text.split(' (')[1].split('/')[0])
    if not hero['space']['cosmos']:
        if hero['state'] == 'prof' and (hero['mode'] == 'farm' or hero['mode'] == 'boost') and hero["hero"][
            'energy'] >= 4 and const["fish_timer"] is False:
            hero['state'] = 'going home'
            await asyncio.sleep(randint(2, 5))
            await client.send_message(const["game"], '🔙 Назад')
            await asyncio.sleep(randint(2, 5))
            if hero["general_cfg"]['edem'] is False:
                await client.send_message(const["game"], '🏛 Некрополис')
                const["last_action"] = '🏛 Некрополис'
            else:
                await client.send_message(const["game"], '🌎 Новый Эдем')
                const["last_action"] = '🌎 Новый Эдем'
            await change_status("Иду домой")
            hero['state'] = 'to home'
        if hero['state'] == 'healed' and const["day_or_night"] == 'day' and (hero['mode'] == 'farm' or hero['mode'] == 'boost'):
            await asyncio.sleep(randint(2, 15))
            await change_status("Ухожу из города")
            await do_move()
