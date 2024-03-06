from telethon import events
import asyncio
from modules.starter.starter import client, hero, const
from modules.peh.peh import get_peh_point
from modules.utils.files import update_file


@events.register(events.NewMessage(chats='me', from_users='me'))
async def user_handler(event):
    message = event.message.to_dict()
    text = message['message']
    if text.lower() == '.help':
        await client.send_message('me', 'Доступные команды:\n\n'
                                        '.mobs lvl cls — указать уровень моба для фарма, где __lvl__ — числовой уровень моба,'
                                        ' а __cls__ — его класс (w - Воин, r - Лучник, m - Маг)\n'
                                        '.farm — режим обычного гринда мобов\n'
                                        '.boost — режим гринда с банками\n'
                                        '.peh — режим перемещения на ПЕХе (перед включением необходимо долететь до Островов)\n'
                                        '.stop — поставить бота на паузу\n'
                                        '.farm_loc — указать локацию для фарма '
                                        '(указать через пробел полное название локации из игры вместе с эмодзи '
                                        'или "БукваЧисло"-названия планеты для космоса)\n'
                                        '.prof_loc — указать через пробел профессию добычи ресурсов: трава, камень, лес, рыба\n'
                                        '.edem on/off — включить/выключить фарм в Эдеме (это не замена режиму .farm или .boost)\n'
                                        '.multitool on/off — включить/выключить добычу ресурсов мультитулом\n'
                                        '.cosmos on/off — включить/выключить фарм в космосе (это не замена режиму .farm или .boost)\n'
                                        '.captcha on/off — включить/выключить автопрохождение капчи')
    if text == '.stop' or text == '.farm' or text == '.dg' or text == '.boost' or text == '.peh':
        hero['mode'] = text.split('.')[1]
        const['orig_msg_status'] = f'Включен режим **{hero["mode"]}**'
        if text.lower() == '.stop':
            const['orig_msg_status'] = f'Бот остановлен'
            hero['state'] = 'none'
            hero['loc'] = 'default'
        const["msg_status"] = await client.send_message('me', const['orig_msg_status'])
        if hero['farm_loc'] == 'none':
            msg_to_del = await client.send_message('me',
                                                   f'Не указана локация для фарма, используй "`.farm_loc` " '
                                                   f'и название, чтоб выставить локацию')
            await asyncio.sleep(60)
            await client.delete_messages('me', msg_to_del)
        if hero['prof_loc'] == 'none':
            msg_to_del = await client.send_message('me',
                                                   f'Не указана локация для профы, используй "`.prof_loc` " '
                                                   f'и вид добычи (лес, трава, рыба или камень)')
            await asyncio.sleep(60)
            await client.delete_messages('me', msg_to_del)
        if hero['mob_lvl'] == 1 or hero['mob_cls'] not in ['warrior', 'ranger', 'mage']:
            msg_to_del = await client.send_message('me',
                                                   f'Не указан моб для фарма! Чтобы указать, используй "`.mobs lvl cls`",'
                                                   f' где __lvl__ — числовой уровень моба, а __cls__ — его класс '
                                                   f'(w - Воин, r - Лучник, m - Маг)')
            await asyncio.sleep(60)
            await client.delete_messages('me', msg_to_del)
    if '.edem ' in text:
        if text == '.edem on':
            hero['edem'] = True
            await event.reply('Включен Эдем')
        elif text == '.edem off':
            hero['edem'] = False
            await event.reply('Выключен Эдем')
    if '.farm_loc ' in text:
        hero['farm_loc'] = text.split('farm_loc ')[1]
        await event.reply(f'Локация для фарма: **{hero["farm_loc"]}**')
    if '.prof_loc ' in text:
        prof = text.split('prof_loc ')[1]
        hero['prof'] = prof
        if prof == 'рыба':
            if not hero['edem']:
                hero['prof_loc'] = '🏝 Побережье Карха'
            else:
                hero['prof_loc'] = '🌉 Дистрикт Вайресс'
        elif prof == 'лес' or prof == 'трава':
            if not hero['edem']:
                hero['prof_loc'] = '🌳 Лес Предтеч'
            else:
                if prof == 'лес':
                    hero['prof_loc'] = '🌃 Дистрикт Аппалачи'
                elif prof == 'трава':
                    hero['prof_loc'] = '🌇 Дистрикт Древних'
        elif prof == 'камень':
            if not hero['edem']:
                hero['prof_loc'] = '🧊 Кварцевое Плато'
            else:
                hero['prof_loc'] = '🌃 Дистрикт Аппалачи'
        await event.reply(f'Локация для фарма профессии {hero["prof"]}: **{hero["prof_loc"]}**')
    if '.multitool ' in text:
        if text == '.multitool on':
            hero['multitool'] = True
            await event.reply('Включен 🔫Мультитул')
        elif text == '.multitool off':
            hero['multitool'] = False
            await event.reply('Выключен 🔫Мультитул')
    if '.captcha ' in text:
        if text == '.captcha on':
            hero['captcha'] = True
            await event.reply('Включен автопроход капчи')
        elif text == '.captcha off':
            hero['captcha'] = False
            await event.reply('Выключен автопроход капчи')
    if '.mobs ' in text:
        if len(text.split(' ')) == 3:
            try:
                mob_lvl = int(text.split(' ')[1])
                mob_cls_raw = text.split(' ')[2]
                if mob_cls_raw in ['w', 'r', 'm']:
                    if mob_cls_raw == 'w':
                        hero['mob_cls'] = 'warrior'
                    elif mob_cls_raw == 'r':
                        hero['mob_cls'] = 'ranger'
                    elif mob_cls_raw == 'm':
                        hero['mob_cls'] = 'mage'
                    hero['mob_lvl'] = mob_lvl
                    await event.reply(f'Выбран {mob_lvl} уровень моба для фарма')
                else:
                    await event.reply(f'Неверно указан класс моба. Используй команду "`.mobs {mob_lvl} cls`", '
                                      f'где __cls__ — класс моба (w - Воин, r - Лучник, m - Маг)')
            except:
                await event.reply('Неправильно указан уровень моба для фарма.\n'
                                  'Используй команду "`.mobs lvl`" или "`.mobs lvl cls`", '
                                  'где __lvl__ — уровень моба для фарма, '
                                  'а __cls__ — класс моба (w - Воин, r - Лучник, m - Маг)')
        else:
            await event.reply('Неправильно указан уровень моба для фарма.\n'
                              'Используй команду "`.mobs lvl`" или "`.mobs lvl cls`", '
                              'где __lvl__ — уровень моба для фарма, '
                              'а __cls__ — класс моба (w - Воин, r - Лучник, m - Маг)')
    if text.startswith('⚔️ '):
        pin = text.split('\n')[0].split(' ')[1]
        point = await get_peh_point(pin.lower())
        print(point)
    update_file('hero', hero)
