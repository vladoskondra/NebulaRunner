import asyncio
from datetime import datetime, timedelta
from random import randint
from modules.starter.starter import client, hero, const
from modules.game.fight_sim import fight_simulation
from modules.utils.files import update_file

async def after_fight(text):
    hero["hero"]['energy'] = int(text.split('⚡️ Энергия: ')[1].split('/')[0])
    if 'Потерянный опыт' not in text:
        await asyncio.sleep(randint(2, 5))
        if f"{hero['hero']['name']}(❤️" in text:
            hero['hero']['cur_hp'] = int(text.split(f"{hero['hero']['name']}(❤️")[1].split('/')[0])
        elif f"{hero['hero']['name']}(💔" in text:
            hero['hero']['cur_hp'] = int(text.split(f"{hero['hero']['name']}(💔")[1].split('/')[0])
        print(hero['hero']['cur_hp'])
        win_chance = await fight_simulation()
        if win_chance >= 99.5 and hero['hero']['energy'] > 0:
            print(f'Can still fight with chance of {win_chance}')
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\n"
                                                                 f"Статус: Готов еще бить, шанс на успех: {win_chance}")
            if hero['space']['cosmos']:
                if not hero['space']['cosmos_farm_seek']:
                    now = datetime.now()
                    resp = now + timedelta(minutes=15)
                    resp_text = resp.strftime("%H:%M:%S")
                    await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\n"
                                                                         f"Статус: Жду реса моба в {resp_text}")
                    hero['state'] = 'waiting for mob res'
                    await asyncio.sleep(15*60)
                    hero['state'] = 'map seeker'
                await client.send_message(const['game'], '🗺 Исследовать')
            else:
                await client.send_message(const["game"], '👀 Осмотреть местность')
        else:
            await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\n"
                                                                 f"Статус: Собираюсь домой")
            if hero['space']['cosmos']:
                hero['state'] = 'back to ship'
                await client.send_message(const['game'], '🗺 Исследовать')
            elif hero["general_cfg"]['edem'] is False:
                await client.send_message(const["game"], '🏛 Некрополис')
                const["last_action"] = '🏛 Некрополис'
                hero['state'] = 'to home'
            else:
                await client.send_message(const["game"], '🌎 Новый Эдем')
                const["last_action"] = '🌎 Новый Эдем'
                hero['state'] = 'to home'
    else:
        await client.edit_message('me', const["msg_status"], f"{const['orig_msg_status']}\n\n"
                                                             f"Статус: Умер, жду реса")
    print(f"End of AFTER FIGHT, current status: {hero['state']}")

    update_file('hero', hero)