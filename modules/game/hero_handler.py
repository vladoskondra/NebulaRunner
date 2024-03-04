import asyncio

from modules.starter.starter import hero, client, const
from modules.utils.files import update_file


async def update_hero_from_game(text):
    if '🧬 Cимуляция №: ' in text:
        hero['name'] = text.split('📝 Имя: ')[1].split('\n')[0]
        hero['cur_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[0])
        hero['max_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[1].split('\n')[0])
        hero['lvl'] = int(text.split('🏅 Уровень: ')[1].split(' 💠 ')[0])
        hero['energy'] = int(text.split('⚡️ Энергия: ')[1].split('/')[0])
        class_raw = text.split('\n')[3].split(' ')[0]
        class_e = ''
        if class_raw in ['⚔️', '🛡', '🌀', '⛰', '🧛‍♂️', '✨', '💫', '🩸', '🪓']:
            class_e = 'warrior'
        elif class_raw in ['🏹', '🎯', '🌪', '🌧', '🧪', '⚙️', '👻', '🉐', '😶‍🌫️']:
            class_e = 'ranger'
        elif class_raw in ['🔮', '☄️', '💞', '🌊', '🔥', '🤪', '♨️', '🌐', '⚰️']:
            class_e = 'mage'
        hero['stats']['class'] = class_e
        hero['stats']['atk'] = int(text.split('⚔️ Атака: ')[1].split('  🛡 Защита: ')[0])
        hero['stats']['def'] = int(text.split('🛡 Защита: ')[1].split('\n')[0])
        hero['stats']['ddg'] = float(text.split('💨 Уворот: ')[1].split('%')[0])
        hero['stats']['crit'] = float(text.split('💥 Крит: ')[1].split('%')[0])
        hero['stats']['acc'] = float(text.split('🎯 Точность: ')[1].split('%')[0])
        hero['stats']['spd'] = float(text.split('🎲 Инициатива: ')[1].split('\n')[0])
        update_file('hero', hero)
    elif '/' in text.split('❤️: ')[1].split(' 🧡: ')[0]:
        hero['name'] = text.split('📝 Имя: ')[1].split('\n')[0]
        hero['cur_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[0])
        hero['max_hp'] = int(text.split('❤️ Здоровье: ')[1].split('/')[1].split('\n')[0])
        hero['lvl'] = int(text.split('🏅 Уровень: ')[1].split(' 💠 ')[0])
        hero['energy'] = int(text.split('⚡️ Энергия: ')[1].split('/')[0])
        class_raw = text.split('\n')[3].split(' ')[0]
        class_e = ''
        if class_raw in ['⚔️', '🛡', '🌀', '⛰', '🧛‍♂️', '✨', '💫', '🩸', '🪓']:
            class_e = 'warrior'
        elif class_raw in ['🏹', '🎯', '🌪', '🌧', '🧪', '⚙️', '👻', '🉐', '😶‍🌫️']:
            class_e = 'ranger'
        elif class_raw in ['🔮', '☄️', '💞', '🌊', '🔥', '🤪', '♨️', '🌐', '⚰️']:
            class_e = 'mage'
        hero['stats']['class'] = class_e
        hero['stats']['atk'] = int(text.split('⚔️ Атака: ')[1].split('  🛡 Защита: ')[0])
        hero['stats']['def'] = int(text.split('🛡 Защита: ')[1].split('\n')[0])
        hero['stats']['ddg'] = float(text.split('💨 Уворот: ')[1].split('%')[0])
        hero['stats']['crit'] = float(text.split('💥 Крит: ')[1].split('%')[0])
        hero['stats']['acc'] = float(text.split('🎯 Точность: ')[1].split('%')[0])
        hero['stats']['spd'] = float(text.split('🎲 Инициатива: ')[1].split('\n')[0])
        update_file('hero', hero)
    else:
        await client.send_message('me', 'Неподходящий формат отображения героя, '
                                        'меняю на Полный')
        await client.send_message(const['game'], '/size_full')
        await asyncio.sleep(1)
        await client.send_message(const['game'], '/hero')
