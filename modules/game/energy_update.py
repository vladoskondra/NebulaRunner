import asyncio
from random import randint
from modules.starter.starter import client, hero, const
from modules.game.movement import do_move


async def energy_full(text):
    if 'Вы восполнили энергию!' in text:
        hero['energy'] = int(text.split('Энергия: ')[1].split('/')[0])
        i_text = text.split('Интоксикация: ')[1]
        intox = int(i_text.split('/')[1]) - int(i_text.split('/')[0])
        print(intox)
        if intox <= 100:
            hero['intox'] = True
        else:
            print('no intox, going to move')
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Собираюсь двигаться")
            await asyncio.sleep(randint(2, 15))
            # await do_move()
    elif 'Сервер был перезапущен' in text and hero['state'] != 'none':
        hero['energy'] = 5
        hero['intox'] = False
        await asyncio.sleep(randint(60, 120))
        if hero['state'] == 'prof':
            hero['state'] = 'going home'
            await asyncio.sleep(randint(2, 5))
            await client.send_message(const["game"], '🔙 Назад')
            await asyncio.sleep(randint(2, 5))
            if hero['edem'] is False:
                await client.send_message(const["game"], '🏛 Некрополис')
            else:
                await client.send_message(const["game"], '🌎 Новый Эдем')
        else:
            await client.send_message(const["game"], const["last_action"])
    else:
        hero['energy'] = 5
        if hero['state'] == 'prof':
            hero['state'] = 'going home'
            await asyncio.sleep(randint(2, 5))
            await client.send_message(const["game"], '🔙 Назад')
            await asyncio.sleep(randint(2, 5))
            if hero['edem'] is False:
                await client.send_message(const["game"], '🏛 Некрополис')
                const["last_action"] = '🏛 Некрополис'
            else:
                await client.send_message(const["game"], '🌎 Новый Эдем')
                const["last_action"] = '🌎 Новый Эдем'
            hero['state'] = 'to home'
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Иду домой")
        elif hero['state'] == 'healed' and const["day_or_night"] == 'night' and (
                hero['mode'] == 'farm' or hero['mode'] == 'boost'):
            await asyncio.sleep(randint(30, 125))
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Ухожу из города")
            await do_move()
        elif hero['state'] == 'healed' and const["day_or_night"] == 'day' and (
                hero['mode'] == 'farm' or hero['mode'] == 'boost'):
            await asyncio.sleep(randint(2, 15))
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Ухожу из города")
            await do_move()


async def energy_plus(text):
    hero['energy'] = int(text.split(' (')[1].split('/')[0])
    if hero['state'] == 'prof' and (hero['mode'] == 'farm' or hero['mode'] == 'boost') and hero[
        'energy'] >= 4 and const["fish_timer"] is False:
        hero['state'] = 'going home'
        await asyncio.sleep(randint(2, 5))
        await client.send_message(const["game"], '🔙 Назад')
        await asyncio.sleep(randint(2, 5))
        if hero['edem'] is False:
            await client.send_message(const["game"], '🏛 Некрополис')
            const["last_action"] = '🏛 Некрополис'
        else:
            await client.send_message(const["game"], '🌎 Новый Эдем')
            const["last_action"] = '🌎 Новый Эдем'
        await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Иду домой")
        hero['state'] = 'to home'
    if hero['state'] == 'healed' and const["day_or_night"] == 'day' and (hero['mode'] == 'farm' or hero['mode'] == 'boost'):
        await asyncio.sleep(randint(2, 15))
        await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Ухожу из города")
        await do_move()
