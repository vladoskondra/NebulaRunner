import asyncio
from random import randint
from modules.starter.starter import client, hero, const
from modules.game.movement import do_move
from modules.game.healing import do_heal
from modules.game.farm_resources import farm_prof
from modules.game.boost_energy import drink_energy
from modules.game.after_fight import after_fight


async def mob_farm(event):
    message = event.message
    text = message.text
    if '🏛 Некрополис.\n🏕 Выберите локацию:' in text or '🏞 Выберите локацию:' in text:
        if hero['state'] == 'ready to leave Town' or hero['state'] == 'going to farm':
            print(f'Going to farm loc')
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Иду фармить")
            await asyncio.sleep(randint(2, 7))
            await client.send_message(const["game"], hero["farm_cfg"]['farm_loc'])
            const["last_action"] = hero["farm_cfg"]['farm_loc']
        elif hero['state'] == 'going to prof':
            if hero["general_cfg"]['edem'] is True:
                await asyncio.sleep(randint(2, 4))
                await client.send_message(const["game"], '🔙 Вернуться')
                await asyncio.sleep(randint(2, 4))
                await client.send_message(const["game"], '🏙 Дистрикты')
            print(f'Going to prof loc')
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Иду на профу!")
            await asyncio.sleep(randint(2, 7))
            await client.send_message(const["game"], hero["prof_cfg"]['prof_loc'])
            const["last_action"] = hero["prof_cfg"]['prof_loc']
    elif '🛠 Произведена диагностика и устранение неисправностей. Все показатели в норме.' in text:
        hero['state'] = 'healed'
        hero["hero"]['cur_hp'] = hero["hero"]['max_hp']
        # DAY TIME
        if hero["hero"]['energy'] > 0:
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Ухожу из города")
            print(f'Ready to move')
            hero['state'] = 'going to farm'
            await asyncio.sleep(randint(2, 7))
            await do_move()
        elif hero["hero"]['energy'] == 0 and hero['mode'] == 'boost' and hero["hero"]['intox'] is False:
            # TODO: Drink boost energy
            await asyncio.sleep(randint(2, 7))
            await client.send_message(const["game"], '/potions')
        elif hero["hero"]['energy'] == 0 and (hero['mode'] == 'farm' or hero["hero"]['intox'] is True):
            print('going to farm prof')
            hero['state'] = 'going to prof'
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Иду на профу")
            await asyncio.sleep(randint(2, 5))
            await client.send_message(const["game"], '🗺 Локации')
            const["last_action"] = '🗺 Локации'
    elif '🧪 Зелья:' in text and '🎒 Инвентарь:' in text and hero['mode'] == 'boost' and hero["hero"]['intox'] is False:
        await drink_energy(text)
    elif '🏛 Вы прибыли в Некрополис' in text or 'Сознание загружено в хост' in text or \
            ('Вы прибыли в Новый Эдем' in text and hero["general_cfg"]['edem'] is True):
        hero['loc'] = 'Town'
        hero['state'] = 'waiting for heal'
        print(f'Going to heal')
        await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Хилюсь")
        await asyncio.sleep(randint(2, 15))
        await do_heal()
    elif 'Вы направляетесь в ' in text:
        if hero["farm_cfg"]['farm_loc'] in text:
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Иду на фарм")
            hero['state'] = 'going to farm loc'
        elif 'Некрополис' in text:
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Иду домой")
            hero['state'] = 'going to home'
        elif 'Новый Эдем' in text and hero["general_cfg"]['edem'] is True:
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Иду домой")
            hero['state'] = 'going to home'
    elif 'Вы прибыли в ' in text and hero["farm_cfg"]['farm_loc'].split(hero["farm_cfg"]['farm_loc'].split(' ')[0])[1] in text:
        hero['loc'] = hero["farm_cfg"]['farm_loc']
        hero['state'] = 'in farming loc'
        print(f'Going to farm')
        await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Атакую моба")
        await asyncio.sleep(randint(2, 15))
        await event.message.click(0)
    elif 'Вы прибыли в ' in text and hero["prof_cfg"]['prof_loc'].split(hero["prof_cfg"]['prof_loc'].split(' ')[0])[1] in text and \
            hero['state'] == 'going to prof':
        hero['loc'] = hero["prof_cfg"]['prof_loc']
        hero['state'] = 'prof'
        print(f'Going to farm')
        await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Пришел в локу профы")
        await asyncio.sleep(randint(2, 5))
        await farm_prof()
    elif 'Выберите действие?' in text and hero['state'] == 'in farming loc':
        print(f'Going to fight')
        await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\nСтатус: Бью моба")
        await asyncio.sleep(randint(2, 5))
        await event.message.click(0)
    elif 'Вы вступаете в бой с' in text and hero['state'] == 'in farming loc':
        print(f'Going to home')
        await after_fight(text)
    elif '🔫 У вас обнаружен мультитул' in text and hero['state'] == 'prof':
        if hero["prof_cfg"]['multitool']:
            await event.click(0)
        else:
            await event.click(1)
