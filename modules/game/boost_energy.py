import asyncio
from random import randint
from modules.starter.starter import client, hero, const
from modules.game.movement import do_move
from modules.utils.script_tools import change_status


async def drink_energy(text):
    i_text = text.split('Интоксикация: ')[1].split('\n')[0]
    intox = int(i_text.split('/')[1]) - int(i_text.split('/')[0])
    print(intox)
    if intox <= 100:
        hero["hero"]['intox'] = True
        print('going to farm prof')
        hero['state'] = 'going to prof'
        await change_status("Иду на профу")
        await asyncio.sleep(randint(2, 5))
        await client.send_message(const["game"], '🗺 Локации')
    if hero["hero"]['intox'] is False and 'Зелье Энергии' in text:
        await asyncio.sleep(randint(2, 5))
        if 'III Среднее Зелье Энергии' in text:
            await client.send_message(const["game"], '/use_potion_4019')
        elif 'Зелье Энергии +⚡️5' in text:
            await client.send_message(const["game"], '/use_potion_4009')
        elif 'II Слабое Зелье Энергии' in text:
            await client.send_message(const["game"], '/use_potion_4018')
        elif 'I Бракованное Зелье Энергии' in text:
            await client.send_message(const["game"], '/use_potion_4017')
        await change_status("Ухожу из города")
        await asyncio.sleep(randint(2, 7))
        hero['state'] = 'going to farm'
        await do_move()
    elif 'Зелье Энергии' not in text:
        await client.send_message('me', 'Зелья энергии кончились, режим **boost** сменился на **farm**')
        hero['mode'] = 'farm'
    else:
        await change_status("Интокс, жду энку")
