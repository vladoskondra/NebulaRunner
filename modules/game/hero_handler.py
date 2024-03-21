import asyncio

from modules.starter.starter import hero, client, const
from modules.utils.files import update_file


async def update_hero_from_game(text):
    if '🧬 Cимуляция №: ' in text:
        hero["hero"]['name'] = text.split('📝 Имя: ')[1].split('\n')[0]
        hero["hero"]['cur_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[0])
        hero["hero"]['max_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[1].split('\n')[0])
        hero["hero"]['lvl'] = int(text.split('🏅 Уровень: ')[1].split(' 💠 ')[0])
        hero["hero"]['energy'] = int(text.split('⚡️ Энергия: ')[1].split('/')[0])
        class_raw = text.split(' Класс: ')[0].split('\n')[-1]
        # print(class_raw)
        class_e = ''
        if class_raw in ['⚔️', '🛡', '🌀', '⛰', '🧛‍♂️', '✨', '💫', '🩸', '🪓']:
            class_e = 'warrior'
        elif class_raw in ['🏹', '🎯', '🌪', '🌧', '🧪', '⚙️', '👻', '🉐', '😶‍🌫️']:
            class_e = 'ranger'
        elif class_raw in ['🔮', '☄️', '💞', '🌊', '🔥', '🤪', '♨️', '🌐', '⚰️']:
            class_e = 'mage'
        hero['hero']['class'] = class_e
        hero['hero']['emoji'] = class_raw
        hero['hero']['atk'] = int(text.split('⚔️ Атака: ')[1].split('  🛡 Защита: ')[0])
        hero['hero']['def'] = int(text.split('🛡 Защита: ')[1].split('\n')[0])
        hero['hero']['ddg'] = float(text.split('💨 Уворот: ')[1].split('%')[0])
        hero['hero']['crit'] = float(text.split('💥 Крит: ')[1].split('%')[0])
        hero['hero']['acc'] = float(text.split('🎯 Точность: ')[1].split('%')[0])
        hero['hero']['spd'] = float(text.split('🎲 Инициатива: ')[1].split('\n')[0])
        update_file('hero', hero)
    elif '/' in text.split('❤️: ')[1].split(' 🧡: ')[0]:
        hero["hero"]['name'] = text.split('📝 Имя: ')[1].split('\n')[0]
        hero["hero"]['cur_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[0])
        hero["hero"]['max_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[1].split('\n')[0])
        hero["hero"]['lvl'] = int(text.split('🏅 Уровень: ')[1].split(' 💠 ')[0])
        hero["hero"]['energy'] = int(text.split('⚡️ Энергия: ')[1].split('/')[0])
        class_raw = text.split(' Класс: ')[0].split('\n')[-1]
        class_e = ''
        if class_raw in ['⚔️', '🛡', '🌀', '⛰', '🧛‍♂️', '✨', '💫', '🩸', '🪓']:
            class_e = 'warrior'
        elif class_raw in ['🏹', '🎯', '🌪', '🌧', '🧪', '⚙️', '👻', '🉐', '😶‍🌫️']:
            class_e = 'ranger'
        elif class_raw in ['🔮', '☄️', '💞', '🌊', '🔥', '🤪', '♨️', '🌐', '⚰️']:
            class_e = 'mage'
        hero['hero']['class'] = class_e
        hero['hero']['emoji'] = class_raw
        hero['hero']['atk'] = int(text.split('⚔️ Атака: ')[1].split('  🛡 Защита: ')[0])
        hero['hero']['def'] = int(text.split('🛡 Защита: ')[1].split('\n')[0])
        hero['hero']['ddg'] = float(text.split('💨 Уворот: ')[1].split('%')[0])
        hero['hero']['crit'] = float(text.split('💥 Крит: ')[1].split('%')[0])
        hero['hero']['acc'] = float(text.split('🎯 Точность: ')[1].split('%')[0])
        hero['hero']['spd'] = float(text.split('🎲 Инициатива: ')[1].split('\n')[0])
        update_file('hero', hero)
    else:
        await client.send_message('me', 'Неподходящий формат отображения героя, '
                                        'меняю на Полный')
        await client.send_message(const['game'], '/size_full')
        await asyncio.sleep(1)
        await client.send_message(const['game'], '/hero')
