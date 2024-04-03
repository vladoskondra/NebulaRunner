import asyncio
from datetime import datetime, timedelta
from random import randint
from modules.starter.starter import client, hero, const
from modules.game.fight_sim import fight_simulation
from modules.utils.files import update_file
from modules.utils.script_tools import change_status


async def after_fight(text):
    hero["hero"]['energy'] = int(text.split('⚡️ Энергия: ')[1].split('/')[0])
    if 'Полученный опыт 📖: ' in text:
        const['farm_received']['exp'] += int(text.split('Полученный опыт 📖: ')[1].split('\n')[0].replace(' ', ''))
    if '🎒 Получено (' in text:
        items = text.split('🎒 Получено (')[1].split('):\n')[1].split('\n')
        for it in items:
            item_name = it.split('- ')[1]
            if any(it_d['name'] == item_name for it_d in const['farm_received']['items']):
                f_it = next(it_d for it_d in const['farm_received']['items'] if it_d['name'] == item_name)
                it_index = const['farm_received']['items'].index(f_it)
                const['farm_received']['items'][it_index]['ctx'] += 1
            else:
                const['farm_received']['items'].append({'name': item_name, 'ctx': 1})
    if 'Потерянный опыт 📖: ' in text:
        const['farm_received']['exp'] -= int(text.split('Потерянный опыт 📖: ')[1].split('\n')[0].replace(' ', ''))
    if 'Потерянный опыт' not in text:
        await asyncio.sleep(randint(2, 5))
        if f"{hero['hero']['name']}(❤️" in text:
            hero['hero']['cur_hp'] = int(text.split(f"{hero['hero']['name']}(❤️")[1].split('/')[0])
        elif f"{hero['hero']['name']}(💔" in text:
            hero['hero']['cur_hp'] = int(text.split(f"{hero['hero']['name']}(💔")[1].split('/')[0])
        print(hero['hero']['cur_hp'])
        if hero['hero']['cur_hp'] < hero['hero']['max_hp'] and hero['farm_cfg']['force_heal'] and hero['space']['cosmos']:
            hero['state'] = 'back to ship'
            await client.send_message(const['game'], '🗺 Исследовать')
        else:
            win_chance = await fight_simulation()
            if 'wr' in win_chance and win_chance['wr'] >= 100 and hero['hero']['energy'] > 0:
                print(f'Can still fight with chance of {win_chance}')
                await change_status(f"Готов еще бить, шанс на успех: {win_chance}")
                if hero['space']['cosmos']:
                    if not hero['space']['cosmos_farm_seek']:
                        now = datetime.now()
                        resp = now + timedelta(minutes=15)
                        resp_text = resp.strftime("%H:%M:%S")
                        await change_status(f"Жду реса моба в {resp_text}")
                        hero['state'] = 'waiting for mob res'
                        await asyncio.sleep(15*60)
                    hero['state'] = 'map seeker'
                    await client.send_message(const['game'], '🗺 Исследовать')

                else:
                    await client.send_message(const["game"], '👀 Осмотреть местность')
            else:
                await change_status("Собираюсь домой")
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
        await change_status("Умер, жду реса")
    print(f"End of AFTER FIGHT, current status: {hero['state']}")

    update_file('hero', hero)