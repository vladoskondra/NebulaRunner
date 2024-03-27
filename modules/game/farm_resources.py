import asyncio
from random import randint
from modules.starter.starter import client, hero, const
from modules.utils.script_tools import change_status

game = const['game']


async def farm_prof():
    if not hero["space"]['cosmos']:
        if hero["prof_cfg"]['prof_loc'] == '🏝 Побережье Карха':
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '⚓️ Пирс')
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '🎣 Рыбачить')
            const["last_action"] = '🎣 Рыбачить'
        elif hero["prof_cfg"]['prof_loc'] == '🌳 Лес Предтеч':
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '🏕 Лесничество')
            await asyncio.sleep(randint(1, 4))
            if hero["prof_cfg"]['prof'] == 'лес':
                await client.send_message(game, '🪓 Добыча дерева')
                const["last_action"] = '🪓 Добыча дерева'
            elif hero["prof_cfg"]['prof'] == 'трава':
                await client.send_message(game, '🌱 Сбор растений')
                const["last_action"] = '🌱 Сбор растений'
        elif hero["prof_cfg"]['prof_loc'] == '🧊 Кварцевое Плато':
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '🏗 Шахта')
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '⛏ Добывать')
            const["last_action"] = '⛏ Добывать'
        elif hero["prof_cfg"]['prof_loc'] == '🌉 Дистрикт Вайресс':
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '⚓️ Берег')
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '🎣 Рыбачить')
            const["last_action"] = '🎣 Рыбачить'
        elif hero["prof_cfg"]['prof_loc'] == '🌃 Дистрикт Аппалачи':
            await asyncio.sleep(randint(1, 4))
            if hero["prof_cfg"]['prof'] == 'лес':
                await client.send_message(game, '🪵 Лесопосадка')
                await asyncio.sleep(randint(1, 4))
                await client.send_message(game, '🪓 Добыча дерева')
                const["last_action"] = '🪓 Добыча дерева'
            elif hero["prof_cfg"]['prof'] == 'камень':
                await client.send_message(game, '🏗 Карьер')
                await asyncio.sleep(randint(1, 4))
                await client.send_message(game, '⛏ Добывать')
                const["last_action"] = '⛏ Добывать'
        elif hero["prof_cfg"]['prof_loc'] == '🌇 Дистрикт Древних':
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '🏕 Луга')
            await asyncio.sleep(randint(1, 4))
            await client.send_message(game, '🌱 Сбор растений')
            const["last_action"] = '🌱 Сбор растений'
        await change_status("Добываю ресурсы")
        hero['state'] = 'prof'
